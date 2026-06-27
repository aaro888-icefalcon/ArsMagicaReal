# World Subsystems — Mythic Europe (Ars Magica 5e)   (hook: world-tick; fired by tick.py at bookkeeping)
# `python3 ../../mythic-gm/scripts/tick.py <this-bridge-dir> <scene#>` reports which are DUE; then
# run the named arm.py command / roll the named table HONESTLY and record the result to campaign-state.md.
# arm.py = ./scripts/arm.py.  cadence: 'every scene' | 'every N scenes' | 'on trigger: …'

| subsystem | cadence | advance by |
|-----------|---------|-----------|
| Aura & Realm watch | every scene | Note the place's Realm and aura; `arm.py realm --aura <n> --realm <R>` prints the modifier to apply to casting totals and botch dice. A change of place re-checks for a regio. |
| Warping & Twilight | every scene | If a magus stood in aura 6+, cast a 6th-magnitude+/constant effect, or BOTCHED a supernatural roll, accrue Warping Points (1 per `0` on the botch dice); `arm.py warping --points <total> --prev <old>` reports the Score and flags Twilight. |
| Theme coverage | every scene | `arm.py themes record --campaign <dir> --used <themes this scene used>`; `arm.py themes status` shows which themes still need a beat before New Year. |
| Covenant season clock | every 3 scenes | Advance one season (Spring→Summer→Autumn→Winter). Resolve each magus's seasonal Lab/study activity offscreen. **At Winter→Spring (new year): `arm.py themes new-year --campaign <dir>`** (re-rolls the year's theme order; coverage-gated). |
| Aging | on trigger: each in-game year (Winter) for any character aged 35+ | `arm.py aging --age <n> [--living <m>] [--longevity <m>]` per such character (and `arm.py crisis …` on a 13/22+); apply Aging Points / Decrepitude / Crisis. |
| Vis economy | on trigger: when a vis source's season comes due, or vis is spent | Add the source's pawns (by Art) to covenant stores; deduct vis used on Ritual magic, enchantment, or boosting. Track scarcity. |
| Order & Tribunal politics | every 5 scenes | A Hermetic faction moves toward/away from an open Thread — `arm.py element surface --campaign <dir>` for a relevant atom, or roll `generators/story_hook.json`. |
| Mundane authority pressure | every 4 scenes | If a Thread involves a lord, bishop, abbot, or town, that authority advances its agenda — Fate Question for the move. |
| Seed refresh | every scene | `arm.py element surface --campaign <dir> --here "<place/realm tags>"` proposes dormant atoms to feed the 30–40 seed deck. |
