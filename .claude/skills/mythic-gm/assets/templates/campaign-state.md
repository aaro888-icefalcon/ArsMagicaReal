# Campaign State — <campaign name>

> The single source of truth. Overwrite this at the end of **every** scene.
> If a change happened in the fiction but isn't written here, it didn't happen.

## Frame
- **Adventure Source mode:** Pure Mythic | Adventure Crafter | Prepared Adventure
- **RPG / System Profile:** <name or "rules-light (Fate Questions only)"> → `system-profile.md`
- **Setting / canon:** <name> → `setting-canon.md`
- **Genre & stakes vocabulary:** <e.g. grimdark-survival — death/maiming/capture>
- **Resolution:** Fate Chart | Fate Check   ·   **Chaos flavor:** normal | mid | low | no
- **Discipline:** HARDCORE (no softening; Peril Points OFF unless player opts in)

## CURRENT ADVENTURE: <title>
_Each adventure has its **own** Threads & Characters Lists and Theme priority. The Lists + Theme order +
tens-counter are the machine source of truth in **`threads.json` / `characters.json` / `adventure.json`**
(the dice roll those, any length); the sections below are a human-readable **snapshot** — keep them
roughly in sync but edit the JSON via `state.py`._
_A **new adventure** begins when the current one's main Thread(s) Conclude (`threads.json` empties) or the
player declares one — then roll new Themes (`adventure_crafter.py themes --campaign <dir>`), clear the
Threads List, carry over only still-relevant Characters, archive the rest._

- **Adventure status:** active | concluding | concluded
- **Theme priority (this adventure):** in `adventure.json` → `state.py adventure show <campaign>`  _(rolled per RPG style)_

## Chaos Factor: 5
_(1–9; −1 if the PC was mostly in control of the last scene, +1 if it was chaotic)_

## Threads List — snapshot of `threads.json` (the dice roll the JSON, not this)
_Manage with `state.py thread add|weight|remove|show <campaign> "<name>"`. **Weight (max 3)** = re-adding
when Invoked/featured → that Thread is weight× as likely. Base list = 25 weighted slots; a longer list
still fully rolls over (two-stage roll: NEW / PRE-EXISTING / CHOOSE MOST LOGICAL). Remove all of a
concluded Thread. Curate — prune the irrelevant._
1.
2.

## Characters List (NPCs/forces; PC is NOT listed) — snapshot of `characters.json`
_Same: `state.py char add|weight|remove|show <campaign> "<name>"`; weight = re-add (max 3); the dice roll
the JSON. Add/weight when an NPC is introduced or featured; remove when it permanently exits._
1.
2.

## Tens-cycle counter (Theme-die 10s rolled so far): in `adventure.json` _(auto-updated by turning-point)_

## Adventure Features List (prepared-adventure mode only)
1.

## Campaign roster (persists across adventures: recurring NPCs, long arcs)
-

## PC(s)
- See `character-sheet.md`. Conditions/injuries: none. Resources: —.

## Overlays
- **Keyed Scenes:** _(Trigger → Event; Count)_ none
- **Thread Progress Track:** _(Focus Thread, Track 10/15/20, points, flashpoint flag)_ none
- **Peril Points:** OFF _(or: N remaining, player-invoked only)_

## Clocks (offscreen factions/threats)
- none

## Adventure Crafter state (crafter mode)
- Active Turning Point: —   ·   Theme priority: Action, Tension, Mystery, Social, Personal

## Scene
- **Last scene recap (2–3 sentences):** <the campaign opens here>
- **Self-audit drift counter (consecutive soft scenes):** 0

## Archive pointer
- Resolved threads / dead characters → `archive.md`
