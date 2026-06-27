# Character sheet — now JSON (the source of truth scripts read from)

The PC record is **`<campaign>/characters/<slug>.json`** (one file per troupe member). The human
`<campaign>/character-sheet.md` is **rendered from those JSONs** and regenerated on every change —
edit the JSON via the `char` commands, not the markdown.

## Build it
```
arm.py char new --type magus|companion|grog --name "<name>" [--house X] [--age N] --campaign <dir>
arm.py char set    --pc <name> --campaign <dir> --set "characteristics.Int=3" --set "size=0" --set "concept=…"
arm.py char art    --pc <name> --campaign <dir> --art Creo --score 10        # magi: Cr/In/Mu/Pe/Re, An/Aq/…/Vi
arm.py char ability --pc <name> --campaign <dir> --name "Magic Theory" --score 3 [--spec "…"]
arm.py char spell  --pc <name> --campaign <dir> --name "Pilum of Fire" --tech Creo --form Ignem --level 20
arm.py char virtue|flaw --pc <name> --campaign <dir> --name "Gentle Gift" --tier Major
arm.py char weapon --pc <name> --campaign <dir> --name Staff --init 2 --attack 5 --defense 6 --damage 2
arm.py char validate --pc <name> --campaign <dir>     # check the build against the creation rules
arm.py char show|sheet|list --campaign <dir>
```

## Play (live values mutate the JSON)
```
arm.py char wound   --pc <name> --campaign <dir> --add Light | --heal Light
arm.py char fatigue --pc <name> --campaign <dir> --set Weary
arm.py char vis     --pc <name> --campaign <dir> --art Creo --delta +3
arm.py warping      --pc <name> --campaign <dir> --add 1
```

## Scripts read from it — pass `--pc <name> --campaign <dir>`
```
arm.py cast    --pc <name> --campaign <dir> --spell "Pilum of Fire" --aura 3      # pulls Te/Fo/Sta/Penetration
arm.py cast    --pc <name> --campaign <dir> --tech Creo --form Ignem --level 5 --kind spont-nonfat --aura 3
arm.py ability --pc <name> --campaign <dir> --stat Per --skill Awareness --ef 9
arm.py combat  attack --pc <name> --campaign <dir> --weapon Staff --def 7 --soak 4 --size 0
arm.py aging   --pc <name> --campaign <dir>                                       # reads age
arm.py certamen --pc <attacker> --pc-def <defender> --campaign <dir> --a-art Ignem --d-art Ignem
```

## JSON shape (schema `arm.character/1`)
`name` · `type` (magus|companion|grog) · `house` · `covenant` · `concept` · `age{actual,apparent}` · `size` ·
`characteristics{Int,Per,Pre,Com,Str,Sta,Dex,Qik}` (−3..+3) · `confidence{score,points}` ·
`decrepitude{score,points}` · `warping{score,points}` · `virtues[]`/`flaws[]` `{name,tier}` ·
`personality[]` · `reputations[]` · `abilities{<name>:{score,spec}}` ·
`arts{techniques{Cr…Re}, forms{An…Vi}}` (magi) · `spells[]{name,tech,form,level,mastery}` ·
`combat[]{name,init,attack,defense,damage}` · `soak` · `fatigue{current}` · `wounds[]` ·
`vis{<Art>:pawns}` (magi) · `equipment[]` · `bonds[]`.
