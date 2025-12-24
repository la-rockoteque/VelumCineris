# Spell Updates Integration Guide

## Overview

D&D Beyond spell creation is a two-phase process:
1. **Create** spell with basic information
2. **Update** spell with additional details (AOE, save, attack, higher level, modifiers, conditions)

## New API Methods

### 1. `update_basic_information(spell_id, slug, data)`
Updates core spell info with additional fields not available during creation.

**Additional fields**:
- `aoe_type`: Area of effect type ("1"=Cone, "2"=Cube, "3"=Cylinder, "4"=Line, "5"=Sphere)
- `aoe_size`: Size in feet (e.g., "15", "20")
- `attack_type`: Attack type ("1"=Ranged spell attack, "2"=Melee spell attack)
- `save_type`: Saving throw ability ("1"=STR, "2"=DEX, "3"=CON, "4"=INT, "5"=WIS, "6"=CHA)
- `on_miss`: What happens on a miss (free text)
- `save_success`: What happens on successful save (free text)
- `save_fail`: What happens on failed save (free text)

### 2. `create_higher_level(spell_id, level_data)`
Adds higher level scaling information.

**Fields**:
- `level`: Specific level or "" for per-slot scaling
- `modifier`: Modifier ID or ""
- `effect_type`: "16" for damage, other values for healing, temporary HP, etc.
- `dice_count`: Number of dice (e.g., "1")
- `dice_value`: Die type (e.g., "8" for d8)
- `dice_fixed`: Fixed bonus (e.g., "3")
- `dice_details`: Damage type or description (e.g., "fire")

### 3. `create_modifier(spell_id, modifier_data)`
Adds stat bonuses, temporary effects, etc.

**Fields**:
- `modifier_type`: Type of modifier (e.g., "3" for bonus)
- `modifier_sub_type`: Sub-type (e.g., "68" for AC)
- `dice_count`, `dice_value`, `fixed_value`: Modifier amount
- `duration`, `duration_unit`: How long it lasts

### 4. `create_condition(spell_id, condition_data)`
Adds conditions like blinded, charmed, frightened, etc.

**Fields**:
- `condition_effect`: "1" for grants condition, "2" for removes condition
- `condition`: Condition ID (e.g., "1" for Blinded)
- `condition_duration`: Duration amount
- `duration_unit`: Duration unit ID
- `condition_exception`: Exception text

### 5. `create_slug(spell_name)` (static method)
Creates URL-safe slug from spell name (e.g., "Ashen Breath" → "ashen-breath")

## Converter Updates

The converter now extracts these additional fields from 5etools format:

### AOE Detection
```python
# From range.type
{"range": {"type": "cone", "distance": {"type": "feet", "amount": 15}}}
# Extracts: aoe_type="1" (Cone), aoe_size="15"
```

### Save Type Detection
```python
# From description text
"The target must make a Constitution saving throw."
# Extracts: save_type="3" (Constitution)
```

### Attack Type Detection
```python
# From description text
"Make a ranged spell attack against the target."
# Extracts: attack_type="1" (Ranged spell attack)
```

## Integration Example

### Basic Integration (Minimal)

Add this after spell creation in the notebook:

```python
spell_id = ddb_api.create_spell(ddb_data)

if spell_id:
    print(f"  ✓ Created: ID {spell_id}")

    # Create slug for updates
    slug = DnDBeyondAPI.create_slug(spell_name)

    # Update with additional fields (AOE, save, attack)
    if VERBOSE:
        print(f"  → Updating additional fields...")

    updated = ddb_api.update_basic_information(spell_id, slug, ddb_data)

    if updated and VERBOSE:
        print(f"    ✓ Additional fields updated")
    elif not updated:
        print(f"    ⚠️  Warning: Could not update additional fields")

    # Rest of existing code...
```

### Full Integration (with higher level, modifiers, conditions)

```python
spell_id = ddb_api.create_spell(ddb_data)

if spell_id:
    print(f"  ✓ Created: ID {spell_id}")
    print(f"    URL: {DDB_BASE_URL}/homebrew/creations/spells/{spell_id}")

    # Create slug for updates
    slug = DnDBeyondAPI.create_slug(spell_name)

    # 1. Update basic information with additional fields
    if VERBOSE:
        print(f"  → Updating additional fields...")

    updated = ddb_api.update_basic_information(spell_id, slug, ddb_data)

    if updated and VERBOSE:
        print(f"    ✓ Additional fields updated (AOE: {ddb_data.get('aoe_type', 'none')}, Save: {ddb_data.get('save_type', 'none')}, Attack: {ddb_data.get('attack_type', 'none')})")
    elif not updated:
        print(f"    ⚠️  Warning: Could not update additional fields")

    # 2. Add higher level scaling if applicable
    if ddb_data.get("can_cast_at_higher_level"):
        if VERBOSE:
            print(f"  → Adding higher level scaling...")

        # Example: adds 1d8 damage per slot level above base
        higher_level_data = {
            "level": "",  # Per slot level
            "modifier": "",
            "effect_type": "16",  # Damage
            "dice_count": "1",
            "dice_value": "8",
            "dice_fixed": "",
            "dice_details": "fire"  # Or extract from spell data
        }

        hl_created = ddb_api.create_higher_level(spell_id, higher_level_data)

        if hl_created and VERBOSE:
            print(f"    ✓ Higher level scaling added")
        elif not hl_created:
            print(f"    ⚠️  Warning: Could not add higher level scaling")

    # 3. (Optional) Add modifiers if any
    # modifiers = extract_modifiers(spell)  # Implement based on your data
    # for mod in modifiers:
    #     ddb_api.create_modifier(spell_id, mod)

    # 4. (Optional) Add conditions if any
    # conditions = extract_conditions(spell)  # Implement based on your data
    # for cond in conditions:
    #     ddb_api.create_condition(spell_id, cond)

    # Add to spreadsheet update queue
    spreadsheet_updates.append({
        'match_value': spell_name,
        'update_column': 'DDB',
        'update_value': spell_id
    })

    results["created"] += 1
    results["details"].append({
        "title": spell_name,
        "action": "created",
        "success": True,
        "id": spell_id
    })

    # Add to existing list for subsequent checks
    existing_spells.append({"name": spell_name, "id": spell_id})
```

## Testing

### Run All Tests
```bash
poetry run pytest tests/ -v
```

**Expected**: 58 tests pass (45 original + 13 new)

### Test Categories
- **API Tests** (18 total):
  - 13 original tests (form data, response handling, spell lookup)
  - 5 new tests (update_basic_information, create_higher_level, create_modifier, create_condition, create_slug)

- **Converter Tests** (33 total):
  - 25 original tests (school, range, duration, components, classes, higher level)
  - 8 new tests (AOE extraction, save type detection, attack type detection)

- **Duplicate Detection Tests** (7 total):
  - All passing

## Field Mappings Reference

### AOE Types
- 1 = Cone
- 2 = Cube
- 3 = Cylinder
- 4 = Line
- 5 = Sphere/Radius

### Save Types
- 1 = Strength
- 2 = Dexterity
- 3 = Constitution
- 4 = Intelligence
- 5 = Wisdom
- 6 = Charisma

### Attack Types
- 1 = Ranged spell attack
- 2 = Melee spell attack

### Effect Types (for higher level)
- 16 = Damage
- (Other values for healing, temporary HP, etc. - check D&D Beyond UI)

### Condition Effects
- 1 = Grants condition
- 2 = Removes condition

## Notes

- **Rate Limiting**: Add delays between update requests if syncing many spells
- **Error Handling**: Updates return `True` on success (303 redirect), `False` on failure
- **Slug Generation**: Use `DnDBeyondAPI.create_slug()` to create URL-safe slugs
- **Optional Fields**: Modifiers and conditions are optional - only add if your spell data includes them
- **Manual Entry**: Some fields (on_miss, save_success, save_fail) may need manual entry as they're not in 5etools format

## Example Spell Data Flow

**5etools Format**:
```json
{
  "name": "Ashen Breath",
  "level": 0,
  "school": "V",
  "range": {"type": "cone", "distance": {"type": "feet", "amount": 15}},
  "entries": ["Creatures in the area must make a Constitution saving throw."]
}
```

**Converted to D&D Beyond**:
```python
{
  "name": "Ashen Breath",
  "level": 0,
  "school_id": 7,  # Evocation
  "aoe_type": "1",  # Cone
  "aoe_size": "15",
  "save_type": "3",  # Constitution
  # ... other fields
}
```

**API Calls**:
1. `create_spell(data)` → Returns spell_id
2. `update_basic_information(spell_id, "ashen-breath", data)` → Updates AOE, save
3. (Optional) `create_higher_level(spell_id, {...})` → Adds scaling
4. (Optional) `create_modifier(spell_id, {...})` → Adds bonuses
5. (Optional) `create_condition(spell_id, {...})` → Adds conditions

## Files Modified

- `dnd_beyond/helpers/DnDBeyondAPI.py`: Added 5 new methods
- `dnd_beyond/helpers/converter.py`: Added AOE, save, attack extraction
- `tests/test_api.py`: Added 5 new tests for update endpoints
- `tests/test_converter.py`: Added 8 new tests for additional fields

**Total**: 58 tests passing (100% pass rate)
