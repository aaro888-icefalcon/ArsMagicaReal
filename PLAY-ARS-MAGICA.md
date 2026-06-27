# Play Ars Magica solo — quickstart

This repository is set up to run a **solo / GM-less game of Ars Magica 5th Edition** in Mythic
Europe (year 1220), using the **mythic-gm** engine plus an **Ars Magica companion bridge**. The
engine drives every die and honours the oracle without softening; the companion supplies the
Hermetic rules and the world.

## What's installed

```
.claude/skills/
├── mythic-gm/        # the ENGINE (Mythic GME 2e + The Adventure Crafter) — drives dice, scenes, Chaos, oracle
│   └── scripts/ data/ references/ assets/ SKILL.md …
└── ars-magica/       # the COMPANION (this game)
    ├── SKILL.md
    └── bridge/       # fills the engine's hooks with Ars Magica 5e + Mythic Europe
        ├── bridge.md             system-profile.md     interpretation.md
        ├── chaos-tendency.md     theme-weights.md      subsystems.md      seeds.md
        ├── setting-canon.md      character-sheet-template.md
        ├── scripts/{arm.py, themes.py, resolve.py, advanced.py, elements.py, armdice.py, armcore.py}
        ├── data/rules/{arts,ease_factors,wounds,fatigue,casting,realm_interaction,npc_statistics,aging,warping,certamen}.json
        ├── data/elements/{houses,tribunals,realms,code_clauses,npc_archetypes,hooks,
        │                  factions,locations,creatures,virtues_flaws}.json  (134 atoms, 11 types)
        ├── generators/{registry.md, houses.json, tribunals.json, hermetic_npc.json,
        │               realm_encounter.json, story_hook.json}
        └── adventures/broken-covenant-of-calebais.md
campaigns/            # your live saga state (created when you play)
reviewed/ wip/ raw-md/ 3rd-party/   # the full open-licensed Ars Magica corpus (deep reference)
```

## Just play

Say to Claude in this repo: **"Be my GM for a solo game of Ars Magica."** The mythic-gm skill
activates, loads the Ars Magica bridge, runs Session Zero (build your covenant and first magus),
and starts the play loop. You roll real dice through the scripts; the world acts to win.

## Or start it by hand

```bash
# 1. Confirm the engine + bridge are healthy
python3 .claude/skills/mythic-gm/scripts/build_data.py                       # VERIFICATION PASSED ✓
python3 .claude/skills/mythic-gm/scripts/bridge.py validate .claude/skills/ars-magica/bridge
python3 .claude/skills/mythic-gm/scripts/bridge.py summary  .claude/skills/ars-magica/bridge

# 2. Scaffold a saga
python3 .claude/skills/mythic-gm/scripts/state.py init campaigns/my-covenant

# 3. Roll the saga's first (constrained, yearly) Theme order
python3 .claude/skills/ars-magica/bridge/scripts/arm.py themes new-year --campaign campaigns/my-covenant --year 1220

# 4. Take the first Turn — honest Ars Magica resolution via arm.py
python3 .claude/skills/mythic-gm/scripts/dice.py scene 5            # Scene Test (Chaos Factor 5)
python3 .claude/skills/ars-magica/bridge/scripts/arm.py element surface --campaign campaigns/my-covenant --here "covenant,order"
python3 .claude/skills/ars-magica/bridge/scripts/arm.py cast --te 10 --fo 8 --sta 2 --aura 3 --level 15   # e.g. a magus casts
python3 .claude/skills/mythic-gm/scripts/tick.py .claude/skills/ars-magica/bridge 1   # world-tick at bookkeeping
```

## The two questions this setup answers (from `mythic-gm/CONFIGURE.md`)
- **Sourcebooks?** Yes — the full Ars Magica 5e corpus is in this repo; the bridge's
  `system-profile.md` and `setting-canon.md` are faithful to it.
- **Published adventure?** Optional — emergent covenant sandbox by default, or load the bundled
  *Broken Covenant of Calebais*. → This is the **Q1 (with sourcebooks, emergent)** setup, on the
  reusable **bridge** track.

## How it plays (the discipline never relaxes)
Honest dice, always scripted and shown; the GM rolls before narrating and locks the result first;
a *No* from the oracle is a real No; magi are powerful but the Code and the Gift's social friction
make magic an unreliable shortcut; supernatural beings are forces with natures, not monsters to
kill; vis, books, reputation, and standing in the Order are the real currencies; grogs die so magi
needn't. Stakes scale to the mythic-political genre; the honesty never does.
