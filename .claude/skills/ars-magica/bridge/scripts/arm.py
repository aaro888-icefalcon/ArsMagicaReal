#!/usr/bin/env python3
"""
arm.py — single entry point for the Ars Magica companion logic. Every uncertain outcome is
rolled honestly and shown; campaign state is read/written in the engine's schema.

  RESOLUTION (resolve.py)
    arm.py roll [stress|simple] [--botch N]
    arm.py ability --char N --ability N [--ef N] [--simple] [--botch N]
    arm.py cast --te N --fo N --sta N --aura N [--enc N] --level N
                [--kind formulaic|spont-fat|spont-nonfat|ritual] [--calm] [--artes N --philos N] [--pen N] [--botch N]
    arm.py combat init --mod N        | arm.py combat attack --atk N --def N --dam N --soak N [--size 0]
    arm.py npc stat --expect N --answer yes|exc_yes|no|exc_no   | arm.py npc might --realm R --might N

  LONG-TERM (advanced.py)
    arm.py certamen init --qik N --finesse N
    arm.py certamen --a-pre N --a-art N --a-int N --a-pen N --d-per N --d-art N --d-sta N --d-parma N
    arm.py aging --age N [--living N] [--longevity N]   | arm.py crisis --age N [--decrepitude N]
    arm.py warping --points N [--prev N]

  THEMES — yearly, constrained, coverage-gated (themes.py)
    arm.py themes new-year --campaign DIR [--year N] [--force]
    arm.py themes status|show|record --campaign DIR [--used Mystery,Social]

  CHARACTER CREATOR — guided, validated build (chargen.py)
    arm.py char new --type magus|companion|grog [--name N] [--campaign DIR]
    arm.py char houses | points --set "Int=3,…" | vf --type T --virtues … --flaws …
    arm.py char cost --ability N|--art N | spellcap --te N --fo N --int N --mt N | abilities | budget --type T

  ELEMENTS — atomic setting library, insert/surface into the live Lists (elements.py)
    arm.py element search|show|insert|surface|new …

  REFERENCE
    arm.py realm --aura N --realm Magic|Faerie|Divine|Infernal     (aura modifier to magic)
"""
import sys
import armcore as C

def cmd_realm(argv):
    aura = C.opt(argv, "--aura", 0, int); realm = (C.opt(argv, "--realm", "Magic") or "Magic").capitalize()
    tbl = C.load_rule("realm_interaction")
    row = tbl["auras"].get(realm)
    if not row: sys.exit("--realm Magic|Faerie|Divine|Infernal")
    print(f"🌀 In a {realm} aura of {aura}:")
    for power, expr in row["to_power"].items():
        val = eval(expr, {"a": aura})   # expr uses 'a' = aura, e.g. "a", "-3*a", "a//2"
        print(f"   {power:9} magic: {val:+d}" + ("   (extra botch dice when foreign to the aura)"
                                                 if power != realm and val < 0 else ""))
    print(f"   note: {row.get('note', '')}")

def roll_alias(argv):
    # `arm.py roll` / `roll stress` / `roll simple` → resolve.roll
    import resolve
    rest = argv[1:]
    if rest and rest[0] == "simple": rest = ["--simple"] + rest[1:]
    elif rest and rest[0] == "stress": rest = rest[1:]
    resolve.cmd_roll(["roll"] + rest)

def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"): print(__doc__); return
    head = a[0]
    if head == "roll":
        roll_alias(a)
    elif head in ("ability", "cast", "combat", "npc"):
        import resolve; resolve.run(a)
    elif head in ("certamen", "aging", "crisis", "warping"):
        import advanced; advanced.run(a)
    elif head == "char":
        import chargen; chargen.run(a[1:])
    elif head == "themes":
        import themes; themes.run(a[1:])
    elif head == "element":
        import elements; elements.run(a[1:])
    elif head == "realm":
        cmd_realm(a)
    else:
        sys.exit(f"unknown command '{head}'. See arm.py --help.")

if __name__ == "__main__":
    main()
