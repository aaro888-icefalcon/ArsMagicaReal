#!/usr/bin/env python3
"""
tick.py — world-tick dispatcher (hook: world-tick). At bookkeeping, reads the
companion's subsystems.md registry and reports which subsystems are DUE this scene
and how to advance them (the engine then rolls the named tables honestly).

Usage:  python3 scripts/tick.py <bridge_dir> <scene_number>
A subsystem row is:  | name | cadence | advance by |
cadence: 'every scene' | 'every N scenes' | 'on trigger: …'
"""
import os, re, sys

def main():
    if len(sys.argv) < 3:
        print(__doc__); return
    bdir, scene = sys.argv[1], int(sys.argv[2])
    p = os.path.join(bdir, "subsystems.md")
    if not os.path.exists(p):
        print("No subsystems.md — only Mythic's default offscreen-clock advance applies."); return
    due = []
    for ln in open(p, encoding="utf-8"):
        if not ln.strip().startswith("|"): continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0].lower() in ("subsystem","name","") or set(cells[0]) <= set("-"): continue
        name, cadence, advance = cells[0], cells[1].lower(), cells[2]
        fire = False
        if "every scene" in cadence: fire = True
        else:
            m = re.search(r"every\s+(\d+)", cadence)
            if m and scene % int(m.group(1)) == 0: fire = True
            elif "trigger" in cadence: fire = None  # conditional — surface for the GM to judge
        if fire is True: due.append((name, advance, "DUE"))
        elif fire is None: due.append((name, advance, "check trigger"))
    print(f"🌍 WORLD TICK — scene {scene}")
    if not due: print("   (nothing due this scene)")
    for name, advance, status in due:
        print(f"   • [{status}] {name} → {advance}")
    print("   → advance each by rolling its named table (dice.py table <path>) / ticking its clock; record to state.")

if __name__ == "__main__":
    main()
