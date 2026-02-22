# Google Sheets Mode - Direct Extraction

## Overview

The LLM extraction script can now read from and write directly to Google Sheets, eliminating the need for CSV export/import cycles.

**Benefits:**
- ✅ Single source of truth (no CSV sync needed)
- ✅ Auto-saves progress to Google Sheets
- ✅ Works with your existing Google Sheets workflow
- ✅ No manual CSV upload required

---

## Prerequisites

1. **Google Sheets credentials** (`credentials.json`)
   - Service account with Sheets API access
   - Already configured in your project

2. **Ollama** installed and running
   ```bash
   ollama list  # Check if llama3 is available
   ```

---

## Usage

### Basic Command (Google Sheets Mode)

```bash
poetry run python DNDBeyond/scripts/extract_modifiers_llm.py --google-sheets
```

**What it does:**
1. Reads spell data from Google Sheets (GID: 625265890)
2. Extracts modifiers using LLM
3. Writes results back to Google Sheets
4. Auto-saves progress every 10 spells

### Custom GID

If you want to use a different sheet:

```bash
poetry run python DNDBeyond/scripts/extract_modifiers_llm.py \
    --google-sheets \
    --gid 123456789
```

### Options

```bash
# Use different model
poetry run python DNDBeyond/scripts/extract_modifiers_llm.py \
    --google-sheets \
    --model llama3

# Save more frequently
poetry run python DNDBeyond/scripts/extract_modifiers_llm.py \
    --google-sheets \
    --batch-size 5

# Combine options
poetry run python DNDBeyond/scripts/extract_modifiers_llm.py \
    --google-sheets \
    --gid 625265890 \
    --model llama3 \
    --batch-size 10
```

---

## How It Works

### 1. Initial Read

The script:
- Connects to Google Sheets API
- Reads the entire sheet into memory
- Ensures modifier columns exist

### 2. Processing

For each spell:
- Extracts modifiers using LLM
- Stores in memory (DataFrame)
- Shows progress in console

### 3. Auto-Save (Every N Spells)

Every `batch-size` spells (default: 10):
- Updates all modifier columns in Google Sheets
- Uses batch updates for efficiency
- Shows progress per column

**Columns updated:**
- Modifiers JSON (all modifiers)
- Modifier Type (primary)
- Modifier Subtype
- Modifier Dice Count
- Modifier Dice Type
- Modifier Fixed Value
- Modifier Duration
- Modifier Duration Unit
- Modifier Details

---

## Example Output

```
✓ Google Sheets mode enabled
  GID: 625265890
✓ Ollama is running
Reading from Google Sheets (GID: 625265890)...
Loaded 968 rows
Using model: llama3

[1] Processing: Battle-Fury Ascension
  ✓ Found AC: +2 bonus to ac...
  ✓ Stored 2 total modifiers in JSON
      2. Damage: extra 1d6 damage...

[2] Processing: Duinir's Respite of Flames
  ✓ Found Temp HP: gains 2d4 temporary hit points...

...

[10] Processing: Spell Name
  ✓ Found AC: ...

💾 Saving progress to Google Sheets...
  ✓ Updated Modifiers JSON: 10 spells
  ✓ Updated Modifier Type: 10 spells
  ✓ Updated Modifier Subtype: 3 spells
  ✓ Updated Modifier Dice Count: 5 spells
  ✓ Updated Modifier Dice Type: 5 spells
  ✓ Updated Modifier Fixed Value: 5 spells
  ✓ Updated Modifier Duration: 2 spells
  ✓ Updated Modifier Duration Unit: 2 spells
  ✓ Updated Modifier Details: 10 spells
  ✓ Total spells updated: 10

...

💾 Saving final results to Google Sheets...
  ✓ Updated Modifiers JSON: 45 spells
  ✓ Updated Modifier Type: 45 spells
  ✓ Total spells updated: 45

✓ Complete!
  Total rows: 968
  Already processed (skipped): 923
  Newly processed: 45
  Modifiers found: 45
```

---

## Comparison: CSV vs Google Sheets Mode

| Aspect | CSV Mode | Google Sheets Mode |
|--------|----------|-------------------|
| Source | Local CSV file | Google Sheets |
| Write destination | Local CSV file | Google Sheets |
| Sync required | Yes (manual upload) | No (automatic) |
| Source of truth | Requires manual sync | Always current |
| Speed | Slightly faster | Slightly slower (API calls) |
| Offline | Works offline | Requires internet |
| Credentials | None | Requires credentials.json |

---

## Workflow Comparison

### CSV Mode Workflow (Old)
```
1. Export Google Sheets → Orimond.csv
2. Run extraction script → Updates Orimond.csv
3. Import Orimond.csv → Google Sheets
```

### Google Sheets Mode Workflow (New)
```
1. Run extraction script with --google-sheets
   (Reads + writes directly to Google Sheets)
2. Done! ✨
```

---

## Troubleshooting

### "Error: credentials.json not found"

**Solution:**
- Make sure `credentials.json` is in your project root
- Or set `GOOGLE_APPLICATION_CREDENTIALS` environment variable

### "Permission denied" errors

**Solution:**
- Check service account has edit access to the sheet
- Verify the sheet is shared with the service account email

### "Sheet not found" or "GID error"

**Solution:**
- Check the GID is correct (use `--gid` parameter)
- Verify the sheet exists in your Google Sheets

### Slow performance

**Solution:**
- This is normal - API calls take time
- Progress is auto-saved every 10 spells
- You can stop/resume anytime

---

## When to Use Each Mode

### Use CSV Mode When:
- ✅ Working offline
- ✅ Testing locally
- ✅ Want faster processing
- ✅ Don't have Google credentials set up

### Use Google Sheets Mode When:
- ✅ Want single source of truth
- ✅ Avoid manual CSV sync
- ✅ Working with team (shared sheet)
- ✅ Want auto-sync workflow

---

## Advanced: Resumable Processing

Google Sheets mode automatically resumes from where you left off:

1. Run the script
2. Stop it anytime (Ctrl+C)
3. Re-run with same command
4. Skips already-processed spells
5. Continues from where it left off

**Example:**
```bash
# First run (processes 50 spells, then you stop it)
poetry run python DNDBeyond/scripts/extract_modifiers_llm.py --google-sheets

# Resume later
poetry run python DNDBeyond/scripts/extract_modifiers_llm.py --google-sheets
# ✓ Skips the 50 already processed
# Continues with spell #51
```

---

## Full Example: End-to-End

```bash
# 1. Check Ollama is running
ollama list

# 2. Run extraction (Google Sheets mode)
cd /Users/rocko/dev/Perso/VelumCineris
poetry run python DNDBeyond/scripts/extract_modifiers_llm.py --google-sheets

# 3. Let it run (30-50 minutes for full extraction)
#    Progress auto-saved every 10 spells

# 4. Check Google Sheets
#    New columns populated with modifier data

# 5. Run D&D Beyond sync
poetry run jupyter notebook DNDBeyond/dnd_beyond_spells.ipynb
#    Modifiers automatically synced from Google Sheets
```

---

## Questions?

- How do I switch back to CSV mode? → Just omit `--google-sheets` flag
- Can I use both modes? → Yes, but choose one to avoid conflicts
- What if I stop mid-process? → Resume anytime, it skips processed spells
- Does it overwrite my data? → Only updates modifier columns

Ready to try it?

```bash
poetry run python DNDBeyond/scripts/extract_modifiers_llm.py --google-sheets
```
