# Modifier Extraction with LLM - Complete Guide

## What's Been Implemented

You now have a complete LLM-powered modifier extraction system that can extract **multiple modifiers per spell** and sync them to D&D Beyond.

### New Features

1. **`Modifiers JSON` Column** - Stores all modifiers as JSON array
2. **Individual Modifier Columns** - Primary modifier for human readability
3. **LLM Extraction Script** - Uses Ollama/llama3 for accurate extraction
4. **Multi-Modifier Support** - Handles spells with multiple modifiers
5. **Sync Integration** - Ready to sync to D&D Beyond

---

## Step-by-Step Workflow

### 1. Extract Modifiers with LLM

Run the LLM-powered extraction:

```bash
cd /Users/rocko/dev/Perso/VelumCineris
poetry run python DNDBeyond/scripts/extract_modifiers_llm.py
```

**What it does:**
- Processes ~2-3 seconds per spell
- Extracts ALL modifiers from each spell description
- Stores them in both JSON format (all modifiers) and individual columns (primary modifier)
- Auto-saves progress every 10 spells
- Skips already-processed spells

**Expected results:**
- **Regex version** found: 20 modifiers (2%)
- **LLM version** expected: 40-60+ modifiers (5-10%)

**Options:**
```bash
# Use different model
poetry run python DNDBeyond/scripts/extract_modifiers_llm.py --model llama3

# Save more frequently (useful for testing)
poetry run python DNDBeyond/scripts/extract_modifiers_llm.py --batch-size 5

# Custom input file
poetry run python DNDBeyond/scripts/extract_modifiers_llm.py --input path/to/csv
```

---

### 2. Review Extracted Data

Open `DNDBeyond/Orimond.csv` and check the new columns:

**New Columns:**
- **Modifiers JSON** - All modifiers in JSON format (for sync)
- **Modifier Type** - Primary modifier type (for readability)
- **Modifier Subtype** - Ability score if applicable
- **Modifier Dice Count/Type** - Dice notation components
- **Modifier Fixed Value** - Fixed bonus/penalty
- **Modifier Duration/Unit** - How long it lasts

**Example JSON format:**
```json
[
  {
    "type": "1",
    "subtype": "",
    "dice_count": "",
    "dice_type": "",
    "fixed_value": "2",
    "duration": "",
    "duration_unit": "",
    "details": "gains a +2 bonus to AC"
  },
  {
    "type": "3",
    "subtype": "",
    "dice_count": "1",
    "dice_type": "6",
    "fixed_value": "",
    "duration": "",
    "duration_unit": "",
    "details": "deals an extra 1d6 fire damage"
  }
]
```

---

### 3. Update Sync Notebook

Replace **cell-14** in `DNDBeyond/dnd_beyond_spells.ipynb` with the code from:

```
DNDBeyond/sync_modifiers_cell.py
```

**Key changes:**
- Imports `extract_spell_modifiers`
- Adds `SYNC_MODIFIERS = True` configuration
- Creates modifiers via `ddb_api.create_modifier()`
- Tracks modifier creation count

**Configuration:**
```python
SYNC_CONDITIONS = True      # Sync conditions
SYNC_MODIFIERS = True       # NEW! Sync modifiers
SYNC_HIGHER_LEVELS = False  # Sync scaling
ONLY_NEW_SPELLS = False     # Process all or only new
DRY_RUN_EXTRAS = False      # False = actually create
```

---

### 4. Run the Sync

1. Open the notebook:
   ```bash
   poetry run jupyter notebook DNDBeyond/dnd_beyond_spells.ipynb
   ```

2. Run cells 1-13 to sync base spell data

3. Run cell-14 (the updated one) to sync modifiers

**What happens:**
- Reads `Modifiers JSON` column from each spell
- Parses the JSON array
- Creates **each modifier** as a separate API call
- Tracks success/errors
- Shows progress for each spell

**Example output:**
```
[1/406] Processing: Battle-Fury Ascension (ID: 3137528)
  → Found 2 modifier(s) to add
    ✓ Created modifier (AC +2)
    ✓ Created modifier (Damage 1d6)
[2/406] Processing: Duinir's Respite of Flames (ID: 3137xxx)
  → Found 1 modifier(s) to add
    ✓ Created modifier (Temp HP 2d4)
...
```

---

## Data Flow Diagram

```
Google Sheets (Orimond.csv)
    ↓
extract_modifiers_llm.py
    ↓
CSV with "Modifiers JSON" column
    ↓
FiveETools/core/fantasy/spells.py (reads CSV)
    ↓
DNDBeyond/helpers/converter.py (parses JSON)
    ↓
dnd_beyond_spells.ipynb cell-14
    ↓
DnDBeyondAPI.create_modifier() (for each)
    ↓
D&D Beyond Spell Page (multiple modifiers)
```

---

## Understanding the JSON Format

### Modifier Type IDs

| ID | Type | Description |
|----|------|-------------|
| 1 | AC | Armor Class bonus |
| 2 | Attack | Attack roll bonus |
| 3 | Damage | Damage bonus |
| 4 | Save | Saving throw bonus |
| 5 | Ability Check | Ability check bonus |
| 6 | Skill | Skill check bonus |
| 7 | Speed | Speed increase/decrease |
| 8 | Initiative | Initiative bonus |
| 9 | HP | Hit point bonus |
| 10 | Temp HP | Temporary hit points |

### Modifier Subtype IDs (for Saves/Checks)

| ID | Ability |
|----|---------|
| 1 | Strength |
| 2 | Dexterity |
| 3 | Constitution |
| 4 | Intelligence |
| 5 | Wisdom |
| 6 | Charisma |

### Duration Unit IDs

| ID | Unit |
|----|------|
| 1 | Rounds |
| 2 | Minutes |
| 3 | Hours |
| 4 | Days |
| (empty) | Spell duration |

---

## Example: Spell with Multiple Modifiers

**Spell:** "Warrior's Blessing"
**Description:** "The target gains a +2 bonus to AC and deals an extra 1d6 radiant damage for 1 hour."

**Extracted JSON:**
```json
[
  {
    "type": "1",
    "subtype": "",
    "dice_count": "",
    "dice_type": "",
    "fixed_value": "2",
    "duration": "1",
    "duration_unit": "3",
    "details": "+2 bonus to AC for 1 hour"
  },
  {
    "type": "3",
    "subtype": "",
    "dice_count": "1",
    "dice_type": "6",
    "fixed_value": "",
    "duration": "1",
    "duration_unit": "3",
    "details": "extra 1d6 radiant damage for 1 hour"
  }
]
```

**D&D Beyond Result:**
- Two separate modifier entries
- AC bonus: +2 for 1 hour
- Damage bonus: 1d6 for 1 hour

---

## Troubleshooting

### LLM Extraction Issues

**Problem:** "Model 'llama3.2' not found"
**Solution:** Use `--model llama3` or pull the model:
```bash
ollama pull llama3
```

**Problem:** LLM is slow
**Solution:**
- Use a smaller model (llama3.2 is faster than llama3)
- Reduce batch-size for more frequent saves
- Run overnight (30-50 minutes for 968 spells)

**Problem:** LLM extracts wrong modifier type
**Solution:**
- Review the extracted JSON in the CSV
- Manually correct the type ID
- The sync will use the corrected value

### Sync Issues

**Problem:** Modifiers not appearing on D&D Beyond
**Solution:**
- Check `SYNC_MODIFIERS = True`
- Check `DRY_RUN_EXTRAS = False`
- Verify spell has `Modifiers JSON` in CSV
- Check sync output for errors

**Problem:** "AttributeError: 'DnDBeyondAPI' object has no attribute 'create_modifier'"
**Solution:**
- Update your `DNDBeyond/helpers/DnDBeyondAPI.py`
- Make sure `create_modifier()` method exists
- Check the earlier conversation for the implementation

### Data Issues

**Problem:** JSON parsing error in sync
**Solution:**
- Check the JSON is valid in CSV
- Use a JSON validator
- Re-run extraction with LLM

**Problem:** Some spells missing modifiers
**Solution:**
- LLM might have missed complex descriptions
- Manually add to CSV:
  ```json
  [{"type": "1", "fixed_value": "2", "details": "bonus text"}]
  ```
- Or create a custom prompt for those spells

---

## Performance Comparison

| Aspect | Regex | LLM |
|--------|-------|-----|
| Speed | ~1 sec total | ~30-50 min total |
| Coverage | 20/968 (2%) | 40-60+/968 (5-10%) |
| Accuracy | Good for patterns | Excellent all-around |
| Multi-modifier | No | Yes |
| Complex descriptions | ❌ | ✅ |
| Setup | None | Ollama + model |

---

## Next Steps

1. **Run LLM extraction** (~30-50 minutes)
   ```bash
   poetry run python DNDBeyond/scripts/extract_modifiers_llm.py
   ```

2. **Review results** in `Orimond.csv`
   - Check `Modifiers JSON` column
   - Verify extracted data looks correct

3. **Update sync notebook**
   - Replace cell-14 with code from `sync_modifiers_cell.py`

4. **Run sync**
   - Test with `DRY_RUN_EXTRAS = True` first
   - Then run with `DRY_RUN_EXTRAS = False`

5. **Verify on D&D Beyond**
   - Check a few spells with multiple modifiers
   - Confirm all modifiers appear correctly

---

## Files Modified

- ✅ `DNDBeyond/scripts/extract_modifiers_llm.py` - NEW LLM extraction script
- ✅ `DNDBeyond/scripts/extract_modifiers.py` - Updated with JSON support
- ✅ `FiveETools/core/fantasy/spells.py` - Reads `Modifiers JSON` column
- ✅ `DNDBeyond/helpers/converter.py` - Parses JSON, returns all modifiers
- ✅ `DNDBeyond/helpers/__init__.py` - Exports `extract_spell_modifiers`
- ✅ `DNDBeyond/scripts/README.md` - Documentation updated
- 📝 `DNDBeyond/sync_modifiers_cell.py` - NEW cell code for notebook

---

## Questions?

If you need help with:
- Custom modifier extraction prompts
- Handling edge cases
- Debugging sync issues
- Adding more modifier types

Just ask!
