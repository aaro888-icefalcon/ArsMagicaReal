#!/usr/bin/env python3
"""
character.py — the character sheet as JSON (the source of truth scripts read from).

Each PC lives at  <campaign>/characters/<slug>.json  (engine-agnostic; the human
<campaign>/character-sheet.md is RENDERED from these on every save). Resolution
commands take `--pc <name> --campaign <dir>` and pull Arts/Characteristics/abilities
straight from the JSON, so you don't retype them.

Commands (run as `arm.py char <cmd>`):
  set    --pc N --campaign DIR --set "characteristics.Int=3" --set "house=Bonisagus" …
  ability --pc N --campaign DIR --name "Magic Theory" --score 3 [--spec "…"]
  art    --pc N --campaign DIR --art Creo|Ig|… --score 10
  spell  --pc N --campaign DIR --name "Pilum of Fire" --tech Creo --form Ignem --level 20 [--mastery 0]
  virtue|flaw --pc N --campaign DIR --name "Gentle Gift" [--tier Major]
  weapon --pc N --campaign DIR --name Staff --init 2 --attack 5 --defense 6 --damage 2
  wound  --pc N --campaign DIR --add Light|Medium|Heavy|Incapacitating | --heal Light
  fatigue --pc N --campaign DIR --set Fresh|Winded|Weary|Tired|Dazed|Unconscious
  vis    --pc N --campaign DIR --art Creo --delta +3
  show   --pc N --campaign DIR        (print the JSON-backed sheet)
  sheet  --campaign DIR               (re-render character-sheet.md from all characters)
  list   --campaign DIR
  validate --pc N --campaign DIR      (check the build against the creation rules)
"""
import json, os, sys
import armcore as C

SCHEMA = "arm.character/1"
CHARS = ["Int", "Per", "Pre", "Com", "Str", "Sta", "Dex", "Qik"]
TECHS = ["Cr", "In", "Mu", "Pe", "Re"]
FORMS = ["An", "Aq", "Au", "Co", "He", "Ig", "Im", "Me", "Te", "Vi"]
ART_ABBR = {"creo": "Cr", "intellego": "In", "muto": "Mu", "perdo": "Pe", "rego": "Re",
            "animal": "An", "aquam": "Aq", "auram": "Au", "corpus": "Co", "herbam": "He",
            "ignem": "Ig", "imaginem": "Im", "mentem": "Me", "terram": "Te", "vim": "Vi"}
FATIGUE = ["Fresh", "Winded", "Weary", "Tired", "Dazed", "Unconscious"]
WOUNDS = ["Light", "Medium", "Heavy", "Incapacitating"]

# ----------------------------------------------------------------- paths / io
def slug(name): return "".join(c if c.isalnum() else "-" for c in name.lower()).strip("-") or "pc"
def _dir(campaign): return os.path.join(campaign, "characters")

def default_char(typ, name, age=25, house=""):
    c = {"schema": SCHEMA, "name": name, "type": typ, "concept": "", "house": house if typ == "magus" else "",
         "covenant": "", "age": {"actual": age, "apparent": age}, "size": 0,
         "characteristics": {k: 0 for k in CHARS},
         "confidence": None if typ == "grog" else {"score": 1, "points": 3},
         "decrepitude": {"score": 0, "points": 0}, "warping": {"score": 0, "points": 0},
         "virtues": [], "flaws": [], "personality": [], "reputations": [],
         "abilities": {}, "combat": [], "soak": 0,
         "fatigue": {"current": "Fresh"}, "wounds": [], "equipment": [], "bonds": []}
    if typ == "magus":
        c["arts"] = {"techniques": {t: 0 for t in TECHS}, "forms": {f: 0 for f in FORMS}}
        c["spells"] = []; c["vis"] = {}; c["sigil"] = ""; c["longevity_ritual"] = None
    return c

def load(campaign, name=None):
    d = _dir(campaign)
    if not os.path.isdir(d): sys.exit(f"no characters/ in {campaign} — make one with `char new`.")
    files = [f for f in sorted(os.listdir(d)) if f.endswith(".json")]
    if not files: sys.exit(f"no characters in {d}.")
    if name:
        want = slug(name)
        for f in files:
            if f[:-5] == want or want in f[:-5]: return json.load(open(os.path.join(d, f), encoding="utf-8"))
        sys.exit(f"no character matching '{name}' in {d} (have: {[f[:-5] for f in files]})")
    if len(files) == 1: return json.load(open(os.path.join(d, files[0]), encoding="utf-8"))
    sys.exit(f"several characters — pass --pc <name>: {[f[:-5] for f in files]}")

def save(campaign, char):
    d = _dir(campaign); os.makedirs(d, exist_ok=True)
    json.dump(char, open(os.path.join(d, slug(char["name"]) + ".json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    render_campaign_sheet(campaign)            # keep the human character-sheet.md in sync

# ----------------------------------------------------------------- accessors (scripts read these)
def art_score(char, name):
    abbr = ART_ABBR.get(str(name).strip().lower(), str(name).strip().capitalize())
    arts = char.get("arts", {})
    for grp in ("techniques", "forms"):
        if abbr in arts.get(grp, {}): return arts[grp][abbr]
    return 0

def char_val(char, key): return char.get("characteristics", {}).get(key, 0)
def ability_score(char, name):
    a = char.get("abilities", {}).get(name)
    return (a.get("score", 0) if isinstance(a, dict) else (a or 0))
def parma(char): return ability_score(char, "Parma Magica")

def pc_from_argv(argv):
    """Used by resolution commands: returns the char dict if --pc given, else None."""
    name = C.opt(argv, "--pc"); campaign = C.opt(argv, "--campaign")
    if not name: return None
    if not campaign: sys.exit("--pc needs --campaign DIR")
    return load(campaign, name)

# ----------------------------------------------------------------- render
def render_sheet(c):
    L = [f"## {c['name']} — {c['type']}" + (f" of House {c['house']}" if c.get("house") else "")]
    if c.get("concept"): L.append(f"*{c['concept']}*")
    ch = c["characteristics"]
    L.append("- **Characteristics:** " + " · ".join(f"{k} {ch[k]:+d}" for k in CHARS) +
             f"   · Size {c['size']:+d}   · Age {c['age']['actual']}")
    if c.get("confidence"): L.append(f"- **Confidence:** Score {c['confidence']['score']}, Points {c['confidence']['points']}")
    L.append(f"- **Warping:** {c['warping']['score']} ({c['warping']['points']})   · "
             f"**Decrepitude:** {c['decrepitude']['score']} ({c['decrepitude']['points']})")
    if c["virtues"]: L.append("- **Virtues:** " + ", ".join(f"{v['name']}({v.get('tier','?')})" for v in c["virtues"]))
    if c["flaws"]: L.append("- **Flaws:** " + ", ".join(f"{f['name']}({f.get('tier','?')})" for f in c["flaws"]))
    if c["abilities"]:
        L.append("- **Abilities:** " + ", ".join(
            f"{n} {a.get('score',0) if isinstance(a,dict) else a}" +
            (f" ({a['spec']})" if isinstance(a, dict) and a.get("spec") else "")
            for n, a in c["abilities"].items()))
    if c.get("arts"):
        L.append("- **Techniques:** " + " ".join(f"{t}{c['arts']['techniques'][t]}" for t in TECHS))
        L.append("- **Forms:** " + " ".join(f"{f}{c['arts']['forms'][f]}" for f in FORMS))
    if c.get("spells"):
        L.append("- **Spells:** " + "; ".join(f"{s['name']} ({s.get('tech','')}{s.get('form','')} {s.get('level','')})" for s in c["spells"]))
    for w in c.get("combat", []):
        L.append(f"- **Weapon {w['name']}:** Init {w.get('init',0):+d}, Attack {w.get('attack',0):+d}, "
                 f"Defense {w.get('defense',0):+d}, Damage {w.get('damage',0):+d}")
    L.append(f"- **Soak:** {c['soak']}   · **Fatigue:** {c['fatigue']['current']}   · "
             f"**Wounds:** {', '.join(c['wounds']) if c['wounds'] else 'none'}")
    if c.get("vis"): L.append("- **Vis (pawns):** " + ", ".join(f"{k} {v}" for k, v in c["vis"].items()))
    if c.get("bonds"): L.append("- **Bonds/drives:** " + "; ".join(c["bonds"]))
    return "\n".join(L)

def render_campaign_sheet(campaign):
    d = _dir(campaign)
    files = [f for f in sorted(os.listdir(d)) if f.endswith(".json")] if os.path.isdir(d) else []
    chars = [json.load(open(os.path.join(d, f), encoding="utf-8")) for f in files]
    body = ("# Characters — rendered from characters/*.json (the JSON is the source of truth)\n\n"
            "> Edit the JSON via `arm.py char set|ability|art|spell|wound|fatigue|vis …`; this file is regenerated.\n\n"
            + "\n\n".join(render_sheet(c) for c in chars))
    open(os.path.join(campaign, "character-sheet.md"), "w", encoding="utf-8").write(body)

# ----------------------------------------------------------------- mutating commands
def _coerce(v):
    try: return int(v)
    except ValueError:
        try: return float(v)
        except ValueError: return v

def _set_path(obj, path, val):
    keys = path.split("."); cur = obj
    for k in keys[:-1]: cur = cur.setdefault(k, {})
    cur[keys[-1]] = val

def cmd_set(argv):
    campaign = C.opt(argv, "--campaign"); char = load(campaign, C.opt(argv, "--pc"))
    sets = [argv[i + 1] for i, a in enumerate(argv) if a == "--set"]
    if not sets: sys.exit('set needs one or more --set "path=value"')
    for s in sets:
        if "=" not in s: sys.exit(f"bad --set '{s}' (need path=value)")
        path, val = s.split("=", 1); _set_path(char, path.strip(), _coerce(val.strip()))
        print(f"   set {path.strip()} = {val.strip()}")
    save(campaign, char)

def cmd_ability(argv):
    campaign = C.opt(argv, "--campaign"); char = load(campaign, C.opt(argv, "--pc"))
    name = C.opt(argv, "--name"); score = C.opt(argv, "--score", 0, int); spec = C.opt(argv, "--spec")
    if not name: sys.exit("ability --name N --score S")
    char.setdefault("abilities", {})[name] = {"score": score, **({"spec": spec} if spec else {})}
    save(campaign, char); print(f"🎓 {char['name']}: {name} {score}" + (f" ({spec})" if spec else ""))

def cmd_art(argv):
    campaign = C.opt(argv, "--campaign"); char = load(campaign, C.opt(argv, "--pc"))
    if char["type"] != "magus": sys.exit("only magi have Arts")
    art = C.opt(argv, "--art"); score = C.opt(argv, "--score", 0, int)
    abbr = ART_ABBR.get((art or "").lower(), (art or "").capitalize())
    grp = "techniques" if abbr in TECHS else ("forms" if abbr in FORMS else None)
    if not grp: sys.exit(f"--art must be one of {TECHS + FORMS} or a full Art name")
    char["arts"][grp][abbr] = score; save(campaign, char)
    print(f"🔮 {char['name']}: {abbr} {score}")

def cmd_spell(argv):
    campaign = C.opt(argv, "--campaign"); char = load(campaign, C.opt(argv, "--pc"))
    name = C.opt(argv, "--name"); tech = C.opt(argv, "--tech", ""); form = C.opt(argv, "--form", "")
    level = C.opt(argv, "--level", 0, int); mastery = C.opt(argv, "--mastery", 0, int)
    if not name: sys.exit("spell --name N --tech Creo --form Ignem --level L")
    ta = ART_ABBR.get(tech.lower(), tech.capitalize()); fa = ART_ABBR.get(form.lower(), form.capitalize())
    char.setdefault("spells", []).append({"name": name, "tech": ta, "form": fa, "level": level, "mastery": mastery})
    save(campaign, char); print(f"📖 {char['name']} learns {name} ({ta}{fa} {level})")

def _add_vf(argv, kind):
    campaign = C.opt(argv, "--campaign"); char = load(campaign, C.opt(argv, "--pc"))
    name = C.opt(argv, "--name"); tier = C.opt(argv, "--tier", "Minor")
    if not name: sys.exit(f"{kind} --name N [--tier Major|Minor|Free]")
    char.setdefault(kind + "s", []).append({"name": name, "tier": tier})
    save(campaign, char); print(f"✦ {char['name']} gains {kind}: {name} ({tier})")

def cmd_weapon(argv):
    campaign = C.opt(argv, "--campaign"); char = load(campaign, C.opt(argv, "--pc"))
    w = {"name": C.opt(argv, "--name", "weapon"), "init": C.opt(argv, "--init", 0, int),
         "attack": C.opt(argv, "--attack", 0, int), "defense": C.opt(argv, "--defense", 0, int),
         "damage": C.opt(argv, "--damage", 0, int)}
    char.setdefault("combat", []).append(w); save(campaign, char)
    print(f"⚔️  {char['name']} arms {w['name']} (Atk {w['attack']:+d}, Def {w['defense']:+d}, Dam {w['damage']:+d})")

def cmd_wound(argv):
    campaign = C.opt(argv, "--campaign"); char = load(campaign, C.opt(argv, "--pc"))
    add = C.opt(argv, "--add"); heal = C.opt(argv, "--heal")
    if add: char.setdefault("wounds", []).append(add.capitalize())
    if heal and heal.capitalize() in char.get("wounds", []): char["wounds"].remove(heal.capitalize())
    save(campaign, char); print(f"🩸 {char['name']} wounds: {char['wounds'] or 'none'}")

def cmd_fatigue(argv):
    campaign = C.opt(argv, "--campaign"); char = load(campaign, C.opt(argv, "--pc"))
    lv = (C.opt(argv, "--set", "Fresh") or "Fresh").capitalize()
    if lv not in FATIGUE: sys.exit(f"--set one of {FATIGUE}")
    char["fatigue"]["current"] = lv; save(campaign, char); print(f"😮‍💨 {char['name']} fatigue: {lv}")

def cmd_vis(argv):
    campaign = C.opt(argv, "--campaign"); char = load(campaign, C.opt(argv, "--pc"))
    art = C.opt(argv, "--art"); delta = C.opt(argv, "--delta", 0, int)
    if not art: sys.exit("vis --art Creo --delta +3")
    v = char.setdefault("vis", {}); v[art] = max(0, v.get(art, 0) + delta)
    save(campaign, char); print(f"⚗️  {char['name']} vis {art}: {v[art]} pawns")

def cmd_show(argv):
    char = load(C.opt(argv, "--campaign"), C.opt(argv, "--pc")); print(render_sheet(char))

def cmd_sheet(argv):
    campaign = C.opt(argv, "--campaign"); render_campaign_sheet(campaign)
    print(f"✔ rendered {os.path.join(campaign, 'character-sheet.md')} from characters/*.json")

def cmd_list(argv):
    d = _dir(C.opt(argv, "--campaign"))
    files = [f[:-5] for f in sorted(os.listdir(d))] if os.path.isdir(d) else []
    print("👤 characters: " + (", ".join(files) if files else "(none)"))

def cmd_validate(argv):
    import chargen
    char = load(C.opt(argv, "--campaign"), C.opt(argv, "--pc"))
    cc = C.load_rule("character_creation"); buy = cc["characteristic_point_buy"]
    print(f"🔎 validating {char['name']} ({char['type']})")
    spent = sum(buy["cost"][str(char["characteristics"][k])] for k in CHARS)
    print(f"   Characteristics: spent {spent} of {buy['start']} → " +
          ("OK ✓" if spent == buy["start"] else f"{'OVER' if spent>buy['start'] else 'UNSPENT'} ✗"))
    chargen.cmd_vf(["vf", "--type", char["type"],
                    "--virtues", ",".join(f"{v['name']}:{v.get('tier','Minor')}" for v in char["virtues"]),
                    "--flaws", ",".join(f"{f['name']}:{f.get('tier','Minor')}" for f in char["flaws"])])
    if char["type"] == "magus":
        req = cc["apprenticeship"]["required_abilities"]
        missing = [a for a in req if ability_score(char, a) < req[a]]
        print("   Required magus abilities: " + ("all present ✓" if not missing else f"MISSING/low: {missing} ✗"))

def dispatch(argv):
    cmd = argv[0]
    table = {"set": cmd_set, "ability": cmd_ability, "art": cmd_art, "spell": cmd_spell,
             "virtue": lambda a: _add_vf(a, "virtue"), "flaw": lambda a: _add_vf(a, "flaw"),
             "weapon": cmd_weapon, "wound": cmd_wound, "fatigue": cmd_fatigue, "vis": cmd_vis,
             "show": cmd_show, "sheet": cmd_sheet, "list": cmd_list, "validate": cmd_validate}
    if cmd not in table: sys.exit(f"unknown char command '{cmd}'")
    table[cmd](argv)

if __name__ == "__main__":
    if not sys.argv[1:] or sys.argv[1] in ("-h", "--help"): print(__doc__)
    else: dispatch(sys.argv[1:])
