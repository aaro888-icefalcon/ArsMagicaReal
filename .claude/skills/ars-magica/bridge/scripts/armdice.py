#!/usr/bin/env python3
"""
armdice.py — the Ars Magica d10 die, honest and shown. Engine convention: a d10 rolls 1..10
with the face 10 standing for the Ars "0" (the ten / botch face).

  simple_die()              -> face value (10 = ten); no explosion, no botch.
  stress_die(botch_dice=N)  -> 2..9 = value; 1 explodes (reroll & double, repeating);
                               10 = the "0": roll N botch dice (d10), any 10 ("0") = BOTCH
                               (value forced to 0 and the actor's modifier is negated upstream).

Every result is a dict carrying the faces rolled, so callers can print the whole roll.
CLI:  python3 armdice.py stress [--botch N] | simple
"""
import random, sys

def _d10(): return random.randint(1, 10)     # 1..10; 10 == the Ars "0"/ten face

def simple_die():
    r = _d10()
    return {"kind": "simple", "faces": [r], "value": r, "botch": False}

def stress_die(botch_dice=1):
    faces = []
    r = _d10(); faces.append(r)
    if r == 1:                                # explode: reroll & double, repeat on further 1s
        mult = 2
        while True:
            r2 = _d10(); faces.append(r2)
            if r2 == 1:
                mult *= 2; continue
            return {"kind": "stress", "faces": faces, "value": r2 * mult,
                    "botch": False, "exploded": True, "mult": mult}
    if r == 10:                               # the "0": botch check
        bd = max(0, int(botch_dice))
        bfaces = [_d10() for _ in range(bd)]
        zeros = sum(1 for b in bfaces if b == 10)
        return {"kind": "stress", "faces": faces, "value": 0,
                "botch": zeros > 0, "botch_count": zeros, "botch_dice": bd, "botch_faces": bfaces}
    return {"kind": "stress", "faces": faces, "value": r, "botch": False}

def render(roll):
    """Human one-liner for a die result."""
    if roll["kind"] == "simple":
        return f"simple die [{roll['faces'][0]}] → {roll['value']}"
    if roll.get("exploded"):
        chain = "→".join(str(f) for f in roll["faces"])
        return f"stress die [{chain}] EXPLODES (×{roll['mult']}) → {roll['value']}"
    if roll["faces"][0] == 10:
        bd = roll.get("botch_dice", 0); bf = roll.get("botch_faces", [])
        if roll["botch"]:
            return (f"stress die [0] → BOTCH! ({roll['botch_count']} zero(s) on {bd} botch dice "
                    f"{bf}) → value 0, modifier NEGATED")
        return f"stress die [0] → no botch ({bd} botch dice {bf}, no zeros) → value 0"
    return f"stress die [{roll['faces'][0]}] → {roll['value']}"

def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"): print(__doc__); return
    if a[0] == "simple":
        print("🎲 " + render(simple_die())); return
    if a[0] == "stress":
        bd = int(a[a.index("--botch") + 1]) if "--botch" in a else 1
        print("🎲 " + render(stress_die(bd))); return
    sys.exit("usage: armdice.py stress [--botch N] | simple")

if __name__ == "__main__":
    main()
