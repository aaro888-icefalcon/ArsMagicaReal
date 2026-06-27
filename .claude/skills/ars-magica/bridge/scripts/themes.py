#!/usr/bin/env python3
"""
themes.py — the YEARLY Ars Magica theme engine (hook: themes).

Each in-game New Year the 5 Adventure-Crafter themes are re-ordered (so the priorities
change every year), drawn by the saga's base weights but constrained:

  C1  Action   is one of the top THREE priorities      (pos ≤ 3)
  C2  Social   is one of the top FOUR  priorities       (pos ≤ 4)
  C3  Personal OR Social is one of the top TWO           (pos ≤ 2)
  C4  every theme is present (a full permutation) AND must be USED at least once per year
      — enforced by a hard coverage gate at year roll-over.

The order is written to the campaign's adventure.json (theme_order, which the engine's
adventure_crafter.py reads) and mirrored, with a per-year usage tally, in year-state.json.

Commands (all take --campaign DIR):
  new-year [--year N] [--force]   Close the old year (coverage gate) and roll the new order.
  status                          Show this year's order + which themes still need a beat.
  record --used Mystery,Social    Tally themes that drove a Turning Point / scene this year.
  show                            Print the current order only.
Roll the draw transparently: every rejected draw is shown.
"""
import random, sys
import armcore as C

BASE_WEIGHTS = {"Mystery": 5, "Social": 5, "Personal": 4, "Tension": 3, "Action": 2}

def weighted_order(weights):
    pool = list(weights.items()); order = []
    while pool:
        total = sum(w for _, w in pool); r = random.uniform(0, total); acc = 0
        for i, (t, w) in enumerate(pool):
            acc += w
            if r <= acc: order.append(t); pool.pop(i); break
    return order

def satisfies(order):
    p = {t: i + 1 for i, t in enumerate(order)}
    return p["Action"] <= 3 and p["Social"] <= 4 and (p["Social"] <= 2 or p["Personal"] <= 2)

def generate(weights=BASE_WEIGHTS, max_tries=300, verbose=True):
    """Rejection-sample a weighted permutation until the constraints hold (preserves the
    weighted distribution conditioned on the rules). Falls back to a uniform pick among all
    satisfying permutations if the draw is pathologically unlucky."""
    for n in range(1, max_tries + 1):
        o = weighted_order(weights)
        if satisfies(o):
            if verbose: print(f"   draw #{n}: {', '.join(o)}  ✓ satisfies the constraints")
            return o, n
        if verbose and n <= 8: print(f"   draw #{n}: {', '.join(o)}  ✗ rejected")
    from itertools import permutations
    ok = [list(p) for p in permutations(C.THEMES) if satisfies(p)]
    o = random.choice(ok)
    if verbose: print(f"   (fallback) uniform pick among {len(ok)} valid orders: {', '.join(o)}")
    return o, max_tries

def _write_order(campaign, order, year):
    L = C.lists()
    adv = L.load_adventure(campaign); adv["theme_order"] = order; L.save_adventure(campaign, adv)
    C.save_year(campaign, {"year": year, "theme_order": order,
                           "themes_used": {t: 0 for t in C.THEMES}})

def cmd_new_year(campaign, year_arg, force):
    ys = C.load_year(campaign)
    if ys:                                    # close the OLD year: coverage gate (C4)
        unused = [t for t in C.THEMES if ys.get("themes_used", {}).get(t, 0) == 0]
        if unused and not force:
            print(f"⛔ Year {ys['year']} cannot close — these themes were never used: {', '.join(unused)}")
            print("   Run a forced beat for each before rolling the new year, e.g.:")
            print(f"     python3 {C.ENGINE}/adventure_crafter.py turning-point --campaign {campaign} "
                  f"--themes {','.join(unused)}")
            print("   …then `themes record --used " + ",".join(unused) + "`. "
                  "(Or pass --force to override.)")
            sys.exit(2)
        new_year = year_arg if year_arg is not None else ys["year"] + 1
    else:
        new_year = year_arg if year_arg is not None else 1220   # default saga start
    print(f"🎭 NEW YEAR {new_year} — rolling theme priorities (weights {BASE_WEIGHTS}):")
    order, _ = generate()
    _write_order(campaign, order, new_year)
    print("   Priority order: " + " > ".join(f"{i+1}.{t}" for i, t in enumerate(order)))
    print(f"   ✔ written to adventure.json (theme_order) and year-state.json (year {new_year}).")
    print("   Each theme must drive at least one beat before next New Year (coverage gate).")

def cmd_status(campaign):
    ys = C.load_year(campaign)
    if not ys: sys.exit("No year-state.json yet — run `themes new-year --campaign <dir>` first.")
    print(f"🎭 Year {ys['year']} — " + " > ".join(f"{i+1}.{t}" for i, t in enumerate(ys["theme_order"])))
    used = ys.get("themes_used", {})
    for t in ys["theme_order"]:
        n = used.get(t, 0)
        print(f"   {'✓' if n else '·'} {t:8} used {n}×")
    pending = [t for t in C.THEMES if used.get(t, 0) == 0]
    print("   coverage: " + ("ALL themes used ✓" if not pending else "still needed → " + ", ".join(pending)))

def cmd_record(campaign, used_csv):
    ys = C.load_year(campaign)
    if not ys: sys.exit("No year-state.json yet — run `themes new-year` first.")
    bumped = []
    for t in [x.strip().capitalize() for x in used_csv.split(",") if x.strip()]:
        if t in C.THEMES:
            ys["themes_used"][t] = ys["themes_used"].get(t, 0) + 1; bumped.append(t)
    C.save_year(campaign, ys)
    print(f"📌 recorded use of: {', '.join(bumped) if bumped else '(nothing valid)'}")
    cmd_status(campaign)

def cmd_show(campaign):
    L = C.lists(); print(" > ".join(L.load_adventure(campaign)["theme_order"]))

def run(argv):
    if not argv or argv[0] in ("-h", "--help"): print(__doc__); return
    campaign = C.opt(argv, "--campaign")
    if not campaign: sys.exit("themes needs --campaign <dir>")
    cmd = argv[0]
    if cmd == "new-year":
        cmd_new_year(campaign, C.opt(argv, "--year", None, int), C.has(argv, "--force"))
    elif cmd == "status": cmd_status(campaign)
    elif cmd == "record": cmd_record(campaign, C.opt(argv, "--used", ""))
    elif cmd == "show":   cmd_show(campaign)
    else: sys.exit(f"unknown themes command '{cmd}'")

if __name__ == "__main__":
    run(sys.argv[1:])
