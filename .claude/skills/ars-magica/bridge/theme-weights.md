# Theme Spec — Mythic Europe (Ars Magica 5e)   (hook: themes)
# The theme PRIORITY ORDER is regenerated EVERY in-game year (it changes annually), drawn by the
# base weights below and bound by hard constraints. The logic lives in scripts/themes.py and is
# called via:  python3 scripts/arm.py themes new-year --campaign <dir>
# It writes `theme_order` to the campaign's adventure.json (which the engine's adventure_crafter.py
# reads) and resets the per-year coverage tally in year-state.json.

## Base draw weights (the saga's lean; higher = likelier to land high-priority)
Mystery: 5      # hidden vis, lost texts/Mysteries, regiones, the uncanny, "find out about it"
Social:  5      # Tribunal/Order politics, mundane courts, faerie bargains, troupe ties
Personal: 4     # soap-opera arcs, quests tied to a character, apprentices, Twilight/Warping
Tension: 3      # high stakes (Code, vis, reputation, survival), but failure rarely kills a magus
Action:  2      # lethal combat is infrequent and usually fought by grogs

## Hard constraints on each year's order (enforced by themes.py; rejection-sampled, shown)
- C1  Action is one of the top THREE priorities        (position ≤ 3)
- C2  Social is one of the top FOUR priorities          (position ≤ 4)
- C3  Personal OR Social is one of the top TWO          (position ≤ 2)
- C4  every theme is present (a full permutation) AND must be USED at least once per year —
      `themes new-year` HARD-BLOCKS the year roll-over until each theme has driven ≥1 beat
      (log them with `themes record --used <theme,…>`; `themes status` shows the gaps).

## Cadence
- Session Zero: `arm.py themes new-year --campaign <dir> --year 1220`  (first order + coverage tally).
- Each scene/Turning Point: after the engine generates plot points, `arm.py themes record --used …`.
- World-tick Covenant-season clock rolls Winter→Spring → `arm.py themes new-year` (coverage-gated).
# (This replaces the engine's per-adventure `adventure_crafter.py themes --style …` for this companion;
#  the engine still rolls the theme die from the order arm.py wrote.)
