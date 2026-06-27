# CONFIGURE — point the engine at a new RPG system

mythic-gm is **system-agnostic**: a content-free engine (Mythic GME 2e + The
Adventure Crafter, all tables hard-coded) that plays a full game on its own and
layers **any** ruleset, setting, or published adventure on top. Nothing in the
engine is specific to a game; you configure a system by filling a few of the
engine's **hooks** and letting the rest fall to the default. **A partial config
always plays** — every hook you leave alone uses the Mythic/AC default, so the
engine never stops working while you build out.

This file is the entry point for *"let's set up / play `<some RPG>`."* It routes
you through two axes — **do you have sourcebooks?** and **is there a published
adventure?** — to one of four setups. Deep, step-by-step walkthroughs for each
quadrant live in **`references/adapting/configure-matrix.md`**.

---

## The two questions that decide everything

- **Sourcebooks** = do you have *text to be faithful to* — an uploaded core
  rulebook, a setting bible, or a well-defined published system Claude knows in
  detail? **Without** sourcebooks means homebrew, rules-light, "just make it
  fun," or a system known only vaguely.
- **Published adventure** = a specific module/campaign to run, vs. emergent
  sandbox play the engine generates as you go.

Rules and setting are separable: you may have the **rules** book but no
**setting** book (or the reverse). Build a profile from whatever rules you have;
generate the setting if you lack one. See *Mixed cases* below.

## Decision tree (answer at Session Zero)

```
1. A ruleset to be faithful to?
     yes → build a System Profile        (references/adapting/adapt-ruleset.md)
     no  → rules-light: Fate Questions    (optionally a few-line micro-profile)
2. A setting bible / sourcebook?
     yes → setting-canon from it          (references/adapting/adapt-lore.md)
     no  → generate it collaboratively, record answers back to canon
3. A published adventure?
     yes → ingest it (see the matrix)     (keyed-scenes, or bridge/adventures/)
     no  → Pure Mythic / Adventure Crafter sandbox
4. One-off, or a system you'll replay?
     one-off  → campaign-folder quick path
     replay   → a reusable bridge/ (a companion skill)
```

Anything you don't define falls back to the engine default. Start minimal; add
hooks as the campaign reveals what it needs.

## The 2×2

| | **No published adventure** (emergent) | **With a published adventure** (run the module) |
|---|---|---|
| **With sourcebooks** | **Q1 — faithful system, emergent campaign.** Build System Profile + generators + setting-canon. Sandbox via Pure Mythic / Adventure Crafter. | **Q2 — faithful system, run the module.** Q1 **plus** ingest the module (keyed-scenes *or* `bridge/adventures/`); pick a Diminisher. |
| **Without sourcebooks** | **Q3 — rules-light emergent.** The engine's native standalone mode: concept + genre, resolve by Fate Questions; generate the setting in play. | **Q4 — known module, no rules text.** Ingest the module's content; resolve mechanics by rule-mode Fate Questions; estimate a Diminisher. |

---

## Per-quadrant playbook

### Q1 — With sourcebooks, no adventure
1. **Rules → System Profile.** `references/adapting/adapt-ruleset.md` → fill `system-profile.md` (dice convention, core resolution, degrees of success?, stats/skills, combat & death, NPC-stat units, routing default).
2. **Setting → canon.** `adapt-lore.md` → `setting-canon.md` (places, factions+wants, timeline, named NPCs, hard content lines).
3. **Tone & themes.** Pick a `references/genres/` pack; fix theme weights (`theme-weights.md`, bridge track) or just roll them: `python3 scripts/adventure_crafter.py themes --style <action|horror|mystery|intrigue|drama|balanced> --campaign <dir>`.
4. **Tables & clocks (optional).** Convert the book's random tables to generators (`*.json`); list any sanity/war/economy clocks as subsystems.
5. **Play.** Scene Test in crafter mode (`dice.py scene <cf>`), resolve actions via the profile (`dice.py roll …`, `system.py route`), bookkeep + `tick.py`.

### Q2 — With sourcebooks, with an adventure
Do Q1, then **ingest the module** (`references/adapting/adapt-adventure.md` or, for a reusable pack, `references/ingest-adventure.md`):
- **Goals → Threads, NPCs/locations → Characters, set-pieces/hazards → Adventure Features** (`state.py thread|char add <dir> "<name>"`).
- **Scale for solo:** pick a **Diminisher** (½, ⅓, ¼, ⅕) from PC-power vs. the party the module assumes; apply it to stats as you meet them.
- **Run it honestly:** the module is a **map, not a script**. The dice still decide; if an honest result kills an "essential" NPC or skips the intended path, **adapt**. Apply Player ≠ PC knowledge — don't act on module facts the PC hasn't discovered.
- **Scene handling** depends on track (below): keyed-scenes (Prepared mode, no Altered/Interrupt; within-CF adds a Random Event) *or* clusters that surface by relevance (pure sandbox).

### Q3 — No sourcebooks, no adventure  (the engine's native mode)
1. **No System Profile needed** — resolve every uncertain action with a Fate Question (`dice.py fate <odds> <cf>`). Optionally co-design a **micro-profile**: a couple of lines (dice convention + what the "rules" cover) so recurring resolutions stay consistent.
2. **Generate the setting** collaboratively: a `references/genres/` pack sets tone; Meaning Tables (`oracle.py pair …`) and a few Fate Questions seed places/factions — **record answers to `setting-canon.md`** so it stays consistent.
3. **Character** = concept + a few descriptive traits + whatever the genre needs.
4. **Play** Pure Mythic or Adventure Crafter. This is literally *"be my GM for a `<genre>` game"* with nothing else loaded.

### Q4 — No sourcebooks, with an adventure
1. **Ingest the module from whatever you have** (its text, or your memory of it): goals → Threads, NPCs/locations → Characters, set-pieces → Features/clusters.
2. **Resolve mechanics by rule-mode Fate Questions** (`dice.py fate <odds> <cf> --mode rule`); add a micro-profile if a system is loosely implied. Stat foes on the fly via the **NPC Statistics Table** (decide the expected value → Fate Question → `oracle.py answer npc_statistics …`: Yes = as expected, ExcYes +25%, No −25%, ExcNo −50%).
3. **Estimate a Diminisher** for solo scaling.
4. **Anti-railroad is strongest here:** with no stat baseline, lean on honest Fate Questions and **log the caveat** in `session-log` — where the adventure assumes system-specific mechanics, you're approximating.

---

## Two tracks: where the config lives

| | **Campaign-folder quick path** | **Reusable bridge** |
|---|---|---|
| Use when | a single campaign / one-off / trying a system out | an RPG you'll replay across campaigns (a real companion) |
| Files | next to `campaign-state.md`: `system-profile.md` · `character-sheet.md` · `setting-canon.md` · `keyed-scenes.md` | a `bridge/` declared in a companion `SKILL.md` (copy `assets/bridge-templates/*`) |
| Adventure | `keyed-scenes.md` (Trigger→Event) + seeded Lists; **Prepared Adventure** mode | `bridge/adventures/*.md` clusters + fragments (pure sandbox) |
| Build from | `references/adapting/` + `assets/templates/` | `assets/bridge-templates/` + **`COMPANION-SKILLS.md`** |
| Validate | `state.py validate <statefile>` | `bridge.py validate <bridge_dir>` (roll-tests generators) |

A bridge is the richer contract (9 hooks, fixed theme weights, an interpretation
lens, world-tick subsystems, reusable generators). The campaign-folder path is a
thin subset for when you don't need reuse. You can start in a campaign folder and
promote it to a bridge later. To migrate a *whole repo* of an old engine + RPG
skill, see **`CONVERSION.md`**; to bump an existing engine, **`UPGRADE.md`**.

## Mixed & partial cases
- **Rules but no setting** → build `system-profile.md` from the book; *generate* the setting (Q3 step 2) and write it to `setting-canon.md`.
- **Setting but no rules** → write `setting-canon.md` from the bible; resolve actions rules-light (Q3 step 1).
- **System known only from training** → treat it as "with sourcebooks" but verify ambiguous mechanics with the player; when you can't recall a rule, use a rule-mode Fate Question and, if it recurs, write it into the profile (System Profile > training knowledge).
- **Nothing filled** → the engine plays pure rules-light Mythic. Always valid.

## What never changes (the discipline survives every config)
No configuration may weaken these:
- **Honest dice, always scripted and shown.** Every uncertain outcome goes through `scripts/*.py`.
- **Roll before you narrate** — lock the result in a bracketed `[Adjudication: …]` block first.
- **Honor the oracle** — a No is a real No; a bad Random Event is not rescued.
- **NPCs/world act to win;** never soften an honest result; consequence scales to genre, honesty never relaxes.
- **Peril Points / "the PC can't die" are OFF** by default.
- **A published module is a map, not a script;** **Player ≠ PC knowledge.**

## Cross-reference map
| You need… | Read |
|---|---|
| The full bridge contract (9 hooks, file specs) | `COMPANION-SKILLS.md` |
| Per-quadrant deep walkthroughs (this file's detail) | `references/adapting/configure-matrix.md` |
| Adapt a ruleset / char-gen / lore / adventure | `references/adapting/{adapt-ruleset,adapt-character-creation,adapt-lore,adapt-adventure}.md` |
| The fixed shapes the loop reads | `references/adapting/compatibility-spec.md` |
| Ingest a module as clusters + fragments | `references/ingest-adventure.md` |
| Genre tone + stakes vocabulary | `references/genres/` |
| Migrate a whole repo / version-bump the engine | `CONVERSION.md` · `UPGRADE.md` |

## Validate before you play
```
python3 scripts/build_data.py                       # engine tables: VERIFICATION PASSED ✓
python3 scripts/bridge.py validate <bridge_dir>     # bridge track: files + generator coverage
python3 scripts/bridge.py summary  <bridge_dir>     # which hooks override vs default
python3 scripts/state.py init <campaign_dir>        # scaffold a campaign (state + JSON Lists)
```
Then run one Turn: `dice.py scene 5` → resolve via the profile → `tick.py <bridge_dir> <scene#>` at bookkeeping. If it plays, the config is good enough; deepen it as you go.
