#!/usr/bin/env python3
"""
advanced.py — Certámen, Aging, and Warping resolution (honest dice, shown).
Faithful to the Core Rules; tables in data/rules/{certamen,aging,warping}.json.
"""
import math, sys
import armcore as C
import armdice as D

# ---------------------------------------------------------------- Certámen
def cmd_certamen(argv):
    import character
    pc = character.pc_from_argv(argv)          # attacker (--pc)
    defc = None
    if C.opt(argv, "--pc-def"): defc = character.load(C.opt(argv, "--campaign"), C.opt(argv, "--pc-def"))
    if len(argv) > 1 and argv[1] == "init":
        qik = C.opt(argv, "--qik", character.char_val(pc, "Qik") if pc else 0, int)
        fin = C.opt(argv, "--finesse", character.ability_score(pc, "Finesse") if pc else 0, int)
        r = D.stress_die(1)
        print(f"⚔️  [Certámen Init]{' '+pc['name'] if pc else ''} {D.render(r)} | Qik {qik:+d} + Finesse {fin} + die = "
              f"{0 if r['botch'] else qik + fin + r['value']}")
        return
    # --a-art / --d-art may be an Art NAME (resolved from the PC) or a numeric score
    def art_or_num(flag, who):
        v = C.opt(argv, flag)
        if v is None: return 0
        try: return int(v)
        except ValueError: return character.art_score(who, v) if who else 0
    a_pre = C.opt(argv, "--a-pre", character.char_val(pc, "Pre") if pc else 0, int)
    a_int = C.opt(argv, "--a-int", character.char_val(pc, "Int") if pc else 0, int)
    a_pen = C.opt(argv, "--a-pen", character.ability_score(pc, "Penetration") if pc else 0, int)
    a_art = art_or_num("--a-art", pc)
    d_per = C.opt(argv, "--d-per", character.char_val(defc, "Per") if defc else 0, int)
    d_sta = C.opt(argv, "--d-sta", character.char_val(defc, "Sta") if defc else 0, int)
    d_parma = C.opt(argv, "--d-parma", character.parma(defc) if defc else 0, int)
    d_art = art_or_num("--d-art", defc)
    ra = D.stress_die(1); rd = D.stress_die(1)
    atk = 0 if ra["botch"] else a_pre + a_art + ra["value"]
    dfn = 0 if rd["botch"] else d_per + d_art + rd["value"]
    print(f"⚔️  [Certámen round]\n   Attack  {D.render(ra)} | Pre {a_pre:+d} + Art {a_art} + die = {atk}")
    print(f"   Defense {D.render(rd)} | Per {d_per:+d} + Art {d_art} + die = {dfn}")
    adv = atk - dfn
    if adv <= 0:
        print(f"   → no advantage ({adv}); defender holds, no Fatigue this round."); return
    weak = a_int + a_pen + adv; resist = d_sta + d_parma
    over = weak - resist
    fat = math.ceil(over / 5) if over > 0 else 0
    print(f"   Advantage {adv} → Weakening = Int {a_int:+d} + Pen {a_pen} + Adv {adv} = {weak}")
    print(f"   vs Resistance = Sta {d_sta:+d} + Parma {d_parma} = {resist}")
    print(f"   → {over} over → defender loses {fat} Fatigue level(s)  (exhaustion only, never wounds)")

# ---------------------------------------------------------------- Aging
def _aging_band(total):
    bands = C.load_rule("aging")["result_bands"]
    if total <= 2:  return bands[0]["result"]
    if total <= 9:  return bands[1]["result"]
    if total <= 12: return bands[2]["result"]
    if total == 13: return bands[3]["result"]
    if total <= 21: return next(b["result"] for b in bands if b["band"] == str(total))
    return bands[-1]["result"]

def cmd_aging(argv):
    import character
    pc = character.pc_from_argv(argv)
    age = C.opt(argv, "--age", None, int)
    if pc and age is None: age = pc["age"]["actual"]
    age = age if age is not None else 35
    living = C.opt(argv, "--living", 0, int); longev = C.opt(argv, "--longevity", 0, int)
    r = D.stress_die(0)          # no-botch stress die
    base = age // 10 + (1 if age % 10 else 0)   # ceil(age/10)
    raw = r["value"]
    if longev or living:         # Longevity: 10+ counts as 9 until 35
        if age < 35 and raw >= 10: raw = 9
    total = raw + base - living - longev
    print(f"⏳ [Aging] {D.render(r)} | die {raw} + ceil(age {age}/10)={base} − living {living} − longevity {longev} = {total}")
    print(f"   → {_aging_band(total)}")
    if total == 13 or total >= 22:
        print(f"   ⚠ CRISIS — Crisis Total = simple die + ceil(age/10) + Decrepitude; "
              f"resolve on the Crisis Table (`data/rules/aging.json`).")

def cmd_crisis(argv):
    age = C.opt(argv, "--age", 35, int); decr = C.opt(argv, "--decrepitude", 0, int)
    r = D.simple_die(); base = age // 10 + (1 if age % 10 else 0)
    total = r["value"] + base + decr
    bands = C.load_rule("aging")["crisis_bands"]
    if total <= 8: res = bands[0]["result"]
    elif total <= 14: res = bands[1]["result"]
    elif total >= 19: res = bands[-1]["result"]
    else: res = next(b["result"] for b in bands if b["band"] == str(total))
    print(f"💀 [Crisis] {D.render(r)} | die {r['value']} + ceil(age/10)={base} + Decrepitude {decr} = {total}\n   → {res}")

# ---------------------------------------------------------------- Warping
def _warp_score(points):
    th = C.load_rule("warping")["thresholds"]
    score = 0
    for t in th:
        if points >= t["points_to_reach"]: score = t["score"]
    return score

def cmd_warping(argv):
    import character
    pc = character.pc_from_argv(argv); add = C.opt(argv, "--add", None, int)
    if pc:
        prev_pts = pc["warping"]["points"]
        pts = prev_pts + (add or 0)
        prev = prev_pts
        if add:
            pc["warping"]["points"] = pts; pc["warping"]["score"] = _warp_score(pts)
            character.save(C.opt(argv, "--campaign"), pc)
    else:
        pts = C.opt(argv, "--points", 0, int); prev = C.opt(argv, "--prev", None, int)
    score = _warp_score(pts)
    who = (pc["name"] + ": ") if pc else ""
    print(f"🌀 [Warping] {who}total {pts} Warping Point(s) → Warping Score {score}" + (f"  (+{add})" if pc and add else ""))
    th = C.load_rule("warping")["thresholds"]
    nxt = next((t for t in th if t["points_to_reach"] > pts), None)
    if nxt: print(f"   next: Score {nxt['score']} at {nxt['points_to_reach']} points ({nxt['points_to_reach'] - pts} more)")
    if prev is not None and _warp_score(prev) < score:
        print(f"   ⚠ Warping Score rose {_warp_score(prev)} → {score}: for a magus, check for Wizard's Twilight (Ch.7 Dangers).")

def run(argv):
    if not argv or argv[0] in ("-h", "--help"): print(__doc__); return
    {"certamen": cmd_certamen, "aging": cmd_aging, "crisis": cmd_crisis, "warping": cmd_warping}.get(
        argv[0], lambda a: sys.exit(f"unknown advanced command '{argv[0]}'"))(argv)

if __name__ == "__main__":
    run(sys.argv[1:])
