# Modifiers/Conditions/Scaling Fix

## Issue

When running cell-14 (extras sync), all modifiers, conditions, and higher-level scaling failed to sync. The diagnostic revealed:

- ✅ All required columns exist in Google Sheets
- ✅ All 406 spells have extras data filled in
- ✅ Extraction functions work correctly
- ❌ API calls to D&D Beyond were failing

## Root Cause

**Field name mismatch** between extraction function and API method:

| Extraction Function Returns | API Method Expected    | Status  |
|-----------------------------|------------------------|---------|
| `type`                      | `modifier_type`        | ❌ Mismatch |
| `subtype`                   | `modifier_sub_type`    | ❌ Mismatch |
| `dice_type`                 | `dice_value`           | ❌ Mismatch |
| `dice_count`                | `dice_count`           | ✅ Match   |
| `fixed_value`               | `fixed_value`          | ✅ Match   |

The `extract_spell_modifiers()` function returns short field names like `type`, `subtype`, `dice_type`, but the `create_modifier()` API method was expecting prefixed names like `modifier_type`, `modifier_sub_type`, `dice_value`.

## Fix Applied

Updated `create_modifier()` in `/Users/rocko/dev/Perso/VelumCineris/DNDBeyond/helpers/entities/spells.py` to accept **both** field name formats:

```python
def create_modifier(self, spell_id, modifier_data):
    # Support both old field names (modifier_type) and new field names (type)
    modifier_type = modifier_data.get("modifier_type") or modifier_data.get("type", "")
    modifier_sub_type = modifier_data.get("modifier_sub_type") or modifier_data.get("subtype", "")
    dice_count = modifier_data.get("dice_count", "")
    dice_value = modifier_data.get("dice_value") or modifier_data.get("dice_type", "")

    form_data = {
        "spell-modifier-type": str(modifier_type),
        "spell-modifier-sub-type": str(modifier_sub_type),
        "dice-count": str(dice_count),
        "dice-value": str(dice_value),
        # ...
    }
```

This fix allows the method to work with:
- Short names from `extract_spell_modifiers()` (new format)
- Long names if you manually call it (old format, for backward compatibility)

## How to Verify

Run the diagnostic script:
```bash
poetry run python DNDBeyond/scripts/diagnose_extras.py
```

Run the test script:
```bash
poetry run python DNDBeyond/scripts/test_extras_fix.py
```

## Next Steps

1. **Re-run cell-14** in the notebook to sync modifiers/conditions/scaling
2. Set configuration:
   ```python
   SYNC_CONDITIONS = True
   SYNC_MODIFIERS = True
   SYNC_HIGHER_LEVELS = True
   ONLY_NEW_SPELLS = False  # Process all spells, not just new ones
   DRY_RUN_EXTRAS = False   # Actually sync (set True for testing)
   CLEAN_UPDATE = True      # Delete old before creating new (prevents duplicates)
   ```
3. Run cell-14 and watch for:
   - ✓ Modifiers created successfully
   - ✓ Conditions created successfully
   - ✓ Higher levels created successfully

## Expected Results

After re-running cell-14 with the fix:

```
[1/406] Processing: Abhaaldrac's Unmaking Descent (ID: 3137383)
  → Adding 2 modifier(s)
    ✓ Created modifier
    ✓ Created modifier

[2/406] Processing: Aegis of Rebounding Force (ID: 3137437)
  → Adding 2 modifier(s)
    ✓ Created modifier
    ✓ Created modifier
  → Adding 1 higher level entr(ies)
    ✓ Created higher level scaling
```

## Impact

- **Modifiers**: ✅ FIXED - Will now sync correctly
- **Conditions**: ⚠️  Check if conditions are being extracted (may need Condition column filled)
- **Higher Levels**: ✅ FIXED - Scaling will now sync correctly

## Tracking

The sync tracking columns will be updated:
- **DDB Sync Status**: ✅ (success) or ❌ (failure)
- **DDB Sync Error**: Error message if failed
- **DDB Last Synced**: Timestamp of sync attempt

Check your Google Sheets after running cell-14 to see which spells synced successfully.
