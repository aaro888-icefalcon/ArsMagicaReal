# World Subsystems — Mythic Europe (Ars Magica 5e)   (hook: world-tick; fired by tick.py at bookkeeping)
# `python3 ../../mythic-gm/scripts/tick.py <this-bridge-dir> <scene#>` reports which are DUE; then
# roll each named table / advance each clock HONESTLY and record the result to campaign-state.md.
# cadence: 'every scene' | 'every N scenes' | 'on trigger: …'  (the engine reads these literally)

| subsystem | cadence | advance by |
|-----------|---------|-----------|
| Aura & Realm watch | every scene | Note the current place's Realm and aura (Magic/Faerie/Divine/Infernal/none); apply its modifier to casting totals and botch dice (Realm Interaction Table). A change of place re-checks for a regio. |
| Warping & Twilight | every scene | If a magus stood in aura 6+, cast a 6th-magnitude+ or constant effect, or BOTCHED a supernatural roll this scene, accrue Warping Points (1 per `10` rolled on the botch dice); at a new Warping-Score threshold roll for Wizard's Twilight. |
| Covenant season clock | every 3 scenes | Advance one season of game-time (Spring→Summer→Autumn→Winter). Resolve each magus's chosen seasonal Lab/study/writing activity offscreen (rule-mode Fate Question or Lab Total); at Winter's end tick the year. |
| Aging | on trigger: each in-game year (Winter) for any character aged 35+ | Roll an Aging Total per such character (`dice.py roll 1d10` no-botch + age/10 − living conditions − longevity ritual); apply Aging Points / Decrepitude / Crisis. |
| Vis economy | on trigger: when a vis source's season comes due, or vis is spent | Add the source's pawns (by Art) to covenant stores; deduct vis used on Ritual magic, enchantment, or boosting. Track scarcity. |
| Order & Tribunal politics | every 5 scenes | A Hermetic faction (rival covenant, Quaesitor, Redcap network, a House) makes an offscreen move toward or away from an open Thread — roll `generators/story_hook.json` or a Fate Question for what they do. |
| Mundane authority pressure | every 4 scenes | If a Thread involves a lord, bishop, abbot, or town, that authority advances its agenda (taxes, scrutiny, encroachment, a heresy rumor) — Fate Question for the move. |
| Offscreen clocks | every scene | Advance any other faction/threat clocks recorded in campaign-state.md (the engine default world-tick). |
