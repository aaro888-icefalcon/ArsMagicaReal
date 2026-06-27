#!/usr/bin/env python3
"""
chargen.py — guided, VALIDATED Ars Magica 5e character creator (hook: generate:character, PC build).

This is a builder/validator, not an auto-roller: the engine's rule is "make real choices."
It walks the canonical 12-step sequence, checks every budget (7 Characteristic points, the
Virtue/Flaw balance per type, XP costs, the Gauntlet spell-level cap), and scaffolds a sheet.
All rules live in data/rules/character_creation.json; Virtues/Flaws are classified from the
data/elements/virtues_flaws.json library. Dice (if you roll Characteristics) go through armdice.

Commands (run as `arm.py char <cmd>`):
  new   --type magus|companion|grog|mythic_companion [--name N] [--age N] [--campaign DIR]
  houses                                              the 12 Houses + their free creation Virtue
  points --set "Int=3,Sta=2,Dex=1,Qik=1,Per=0,Pre=0,Com=-1,Str=-2"   validate the 7-point buy
  vf     --type T --virtues "id,id:Major,…" --flaws "id,…"            validate the V&F balance
  cost   --ability N | --art N | --ability-from A --ability-to B | --art-from A --art-to B
  spellcap --te N --fo N --int N --mt N [--aura 3]    max Formulaic spell level at Gauntlet
  abilities [--type general|academic|arcane|martial|supernatural]
  budget --type T [--years N] [--age N] [--wealth default|wealthy|poor]
"""
import os, sys
import armcore as C
import armdice as D

def CC(): return C.load_rule("character_creation")

# ----------------------------------------------------------------- helpers
def triangular(n): return n * (n + 1) // 2
def ability_xp(score): return 5 * triangular(score)
def art_xp(score): return triangular(score)

def _slug(s): return "".join(c if c.isalnum() else "_" for c in s.lower()).strip("_")

def _vf_library():
    """Many keys -> {'vf','tier','category','name'} so `the_gift` / `The Gift` / `virtue.the_gift` all match."""
    out = {}
    for r in C.load_all_elements().values():
        if r.get("type") in ("virtue", "flaw"):
            cost = (r.get("cost") or "Minor").split()
            tier = cost[0] if cost else "Minor"
            cat = cost[1] if len(cost) > 1 else "General"
            rec = {"vf": r["type"], "tier": tier, "category": cat, "name": r["name"]}
            fid = r["id"].lower()
            for k in {fid, fid.split(".", 1)[-1], r["name"].lower(), _slug(r["name"])}:
                out[k] = rec
    return out

# ----------------------------------------------------------------- commands
def cmd_houses(_argv):
    cc = CC(); print("🏛  Houses of Hermes — free creation Virtue (magi pick one House):")
    for h, b in cc["house_benefits"].items():
        print(f"   {h:16} {b}")

def cmd_points(argv):
    cc = CC(); buy = cc["characteristic_point_buy"]; cost_tbl = buy["cost"]
    raw = C.opt(argv, "--set", "")
    if not raw: sys.exit('points --set "Int=3,Sta=2,Dex=1,Qik=1,Per=0,Pre=0,Com=-1,Str=-2"')
    vals = {}
    for tok in raw.split(","):
        if "=" not in tok: continue
        k, v = tok.split("=", 1); vals[k.strip().capitalize()] = int(v)
    total = 0; print("🧮 Characteristic point-buy (start 7):")
    for ch in cc["characteristics"]:
        v = vals.get(ch, 0)
        if not (buy["min"] <= v <= buy["max"]):
            print(f"   ✗ {ch} {v:+d}  OUT OF RANGE (−3..+3)"); continue
        c = cost_tbl[str(v)]; total += c
        print(f"   {ch} {v:+d}  (cost {c:+d})")
    rem = buy["start"] - total
    verdict = "OK ✓" if rem == 0 else (f"{rem} point(s) UNSPENT" if rem > 0 else f"OVER by {-rem} point(s) ✗")
    print(f"   → spent {total} of {buy['start']}  →  {verdict}")

def cmd_vf(argv):
    cc = CC(); lib = _vf_library(); pts = cc["vf_points"]
    typ = (C.opt(argv, "--type", "magus") or "magus").lower()
    rules = cc["vf_rules"].get(typ)
    if not rules: sys.exit(f"--type must be one of {cc['types']}")

    def eff_tier(tier, override):
        if override: return override.strip().capitalize()
        if tier in pts: return tier
        parts = tier.replace("/", " ").split()         # e.g. "Major/Minor" → default to the lesser
        for p in ("Minor", "Major", "Free"):
            if p in parts: return p
        return "Minor"

    def parse(s):
        out = []
        for tok in (s or "").split(","):
            tok = tok.strip()
            if not tok: continue
            override = None
            if ":" in tok: tok, override = tok.split(":", 1); tok = tok.strip()
            info = lib.get(tok.lower()) or lib.get(_slug(tok))
            tier = eff_tier(info["tier"] if info else "Minor", override)
            cat = info["category"] if info else "?"
            name = info["name"] if info else tok
            out.append({"name": name, "tier": tier, "category": cat, "known": info is not None})
        return out

    virtues = parse(C.opt(argv, "--virtues", "")); flaws = parse(C.opt(argv, "--flaws", ""))
    is_free = lambda x: x["tier"] == "Free" or x["name"] in rules.get("required_free", [])
    v_pts = sum(pts.get(v["tier"], 0) for v in virtues if not is_free(v))
    f_pts = sum(pts.get(f["tier"], 0) for f in flaws)
    print(f"⚖️  Virtue/Flaw check — {typ}")
    print("   Virtues: " + ", ".join(f"{v['name']}({v['tier']})" for v in virtues))
    print("   Flaws:   " + ", ".join(f"{f['name']}({f['tier']})" for f in flaws))
    print(f"   costed Virtue points = {v_pts}   ·   Flaw points = {f_pts}   (free: Gift/Status/House not counted)")
    ok = []

    def chk(cond, good, bad): ok.append(cond); print("   " + ("✓ " if cond else "✗ ") + (good if cond else bad))

    if "max_flaw_points" in rules:
        chk(f_pts <= rules["max_flaw_points"], f"Flaw points {f_pts} ≤ {rules['max_flaw_points']}",
            f"Flaw points {f_pts} EXCEED {rules['max_flaw_points']}")
    bal = rules.get("balance", "")
    if "2 ×" in bal:
        chk(v_pts <= 2 * f_pts, f"Virtue pts {v_pts} ≤ 2×Flaw {2*f_pts} (Mythic Companion)",
            f"Virtue pts {v_pts} exceed 2×Flaw {2*f_pts}")
    elif "minor" in bal:
        mv = sum(1 for v in virtues if v["tier"] == "Minor" and not is_free(v))
        mf = sum(1 for f in flaws if f["tier"] == "Minor")
        chk(mv == mf, f"Minor Virtues {mv} == Minor Flaws {mf}", f"Minor Virtues {mv} ≠ Minor Flaws {mf}")
    elif bal:
        chk(v_pts == f_pts, f"Virtue pts == Flaw pts ({v_pts})", f"Virtue pts {v_pts} ≠ Flaw pts {f_pts} (must balance)")
    if "max_minor_flaws" in rules:
        mf = sum(1 for f in flaws if f["tier"] == "Minor")
        chk(mf <= rules["max_minor_flaws"], f"Minor Flaws {mf} ≤ {rules['max_minor_flaws']}",
            f"Minor Flaws {mf} exceed {rules['max_minor_flaws']}")
    if rules.get("no_major_vf"):
        majors = [x["name"] for x in virtues + flaws if x["tier"] == "Major"]
        chk(not majors, "no Major Virtues/Flaws (grog)", f"grogs take NO Major V/F: {majors}")
    if "max_story_flaws" in rules:
        sf = sum(1 for f in flaws if f["category"] == "Story")
        chk(sf <= rules["max_story_flaws"], f"Story Flaws {sf} ≤ {rules['max_story_flaws']}",
            f"Story Flaws {sf} exceed {rules['max_story_flaws']}")
    if rules.get("no_story_flaws"):
        sf = [f["name"] for f in flaws if f["category"] == "Story"]
        chk(not sf, "no Story Flaws (grog)", f"grogs take no Story Flaws: {sf}")
    if "max_personality_flaws" in rules:
        pf = sum(1 for f in flaws if f["category"] == "Personality")
        chk(pf <= rules["max_personality_flaws"], f"Personality Flaws {pf} ≤ {rules['max_personality_flaws']}",
            f"Personality Flaws {pf} exceed {rules['max_personality_flaws']}")
    if "max_major_hermetic_virtues" in rules:
        mh = sum(1 for v in virtues if v["tier"] == "Major" and v["category"] == "Hermetic")
        chk(mh <= rules["max_major_hermetic_virtues"], f"Major Hermetic Virtues {mh} ≤ {rules['max_major_hermetic_virtues']}",
            f"Major Hermetic Virtues {mh} exceed {rules['max_major_hermetic_virtues']}")
    if rules.get("no_hermetic_vf"):
        herm = [x["name"] for x in virtues + flaws if x["category"] == "Hermetic"]
        chk(not herm, "no Hermetic V/F (grog)", f"grogs take no Hermetic V/F: {herm}")
    for req in rules.get("required_free", []):
        chk(any(v["name"] == req for v in virtues), f"has required '{req}'", f"MISSING required '{req}'")
    if rules.get("no_gift"):
        chk(not any("Gift" in v["name"] for v in virtues), "no The Gift (non-magus)", "should NOT have The Gift")
    if rules.get("recommend_at_least_one_hermetic_flaw"):
        hf = any(f["category"] == "Hermetic" for f in flaws)
        print("   " + ("✓ has a Hermetic Flaw" if hf else "• recommended: take at least one Hermetic Flaw"))
    print("   " + ("RESULT: VALID ✓" if all(ok) else "RESULT: fix the ✗ items above"))

def cmd_cost(argv):
    af, at = C.opt(argv, "--ability-from", None, int), C.opt(argv, "--ability-to", None, int)
    rf, rt = C.opt(argv, "--art-from", None, int), C.opt(argv, "--art-to", None, int)
    if C.opt(argv, "--ability", None, int) is not None:
        n = C.opt(argv, "--ability", 0, int); print(f"📚 Ability score {n} costs {ability_xp(n)} xp (from 0).")
    elif af is not None and at is not None:
        print(f"📚 Ability {af}→{at}: {ability_xp(at) - ability_xp(af)} xp.")
    elif C.opt(argv, "--art", None, int) is not None:
        n = C.opt(argv, "--art", 0, int); print(f"🔮 Art score {n} costs {art_xp(n)} xp (from 0).")
    elif rf is not None and rt is not None:
        print(f"🔮 Art {rf}→{rt}: {art_xp(rt) - art_xp(rf)} xp.")
    else:
        sys.exit("cost --ability N | --art N | --ability-from A --ability-to B | --art-from A --art-to B")

def cmd_spellcap(argv):
    te = C.opt(argv, "--te", 0, int); fo = C.opt(argv, "--fo", 0, int)
    intg = C.opt(argv, "--int", 0, int); mt = C.opt(argv, "--mt", 0, int); aura = C.opt(argv, "--aura", 3, int)
    cap = te + fo + intg + mt + aura
    print(f"📖 Gauntlet spell-level cap = Te {te} + Fo {fo} + Int {intg:+d} + Magic Theory {mt} + aura {aura} = "
          f"**{cap}**  (no starting spell may exceed this Lab Total).")

def cmd_abilities(argv):
    cc = CC(); t = (C.opt(argv, "--type") or "").capitalize()
    groups = cc["abilities_by_type"]
    for name, lst in groups.items():
        if t and name != t: continue
        print(f"🎓 {name}: " + ", ".join(lst))

def cmd_budget(argv):
    cc = CC(); typ = (C.opt(argv, "--type", "magus") or "magus").lower()
    age = C.opt(argv, "--age", 25, int); wealth = C.opt(argv, "--wealth", "default")
    rate = cc["later_life"]["xp_per_year"].get(wealth, 15)
    ec = cc["early_childhood"]
    print(f"💰 XP budget — {typ}, age {age}, {wealth} ({rate} xp/yr):")
    print(f"   Early Childhood: {ec['native_language_xp']} xp Native Language + {ec['spread_xp']} xp spread.")
    if typ == "magus":
        years = C.opt(argv, "--years", 5, int)
        ap = cc["apprenticeship"]
        print(f"   Later Life ({years} yr pre-apprenticeship): {years * rate} xp.")
        print(f"   Apprenticeship: {ap['xp']} xp (Arts & Abilities) + {ap['spell_levels']} spell levels "
              f"(suggested split {ap['suggested_split']['abilities_xp']}/{ap['suggested_split']['arts_xp']}).")
        print(f"   Required: {ap['required_abilities']}  ·  Recommended: {ap['recommended_abilities']}")
    else:
        years = C.opt(argv, "--years", max(0, age - 5), int)
        print(f"   Later Life ({years} yr): {years * rate} xp into permitted Abilities.")

def cmd_new(argv):
    cc = CC(); typ = (C.opt(argv, "--type", "magus") or "magus").lower()
    if typ not in cc["types"]: sys.exit(f"--type must be one of {cc['types']}")
    name = C.opt(argv, "--name", "<name>"); age = C.opt(argv, "--age", None, int)
    print(f"🧙 CHARACTER CREATOR — {typ}: {name}")
    print("   Make real choices with the player; validate each step with the `char` sub-commands.\n")
    print("   Sequence:")
    for step in cc["creation_sequence"]: print("     " + step)
    r = cc["vf_rules"][typ]
    print(f"\n   Virtue/Flaw rule ({typ}): {r}")
    if typ == "magus":
        ap = cc["apprenticeship"]
        print(f"\n   Magus budgets: Characteristics 7 pts · Apprenticeship {ap['xp']} xp + {ap['spell_levels']} spell levels.")
        print(f"   Required abilities at Gauntlet: {ap['required_abilities']}.")
        print(f"   Spell-level cap = {ap['spell_level_cap_formula']}  (use `char spellcap`).")
        print("   Pick a House for its free Virtue (use `char houses`).")
    print("\n   Commands: char houses · char points · char vf · char cost · char spellcap · char abilities · char budget")
    campaign = C.opt(argv, "--campaign")
    if campaign:
        import character
        path = os.path.join(character._dir(campaign), character.slug(name) + ".json")
        if os.path.exists(path):
            print(f"\n   ({path} already exists — not overwritten)")
        else:
            ch = character.default_char(typ, name, age=age or 25, house=C.opt(argv, "--house", ""))
            character.save(campaign, ch)       # writes the JSON + renders character-sheet.md
            print(f"\n   ✔ created {path} (the JSON source of truth) and rendered character-sheet.md.")
            print("   Build it: `char set/ability/art/spell/virtue/flaw/weapon …`; check with `char validate`.")

STORE_CMDS = {"set", "ability", "art", "spell", "virtue", "flaw", "weapon",
              "wound", "fatigue", "vis", "show", "sheet", "list", "validate"}

def run(argv):
    if not argv or argv[0] in ("-h", "--help"): print(__doc__); return
    if argv[0] in STORE_CMDS:                          # JSON character store (character.py)
        import character; character.dispatch(argv); return
    {"new": cmd_new, "houses": cmd_houses, "points": cmd_points, "vf": cmd_vf, "cost": cmd_cost,
     "spellcap": cmd_spellcap, "abilities": cmd_abilities, "budget": cmd_budget}.get(
        argv[0], lambda a: sys.exit(f"unknown char command '{argv[0]}'"))(argv)

if __name__ == "__main__":
    run(sys.argv[1:])
