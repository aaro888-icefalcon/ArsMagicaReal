# Generator Index — <Setting>   (hooks: generate:*)
# need | when it's called | table(s) | mode (replace | conjunction | default)
| need              | when called                     | table(s)                          | mode        |
|-------------------|---------------------------------|-----------------------------------|-------------|
| new NPC (generic) | any new Character invoked       | AC Character Crafter + npc_role.json | conjunction |
| location          | a scene needs a place           | region.json                       | replace     |
| faction           | a new faction/org               | faction.json                      | replace     |
| generic inspiration | Discover Meaning, no need     | Mythic Elements                   | default     |
# Anything not listed -> Mythic/AC default. Tables are list_d100/list_d10 JSON in this folder,
# rolled with: python3 mythic-gm/scripts/dice.py table <abs path to the json>
