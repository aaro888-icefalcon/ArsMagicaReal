# Generator Index — Mythic Europe (Ars Magica 5e)   (hooks: generate:*)
# Human index of the bridge's generators. The engine reads the machine-readable `generators_map`
# in bridge.md; only `character` auto-fires today. Roll any table on demand with:
#   python3 ../../mythic-gm/scripts/dice.py table <abs path to the json>
# need | when it's called | table(s) | mode (replace | conjunction | default)

| need | when called | table(s) | mode |
|------|-------------|----------|------|
| new NPC (any) | any NEW CHARACTER result (character-list NEW, Event Focus = New NPC, AC Plot Point) | AC Character Crafter **+** generators/hermetic_npc.json | conjunction |
| supernatural / mundane encounter | a scene needs a creature, threat, or uncanny presence | generators/realm_encounter.json | replace |
| story complication | opening a scene/adventure, seeding a Thread, an offscreen faction move | generators/story_hook.json | replace |
| a magus's House | statting a magus NPC, locating an Order matter | generators/houses.json | replace |
| a region / Tribunal | placing a covenant, rival, or Order affair on the map | generators/tribunals.json | replace |
| generic inspiration (Discover Meaning, no specific need) | — | Mythic Elements (engine default) | default |

# Anything not listed -> Mythic/AC default. All tables are list_d100 in the engine schema and are
# roll-tested by `python3 ../../mythic-gm/scripts/bridge.py validate <this bridge>`.
