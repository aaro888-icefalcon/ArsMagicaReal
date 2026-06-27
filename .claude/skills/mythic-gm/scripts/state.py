#!/usr/bin/env python3
"""
state.py — campaign bookkeeping helpers. campaign-state.md stays the human-readable
source of truth for prose; the Threads/Characters Lists and adventure config live in
JSON (threads.json / characters.json / adventure.json) so the dice can roll the FULL
list however long. These helpers keep that JSON correct.

Commands:
  init <campaign_dir>              Copy the state template + scaffold the JSON Lists/config
  chaos <+1|-1> <current>          Apply a clamped Chaos Factor change (1..9)
  validate <statefile>             Check the required sections are present
  thread  add|weight|remove|show <campaign> ["name"]   Manage threads.json
  char    add|weight|remove|show <campaign> ["name"]   Manage characters.json
  adventure show <campaign>                            Show theme order / tens / style
  adventure set-themes <campaign> A,B,C,D,E            Set this adventure's Theme priority order
  list-count <campaign>            Report Threads & Characters weighted-slot counts + flags
  migrate <campaign>               One-time upgrade: build threads.json/characters.json/adventure.json
                                   from an OLD markdown campaign-state.md (lists = numbered lines,
                                   weight = repetition; Theme priority + Tens-cycle counter lines)
"""
import os, re, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lists

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "assets", "templates", "campaign-state.md")
REQUIRED = ["Chaos Factor", "Threads List", "Characters List", "Adventure Source",
            "Discipline", "Scene"]

def cmd_init(dirpath):
    os.makedirs(dirpath, exist_ok=True)
    dst = os.path.join(dirpath, "campaign-state.md")
    if os.path.exists(dst): sys.exit(f"{dst} already exists — refusing to overwrite.")
    shutil.copy(TEMPLATE, dst)
    lists.save_list(dirpath, {"kind": "thread", "new_weight": 2, "entries": []})
    lists.save_list(dirpath, {"kind": "character", "new_weight": 4, "entries": []})
    lists.save_adventure(dirpath, lists.load_adventure(dirpath))   # writes defaults
    print(f"Initialised {dst}\n  + threads.json, characters.json, adventure.json (empty)")

def cmd_chaos(delta, current):
    cur = int(current); dv = int(delta)
    new = max(1, min(9, cur + dv))
    note = "" if new != cur else "  (clamped — no change)"
    print(f"Chaos Factor {cur} {dv:+d} → {new}{note}")

def cmd_validate(path):
    txt = open(path, encoding="utf-8").read()
    missing = [s for s in REQUIRED if s.lower() not in txt.lower()]
    cf = re.search(r"Chaos Factor[^0-9]*([1-9])", txt)
    if cf and not (1 <= int(cf.group(1)) <= 9): missing.append("Chaos Factor in range 1-9")
    if missing:
        print("INVALID — missing/!ok:", ", ".join(missing)); sys.exit(1)
    print("State valid ✓  (Chaos Factor = %s)" % (cf.group(1) if cf else "?"))

def _render(obj, full=False):
    K = obj["kind"].capitalize()
    if not obj["entries"]:
        print(f"  ({K}s List empty)"); return
    for i, e in enumerate(obj["entries"], 1):
        w = int(e.get("weight", 1))
        wtag = "held·w0" if w == 0 else f"w{w}"
        st = e.get("status")
        print(f"  {i}. {e['name']}  ({wtag}" + (f" · {st}" if st else "") + ")")
        doss = e.get("dossier")
        if doss:
            preview = doss if (full or len(doss) <= 160) else doss[:159].rstrip() + "…"
            print(f"       {preview}")
    S = lists.total_weight(obj["entries"])
    live = sum(1 for e in obj["entries"] if int(e.get("weight", 1)) > 0)
    held = len(obj["entries"]) - live
    nw = obj.get("new_weight")
    tail = ""
    if nw:
        tail = f"  ·  NEW slot = {nw}  → P(new) = {nw}/{S+nw} ≈ {round(100*nw/(S+nw))}%"
    print(f"  Σ weighted slots = {S}  ({live} live" + (f", {held} held" if held else "") + f"){tail}")

def cmd_listcmd(kind, action, campaign, name=None, full=False):
    obj = lists.load_list(campaign, kind)
    if action == "show":
        _render(obj, full=full); return
    if action in ("add", "weight"):
        status, obj = lists.add_entry(obj, name, bump=True)
        lists.save_list(campaign, obj); print(f"{kind} '{name}': {status}.")
    elif action == "remove":
        status, obj = lists.remove_entry(obj, name)
        lists.save_list(campaign, obj); print(f"{kind} '{name}': {status}.")
    else:
        sys.exit(f"Unknown {kind} action '{action}' (add|weight|remove|show).")
    _render(obj)

def cmd_adventure(action, campaign, arg=None):
    adv = lists.load_adventure(campaign)
    if action == "show":
        print(f"Theme priority: {', '.join(adv['theme_order'])}")
        print(f"Tens-cycle counter: {adv['tens']}   |   style: {adv['style']}")
    elif action == "set-themes":
        order = [t.strip().capitalize() for t in arg.split(",") if t.strip()]
        adv["theme_order"] = order; lists.save_adventure(campaign, adv)
        print(f"Theme priority set → {', '.join(order)}")
    else:
        sys.exit("adventure: show | set-themes <A,B,C,D,E>")

def cmd_migrate(campaign):
    """Build the JSON Lists + adventure config from an OLD markdown campaign-state.md."""
    from collections import Counter
    path = os.path.join(campaign, "campaign-state.md")
    if not os.path.exists(path): sys.exit(f"No campaign-state.md in {campaign}")
    lines = open(path, encoding="utf-8").read().split("\n")
    def section(*headers):
        out, grab = [], False
        for ln in lines:
            s = ln.strip()
            if s.startswith("## "):
                grab = any(h.lower() in s.lower() for h in headers); continue
            if grab:
                m = re.match(r"^\s*\d+\.\s+(.*\S)\s*$", ln)
                if m and m.group(1).strip() not in ("", "—", "-"): out.append(m.group(1).strip())
        return out
    made = []
    for kind, hdr in [("thread", "Threads List"), ("character", "Characters List")]:
        jp = os.path.join(campaign, lists.KIND_FILE[kind])
        if os.path.exists(jp):
            print(f"  • {os.path.basename(jp)} already exists — skipping (delete it first to re-migrate)."); continue
        names = section(hdr)
        weights = Counter(n.lower() for n in names)
        seen, entries = set(), []
        for n in names:                       # preserve first-seen order; weight = repetition (cap 3)
            k = n.lower()
            if k in seen: continue
            seen.add(k); entries.append({"name": n, "weight": min(weights[k], lists.WEIGHT_CAP)})
        lists.save_list(campaign, {"kind": kind, "entries": entries}); made.append(f"{lists.KIND_FILE[kind]} ({len(entries)} entries)")
    # adventure.json: pull Theme priority + Tens counter if present
    if not os.path.exists(os.path.join(campaign, "adventure.json")):
        adv = lists.load_adventure(campaign)
        joined = "\n".join(lines)
        tm = re.search(r"Theme priority[^:]*:\s*(.+)", joined)
        if tm:
            order = re.findall(r"[A-Za-z]+", re.sub(r"\d+\.", " ", tm.group(1)))
            order = [w.capitalize() for w in order if w.capitalize() in
                     ("Action","Tension","Mystery","Social","Personal")]
            if len(order) == 5: adv["theme_order"] = order
        tn = re.search(r"Tens-cycle counter[^:]*:\s*(\d+)", joined)
        if tn: adv["tens"] = int(tn.group(1))
        lists.save_adventure(campaign, adv); made.append(f"adventure.json (themes {adv['theme_order']}, tens {adv['tens']})")
    print("Migrated:", "; ".join(made) if made else "nothing (all JSON already present)")
    print("Now treat the JSON as the source of truth; the markdown Lists become a snapshot.")

def cmd_list_count(campaign):
    for kind, flag in [("thread", "--threads"), ("character", "--characters")]:
        obj = lists.load_list(campaign, kind); S = lists.total_weight(obj["entries"])
        over = [f"{e['name']}×{e['weight']}" for e in obj["entries"] if e.get("weight",1) > 3]
        wq = ("  ⚠ weight>3: " + ", ".join(over)) if over else ""
        nw = obj.get("new_weight")
        nwt = f"  + NEW slot {nw} (P≈{round(100*nw/(S+nw))}%)" if nw else ""
        print(f"{kind.capitalize()}s List: {len(obj['entries'])} entr(y/ies), Σ slots {S}{nwt}{wq}".rstrip())

def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h","--help"): print(__doc__); return
    c = a[0]
    if c == "init": cmd_init(a[1])
    elif c == "chaos": cmd_chaos(a[1], a[2])
    elif c == "validate": cmd_validate(a[1])
    elif c in ("thread", "char"):
        kind = "thread" if c == "thread" else "character"
        pos = [x for x in a[1:] if not x.startswith("--")]   # flag-aware positional parse
        cmd_listcmd(kind, pos[0], pos[1], pos[2] if len(pos) > 2 else None, full=("--full" in a))
    elif c == "adventure": cmd_adventure(a[1], a[2], a[3] if len(a) > 3 else None)
    elif c == "migrate": cmd_migrate(a[1])
    elif c == "list-count": cmd_list_count(a[1])
    else: sys.exit(f"Unknown command '{c}'. See --help.")

if __name__ == "__main__":
    main()
