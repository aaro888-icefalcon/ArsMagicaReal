# campaigns/ — live play state

Each Ars Magica saga you play lives in its own folder here, created by the mythic-gm engine:

```
python3 .claude/skills/mythic-gm/scripts/state.py init campaigns/<your-saga>
```

That scaffolds the saga's source of truth:

- `campaign-state.md` — the single source of truth, overwritten at the end of every scene
  (Frame, Chaos Factor, snapshot of the Lists, overlays, clocks, last-scene recap).
- `threads.json` / `characters.json` — the Threads & Characters Lists the dice actually roll
  (manage with `state.py thread|char add|weight|remove|show`).
- `adventure.json` — the current adventure's Theme priority + tens-counter.
- `character-sheet.md` — your magus / companion / grog (copy
  `.claude/skills/ars-magica/bridge/character-sheet-template.md`).
- `setting-canon.md` (optional, per-saga) — facts decided in play, layered over the bridge's
  Mythic Europe canon.

The **engine** (`.claude/skills/mythic-gm/`) and the **Ars Magica companion**
(`.claude/skills/ars-magica/`) are shared and never edited per-saga; only the files in here
change as you play. This folder starts empty (a saga is created when you sit down to play) —
see `../PLAY-ARS-MAGICA.md` for the quickstart.
