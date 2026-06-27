# Ingested Adventure — The Broken Covenant of Calebais   (hook: adventure-ingest; pure sandbox)
fidelity: light
source: wip/Ars Magica 5e - Adventure - Broken Covenant of Calebais.md   (read one detail at a time, as the PCs reach it)
diminisher: 1/3   # The module assumes a multi-magus troupe with expendable grogs; scale opposition
                  # (Hrool numbers, ghost Might, trap Ease Factors) down ~⅓ for a lone/small magus party.
                  # Use 1/2 for a freshly-gauntleted lone magus; 1/4 only for a single very weak character.

## Premise / hook
A Redcap (**Ash**) delivers a tattered letter written by a dying magus of **Calebais** — a once-powerful covenant tunneled into Two Crag Hill that fell ~50 years ago (~1170) in an internecine slaughter the survivors call "the Sundering." Passed on by an aged ex-Calebais nun, the letter warns the Order is endangered: a recent killing in the nearby village threatens to draw mundane (and Church) attention to the ruins. The player magi are asked to solve the village mystery, pass Mormulus's Veil, explore the haunted nine-level ruin, and recover its legendary artifact, the **Bell of Ibyn** — while keeping the Order's involvement hidden.

## Seed the Lists from all clusters
**Threads (objectives):**
1. Solve the village mystery (a man gored dead, his pregnant daughter missing, her lover amnesiac); keep mundane/Church scrutiny off Calebais.
2. Penetrate the forest and Mormulus's Veil (the satyrs, the bound dryad, the twelve guides and their riddle).
3. Explore the ruins of Calebais and recover the Bell of Ibyn.
4. Unlock the Bell's powers — track down Sister Larine at the convent for the key. *(long-delayed)*
5. (Optional) Lay the restless dead to rest; rescue the satyrs' captive girl; decide the fate of the Hrools; explore the flooded lower levels.

**Characters (NPCs / factions):** Ash (Redcap; wants respect, guards the nun's secret) · Sir Gilbert (knight-errant hunting the rumored dragon; knows 4 of the 12 guides) · Boch (satyr; holds the captive girl, misses the dryad) · the Dryad (controls the Veil; lonely, bound by a Calebais bargain) · Father Eric (abbot; wants rumors quieted) · Stephen (reeve; believes great evil lurks in the wood) · the ghosts of Calebais (Crenvalus, Mormulus, Pitsdim, Ierimyra, Ornath — each freed by a specific resolution) · the Hrools (feral, intelligent ferret-folk bred by Ierimyra; attack the Gifted unless the Gentle Gift is present) · Sister Larine (the ex-Calebais nun; holds the Bell's key; dies before the PCs arrive).

**Adventure Features (locations / set-pieces / hazards):** the Village & Cistercian Abbey (social hazard: no women or armed warriors; the Gifted are shunned) · the Wood / Faerie regio (aura 2; levels 3–5: Satyr Hollow, the Veil, Dryad Grove) · the Marker & the Veil puzzle (Latin riddle; twelve illusory guides in the correct order) · the Entrance / the Well (inverted tower; nine levels, lower ones flooded; falling hazard) · the ruined interior (scorch, phoenix light-carvings, Herbam-vis moss, oversized vermin, pervasive Hrool musk → Stamina checks) · the laboratories (largely intact, ghost-guarded) · the Vault / Inner Chamber & traps ("Perilous Sun," "Perilous Water," pitfalls, three guardian ghosts) · the Bell of Ibyn (~600 lb, eye-shaped, twelve runed knobs; damaged, needs diadems + Larine's key).

## Clusters (authored scene-nodes) — surface by relevance; each is Scene-Tested when framed
### cluster: redcap-letter — "The Redcap's Message"   (source: "Ash", "The Redcap's Message", "The Letter from Crenvalus")
scene: Ash arrives at the player covenant with a torn letter from the dead magus Crenvalus; she relays the nun's fear that Calebais's reawakening could implicate the Order, but guards the nun's identity.
threads: [village-mystery, unlock-bell]   characters: [Ash, Crenvalus(letter), Larine(absent)]   elements: [Bell-of-Ibyn, Mormulus-Veil]   themes: [Mystery, Social]
gate: treat Ash with respect (Bargain / Folk Ken) or she withholds extra help and directions.
fragments:
  - plot_point: "The letter is torn mid-sentence, naming the dryad and 'twelve guides' but cutting off before the full order."   themes: [Mystery]   weight: 1
  - plot_point: "The nun warns mundane investigation could expose the Order to the abbot's Church connections."   themes: [Tension]   weight: 1
  - plot_point: "Ash will not reveal the nun's name or location — a withheld thread for later."   themes: [Social]   weight: 1

### cluster: village-mystery — "Death in the Wood"   (source: "The Village", "The Abbey", "The Reeve")
scene: In the village a man lies gored to death, his pregnant daughter vanished, her amnesiac lover convalescing at the abbey; the abbot wants it hushed while the reeve wants the woods hunted.
threads: [village-mystery]   characters: [Father-Eric, Stephen, injured-young-man]   elements: [faerie-forest, the-Bell-sound]   themes: [Social, Mystery]
gate: the Gifted are distrusted; the Cistercians refuse women and warriors — PCs need disguise/cover (steer this to companions/grogs).
fragments:
  - plot_point: "The corpse's wound resembles a horn-goring; tracks hint at goat-footed bipeds (satyrs)."   themes: [Mystery]   weight: 1
  - plot_point: "The amnesiac youth recalls only a great, broken-toned bell tolling in the forest."   themes: [Mystery]   weight: 1
  - plot_point: "Abbot vs. reeve conflict escalates to a mundane search party unless defused."   themes: [Tension]   weight: 1

### cluster: forest-faeries — "Satyrs, Dryad, and the Veil"   (source: "The Wood", "Satyr Hollow", "The Dryad", "The Marker", "The Veil")
scene: Within the Faerie regio the satyrs hold the captive girl and pine for their lost dryad; the dryad controls the Veil and is bound to Calebais, while Sir Gilbert camps nearby hunting his dragon.
threads: [penetrate-veil, rescue-girl(optional)]   characters: [Boch, Dryad, Sir-Gilbert]   elements: [twelve-guides, riddle]   themes: [Social, Mystery]
gate: the dryad leads them to the entrance only once they engage the mystery / can offer her freedom; the satyrs trade the girl only for the dryad's return.
fragments:
  - plot_point: "The dryad is bound by a bargain with the fallen covenant and cannot leave her fountain in body."   themes: [Personal]   weight: 1
  - plot_point: "Twelve guides must be followed in the correct order, then their riddle answered, to pass the Veil."   themes: [Mystery]   weight: 1
  - plot_point: "Sir Gilbert knows four of the twelve guides and may aid the breakthrough."   themes: [Social]   weight: 1

### cluster: well-descent — "Into the Inverted Tower"   (source: "The Entrance", "Falling into the Well", "Inside Calebais", "The Hrools")
scene: The entrance opens onto a deep central well of ruined, scorched halls; the explorers meet the feral, intelligent Hrools and the first restless ghosts amid decay and oversized vermin.
threads: [explore-ruins]   characters: [Hrools, ghosts]   elements: [phoenix-lights, vis-moss]   themes: [Tension, Mystery]
gate: Hrools attack the Gifted on sight unless a character has the Gentle Gift; musk-heavy areas force Stamina checks (EF 3, or 6 in strong-scent zones).
fragments:
  - plot_point: "Falling into the well is an early lethal hazard of the descent."   themes: [Tension]   weight: 1
  - plot_point: "The Hrools are Ierimyra's bred creations, now split into warring groups led by diademed 'ermines'."   themes: [Mystery]   weight: 1
  - plot_point: "Each ghost is freed only by a specific, personalized resolution to its grief or guilt."   themes: [Personal]   weight: 1

### cluster: vault-and-bell — "The Vault and the Bell of Ibyn"   (source: "The Vault", "The Inner Chamber", "Corridor and Pitfalls", "The Bell of Ibyn")
scene: Past trap-laden corridors ("Perilous Sun," "Perilous Water," pitfalls) and three guardian ghosts lie the treasure vault, burial chamber, and the strange eye-shaped Bell of Ibyn.
threads: [explore-ruins, unlock-bell]   characters: [Granorda, Crenvalus(ghost), Uderzus]   elements: [Bell-of-Ibyn, diadems]   themes: [Tension, Mystery]
gate: Uderzus tests the characters and is freed only by answering his questions; reaching the Bell requires surviving the traps and guardians.
fragments:
  - plot_point: "The Bell is found damaged / out of tune — it does almost nothing without a diadem and the missing key."   themes: [Mystery]   weight: 1
  - plot_point: "A diadem plus the phrase 'Corona fracta est' grants Bell-scrying that even bypasses Mormulus's Veil."   themes: [Mystery]   weight: 1
  - plot_point: "None of the ghosts remember the activation ritual — only Ornath led it, pointing toward Sister Larine."   themes: [Personal]   weight: 1

### cluster: convent-key — "The Convent and Larine's Key"   (source: "Options: The Ruins", Chapter Three intro)   gate: long-delayed
scene: Seasons later, with the Bell still inert, the characters persuade Ash to bring them to the Cistercian convent to find Sister Larine — only to learn their benefactor has died, leaving a final message.
threads: [unlock-bell]   characters: [Larine(deceased), Ash, Hedwig(abbess)]   elements: [Bell-key, convent]   themes: [Personal, Social]
gate: Ash escorts them only if they prove trustworthy and swear to keep Larine's identity secret.
fragments:
  - plot_point: "The Bell requires twelve diademed people tuned to their personalities — knowledge only Larine retained."   themes: [Mystery]   weight: 1
  - plot_point: "Larine has died before they arrive; her written deathbed message holds the answer."   themes: [Personal]   weight: 1
  - plot_point: "The characters must prove their virtue at the convent to earn the message."   themes: [Social]   weight: 1

## Anti-railroad (binding)
The dice still decide. The module is a map, not a script — if an honest result kills an "essential" ghost-resolution, frees the dryad early, or skips the intended path, **adapt**. Apply **Player ≠ PC knowledge**: never act on a module fact (a ghost's secret, the guide order, the Bell's key) the PCs haven't discovered in play.
