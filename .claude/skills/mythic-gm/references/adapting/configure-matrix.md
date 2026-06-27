# Configure matrix — the four setups, step by step

The deep-dive behind `CONFIGURE.md`. Two axes give four quadrants:

- **Sourcebooks** — text to be faithful to (core rulebook / setting bible / a
  system Claude knows in detail) vs. none (homebrew, rules-light, vague memory).
- **Published adventure** — a module/campaign to run vs. emergent sandbox.

Each quadrant below shows the work, the **exact commands**, which hooks to fill
vs. leave default, and a tiny worked example. Throughout, two **tracks** are
available — the **campaign-folder quick path** (files next to `campaign-state.md`)
and the **reusable bridge** (`bridge/`, the companion contract in
`COMPANION-SKILLS.md`). Pick the track once; the quadrant work is the same shape
in either.

> **A partial config always plays.** Fill the high-value hooks first
> (`resolve`/System Profile, `meaning`/interpretation, setting-canon); leave the
> rest at the engine default and add them when the campaign asks for them.

---

## Setup, common to all quadrants

```
python3 scripts/state.py init <campaign_dir>     # campaign-state.md + threads.json/characters.json/adventure.json
```
Pick a genre pack from `references/genres/` (it defines what "maximal honest
consequence" means here). Confirm with the player that play is honest and
hardcore. Then do the quadrant-specific work, create the PC
(`references/adapting/adapt-character-creation.md` → `character-sheet.md`), seed
1–2 Threads from the backstory, frame the **First Scene** (not tested), and stop
on *"What do you do?"*

---

## Q1 — With sourcebooks, no adventure
*"A faithful system; the campaign is emergent."*

**Fill these hooks:** `resolve` (System Profile), `meaning` (interpretation /
genre lens), `themes`, and any `generate:*` you have tables for. Leave
`adventure-ingest` at default (there's no module).

1. **Rules → System Profile.** `references/adapting/adapt-ruleset.md` →
   `system-profile.md` (campaign track) or `bridge/system-profile.md` (bridge
   track). Capture: dice convention + how to express a roll for `dice.py roll`;
   core resolution (vs-DC / opposed / PbtA 6-,7-9,10+ / pool); **degrees of
   success?** (drives Exceptional mapping in rule-mode); stats/skills; combat &
   death; **NPC-stat units**; routing default (what the RPG resolves vs. Fate
   Questions). Confirm ambiguous mechanics with the player; leave gaps to Fate
   Questions. Precedence: **profile > uploaded text > training knowledge.**
2. **Setting → canon.** `adapt-lore.md` → `setting-canon.md`: places, factions
   (who wants what), timeline, named NPCs (with wants), tone, hard content lines.
   Canon overrides recollection.
3. **Themes & tone.** Bridge track: fix `theme-weights.md` for the setting.
   Either track: roll the adventure's five Theme priorities —
   `python3 scripts/adventure_crafter.py themes --style <action|horror|mystery|intrigue|drama|balanced> --campaign <campaign_dir>` (saved to `adventure.json`).
4. **Tables → generators (optional).** Convert the book's random tables to the
   engine schema `{id,title,type:"list_d100"|"list_d10","dice","entries":[{min,max,value}]}`
   (model on `assets/bridge-templates/generators/EXAMPLE_npc_role.json`). Roll one
   with `python3 scripts/dice.py table <abs path to the json>`. In a bridge,
   register each in `generators/registry.md` and wire `generators_map.character`
   in `bridge.md` if it's a character generator.
5. **Clocks → subsystems (optional, bridge track).** One row each in
   `subsystems.md`: `name · cadence · advance-by`. Fired at bookkeeping by
   `python3 scripts/tick.py <bridge_dir> <scene#>`.
6. **Play the Turn.** `dice.py scene <cf>` (Adventure Crafter always on:
   Altered/Interrupt → Turning Points) → resolve actions through the profile
   (`python3 scripts/system.py route` prints the seam) → bookkeep, adjust Chaos
   honestly (`state.py chaos <+1|-1> <cf>`), `tick.py`.

*Worked example (D&D-like, campaign track):* profile = "d20+mod vs DC; degrees:
no; combat: initiative d20, attack vs AC, hp damage, death at 0 + death saves;
NPC units AC/HP/damage dice; route all combat/skills to the RPG, world questions
to Fate Questions." Setting from the gazetteer → canon. `themes --style action`.
Play emergent; the Adventure Crafter generates the plot.

---

## Q2 — With sourcebooks, with an adventure
*"A faithful system; run the published module."*

Everything in **Q1**, plus ingest the module. This adds the `adventure-ingest`
hook. Choose the track by how you want the module to behave:

**Campaign-folder track (keyed scenes, Prepared mode)** —
`references/adapting/adapt-adventure.md`:
1. Read the **intro only**. Goals → **Threads**, NPCs/locations → **Characters**,
   set-pieces/wandering tables/hazards → **Adventure Features**
   (`state.py thread|char add <campaign_dir> "<name>"`). Read the rest one detail
   at a time, as the PC reaches it.
2. **Keyed scenes.** For anything the module says *must* happen, write a
   `keyed-scenes.md` entry: a **Trigger** (often a per-scene die —
   `python3 scripts/dice.py keyed 1d10 <target>` — or a count/condition) → the
   **Event**. Check triggers in bookkeeping.
3. **Scale.** Pick a **Diminisher** (½, ⅓, ¼, ⅕) from PC-power vs. the assumed
   party; apply to challenge stats as you meet them.
4. **Scene handling = Prepared mode:** `python3 scripts/dice.py scene <cf> --mode prepared`
   — **no Altered/Interrupt;** within-CF **adds a Random Event to the Expected
   Scene** (the Prepared Event Focus can point at an Adventure Feature). The
   module keeps priority; Mythic is co-GM.

**Reusable-bridge track (clusters + fragments, pure sandbox)** —
`references/ingest-adventure.md` + `assets/bridge-templates/adventures/CLUSTER-SCHEMA.md`:
1. Chop the module into **clusters** (authored scenes/nodes), each a scene-level
   description + member **fragments** (atomic plot points), all tagged
   (themes/threads/characters/elements/location) and cited. Write
   `bridge/adventures/<module>.md`.
2. Seed the Lists from all clusters (as above). Note the Diminisher; convert any
   module tables to `generators/`.
3. **Runs as pure sandbox:** no forced order, no climax, no Plot Armor; content
   bias *medium* (prefer a relevant authored fragment, else roll a random Plot
   Point); weighted-random with an un-used-fragment lean + usage ledger. An
   Expected Scene can draw a whole cluster (then Scene-Tested normally).

**Both tracks — anti-railroad (binding):** the dice still decide. If an honest
result kills the module's "essential" NPC or skips its path, **adapt** — the
module is a map, not a script. Apply **Player ≠ PC knowledge**: never act on
module facts the PC hasn't discovered.

*Worked example (CoC-like + a scenario, bridge track):* Q1 profile (% roll-under,
Sanity as a subsystem clock). Ingest the scenario into `bridge/adventures/`;
Diminisher ⅓ for a lone investigator; clusters surface by relevance; Sanity ticks
fired by `tick.py`. Validate: `python3 scripts/bridge.py validate <bridge_dir>`.

---

## Q3 — No sourcebooks, no adventure
*"Rules-light, emergent — the engine's native standalone mode."*

**Fill almost nothing.** Leave `resolve` at default (Fate Questions). This is
*"be my GM for a `<genre>` game"* with nothing else loaded.

1. **Resolution = Fate Questions.** `python3 scripts/dice.py fate <odds> <cf> --campaign <campaign_dir>`
   for every uncertain action. (Optionally co-design a **micro-profile**: a couple
   of lines — a dice convention and what the "rules" cover — so recurring calls
   stay consistent. Write it to `system-profile.md`.)
2. **Generate the setting in play.** The genre pack sets tone; seed places,
   factions, and people with Meaning pairs (`python3 scripts/oracle.py pair actions`
   / `descriptors`) and a few Fate Questions — then **record each answer to
   `setting-canon.md`** so the world stays consistent (canon is the antidote to
   drift).
3. **Character** = concept + a few descriptive traits + whatever the genre needs.
   Roll any creation dice honestly (`dice.py roll …`).
4. **Play** Pure Mythic or Adventure Crafter. Roll Themes
   (`adventure_crafter.py themes --campaign <campaign_dir>`); the Crafter
   generates the plot via Turning Points.

*Worked example:* "grimdark survival, no system." No profile. Each risky action
is a Fate Question; the Adventure Crafter supplies Turning Points; new NPCs come
from the AC Character Crafter (`oracle.py character`). Setting accretes into
`setting-canon.md` as the dice answer questions.

---

## Q4 — No sourcebooks, with an adventure
*"A known module, but no rules text."*

You have the module (its text, or your memory of it) but no full ruleset. Fill
`adventure-ingest` from what you have; leave `resolve` rules-light.

1. **Ingest from whatever you have.** Same shapes as Q2 — goals → Threads,
   NPCs/locations → Characters, set-pieces → Features/clusters
   (`state.py thread|char add …`). Use the campaign-folder `keyed-scenes.md` for
   "must happen" beats, or a light `bridge/adventures/` ingest.
2. **Resolve mechanics by rule-mode Fate Questions.**
   `python3 scripts/dice.py fate <odds> <cf> --mode rule` (CF treated as 5, no
   Exceptional, ignore events). Add a micro-profile if the module loosely implies
   a system.
3. **Stat foes on the fly** with the **NPC Statistics Table**: decide the
   expected value → Fate Question → `python3 scripts/oracle.py answer npc_statistics <yes|no|exc_yes|exc_no>`
   (Yes = as expected; ExcYes +25%; No −25%; ExcNo −50%). Estimate a Diminisher
   for solo scaling.
4. **Anti-railroad is strongest here.** With no stat baseline, lean on honest
   Fate Questions and **log the caveat** in the session log: where the module
   assumes system-specific mechanics, you're approximating. The module is still a
   map, not a script.

*Worked example:* a beloved boxed adventure you remember but don't own, no rules.
Threads/Characters seeded from memory; every check is a rule-mode Fate Question;
foes statted via the NPC Statistics Table; the dice — not your memory of "how it's
supposed to go" — decide each scene.

---

## Mixed cases (one axis half-met)
- **Rules but no setting** → build `system-profile.md` from the book; *generate*
  the setting (Q3 step 2) into `setting-canon.md`.
- **Setting but no rules** → write `setting-canon.md` from the bible; resolve
  rules-light (Q3 step 1).
- **System known only from training** → treat as "with sourcebooks," but verify
  ambiguous mechanics with the player and fall to rule-mode Fate Questions when
  you can't recall a rule; write recurring rulings into the profile.

## What stays the engine's — never weaken it
Whatever you configure, the engine owns the machinery and the discipline:
scenes, the Scene Test, Chaos math, Fate Questions, Random Events, Turning
Points, the seed/List machinery — and the **no-softening creed**. Honest dice,
rolled through the scripts and shown; roll before you narrate; honor the oracle;
NPCs act to win; never soften an honest result; Peril Points off; a module is a
map not a script; Player ≠ PC knowledge. Configuration supplies the *world*; it
never relaxes the *honesty*.
