#!/usr/bin/env python3
"""
resolve.py — Ars Magica 5e task resolution, honest dice shown (hook: resolve).
Phase-1 subcommands: roll, ability, cast, combat, npc. (certamen/aging/warping → Phase 2.)
All math is faithful to the Core Rules; the stress/simple die comes from armdice.py.
"""
import math, sys
import armcore as C
import armdice as D

# --- wound bands by Size: band width = 5 + Size; level = ceil(over_soak / width) ----
WOUND_LEVELS = ["—", "Light (-1)", "Medium (-3)", "Heavy (-5)", "Incapacitated", "Dead"]
def wound_for(over_soak, size):
    if over_soak <= 0: return 0, "no wound"
    width = max(1, 5 + size)
    lvl = math.ceil(over_soak / width)
    lvl = min(lvl, 5)
    return lvl, WOUND_LEVELS[lvl]

def _die(stress, botch):
    return D.stress_die(botch) if stress else D.simple_die()

def cmd_roll(argv):
    stress = not C.has(argv, "--simple")
    botch = C.opt(argv, "--botch", 1, int)
    r = _die(stress, botch)
    print("🎲 " + D.render(r))

def cmd_ability(argv):
    """Characteristic + Ability + die vs Ease Factor."""
    char = C.opt(argv, "--char", 0, int); ab = C.opt(argv, "--ability", 0, int)
    ef = C.opt(argv, "--ef", None, int); stress = not C.has(argv, "--simple")
    botch = C.opt(argv, "--botch", 1, int)
    r = _die(stress, botch)
    total = (char + ab + r["value"]) if not r["botch"] else 0
    line = f"[Adjudication] {D.render(r)} | Char {char:+d} + Ability {ab:+d} + die {r['value']} = {total}"
    if ef is not None:
        line += f"  vs EF {ef} → {'SUCCESS' if total >= ef else 'FAILURE'}" + (" (BOTCH)" if r['botch'] else "")
    print("⚖️  " + line)

def cmd_cast(argv):
    te = C.opt(argv, "--te", 0, int); fo = C.opt(argv, "--fo", 0, int)
    sta = C.opt(argv, "--sta", 0, int); aura = C.opt(argv, "--aura", 0, int)
    enc = C.opt(argv, "--enc", 0, int); level = C.opt(argv, "--level", 0, int)
    kind = C.opt(argv, "--kind", "formulaic")
    calm = C.has(argv, "--calm"); botch = C.opt(argv, "--botch", 1, int)
    pen = C.opt(argv, "--pen", 0, int)
    artes = C.opt(argv, "--artes", 0, int); philos = C.opt(argv, "--philos", 0, int)
    score = te + fo + sta - enc + aura
    head = f"Casting Score = Te {te} + Fo {fo} + Sta {sta} − Enc {enc} + Aura {aura:+d} = {score}"
    if kind == "spont-nonfat":
        total = score // 5
        print(f"✨ [Adjudication] {head}\n   Spontaneous (non-fatiguing) = Score/5 = {total}  (no die, no botch, no Fatigue)")
    elif kind == "spont-fat":
        r = D.stress_die(botch); base = score + r["value"]; total = 0 if r["botch"] else base // 2
        print(f"✨ [Adjudication] {head}\n   {D.render(r)}\n   Spontaneous (fatiguing) = (Score {score} + die {r['value']})/2 = {total}  · −1 Fatigue")
        _cast_outcome(total, level, pen, fatiguing=False)
        return
    elif kind == "ritual":
        r = D.stress_die(botch); total = 0 if r["botch"] else score + artes + philos + r["value"]
        print(f"✨ [Adjudication] {head}\n   {D.render(r)}\n   Ritual = Score {score} + Artes Lib {artes} + Philos {philos} + die {r['value']} = {total}  (long-term Fatigue)")
        _cast_outcome(total, level, pen, fatiguing=True)
        return
    else:  # formulaic
        r = _die(not calm, botch); total = 0 if r.get("botch") else score + r["value"]
        print(f"✨ [Adjudication] {head}\n   {D.render(r)}\n   Formulaic = Score {score} + die {r['value']} = {total}")
        _cast_outcome(total, level, pen, fatiguing=True)
        return
    _cast_outcome(total, level, pen, fatiguing=False)

def _cast_outcome(total, level, pen, fatiguing):
    diff = total - level
    if diff >= 0: res = "CAST — full success, 0 Fatigue"
    elif diff >= -10: res = "CAST — fell short ≤10, lose 1 Fatigue" if fatiguing else "CAST — fell short"
    else: res = "FAILS — short by >10" + (", lose 1 Fatigue" if fatiguing else "")
    pt = total - level + pen
    print(f"   vs Level {level}: {res}")
    print(f"   Penetration = Total {total} − Level {level} + Bonus {pen} = {pt}  "
          f"({'affects targets with MR < ' + str(pt) if pt > 0 else 'no penetration — fails vs any Magic Resistance'})")

def cmd_combat(argv):
    sub = argv[1] if len(argv) > 1 else ""
    botch = C.opt(argv, "--botch", 1, int)
    if sub == "init":
        mod = C.opt(argv, "--mod", 0, int); r = D.stress_die(botch)
        print(f"⚔️  [Init] {D.render(r)} | Qik+wpn {mod:+d} + die {0 if r['botch'] else r['value']} = "
              f"{0 if r['botch'] else mod + r['value']}")
        return
    if sub == "attack":
        atk = C.opt(argv, "--atk", 0, int); dfn = C.opt(argv, "--def", 0, int)
        dam = C.opt(argv, "--dam", 0, int); soak = C.opt(argv, "--soak", 0, int)
        size = C.opt(argv, "--size", 0, int)
        ra = D.stress_die(botch); rd = D.stress_die(botch)
        atk_total = 0 if ra["botch"] else atk + ra["value"]
        def_total = 0 if rd["botch"] else dfn + rd["value"]
        print(f"⚔️  [Attack] {D.render(ra)} | Attack {atk:+d} + die = {atk_total}")
        print(f"    [Defense] {D.render(rd)} | Defense {dfn:+d} + die = {def_total}")
        adv = atk_total - def_total
        if adv <= 0:
            print(f"    → MISS (advantage {adv} ≤ 0)"); return
        dmg = dam + adv; over = dmg - soak
        lvl, label = wound_for(over, size)
        print(f"    → HIT (advantage {adv}); Damage = Str+wpn {dam} + advantage {adv} = {dmg}  vs Soak {soak}")
        print(f"    → {dmg} − {soak} = {over} over Soak, Size {size:+d} → **{label}**")
        return
    sys.exit("usage: combat init --mod N | combat attack --atk N --def N --dam N --soak N [--size 0]")

def cmd_npc(argv):
    sub = argv[1] if len(argv) > 1 else ""
    if sub == "stat":     # NPC Statistics Table: decide expected value, Fate-Q answer scales it
        exp = C.opt(argv, "--expect", 0, int); ans = C.opt(argv, "--answer", "yes")
        mult = {"yes": 1.0, "exc_yes": 1.25, "no": 0.75, "exc_no": 0.5}.get(ans)
        if mult is None: sys.exit("--answer yes|exc_yes|no|exc_no")
        print(f"📐 NPC Statistics: expected {exp}, answer {ans} → {round(exp * mult)}  "
              f"(Yes=as expected, ExcYes +25%, No −25%, ExcNo −50%)")
        return
    if sub == "might":
        realm = C.opt(argv, "--realm", "Magic"); might = C.opt(argv, "--might", 0, int)
        print(f"👁  {realm} Might {might} → Magic Resistance {might}; powers cost from a Might Pool of {might}.")
        return
    sys.exit("usage: npc stat --expect N --answer yes|exc_yes|no|exc_no | npc might --realm R --might N")

def run(argv):
    if not argv or argv[0] in ("-h", "--help"): print(__doc__); return
    {"roll": cmd_roll, "ability": cmd_ability, "cast": cmd_cast,
     "combat": lambda a: cmd_combat(a), "npc": lambda a: cmd_npc(a)}.get(
        argv[0], lambda a: sys.exit(f"unknown resolve command '{argv[0]}'"))(argv)

if __name__ == "__main__":
    run(sys.argv[1:])
