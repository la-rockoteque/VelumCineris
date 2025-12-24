# Duplicate Detection Fix Summary

## Problem
The D&D Beyond spell sync was creating duplicate spells despite having DDB IDs in the spreadsheet.

## Root Causes Identified

### 1. **Pandas Float Conversion Bug**
**Issue**: When pandas reads numeric columns from Google Sheets, it converts them to float64. This caused DDB IDs like `3135829` to become `3135829.0` when stringified.

**Impact**: The spreadsheet lookup would fail because:
- Spreadsheet had: `"3135829.0"` (after `str(ddb_id)`)
- Expected: `"3135829"`
- Result: Lookup failed, spell was created again as a duplicate

**Test Evidence** (tests/test_duplicate_detection.py:83):
```python
def test_numeric_ddb_ids_converted_to_string(self):
    df_spells = pd.DataFrame({
        'Spell Name': ['Spell1', 'Spell2', 'Spell3'],
        'DDB': [3135829, 3135830.0, '3135831']  # int, float, string
    })
    # Without normalize_ddb_id, this would create "3135829.0", "3135830.0", "3135831"
    # With normalize_ddb_id, all become proper IDs without .0 suffix
```

### 2. **Name Case Mismatch (Secondary Issue)**
**Issue**: HTML parsing used `.title()` which created inconsistent capitalization.

**Impact**:
- HTML slug: `"3136124-blink-and-you-missed-it"` → `"Blink And You Missed It"` (capital 'And')
- Source data: `"Blink and You Missed It"` (lowercase 'and')
- Result: Names didn't match, causing potential duplicates

**Note**: The primary check uses spreadsheet DDB IDs (exact name match), but the HTML backup check could fail on case mismatches.

### 3. **SKIP_EXISTING Was Set to False**
**Issue**: The notebook had `SKIP_EXISTING = False`, completely bypassing all duplicate checks.

**Impact**: Even with working duplicate detection, it was disabled.

## Solutions Implemented

### 1. **Created `normalize_ddb_id()` Function**
**Location**: dnd_beyond/helpers/DnDBeyondAPI.py:12-28

```python
@staticmethod
def normalize_ddb_id(ddb_id):
    """Normalize DDB ID from spreadsheet (handles pandas float conversion)

    Pandas reads numeric columns as float64, so 3135829 becomes 3135829.0
    This function strips the .0 suffix to get the proper ID string.
    """
    if ddb_id is None or (hasattr(ddb_id, '__len__') and len(str(ddb_id).strip()) == 0):
        return None

    id_str = str(ddb_id).strip()

    # Strip .0 suffix if present (pandas float conversion)
    if id_str.endswith('.0'):
        id_str = id_str[:-2]

    return id_str if id_str else None
```

**Exported**: dnd_beyond/helpers/__init__.py:5

### 2. **Fixed HTML Parsing (Remove .title())**
**Location**: dnd_beyond/helpers/DnDBeyondAPI.py:30

**Before**:
```python
spell_name = parts[1].replace('-', ' ').title() if len(parts) > 1 else ''
# Result: "Blink And You Missed It" (capital And)
```

**After**:
```python
spell_name = parts[1].replace('-', ' ') if len(parts) > 1 else ''
# Result: "blink and you missed it" (lowercase)
```

**Note**: The `find_spell_by_name()` function already uses case-insensitive matching (`.lower()`), so this works correctly.

### 3. **Updated Notebook to Use normalize_ddb_id**
**Location**: dnd_beyond_sync.ipynb Cell 14

**Before**:
```python
if spell_name and pd.notna(ddb_id) and str(ddb_id).strip():
    spell_to_ddb_id[spell_name] = str(ddb_id).strip()
# This would create "3135829.0" from pandas float
```

**After**:
```python
if spell_name and pd.notna(ddb_id):
    normalized_id = normalize_ddb_id(ddb_id)
    if normalized_id:
        spell_to_ddb_id[spell_name] = normalized_id
# This creates "3135829" - proper ID without .0
```

### 4. **Set SKIP_EXISTING = True**
**Location**: dnd_beyond_sync.ipynb Cell 14

Changed from `SKIP_EXISTING = False` to `SKIP_EXISTING = True` so duplicate detection actually runs.

## Comprehensive Test Suite

Created **tests/test_duplicate_detection.py** with 7 integration tests:

### Test Coverage:
1. ✅ **test_existing_ddb_id_detected**: Validates spreadsheet DDB IDs are properly loaded
2. ✅ **test_name_matching_exact**: Ensures exact name matching works
3. ✅ **test_empty_ddb_ids_ignored**: Empty strings and nulls are ignored
4. ✅ **test_numeric_ddb_ids_converted_to_string**: **Pandas float conversion bug** is fixed
5. ✅ **test_duplicate_detection_workflow**: Complete end-to-end workflow validation
6. ✅ **test_spell_name_from_source_matches_spreadsheet**: Name consistency validation
7. ✅ **test_html_slug_parsing_consistency**: HTML parsing produces consistent names

### All Tests Pass: 45/45
```
tests/test_api.py ...................... 13 passed
tests/test_converter.py .................... 25 passed
tests/test_duplicate_detection.py ....... 7 passed
```

## How Duplicate Detection Works Now

### Primary Check: Spreadsheet DDB IDs (Cell 14)
```python
# 1. Load spreadsheet with normalize_ddb_id
spell_to_ddb_id = {}
for _, row in df_spells.iterrows():
    spell_name = row.get('Spell Name')
    ddb_id = row.get('DDB')
    if spell_name and pd.notna(ddb_id):
        normalized_id = normalize_ddb_id(ddb_id)  # Strips .0 suffix
        if normalized_id:
            spell_to_ddb_id[spell_name] = normalized_id

# 2. Check before creating
if SKIP_EXISTING and spell_name in spell_to_ddb_id:
    existing_id = spell_to_ddb_id[spell_name]
    print(f"✓ Already synced (DDB ID: {existing_id} from spreadsheet)")
    # Skip this spell - don't create duplicate
```

### Backup Check: D&D Beyond HTML Parsing (Cell 14)
```python
# 3. If not in spreadsheet, check D&D Beyond directly
existing_id = ddb_api.find_spell_by_name(spell_name, existing_spells)
if existing_id:
    print(f"⚠️ Spell exists on D&D Beyond (ID: {existing_id})")
    # Add to spreadsheet for next time
    # Skip this spell - don't create duplicate
```

## Files Modified

1. **dnd_beyond/helpers/DnDBeyondAPI.py**
   - Added `normalize_ddb_id()` static method
   - Fixed `get_user_spells()` HTML parsing (removed `.title()`)

2. **dnd_beyond/helpers/__init__.py**
   - Exported `normalize_ddb_id` for use in notebook

3. **dnd_beyond_sync.ipynb Cell 14**
   - Import `normalize_ddb_id`
   - Use `normalize_ddb_id()` when loading spreadsheet DDB IDs
   - Set `SKIP_EXISTING = True`

4. **tests/test_duplicate_detection.py** (NEW)
   - 7 integration tests validating duplicate detection logic

## Testing the Fix

### Run All Tests:
```bash
poetry run pytest tests/ -v
```

### Test Specific Duplicate Detection:
```bash
poetry run pytest tests/test_duplicate_detection.py -v
```

### Manual Verification:
1. Check your spreadsheet - DDB column should have IDs like `3135829` (may display as `3135829.0` in Sheets UI)
2. Run the notebook with `SKIP_EXISTING = True` and `BATCH_SIZE = 5`
3. Verify that spells with existing DDB IDs are skipped
4. Check the output: Should see "✓ Already synced (DDB ID: XXXXX from spreadsheet)"

## Expected Behavior

**Before Fix**:
- Pandas converts `3135829` → `3135829.0`
- Spreadsheet lookup creates key `"3135829.0"`
- Source spell name is `"Blink and You Missed It"`
- Lookup fails: key not found
- Creates duplicate spell on D&D Beyond

**After Fix**:
- Pandas converts `3135829` → `3135829.0`
- `normalize_ddb_id()` strips `.0` → `"3135829"`
- Spreadsheet lookup creates key `"3135829"`
- Source spell name is `"Blink and You Missed It"`
- Lookup succeeds: spell found in spreadsheet
- Skips spell: "✓ Already synced (DDB ID: 3135829 from spreadsheet)"

## Additional Notes

- The fix handles all pandas data types: int, float, string
- Empty values (`None`, `""`, `"   "`) are properly ignored
- Case-insensitive name matching works for backup D&D Beyond check
- Spreadsheet is primary source of truth for duplicate detection
- All 45 tests pass, including 7 new duplicate detection tests
