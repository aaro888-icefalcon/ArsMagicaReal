# System Profile — Ars Magica 5th Edition (Definitive Edition)   (hook: resolve)

> The RPG owns task resolution and combat; Mythic answers world questions and paces.
> `python3 ../../mythic-gm/scripts/system.py route` prints the seam.
> **Precedence:** this profile > the rulebooks in `reviewed/` > training knowledge.
> Faithful to *Ars Magica – Definitive Edition (Core Rules)*; chapter cites in‑line.

> **Scripted resolution (preferred).** The formulas below are encoded in **`scripts/arm.py`** so play is
> consistent and the dice are honest and shown — use it instead of doing the math by hand:
> `arm.py roll [stress|simple] [--botch N]` · `arm.py ability --char N --ability N [--ef N]` ·
> `arm.py cast --te N --fo N --sta N --aura N --level N [--kind formulaic|spont-fat|spont-nonfat|ritual]` ·
> `arm.py combat init\|attack …` · `arm.py npc stat\|might …` · `arm.py realm --aura N --realm <R>` ·
> `arm.py certamen …` · `arm.py aging --age N …` · `arm.py crisis …` · `arm.py warping --points N …`.
> The data tables live in `data/rules/*.json`. This prose remains the reference for *why* each number is what it is.

## Dice convention — the d10 "stress" and "simple" die  (Ch.1, Die Rolls)
All randomness goes through the engine: **`python3 ../../mythic-gm/scripts/dice.py roll 1d10`**.
The engine reports a face of **1–10**. Map it to the Ars Magica die:

- **Simple die** (calm, no botch possible): face value as rolled. *(The Ars "0" face = 10; the engine already shows 10, so use the number shown.)* No explosion, no botch.
- **Stress die** (pressure, danger, fatiguing magic, combat, rituals): read the shown face, then:
  - **Face `1` → explodes.** Roll `dice.py roll 1d10` again and **double** the new result; if that reroll is also `1`, roll again and **quadruple** (each further `1` doubles the multiplier: ×2, ×4, ×8 …). Treat a rolled `10` on a reroll as ten.
  - **Face `10` → the Ars "0": check for a botch.** Roll the botch dice: **`dice.py roll Nd10`** where **N = number of botch dice** (default **1**; +1 per aggravating factor, +1 per pawn of vis used to boost, double in a foreign‑realm aura, etc.). **Any die showing `10` (the "0" face) = a BOTCH.** On a botch the total is **0 and the Characteristic/Art total is negated**, plus something goes seriously wrong (more zeros = worse). No `10` on the botch dice → the die simply contributed 0.
  - **Faces `2`–`9` →** their value.
  Some stress rolls cannot botch (then a `10` is just 0); qualities can reduce botch dice to zero.

**Always show the roll** (the bracketed `[Adjudication: …]` block) and the explosion/botch resolution.

## Core resolution  (Ch.1)
**Characteristic + Ability + die  vs.  Ease Factor.** Equal‑or‑exceed succeeds; the margin shows how well.
Ease‑Factor ladder: **3** Simple · **6** Easy · **9** Average · **12** Hard · **15** Very Hard · **18** Impressive · **21** Remarkable · **24+** near‑impossible. When a rule divides and is silent on rounding, **round down**.

- **Degrees of success?** **Partial.** The margin over the Ease Factor is the degree; a **botch** is the catastrophic low. For a **rule‑mode Fate Question** standing in for a roll (`dice.py fate <odds> <cf> --mode rule`): map **Exceptional Yes → a clear success / flourish (treat as beating the EF handily)**, **Exceptional No → a botch (something goes badly wrong)**.

## Characteristics & Abilities  (Ch.3, Ch.5)
- **Characteristics** (−3…+3, average 0): **Int, Per, Pre, Com, Str, Sta, Dex, Qik.** Also **Size** (humans 0), **Confidence** (magi/companions: Score, Points; +3 to a roll per Point spent), **Decrepitude**, **Warping Score**.
- **Ability score** N (benchmarks: 3 moderate, 6 skilled, 9 very skilled); roll = Char + Ability + die. Specialization gives +1 when relevant. Types: General, Academic, Arcane, Martial, Supernatural, Spell Mastery (magi).

## Hermetic magic  (Ch.7)  — magi only
**Casting Score = Technique + Form + Stamina − Encumbrance + Aura Modifier.** Then:
| Spell type | Casting Total | Notes |
|---|---|---|
| **Formulaic** | Casting Score **+ die** (stress if stressful; simple if calm) | Cast if Total **≥ spell Level**. Short by 1–10 → cast, −1 Fatigue. Short by 11+ → fails, −1 Fatigue. |
| **Spontaneous, fatiguing** | **(Casting Score + Stress die) / 2** | Always stress die, always −1 Fatigue. |
| **Spontaneous, non‑fatiguing** | **Casting Score / 5** | No die, no botch, no Fatigue. |
| **Ritual** | **Casting Score + Artes Liberales + Philosophiae + Stress die** | 15 min & 1 pawn vis per magnitude; Fatigue is long‑term, shortfall converts to wounds. |
- **Aura Modifier** comes from the Realm of the scene's aura (Realm Interaction Table — see `interpretation.md`/`setting-canon.md`): Magic/Faerie auras boost Hermetic casting; **Infernal −aura, Divine −3×aura** (and add botch dice in foreign auras).
- **Penetration Total = Casting Total − Spell Level + Penetration Bonus.** A spell affects a resisting target only if **Penetration > the target's Magic Resistance**.
- **Magic Resistance:** base = the magus's score in the most applicable **Form** (Vim by default); **Parma Magica adds 5 × Parma score**; **Form Bonus = Form/5 round‑up** vs related mundane harm. A creature's **MR = its Might (+ aura modifier).**

## Combat  (Ch.11) — every total adds a **stress die** except Damage and Soak
- **Initiative = Qik + weapon Init − Encumbrance + stress die** (rolled once; high goes first; ties reroll).
- **Attack = Dex + Combat Ability + weapon Attack + stress die.**
- **Defense = Qik + Combat Ability + weapon Defense + stress die.** (A **Defense botch** drops Defense to 0 — usually fatal.)
- Hit if **Attack > Defense**; **Attack Advantage = Attack − Defense**.
- **Damage = Str + weapon Damage + Attack Advantage** (no die)  vs  **Soak = Sta + armour (+ Form Bonus for magi)** (no die).
- **Wounds** from (Damage − Soak), read against **Size**. For **Size 0**: Light **1–5** (−1), Medium **6–10** (−3), Heavy **11–15** (−5), Incapacitating **16–20** (no actions), **Dead 21+**. Each ±1 Size shifts the bands; every 5+Size over Soak raises the wound a level. Penalties are cumulative (with each other and Fatigue), apply to all rolls/totals **except Soak**.
- **Incapacitated → Dying:** two Recovery rolls/day; **0 or less → dies**; **9+** improves all Incapacitating wounds to Heavy.

## Certámen  (Ch.7) — the lawful wizard's duel; resolve as opposed Art totals  → `arm.py certamen`
Init = Qik + Finesse + stress. Each round: **Attack = Pre + (Technique *or* Form) + stress**, **Defense = Per + (the other Art) + stress**; **Attack Advantage = Atk − Def**. **Weakening = Int + Penetration + Advantage** vs **Resistance = Sta + Parma** (Parma added, *not* ×5); every 5 over = 1 Fatigue lost. Certámen causes **only exhaustion, never wounds**. Win on the opponent falling unconscious, surrendering, or failing Concentration.

## Fatigue  (Ch.11)  — ladder: **Fresh 0 · Winded 0 · Weary −1 · Tired −3 · Dazed −5 · Unconscious**
Short‑term Fatigue test: Sta − Enc + stress vs EF 6 (fail −1 level, botch −2). Long‑term Fatigue: 1 level back per night's sleep. Penalty applies to everything except Soak.

## Long‑term & defeat  — keep the discipline; defeat is real
- **Aging** (yearly from age 35) → `arm.py aging --age N [--living N] [--longevity N]` (and `arm.py crisis …`): Aging Total = stress(no botch) + age/10 (round up) − living‑conditions − longevity ritual; accrues Aging Points → Characteristic loss & Decrepitude; 13 or 22+ triggers a Crisis. Magic can **slow but never halt or reverse** aging. (Tables: `data/rules/aging.json`.)
- **Warping & Twilight** → `arm.py warping --points N [--prev N]`: strong auras (6+), powerful/constant magic, and **supernatural botches** (1 Warping Point per `0` on the botch dice) raise a magus's Warping Score (5 × new score in points to advance) and risk **Wizard's Twilight**. (Tables: `data/rules/warping.json`; see `subsystems.md`.)
- **Death/defeat is honest:** grogs die, magi fall, demons revert to spirit and flee, faeries withdraw when denied their story. Never narrate a rescue the dice didn't grant.

## NPC stat units & on‑the‑fly statting  (Ch.3, Ch.13)
Humans: **Characteristics (−3…+3), Size, relevant Abilities, Soak (Sta+armour), Fatigue/Wound bands by Size**, Personality Traits, Reputation. **Creatures add a `Might (Realm)` score** (Magic/Faerie/Infernal/Divine) that **doubles as their Magic Resistance** and fuels level‑less powers from a Might Pool; Might 20 challenges a fresh magus, 40 a mid‑age one, 75 ≈ near‑immune to Hermetic magic. To stat on the fly: decide the expected value → Fate Question → read **`oracle.py answer npc_statistics …`** (Yes = as expected; ExcYes +25%; No −25%; ExcNo −50%); for a supernatural foe also fix a **Might (Realm)**.

## Routing default
**RPG resolves:** ability rolls, spellcasting, combat, Certámen, lab/seasonal activity, aging, Recovery. **Fate Questions resolve:** world questions, NPC intentions, whether a rumor is true, what's behind the door — anything with no Ars Magica mechanic. Subsystems run as scripted ticks (`subsystems.md`) or rule‑mode Fate Questions: e.g. an offscreen lab season's success, a vis source's yield, a Tribunal vote's outcome.
