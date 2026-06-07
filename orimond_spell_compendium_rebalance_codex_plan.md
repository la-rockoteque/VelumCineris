# Orimond Spell Compendium Rebalance Plan for Codex

## Purpose

Rebalance and rework `Orimond - Spells.csv` so the spell compendium feels like it has gone through real table playtesting. Use the spreadsheet as the source of truth, preserve the setting flavour, and make the mechanical layer consistent enough for players and GMs to compare spells fairly.

Important: use the **original class list** for all class-access analysis and balancing. In the CSV, this means the `Class` column. Do not use `New Class` for balance decisions unless explicitly instructed later.

## Source file

Input file:

```text
/mnt/data/Orimond - Spells.csv
```

Primary output should be a revised CSV with the same columns preserved unless a new audit column is explicitly useful. If temporary helper columns are added, prefix them with `Audit -`.

Recommended output files:

```text
/mnt/data/Orimond - Spells.rebalanced.csv
/mnt/data/Orimond - Spells.rebalance_report.md
```

## Non-negotiable instructions

1. Use `Class`, not `New Class`, when analyzing class balance.
2. Preserve spell names unless a name is clearly duplicated, broken, or typo-ridden.
3. Preserve theme and flavour where possible.
4. Prefer surgical balancing over full rewrites.
5. Do not delete spells automatically. Mark proposed removals or merges in an audit column.
6. Every hostile spell must have a clear resolution model.
7. Every damage spell must have a damage type.
8. Every condition spell must have a condition, save, duration, and end condition.
9. Every permanent hostile spell must have a cost, limitation, repeat save, dispel method, or equivalent balancing mechanism.
10. Normalize data values before doing balance calculations.

## Current compendium snapshot

Total spells: **406**

### Level distribution

| Level | Count | Review |
|---:|---:|---|
| 0, Cantrip | 85 | Too high |
| 1st | 40 | Low |
| 2nd | 56 | Healthy |
| 3rd | 62 | Heavy |
| 4th | 46 | Healthy |
| 5th | 31 | Slightly low |
| 6th | 27 | Acceptable |
| 7th | 26 | Acceptable |
| 8th | 18 | Low |
| 9th | 15 | Acceptable |

Target distribution:

| Level | Target Count |
|---:|---:|
| 0, Cantrip | 45 to 55 |
| 1st | 55 to 65 |
| 2nd | 55 to 65 |
| 3rd | 50 to 60 |
| 4th | 40 to 50 |
| 5th | 32 to 42 |
| 6th | 24 to 32 |
| 7th | 20 to 28 |
| 8th | 16 to 24 |
| 9th | 12 to 18 |

Main action: reduce cantrip bloat by converting, merging, or promoting roughly **25 to 35 cantrips**.

### School distribution

| School | Count | Review |
|---|---:|---|
| Transmutation | 76 | Too dominant |
| Abjuration | 57 | Healthy |
| Evocation | 56 | Healthy |
| Conjuration | 54 | Healthy |
| Necromancy | 53 | Healthy |
| Divination | 40 | Slightly low |
| Enchantment | 40 | Slightly low |
| Illusion | 30 | Too low |

Target adjustment:

- Bring Illusion closer to 38 to 44.
- Reduce Transmutation slightly if effects are actually perception, memory, command, record, fear, charm, or concealment.
- Keep Orimond flavour intact, but classify by mechanical effect first.

School reassignment rules:

| Effect Type | Preferred School |
|---|---|
| Direct damage, force release, destructive burst | Evocation |
| Wards, seals, protection, interdiction, nullification | Abjuration |
| Summoning, gates, imported objects, spatial conjuring | Conjuration |
| Decay, life-force, undeath, disease, soul rot | Necromancy |
| Memory, prophecy, records, hidden information, truth | Divination |
| Charm, fear, compulsion, command, social domination | Enchantment |
| Concealment, decoys, altered perception, false presence | Illusion |
| Flesh, matter, form, body change, time, physical alteration | Transmutation |

### Original class access distribution

Use these counts as the current baseline. These are based on the `Class` column.

| Original Class | Total Spell Access | Review |
|---|---:|---|
| Artificer | 13 | Critically low |
| Bard | 107 | Healthy |
| Cleric | 78 | Moderate |
| Druid | 34 | Too low |
| Paladin | 56 | High for a half-caster |
| Ranger | 19 | Too low |
| Sorcerer | 250 | Extremely high |
| Warlock | 122 | High |
| Wizard | 111 | Healthy |

### Original class access by level

| Level | Artificer | Bard | Cleric | Druid | Paladin | Ranger | Sorcerer | Warlock | Wizard |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 2 | 35 | 10 | 7 | 0 | 0 | 54 | 23 | 26 |
| 1 | 2 | 17 | 2 | 3 | 9 | 9 | 23 | 11 | 5 |
| 2 | 3 | 17 | 15 | 6 | 17 | 4 | 28 | 11 | 8 |
| 3 | 1 | 22 | 11 | 3 | 11 | 4 | 36 | 18 | 14 |
| 4 | 2 | 5 | 13 | 5 | 6 | 1 | 27 | 11 | 15 |
| 5 | 1 | 6 | 7 | 3 | 9 | 1 | 22 | 12 | 9 |
| 6 | 2 | 1 | 4 | 1 | 1 | 0 | 21 | 13 | 12 |
| 7 | 0 | 1 | 6 | 3 | 1 | 0 | 21 | 12 | 12 |
| 8 | 0 | 1 | 6 | 3 | 1 | 0 | 9 | 4 | 6 |
| 9 | 0 | 2 | 4 | 0 | 1 | 0 | 9 | 7 | 4 |

Class fairness observations:

- Sorcerer has excessive access and likely absorbs too many spells by default.
- Artificer, Druid, and Ranger are under-supported.
- Paladin has unusually broad access for a half-caster, including high-level entries. Verify whether this is intentional.
- Bard has very high cantrip access.
- Wizard is reasonable overall but low at 1st level relative to identity.
- Cleric has an odd low 1st-level count and stronger mid/high-level access.
- Warlock is high, especially for a pact-magic class.
- Original class access should be thematic and mechanical, not broad by default.

## Data hygiene pass

Normalize these fields before analysis.

### Level normalization

Current inconsistent values include:

```text
0-Cantrip
1st-level
2nd-level
2nd-Level
3rd-level
...
```

Normalize to:

```text
0-Cantrip
1st-level
2nd-level
3rd-level
4th-level
5th-level
6th-level
7th-level
8th-level
9th-level
```

### Casting Time normalization

Current issues include trailing spaces and pluralized values.

Normalize to:

```text
Action
Bonus Action
Reaction
1 minute
10 minutes
1 hour
Variable
Special
```

### Duration normalization

Normalize common variants:

```text
Instant -> Instantaneous
instantaneous -> Instantaneous
1 minutes -> 1 minute
1 houres -> 1 hour
1 hours -> 1 hour
Premanent -> Permanent
permanent -> Permanent
concentration -> Concentration
up to -> Up to
```

### Boolean normalization

Normalize these columns to true booleans or consistent strings:

```text
Ritual
Techno Magic
Concentration
Blood Pact
Arcane Strain
Consecrated / Desecrated
```

Use:

```text
True
False
```

When a column contains text instead of a boolean, preserve the text in the associated effect column and set the flag to `True`.

### Components normalization

Normalize component order:

```text
Verbal
Somatic
Material
Verbal, Somatic
Verbal, Material
Somatic, Material
Verbal, Somatic, Material
```

Do not change component descriptions except to fix spelling or obvious formatting.

## Metadata repair pass

The CSV currently has these critical metadata gaps:

| Field | Current State | Required Action |
|---|---|---|
| Saving Throw | 0 filled entries | Fill for every hostile save-based spell |
| Damage | 122 filled entries | Validate all damage formulas |
| Damage Type | 70 filled entries | Fill for every damage spell |
| Condition | 1 filled entry | Fill for every condition-bearing spell |
| Success | Mostly empty | Fill for every save-based spell |
| Fail | Mostly empty | Fill for every save-based spell |
| Ritual | 19 true | Increase where appropriate |
| Techno Magic | 0 true | Define and use, or leave intentionally unused |
| Blood Pact | 28 populated | Expand for costly occult spells |
| Arcane Strain | 9 populated | Expand for reality-breaking spells |

### Resolution model requirement

For every hostile spell, set exactly one primary resolution model:

```text
Spell Attack
Saving Throw
Contested Check
Automatic with prerequisite
Environmental with avoidance rules
```

If there is no column for resolution model, add:

```text
Audit - Resolution Model
```

### Saving throw assignment rules

Use these rules:

| Save | Use Case |
|---|---|
| Strength | Forced movement, restraint, grappling pressure, physical holding |
| Dexterity | Dodging blasts, cones, lines, explosions, falling hazards |
| Constitution | Poison, disease, flesh alteration, necrosis, exhaustion, pain |
| Intelligence | Logic traps, paradox, records, memory computation, false causal links |
| Wisdom | Fear, charm, perception, compulsion, spiritual pressure |
| Charisma | Identity, banishment, possession, soul, oath, true name, authority |

### Success and fail text

Every save-based spell must have concise success and fail entries.

Examples:

```text
Success: The target takes half damage and suffers no additional effect.
Fail: The target takes full damage and is restrained until the end of its next turn.
```

For ongoing conditions:

```text
Success: The target is unaffected.
Fail: The target is frightened for up to 1 minute. It repeats the saving throw at the end of each of its turns, ending the effect on a success.
```

## Cantrip rebalance pass

Current cantrip count is **85**. Target is **45 to 55**.

For each cantrip, add:

```text
Audit - Cantrip Decision
```

Allowed values:

```text
Keep as Cantrip
Promote to 1st-level
Convert to Ritual
Convert to Class Feature
Merge
Remove Candidate
Needs Manual Review
```

### Keep as cantrip if

The spell does one narrow thing:

- minor damage
- minor sensory effect
- small utility effect
- minor communication effect
- small movement trick
- cosmetic magical effect
- low-risk exploration aid

### Promote to 1st-level if

The spell does any of the following:

- deals damage and adds a meaningful rider
- imposes a condition
- grants advantage or imposes disadvantage in combat
- alters action economy
- grants stealth, invisibility, or strong concealment
- prevents reactions
- creates battlefield control
- creates a multi-round defensive effect
- provides reliable encounter bypass
- scales better than ordinary cantrip damage

### Convert to ritual if

The spell is primarily:

- detection
- record keeping
- translation
- identity verification
- slow communication
- non-combat warding
- minor divination
- preparation
- exploration infrastructure

### Convert to class feature if

The spell expresses a class core loop better than a spell choice, such as:

- Artificer crafting trick
- Bard performance signature
- Cleric rite
- Druid natural attunement
- Paladin oath expression
- Ranger tracking knack
- Sorcerer innate anomaly
- Warlock pact mark
- Wizard scholarly technique

## Damage calibration pass

Use the following expected damage ranges.

### Single-target damage without major rider

| Spell Level | Expected Damage |
|---:|---:|
| Cantrip | 1d6 to 1d10, scaling by character tier |
| 1st | 2d8 to 3d8 |
| 2nd | 3d8 to 4d8 |
| 3rd | 5d8 to 6d8 |
| 4th | 6d8 to 8d8 |
| 5th | 8d8 to 10d8 |
| 6th | 10d8 to 12d8 |
| 7th | 11d10 to 13d10 |
| 8th | 12d10 to 14d10 |
| 9th | 14d10 to 20d10 |

### Area damage without major rider

Reduce expected damage by roughly 20 percent to 35 percent compared to single-target spells.

### Damage with strong rider

Reduce damage by roughly 25 percent to 50 percent if the spell also applies:

- restrained
- stunned
- paralyzed
- charmed
- frightened
- incapacitated
- action denial
- reaction denial
- movement lock
- invisibility denial
- long-duration curse
- persistent damage
- summoning
- permanent wound
- major forced movement

### Damage audit columns

Add these columns:

```text
Audit - Damage Budget
Audit - Rider Budget
Audit - Damage Verdict
```

Allowed values for `Audit - Damage Verdict`:

```text
Too Low
Acceptable
Too High
Too High Because of Rider
Needs Manual Review
```

### Known damage outliers to review

Prioritize these spells for manual review:

```text
Eyes Behind the Kiss
Festering Graze
Prism Shear
Formula of Unraveling
Fragmentation Rift
Strike from the Loom
```

For each, check:

- Is it single-target or area?
- Is damage initial only or repeatable?
- Does it impose a condition?
- Does it have a permanent or long-duration rider?
- Does it require concentration?
- Does it allow a save?
- What happens on success?

## Concentration and duration pass

Current concentration pattern is uneven. The main problems are excessive concentration among 8th-level spells and underuse of concentration for persistent 9th-level effects.

### Concentration target rates

| Level Band | Target Rate |
|---|---:|
| Cantrip | 0 to 5 percent |
| 1st to 2nd | 20 to 30 percent |
| 3rd to 5th | 30 to 45 percent |
| 6th to 8th | 35 to 55 percent |
| 9th | 25 to 45 percent |

### Add concentration if the spell lasts longer than 1 round and does any of these

- grants repeated advantage
- imposes repeated disadvantage
- creates invisibility or strong concealment
- summons allies
- restrains, frightens, charms, or controls
- creates a persistent damaging zone
- controls movement
- denies reactions
- alters enemy decisions
- creates ongoing protection

### Avoid concentration if

- duration is instantaneous
- effect is a one-time burst
- spell is a simple healing spell
- spell already has a strong cost or drawback
- spell is a permanent ritual with non-combat pacing

### Duration cleanup

Every non-instant hostile effect must specify:

- duration
- whether concentration applies
- whether the target repeats saves
- when repeat saves occur
- what breaks the effect
- whether damage breaks the effect

## Permanent effect pass

Permanent hostile or transformative effects need stricter balancing.

For every spell with duration containing:

```text
Permanent
Until dispelled
Until cured
Until revoked
Until nullified
Until fulfilled
Until broken
```

Add or verify at least three balancing constraints from this list:

- expensive consumed material component
- rare component
- ritual casting time
- Blood Pact
- Arcane Strain
- target must be willing, incapacitated, restrained, named, or helpless
- repeat save after long rest, dawn, damage, or specific trigger
- explicit dispel method
- visible mark or social consequence
- caster cannot maintain multiple instances
- target becomes immune after resisting
- effect only works on a limited creature type or circumstance
- major narrative drawback

Add:

```text
Audit - Permanent Effect Verdict
```

Allowed values:

```text
Safe
Needs Cost
Needs Save
Needs Dispel Method
Needs Prerequisite
Needs Manual Review
```

## Ritual, Blood Pact, Arcane Strain, and Techno Magic pass

### Ritual

Current ritual count is **19**. Target is **35 to 55**.

Add ritual tagging to slow, non-combat, information, warding, identification, legal, planar, record, or communication spells.

### Blood Pact

Current Blood Pact usage is **28**. Target is **45 to 70** if Blood Pact is meant to be a major Orimond balance lever.

Use Blood Pact for:

- cult magic
- oath magic
- sacrifice magic
- summoning
- curse transfer
- identity binding
- debt or bargain spells
- life-force exchange
- spells with large social or narrative consequence

### Arcane Strain

Current Arcane Strain usage is **9**. Target is **35 to 60** if Arcane Strain is meant to regulate dangerous magic.

Use Arcane Strain for:

- resurrection-adjacent effects
- timeline edits
- permanent identity alteration
- reality rewriting
- city-scale effects
- forced transformation
- soul manipulation
- large-scale conjuration
- memory rewriting
- spells that bypass ordinary encounter structure

### Techno Magic

Current true Techno Magic usage is **0**.

Codex should do one of two things:

1. Leave Techno Magic unused and mark it as intentionally inactive in the report.
2. Populate it for spells involving systems, signals, devices, records, computation, surveillance, hacking, networks, artificial bodies, or technological interfaces.

Do not invent Techno Magic mechanics without a clear pattern.

## Original class rebalance pass

Use `Class` as the source of truth.

### General class identity rules

| Original Class | Spell Identity |
|---|---|
| Artificer | Objects, devices, crafting, wards, constructs, systems, alchemy, techno-magic |
| Bard | Performance, emotion, attention, language, glamour, morale, social pressure, memory |
| Cleric | Rites, divine law, restoration, protection, judgment, consecration, souls, sacred harm |
| Druid | Beasts, plants, weather, decay cycles, terrain, natural spirits, transformation |
| Paladin | Oaths, protection, smite-like punishment, courage, judgment, aura-like effects |
| Ranger | Tracking, pursuit, mobility, wilderness, traps, marks, ambush, survival |
| Sorcerer | Innate power, mutation, anomaly, raw energy, instability, self-shaped magic |
| Warlock | Pacts, patrons, curses, names, bargains, forbidden knowledge, occult marks |
| Wizard | Study, formulae, records, structures, broad arcane tools, rituals, precision |

### Full caster targets

Applies to Bard, Cleric, Druid, Sorcerer, Warlock, Wizard.

Recommended spell access ranges after revision:

| Class | Target Total | Notes |
|---|---:|---|
| Bard | 85 to 115 | Current 107 is acceptable, but cantrip count is too high |
| Cleric | 85 to 115 | Current 78 is slightly low, especially at 1st level |
| Druid | 80 to 110 | Current 34 is far too low |
| Sorcerer | 120 to 160 | Current 250 is too high |
| Warlock | 80 to 120 | Current 122 is slightly high but acceptable if tightly thematic |
| Wizard | 110 to 150 | Current 111 is acceptable, but 1st-level access is low |

### Half caster targets

Applies to Paladin and Ranger.

Recommended spell access ranges after revision:

| Class | Target Total | Notes |
|---|---:|---|
| Paladin | 35 to 60 | Current 56 is acceptable only if high-level entries are intentional |
| Ranger | 35 to 60 | Current 19 is too low |

If the system is D&D-like, Paladin and Ranger should generally avoid native access to 6th through 9th-level spells. If high-level access is intentional for Orimond, mark this clearly in the report.

### Artificer target

Artificer currently has **13** spells, which is critically low.

Target: **50 to 80** spells if Artificer is a real spellcasting class in this compendium.

Priority additions:

- object manipulation
- wards
- devices
- constructed bodies
- alchemy
- detection
- repair
- magical tools
- binding
- techno-magic
- traps
- formula spells

### Original class audit columns

Add these columns:

```text
Audit - Original Class Verdict
Audit - Suggested Class Additions
Audit - Suggested Class Removals
Audit - Class Rationale
```

Allowed values for `Audit - Original Class Verdict`:

```text
Keep
Add Classes
Remove Classes
Narrow Access
Broaden Access
Needs Manual Review
```

### Class rebalance rules

Use these rules when adding or removing class access.

#### Remove Sorcerer access if

The spell is primarily:

- scholarly
- ritualistic
- legalistic
- technological
- constructed
- divine
- nature-specific
- pact-specific
- object-crafting

Keep Sorcerer access if the spell is:

- innate
- explosive
- bodily
- unstable
- anomalous
- self-transforming
- raw energy
- mutation-like

#### Add Druid access if

The spell concerns:

- plants
- animals
- terrain
- weather
- rot
- natural cycles
- disease as ecology
- transformation
- wilderness travel
- spirits of place

#### Add Artificer access if

The spell concerns:

- tools
- machines
- constructs
- diagrams
- formulae
- alchemy
- objects
- wards
- locks
- systems
- techno-magic
- repair or sabotage

#### Add Ranger access if

The spell concerns:

- pursuit
- marking targets
- ambush
- tracking
- stealth
- mobility
- survival
- terrain reading
- traps
- ranged precision

#### Add Cleric access if

The spell concerns:

- restoration
- consecration
- souls
- rites
- divine authority
- judgment
- protection
- exorcism
- sacred harm
- death rites

#### Add Wizard access if

The spell is:

- formulaic
- broad utility
- record-based
- spatial
- planar
- ritual
- analytical
- codified
- academically reproducible

#### Add Warlock access if

The spell concerns:

- bargains
- patrons
- curses
- names
- forbidden contact
- summoning
- debt
- compulsion through pact
- occult marks

#### Add Bard access if

The spell concerns:

- performance
- speech
- reputation
- charm
- fear through spectacle
- memory
- stories
- attention
- emotional manipulation
- social coordination

#### Add Paladin access if

The spell concerns:

- oaths
- protection
- single-target punishment
- courage
- fear suppression
- divine command
- aura-like defense
- mounted or martial support

## Action economy pass

Current casting-time distribution:

| Casting Time | Count |
|---|---:|
| Action | 333 |
| Reaction | 20 |
| Bonus Action | 12 |
| 1 minute | 15 |
| 10 minutes | 14 |
| 1 hour | 10 |
| Variable | 1 |
| Special | 1 |

The list is too Action-heavy.

Target changes:

- Convert 20 to 25 suitable spells to Bonus Action.
- Convert 15 to 20 suitable spells to Reaction.
- Convert slow utility spells to 1 minute, 10 minutes, ritual, or 1 hour.
- Keep major attack and control spells as Action.

### Bonus Action candidates

Good candidates are spells that:

- mark a target
- reposition the caster
- enable a weapon strike
- grant a brief self-buff
- activate a minor ward
- issue a command to a summoned or bound effect
- create a quick social or attention shift
- prepare a follow-up spell

### Reaction candidates

Good candidates are spells that:

- reduce damage
- punish being hit
- interrupt movement
- counter fear or charm
- redirect force
- block a condition
- protect an ally
- trigger when a creature lies, breaks an oath, casts a spell, or crosses a threshold

Add:

```text
Audit - Action Economy Verdict
```

Allowed values:

```text
Keep Action
Change to Bonus Action
Change to Reaction
Change to 1 minute
Change to Ritual
Needs Manual Review
```

## Conditions and repeat saves

Every spell that applies one of these conditions should usually allow repeat saves:

```text
Blinded
Charmed
Deafened
Frightened
Grappled
Incapacitated
Invisible
Paralyzed
Petrified
Poisoned
Prone
Restrained
Stunned
Unconscious
Exhaustion
```

Default repeat-save wording:

```text
The target repeats the saving throw at the end of each of its turns, ending the effect on a success.
```

For stronger effects:

```text
The target repeats the saving throw whenever it takes damage and at the end of each of its turns, ending the effect on a success.
```

For curse-like effects:

```text
The target repeats the saving throw at the end of each long rest, ending the effect on a success.
```

For permanent effects:

```text
The effect lasts until removed by [specific countermeasure], [specific spell], or [specific ritual].
```

## Upcasting pass

Every spell that can be cast with a higher-level slot should have a standardized scaling model.

### Damage scaling

Default:

```text
At Higher Levels. When you cast this spell using a spell slot of 2nd level or higher, the damage increases by 1 die for each slot level above 1st.
```

Adjust the spell slot number and die as needed.

### Target scaling

Use sparingly:

```text
At Higher Levels. When you cast this spell using a spell slot of one level higher, you can target one additional creature.
```

### Duration scaling

Use with caution. Avoid duration scaling on strong buffs, control spells, or stealth spells unless concentration applies.

### Area scaling

Use rarely. Area scaling can break encounters quickly.

Add:

```text
Audit - Upcasting Verdict
```

Allowed values:

```text
No Upcast Needed
Add Damage Scaling
Add Target Scaling
Add Duration Scaling
Remove Scaling
Needs Manual Review
```

## Spell text rewriting rules

When rewriting descriptions, use this structure.

```text
[Opening effect sentence.]

Make a [ability] saving throw / Make a ranged spell attack / The target must be [prerequisite].

On a failed save, [effect].
On a successful save, [reduced effect or no effect].

[Duration and repeat save sentence.]

At Higher Levels. [Scaling, if any.]
```

Avoid vague mechanical phrases like:

```text
the target struggles
the target is overwhelmed
reality rejects them
the spell weakens them
the GM decides
```

Replace them with clear terms:

```text
disadvantage on Strength checks
speed is reduced by 10 feet
cannot take reactions
takes 2d6 necrotic damage
is frightened until the end of its next turn
```

Keep flavour, but separate it from rules when possible.

## Suggested processing order for Codex

### Step 1: Load and normalize

- Load CSV.
- Preserve original columns.
- Create normalized helper values for level, casting time, duration, booleans, and classes.
- Do not overwrite original values until all normalization decisions are made.

### Step 2: Generate audit columns

Add:

```text
Audit - Resolution Model
Audit - Cantrip Decision
Audit - Damage Budget
Audit - Rider Budget
Audit - Damage Verdict
Audit - Permanent Effect Verdict
Audit - Original Class Verdict
Audit - Suggested Class Additions
Audit - Suggested Class Removals
Audit - Class Rationale
Audit - Action Economy Verdict
Audit - Upcasting Verdict
Audit - Overall Balance Verdict
Audit - Recommended Change Summary
```

### Step 3: Fill missing mechanical metadata

- Populate `Saving Throw`, `Success`, and `Fail` when the description implies a save.
- Populate `Damage Type` when `Damage` is present.
- Populate `Condition` when the description imposes a known condition.
- Normalize concentration, ritual, duration, casting time, and level.

### Step 4: Cantrip triage

- Classify every cantrip using `Audit - Cantrip Decision`.
- Promote or mark for promotion 25 to 35 cantrips.
- Prioritize moving control, advantage, stealth, rider, and long-duration cantrips.

### Step 5: Damage and rider balancing

- Evaluate every damage spell against the damage table.
- Reduce over-budget damage.
- Increase under-budget 1st-level damage where needed.
- Add concentration or repeat saves to high-value riders.
- Flag uncertain cases instead of guessing.

### Step 6: Duration and concentration balancing

- Audit every spell lasting longer than 1 round.
- Add concentration to persistent combat effects.
- Remove concentration from weak cantrips where appropriate.
- Add repeat saves to ongoing hostile effects.

### Step 7: Permanent effect balancing

- Audit every permanent, until-dispelled, until-cured, until-revoked, or until-fulfilled spell.
- Add cost, ritual time, Blood Pact, Arcane Strain, repeat save, prerequisite, or dispel method.

### Step 8: Original class rebalance

- Use `Class`.
- Reduce Sorcerer over-access.
- Increase Druid, Artificer, and Ranger access.
- Check Paladin high-level access for intentionality.
- Increase Cleric 1st-level access.
- Preserve Bard, Wizard, and Warlock access only where thematic.

### Step 9: Produce report

Write a Markdown report summarizing:

- number of spells changed
- number of cantrips promoted
- number of missing saves filled
- number of damage types filled
- number of conditions filled
- class access before and after
- level distribution before and after
- school distribution before and after
- spells still requiring manual review

## Manual review priority list

Codex should flag these categories for human review instead of silently rewriting them:

1. Any spell with permanent hostile effects.
2. Any spell with unclear target count.
3. Any spell with unclear area damage.
4. Any spell with repeatable damage and long duration.
5. Any spell involving resurrection, timeline change, identity rewrite, soul transfer, or possession.
6. Any spell whose flavour suggests story consequences beyond combat balance.
7. Any spell that appears to reference custom mechanics unavailable in the CSV.
8. Any spell with unusual duration formulas like `4d8 + 12 hours`.
9. Any spell assigned to Paladin or Ranger at 6th level or higher.
10. Any spell where `Class` and description strongly disagree.

## Acceptance criteria

The rebalanced CSV is acceptable when:

- Cantrip count is between 45 and 60, or every excess cantrip has a documented reason.
- Every damage spell has a damage type.
- Every save-based spell has Saving Throw, Success, and Fail populated.
- Every condition-bearing spell has Condition populated.
- Every hostile ongoing condition has a repeat save or a clear break condition.
- Every permanent hostile effect has at least three balancing constraints.
- Sorcerer access is reduced significantly from 250 unless manually justified.
- Druid, Artificer, and Ranger access are increased meaningfully.
- Casting time distribution includes more Bonus Action and Reaction spells.
- Concentration is applied consistently to persistent combat effects.
- All changes are documented in audit columns.
- A Markdown report explains the final balance state.

## Tone and design direction

Keep Orimond magic weird, evocative, and setting-specific. The goal is not to make every spell generic. The goal is to make each spell legible, comparable, and fair at the table.

A play-tested spell should answer these questions quickly:

1. What does it do?
2. Who can cast it?
3. What action does it take?
4. What does the target roll?
5. What happens on success?
6. What happens on failure?
7. How long does it last?
8. How does it end?
9. Why is it this spell level?
10. Why would a player choose it over another spell?

If those questions are clear, the spell will feel play-tested even before deeper campaign testing.
