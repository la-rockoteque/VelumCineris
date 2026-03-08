# Debugging Guide - Modifiers/Conditions/Scaling Sync

## Current Status

**Problems:**
1. ❌ DDB IDs not being updated in spreadsheet for new spells
2. ❌ All modifiers, conditions, and scaling still failing
3. ❌ Error messages still not helpful enough

**Fixes Applied:**
- ✅ Fixed API paths (from `/homebrew/creations/spells/...` to `/spells/...`)
- ✅ Added debug logging to see actual requests and responses
- ✅ Updated Cell 14 with improved error display

## Step-by-Step Debugging

### Step 1: Check DDB IDs in Spreadsheet

Run this command to see which spells are missing DDB IDs:
```bash
poetry run python DNDBeyond/check_ddb_ids.py
```

**Expected output:**
```
Spells WITH DDB IDs:    391
Spells WITHOUT DDB IDs: 15
```

If you have spells without IDs but Cell 13 said it created them:
- Check Cell 13 output for spreadsheet update errors
- Verify the spell names match exactly between notebook and spreadsheet
- Check if there are special characters or trailing spaces in names

### Step 2: Re-run Cell 13 (Base Spell Sync)

**Before running:**
1. Set configuration:
   ```python
   DRY_RUN = False
   SKIP_EXISTING = False
   UPDATE_EXISTING = True  # This will update existing spells
   VERBOSE = True
   ```

2. Run Cell 13 and watch for:
   ```
   ✓ Updated sync status for X spells
   ✓ Updated X/Y spells in spreadsheet
   ```

3. If you see errors like:
   ```
   ⚠️  Failed to update N spells:
     - Spell Name
   ```
   This means those spell names in the notebook don't match the spreadsheet.

### Step 3: Run Cell 14 with Debug Logging

**Before running:**
1. Set configuration:
   ```python
   SYNC_CONDITIONS = True
   SYNC_MODIFIERS = True
   SYNC_HIGHER_LEVELS = True
   ONLY_NEW_SPELLS = False  # Process ALL spells
   DRY_RUN_EXTRAS = False
   CLEAN_UPDATE = True
   ```

2. Run Cell 14 and look for DEBUG output:
   ```
   [1/406] Processing: Spell Name (ID: 123456)
     → Adding 2 modifier(s)
       DEBUG: POST /spells/modifier/create/123456
       DEBUG: Form data: {'spell-modifier-type': '3', ...}
       DEBUG: Response status: 302
       ✓ Created modifier
   ```

3. If you see errors, the DEBUG output will show:
   ```
       DEBUG: Response status: 400
       DEBUG: Response body: <html>Error: Missing required field...</html>
       ✗ Failed to create modifier: HTTP 400: Bad Request | <html>Error...
   ```

### Step 4: Analyze the Error Messages

**Common errors and their meanings:**

| Status Code | Meaning | Solution |
|------------|---------|----------|
| 302/303 | Success (redirect) | Good! |
| 400 | Bad Request - Invalid field data | Check the form data in DEBUG output |
| 401 | Unauthorized - Session expired | Update cookies and tokens in .env |
| 404 | Not Found - Wrong path | Check API path is correct |
| 500 | Server error | D&D Beyond issue, try again later |

**If you see 404 errors:**
The API path is still wrong. Check the DEBUG output:
```
DEBUG: POST /spells/modifier/create/123456
DEBUG: Response status: 404
```
→ The path should be `/spells/modifier/create/{spell_id}` (which it is)
→ If still 404, the spell ID might be invalid

**If you see 400 errors:**
Missing or invalid field data. Check the form data:
```
DEBUG: Form data: {'spell-modifier-type': '', 'spell-modifier-sub-type': '', ...}
```
→ Empty fields might be the problem
→ Compare with working request in `/DNDBeyond/core/requests/spell.update.modifier.create.request.txt`

**If you see 401 errors:**
Your session has expired. Update `.env` file:
1. Go to D&D Beyond in your browser
2. Open DevTools → Network → Copy cookies
3. Update `DDB_COOKIES`, `DDB_SECURITY_TOKEN`, `DDB_AUTHENTICITY_TOKEN`

### Step 5: Compare with Working Request

Look at the actual working request captured:
```bash
cat DNDBeyond/core/requests/spell.update.modifier.create.request.txt
```

Compare with the DEBUG output from Cell 14:
- Are all the same fields present?
- Are the field names exactly the same?
- Are the values in the correct format (strings, not empty)?

### Step 6: Test One Spell Manually

If debugging is hard, test with just one spell:
```python
# In Cell 14, add at the top:
spell_data_map = {k: v for k, v in spell_data_map.items() if k == "Ashen Breath"}
```

Then run Cell 14 and watch the DEBUG output closely for that one spell.

## Quick Checks

### ✅ Verify API Paths Are Correct

```bash
poetry run python DNDBeyond/test_api_paths.py
```

This shows what the paths SHOULD be.

### ✅ Verify Spells Have Modifier Data

Check if your spells actually have modifiers to sync:
```python
from FiveETools.core.fantasy.spells import spells_list
from DNDBeyond.helpers import extract_spell_modifiers

for spell in spells_list[:5]:
    mods = extract_spell_modifiers(spell)
    if mods:
        print(f"{spell['name']}: {len(mods)} modifiers")
        print(f"  {mods[0]}")
```

If no modifiers are extracted, the problem is in the extraction, not the sync.

## Expected Successful Output

When everything works, Cell 14 should show:
```
[1/406] Processing: Abhaaldrac's Unmaking Descent (ID: 3137383)
  → Adding 2 modifier(s)
    DEBUG: POST /spells/modifier/create/3137383
    DEBUG: Form data: {'spell-modifier-type': '3', 'spell-modifier-sub-type': '68', ...}
    DEBUG: Response status: 302
    ✓ Created modifier
    DEBUG: POST /spells/modifier/create/3137383
    DEBUG: Form data: {'spell-modifier-type': '1', 'spell-modifier-sub-type': '5', ...}
    DEBUG: Response status: 302
    ✓ Created modifier

============================================================
EXTRAS SYNC COMPLETE
============================================================
✓ Created: 812 modifiers, 15 conditions, 103 higher levels
✗ Errors: 0
============================================================
```

## Still Having Issues?

If after all this the sync is still failing:

1. **Copy the DEBUG output** for one failing spell
2. **Copy the sync log** from the JSON file
3. **Share both** so we can see:
   - What's being sent (form data)
   - What's being returned (response status + body)
   - Which specific fields might be wrong

The DEBUG output is the key to figuring this out! 🔍
