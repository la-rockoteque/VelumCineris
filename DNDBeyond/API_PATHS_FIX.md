# API Paths Fix - Modifiers, Conditions, and Higher Levels

## Root Cause

**All modifiers, conditions, and higher-level scaling were failing to sync because the API endpoint paths were completely wrong.**

## The Problem

The code was using the long-form `/homebrew/creations/spells/...` paths, but D&D Beyond's actual API uses much shorter `/spells/...` paths.

### Wrong Paths (Before Fix)

```python
# Create endpoints
/homebrew/creations/spells/{spell_id}/modifiers/create
/homebrew/creations/spells/{spell_id}/conditions/create
/homebrew/creations/spells/{spell_id}/higher-levels/create

# Delete endpoints
/homebrew/creations/spells/{spell_id}/modifiers/{modifier_id}/delete
/homebrew/creations/spells/{spell_id}/conditions/{condition_id}/delete
/homebrew/creations/spells/{spell_id}/higher-levels/{level_id}/delete
```

### Correct Paths (After Fix)

```python
# Create endpoints
/spells/modifier/create/{spell_id}
/spells/condition/create/{spell_id}
/spells/additional/create/{spell_id}

# Delete endpoints
/spells/modifier/{modifier_id}/delete
/spells/condition/{condition_id}/delete
/spells/additional/{level_id}/delete
```

## Additional Fix

**Missing `primary-stat` field**: The modifier creation was also missing an optional `primary-stat` field that can be set to `"y"`. This has been added as an optional field.

## Expected Behavior

After this fix:
- **Modifiers** should sync successfully (AC, Attack, Damage, etc.)
- **Conditions** should sync successfully (status effects)
- **Higher Levels** should sync successfully (spell scaling at higher levels)

## How to Verify

Run Cell 14 in the notebook with:
```python
SYNC_CONDITIONS = True
SYNC_MODIFIERS = True
SYNC_HIGHER_LEVELS = True
ONLY_NEW_SPELLS = False
DRY_RUN_EXTRAS = False
CLEAN_UPDATE = True
```

Expected output:
```
[1/406] Processing: Spell Name (ID: 123456)
  → Adding 2 modifier(s)
    ✓ Created modifier
    ✓ Created modifier
```

Instead of:
```
    ✗ Failed to create modifier: HTTP 404: Not Found
```

## Files Changed

- `/Users/rocko/dev/Perso/VelumCineris/DNDBeyond/helpers/entities/spells.py`
  - Fixed `create_modifier()` - changed path and added `primary-stat` field
  - Fixed `create_condition()` - changed path
  - Fixed `create_higher_level()` - changed path
  - Fixed `delete_modifier()` - changed path
  - Fixed `delete_condition()` - changed path
  - Fixed `delete_higher_level()` - changed path

## Status Codes

- **302 Redirect** = Success (redirects to edit page with anchor)
- **404 Not Found** = Wrong path (what we were getting before)
- **400 Bad Request** = Missing/invalid field data

## Next Steps

1. Re-run Cell 14 to sync modifiers/conditions/scaling
2. Check the output for actual error messages (if any remain)
3. Verify in D&D Beyond that modifiers/conditions/scaling appear on the spell edit pages
4. Update spreadsheet tracking columns will show ✅ or ❌ with detailed error messages
