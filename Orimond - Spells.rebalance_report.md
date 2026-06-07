# Orimond Spell Compendium Rebalance Report

## Summary

- Spells processed: 406
- Cantrips promoted to 1st level: 30
- Saving throws populated: 215
- Damage types populated: 135
- Conditions populated: 126
- Ritual spells: 45
- Techno Magic spells: 68
- Spells still requiring manual review: 75

The rebalance uses the original `Class` column. `New Class` was preserved but not
used for balance decisions. Mechanical text was not silently rewritten; uncertain
or story-scale effects remain marked for manual review.

## Acceptance Checks

- Cantrip count: 55 (target 45-60)
- Damage rows missing a damage type: 0
- Save-based rows missing Success or Fail: 0
- Reaction spells missing a trigger: 0
- Sorcerer access: 140 (target 120-160)
- Druid access: 95 (target 80-110)
- Artificer access: 60 (target 50-80)
- Ranger access: 45 (target 35-60)

## Level Distribution Before

| Value | Count |
|---|---:|
| 0-Cantrip | 85 |
| 1st-level | 40 |
| 2nd-Level | 2 |
| 2nd-level | 54 |
| 3rd-level | 62 |
| 4th-level | 46 |
| 5th-level | 31 |
| 6th-level | 27 |
| 7th-level | 26 |
| 8th-level | 18 |
| 9th-level | 15 |

## Level Distribution After

| Value | Count |
|---|---:|
| 0-Cantrip | 55 |
| 1st-level | 70 |
| 2nd-level | 56 |
| 3rd-level | 62 |
| 4th-level | 46 |
| 5th-level | 31 |
| 6th-level | 27 |
| 7th-level | 26 |
| 8th-level | 18 |
| 9th-level | 15 |

## School Distribution Before

| Value | Count |
|---|---:|
| Abjuration | 57 |
| Conjuration | 54 |
| Divination | 40 |
| Enchantment | 40 |
| Evocation | 56 |
| Illusion | 30 |
| Necromancy | 53 |
| Transmutation | 76 |

## School Distribution After

| Value | Count |
|---|---:|
| Abjuration | 57 |
| Conjuration | 54 |
| Divination | 40 |
| Enchantment | 40 |
| Evocation | 56 |
| Illusion | 38 |
| Necromancy | 53 |
| Transmutation | 68 |

## Original Class Access Before

| Value | Count |
|---|---:|
| Artificer | 13 |
| Bard | 107 |
| Cleric | 78 |
| Druid | 34 |
| Paladin | 56 |
| Ranger | 19 |
| Sorcerer | 250 |
| Warlock | 122 |
| Wizard | 111 |

## Original Class Access After

| Value | Count |
|---|---:|
| Artificer | 60 |
| Bard | 107 |
| Cleric | 100 |
| Druid | 95 |
| Paladin | 50 |
| Ranger | 45 |
| Sorcerer | 140 |
| Warlock | 100 |
| Wizard | 130 |

## Original Class Access by Level Before

| Level | Artificer | Bard | Cleric | Druid | Paladin | Ranger | Sorcerer | Warlock | Wizard |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0-Cantrip | 2 | 35 | 10 | 7 | 0 | 0 | 54 | 23 | 26 |
| 1st-level | 2 | 17 | 2 | 3 | 1 | 9 | 23 | 11 | 5 |
| 2nd-level | 3 | 17 | 15 | 6 | 12 | 4 | 28 | 11 | 8 |
| 3rd-level | 1 | 22 | 11 | 3 | 10 | 4 | 36 | 18 | 14 |
| 4th-level | 2 | 5 | 13 | 5 | 11 | 1 | 27 | 11 | 15 |
| 5th-level | 1 | 6 | 7 | 3 | 6 | 1 | 22 | 12 | 9 |
| 6th-level | 2 | 1 | 4 | 1 | 1 | 0 | 21 | 13 | 12 |
| 7th-level | 0 | 1 | 6 | 3 | 6 | 0 | 21 | 12 | 12 |
| 8th-level | 0 | 1 | 6 | 3 | 6 | 0 | 9 | 4 | 6 |
| 9th-level | 0 | 2 | 4 | 0 | 3 | 0 | 9 | 7 | 4 |

## Original Class Access by Level After

| Level | Artificer | Bard | Cleric | Druid | Paladin | Ranger | Sorcerer | Warlock | Wizard |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0-Cantrip | 8 | 10 | 8 | 6 | 0 | 0 | 16 | 12 | 10 |
| 1st-level | 14 | 19 | 17 | 12 | 14 | 13 | 22 | 15 | 18 |
| 2nd-level | 13 | 20 | 17 | 19 | 9 | 12 | 26 | 16 | 21 |
| 3rd-level | 10 | 14 | 18 | 14 | 10 | 11 | 23 | 16 | 17 |
| 4th-level | 8 | 7 | 11 | 13 | 8 | 5 | 11 | 6 | 14 |
| 5th-level | 7 | 14 | 12 | 13 | 9 | 4 | 12 | 5 | 14 |
| 6th-level | 0 | 6 | 6 | 6 | 0 | 0 | 11 | 11 | 12 |
| 7th-level | 0 | 9 | 5 | 4 | 0 | 0 | 8 | 5 | 9 |
| 8th-level | 0 | 4 | 3 | 5 | 0 | 0 | 6 | 7 | 8 |
| 9th-level | 0 | 4 | 3 | 3 | 0 | 0 | 5 | 7 | 7 |

## Casting Time Before

| Value | Count |
|---|---:|
| 1 hours | 10 |
| 1 minutes | 15 |
| 10 minutes | 14 |
| Action | 333 |
| Bonus Action | 12 |
| Reaction | 18 |
| Reaction  | 2 |
| Special | 1 |
| Variable | 1 |

## Casting Time After

| Value | Count |
|---|---:|
| 1 hour | 10 |
| 1 minute | 15 |
| 10 minutes | 14 |
| Action | 297 |
| Bonus Action | 31 |
| Reaction | 37 |
| Special | 1 |
| Variable | 1 |

## Manual Review

| Spell | Level | Reason |
|---|---|---|
| Cinder Veil | 0-Cantrip | Removed Druid access; Review unclear damage |
| Conjure Mild Inconvenience | 1st-level | Promoted from cantrip to 1st level; Review unclear damage |
| Crawling Dread | 0-Cantrip | Removed Sorcerer access; Review unclear damage |
| Dirge Pulse | 0-Cantrip | Removed Sorcerer access; Review unclear damage |
| Lantern of the Forgotten | 1st-level | Promoted from cantrip to 1st level; Added Cleric access; Removed Sorcerer access; Review unclear damage |
| Mage Sand | 0-Cantrip | Review permanent effect |
| Scorned Mark | 1st-level | Promoted from cantrip to 1st level; Added Artificer access; Bonus Action casting; Review unclear damage |
| Spellgraft | 1st-level | Promoted from cantrip to 1st level; Removed Sorcerer access; Review unclear damage |
| Verdant Renewal | 0-Cantrip | Review unclear damage |
| Wisp of the Forgotten | 1st-level | Promoted from cantrip to 1st level; Added Cleric access; Removed Bard, Sorcerer access; Review unclear damage |
| Eternal Etching | 1st-level | Added Ranger access; Bonus Action casting; Review unclear damage; Review permanent effect |
| Inkbound Familiar | 1st-level | Added Artificer, Wizard access; Ritual casting; Review permanent effect |
| Jealousy | 1st-level | Removed Sorcerer access; Review unclear damage |
| Orb of Let's Not | 1st-level | Review unclear damage |
| Amphibious Downpour | 2nd-level | Added Ranger, Warlock, Wizard access; Reaction casting; Review unclear damage |
| Drowsing Embrace | 2nd-level | Review unclear damage |
| Echo of the Hallowed Ground | 2nd-level | Added Druid, Ranger access; Review unclear damage |
| Eldritch Intoxication | 2nd-level | Review unclear damage |
| Eyes Behind the Kiss | 2nd-level | Added Cleric access; Review named damage outlier; Review unclear damage |
| Mnemonic Wipe | 2nd-level | Added Cleric access; Review permanent effect |
| Cerulean Incantation of Pride | 3rd-level | Added Sorcerer access; Removed Bard access; Review unclear damage |
| Delayed Nap | 3rd-level | Review unclear damage |
| Enthralling Kiss | 3rd-level | Review unclear damage; Review permanent effect |
| Festering Graze | 3rd-level | Added Cleric, Druid access; Ritual casting; Review named damage outlier; Review unclear damage |
| Fracturing of the Erelian Ledger | 3rd-level | Added Artificer, Druid access; Ritual casting; Review permanent effect |
| Immutable Clause | 3rd-level | Added Artificer, Druid, Ranger access; Reaction casting; Review unclear damage; Review permanent effect |
| Mirabel's Breath of Dusk | 3rd-level | Removed Sorcerer access; Review permanent effect |
| Regal Cipher of Binding | 3rd-level | Added Artificer access; Review permanent effect |
| Regal Mantling | 3rd-level | Review unclear damage |
| Ricochet | 3rd-level | Review unclear damage |
| Social Sabotage  | 3rd-level | Removed Sorcerer access; Review unclear damage |
| Summon the Pendulum of Ruin | 3rd-level | Added Artificer, Cleric access; Review unclear damage |
| Utallash's Pursuit of Ceramic | 3rd-level | Added Cleric, Ranger access; Review permanent effect |
| Veil-Tread of Uncertain Thread | 3rd-level | Review unclear damage |
| Architect’s Collapse | 4th-level | Review unclear damage; Review permanent effect |
| Dissonant Gestation | 4th-level | Added Druid access; Ritual casting; Review permanent effect |
| Refraction of Self | 4th-level | Removed Warlock access; Review unclear damage |
| Regal Seal of Arrested Passage | 4th-level | Added Artificer access; Reaction casting; Review permanent effect |
| Sever Anomaly | 4th-level | Removed Paladin access; Review permanent effect |
| The Crawling Hunger | 4th-level | Removed Sorcerer access; Review permanent effect |
| Fleshsmith’s Alloy | 5th-level | Added Druid access; Ritual casting; Review permanent effect |
| Hollow of Lingering Thread | 5th-level | Added Bard, Cleric access; Removed Warlock access; Review unclear damage |
| Ledger of Justified Existence | 5th-level | Added Wizard access; Review unclear damage |
| Rite of Twin Accord | 5th-level | Review unclear damage |
| Womb of the Unwritten | 5th-level | Removed Warlock access; Review permanent effect |
| Mannequin's Lament | 6th-level | Added Druid access; Review unclear damage |
| Prism Shear  | 6th-level | Review named damage outlier; Review unclear damage |
| Rimefold Exsanguination | 6th-level | Review unclear damage |
| Sanctioned Haunting | 6th-level | Removed Sorcerer access; Review permanent effect |
| Stone Ship | 6th-level | Removed Artificer, Sorcerer access; Review unclear damage |
| Summon the Saint | 6th-level | Review permanent effect |
| The Bleeding Contract | 6th-level | Review permanent effect |
| Erasure of Pain | 7th-level | Removed Cleric, Paladin, Warlock access; Review unclear damage |
| Formula of Unraveling | 7th-level | Added Bard access; Removed Sorcerer access; Review named damage outlier; Review unclear damage |
| Giocrin's Incantation of Bitterness | 7th-level | Removed Warlock access; Review unclear damage |
| Reality Sidestep | 7th-level | Added Druid access; Removed Sorcerer, Warlock access; Review unclear damage; Review permanent effect |
| Reweaving of the False Thread | 7th-level | Added Bard access; Removed Sorcerer access; Ritual casting; Review permanent effect |
| Skin Unwoven | 7th-level | Added Bard access; Removed Warlock access; Review permanent effect |
| Struck from the Loom | 7th-level | Removed Sorcerer access; Review permanent effect |
| Chronoseal | 8th-level | Added Bard access; Removed Sorcerer access; Review unclear damage |
| Concord of Dissonant Hearts | 8th-level | Added Wizard access; Removed Cleric, Paladin access; Review unclear damage |
| Edict of Absolute Finality | 8th-level | Added Warlock access; Removed Paladin access; Review unclear damage |
| Flesh to Paper | 8th-level | Added Warlock access; Review unclear damage |
| Fleshbound Chronicle | 8th-level | Added Bard access; Review unclear damage |
| Fragmentation Rift | 8th-level | Review named damage outlier; Review unclear damage |
| Man ↔ Cock | 8th-level | Added Druid access; Review unclear damage |
| Paradox of Endless Petition | 8th-level | Removed Paladin access; Review permanent effect |
| Abhaaldrac’s Unmaking Descent | 9th-level | Added Wizard access; Bonus Action casting; Review permanent effect |
| Create Spell | 9th-level | Added Druid access; Ritual casting; Review permanent effect |
| Exiled from the Self | 9th-level | Added Bard, Druid access; Ritual casting; Review permanent effect |
| Heartbreaker | 9th-level | Review permanent effect |
| Judgment of the Loom | 9th-level | Added Bard, Wizard access; Removed Paladin access; Ritual casting; Review permanent effect |
| Mirabel's Final Verse | 9th-level | Added Druid access; Removed Sorcerer access; Review unclear damage; Review permanent effect |
| Strike from the Loom | 9th-level | Added Wizard access; Removed Paladin access; Review named damage outlier; Review unclear damage |
| Vow of Erasure | 9th-level | Removed Sorcerer access; Review permanent effect |
