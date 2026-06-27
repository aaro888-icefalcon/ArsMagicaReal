---
name: ars-magica
description: >-
  Companion content pack that lets the mythic-gm engine run a solo / GM-less game of
  Ars Magica 5th Edition (Definitive Edition) in Mythic Europe, year 1220. Supplies the
  Hermetic ruleset (the d10 stress/simple die, Characteristic+Ability vs Ease Factor, the
  Arts and spellcasting, Certámen, combat, wounds, aging, warping/Twilight), the Order of
  Hermes and four-Realms setting and GM lens, covenant-saga theme weights, world-tick
  subsystems (covenant seasons, vis, aging, Order & mundane politics), faithful generators,
  and the classic adventure The Broken Covenant of Calebais. Use this whenever the user wants
  to PLAY Ars Magica, "be my GM for Ars Magica", run a covenant / magus / Hermetic solo game,
  or play a wizard in 13th-century Mythic Europe. Pairs with the mythic-gm engine, which owns
  the dice, the oracle, scenes, Chaos, and the no-softening discipline.
---

# Ars Magica 5e — a companion bridge for mythic-gm

This skill is a **content pack**, not a game engine. The **`mythic-gm`** skill (in
`../mythic-gm/`) is the engine: it runs the scene / Chaos / Fate-Question / Random-Event /
Turning-Point loop, drives **all** dice through its scripts, and holds the no-softening
discipline. This skill fills the engine's hooks with **Ars Magica 5th Edition** rules and
**Mythic Europe** lore so the engine plays a faithful Hermetic covenant saga.

**Companion bridge for mythic-gm: `./bridge/`.**

## How to run a game

1. **The engine drives.** When the player asks to play Ars Magica / "be my GM", the
   `mythic-gm` engine activates and loads this bridge. From the repo root:
   ```
   python3 .claude/skills/mythic-gm/scripts/bridge.py summary  .claude/skills/ars-magica/bridge
   python3 .claude/skills/mythic-gm/scripts/bridge.py validate .claude/skills/ars-magica/bridge
   ```
   Use an override where the bridge provides one, else the engine default.
2. **Session Zero** (no `campaign-state.md` yet): follow the engine's SESSION ZERO with this
   bridge loaded. This is a **Q1 setup** in `mythic-gm/CONFIGURE.md` — *faithful system,
   emergent campaign* (sourcebooks yes, published adventure optional). Scaffold a campaign:
   ```
   python3 .claude/skills/mythic-gm/scripts/state.py init campaigns/<your-saga>
   ```
   Then build the troupe's first **magus** (and a companion/grog) with `bridge/system-profile.md`
   §character notes → `campaigns/<your-saga>/character-sheet.md` (template in
   `bridge/character-sheet-template.md`), seed 1–2 Threads from the covenant's situation, frame
   the First Scene (not tested), and stop on "What do you do?".
3. **Optional published adventure:** to run the bundled classic, load
   `bridge/adventures/broken-covenant-of-calebais.md` (pure-sandbox clusters + fragments;
   Diminisher ⅓ for a small solo party) and seed its Threads/Characters/Features.
4. **Play the Turn** exactly as the engine's play loop specifies: Scene Test (Adventure Crafter
   on) → resolve actions via `bridge/system-profile.md` (`dice.py roll`, `system.py route`) or a
   Fate Question for world questions → bookkeep, adjust Chaos honestly, and run the world-tick
   (`tick.py .claude/skills/ars-magica/bridge <scene#>`).

## What this bridge provides (the hooks it fills)
- **resolve** → `bridge/system-profile.md` (the full Hermetic resolution: dice, Arts, Certámen, combat, wounds, NPC stats).
- **meaning** → `bridge/interpretation.md` (Order-of-Hermes & four-Realms GM lens; how magi, the Church, nobles, faeries, demons, and the Divine think and act).
- **chaos** → `bridge/chaos-tendency.md` · **themes** → `bridge/theme-weights.md` (Mystery/Social-forward).
- **generate:character / generate:element** → `bridge/generators/` (Hermetic NPC archetype auto-fires; houses, tribunals, realm encounters, story hooks rolled on demand).
- **world-tick** → `bridge/subsystems.md` · **seeds** → `bridge/seeds.md` · **canon** → `bridge/setting-canon.md`.
- **adventure-ingest** → `bridge/adventures/broken-covenant-of-calebais.md`.

## The corpus (deep reference, on demand)
The repository is **the complete open-licensed Ars Magica corpus** in Markdown. When a rule,
spell, creature, virtue/flaw, or Tribunal needs more depth than `setting-canon.md` carries,
read from `reviewed/` (best quality — start with *Ars Magica - Definitive Edition (Core Rules).md*),
then `wip/`, then `raw-md/` / `3rd-party/`. Precedence: **system-profile > the corpus > training knowledge.**

> All randomness lives in the engine's scripts; this skill never rolls its own dice and never
> softens an honest result. It supplies the *world*; the engine supplies the *game*.
