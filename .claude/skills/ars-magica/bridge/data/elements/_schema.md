# Atomic setting-element schema

Each `data/elements/*.json` is `{ "type": "<type>", "elements": [ <record>, … ] }`.
Every record is an addressable atom of Mythic Europe that the companion can search, show,
**insert** into the live Threads/Characters Lists, or **surface** by relevance.

```json
{
  "id":   "house.flambeau",        // unique, dotted: <type>.<slug>
  "type": "house",                 // house | tribunal | realm | code_clause | npc_archetype | faction | hook | …
  "name": "House Flambeau",
  "tags": ["order","societas","fire","martial"],   // lowercase; drive search + surfacing overlap
  "realm": null,                   // Magic|Faerie|Divine|Infernal for realm-bound atoms, else null
  "summary": "one-line ground truth",
  "wants": "what it pursues / how it acts (NPC lens)",
  "as_character": "how to frame it if inserted as a Character",   // optional
  "as_thread":    "how to frame it if inserted as a Thread",      // optional
  "relations": ["other.id", "type.*"],                            // optional soft links
  "source": "reviewed/…#anchor"
}
```

`arm.py element insert <id> --into thread|character --campaign <dir>` appends a normal engine
List entry `{name, weight, element_id, tags, realm, status}` — the dice roll it like any other,
and the GM surfaces the atom's detail when it is invoked. `surface` ranks dormant atoms by tag
overlap with the open Lists + the current scene. Records mirror the prose in `setting-canon.md`;
the prose stays the human lens, these are the machine-addressable decomposition.
