# World Subsystems — <Setting>   (hook: world-tick; fired by tick.py at bookkeeping)
| subsystem        | cadence          | advance by |
|------------------|------------------|-----------|
| <War Front clock>| every scene      | tick +1; at full → roll <table> |
| <Salvage economy>| every scene      | draw 1 on <table> |
| <Faction move>   | every 3 scenes   | roll <faction.json> + a Move Toward/Away a Thread |
