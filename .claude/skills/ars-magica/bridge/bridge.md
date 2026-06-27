# Bridge manifest — Ars Magica 5e (Mythic Europe)

This companion supplies the **Ars Magica 5th Edition (Definitive Edition)** ruleset and the **Mythic Europe** setting (year 1220) to the mythic-gm engine: Hermetic task resolution and combat (`system-profile.md`), the Order-of-Hermes / four-Realms GM lens (`interpretation.md`), fixed saga theme weights, chaos lean, world-tick subsystems (covenant seasons, aging, warping, vis, Order & mundane politics), a covenant-saga seed deck, the setting ground truth (`setting-canon.md`), five faithful generators, and an ingested classic adventure (*The Broken Covenant of Calebais*). Every uncertain outcome still runs through the engine's honest, shown dice. A partial bridge always plays; unfilled hooks use the engine default.

```json
{
  "companion": "Ars Magica 5e (Mythic Europe)",
  "engine": "mythic-gm>=2",
  "overrides": ["resolve","meaning","chaos","themes","generate:character","generate:element","world-tick","seeds","adventure-ingest"],
  "files": {
    "system_profile": "system-profile.md",
    "interpretation": "interpretation.md",
    "chaos": "chaos-tendency.md",
    "themes": "theme-weights.md",
    "generators": "generators/registry.md",
    "subsystems": "subsystems.md",
    "seeds": "seeds.md",
    "canon": "setting-canon.md",
    "adventure": "adventures/broken-covenant-of-calebais.md"
  },
  "generators_map": {
    "character": { "mode": "conjunction", "table": "generators/hermetic_npc.json",
                   "note": "Layer the rolled Hermetic/covenant archetype onto the AC Character Crafter; flesh from setting-canon (House, covenant, Realm) and the current scene. Gifted NPCs carry the Gift's -3 social penalty (-6 Blatant) unless Gentle Gift; Parma negates it among magi. Supernatural NPCs get a Might (Realm) = their Magic Resistance." }
  }
}
```

`generators_map` is the machine-readable routing the engine reads (the prose `generators/registry.md` is the human index). `mode`: `replace` = companion generator instead of the Mythic/AC default · `conjunction` = companion **and** default · `default` = use the engine default. Only `character` auto-fires today (on any **NEW CHARACTER** result); the other generators are rolled on demand with `dice.py table <path>`. Pass `--bridge <this-dir>` to the roller scripts so the override is seen (the loop does this automatically).
