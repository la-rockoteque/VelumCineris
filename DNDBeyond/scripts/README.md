# D&D Beyond Scripts

Utility scripts for automating D&D Beyond authentication and token management.

## Token Extractor (`get_ddb_tokens.py`)

Automatically extracts cookies and security tokens from D&D Beyond using browser automation, eliminating the need to manually copy them from browser DevTools.

### Prerequisites

1. **Install Playwright browsers** (one-time setup):
   ```bash
   poetry run playwright install chromium
   ```

2. **Set credentials** (choose one method):

   **Option A: Environment variables (recommended)**
   ```bash
   export DDB_EMAIL='your-email@example.com'
   export DDB_PASSWORD='your-password'
   ```

   **Option B: Interactive prompt** (no arguments needed)

### Usage

#### Basic Usage (Recommended)
```bash
# With environment variables set
poetry run python DNDBeyond/scripts/get_ddb_tokens.py
```

#### Interactive Mode
```bash
# Will prompt for email and password
poetry run python DNDBeyond/scripts/get_ddb_tokens.py
```

#### Headless Mode
```bash
# No browser window (faster, but harder to debug)
poetry run python DNDBeyond/scripts/get_ddb_tokens.py --headless
```

#### Advanced Options
```bash
# Print tokens instead of saving to file
poetry run python DNDBeyond/scripts/get_ddb_tokens.py --print-only

# Save to custom location
poetry run python DNDBeyond/scripts/get_ddb_tokens.py --output /path/to/.env

# Pass credentials as arguments (NOT RECOMMENDED - stays in shell history)
poetry run python DNDBeyond/scripts/get_ddb_tokens.py \
    --email your-email@example.com \
    --password your-password
```

### What It Does

1. 🌐 Opens a Chromium browser
2. 🔐 Logs into your D&D Beyond account
3. 🍪 Extracts session cookies
4. 🎫 Navigates to the spell creation page
5. 🔑 Extracts security tokens from the form
6. 💾 Saves everything to `DNDBeyond/.env`

### Output

The script creates/updates `DNDBeyond/.env` with:
```bash
DDB_BASE_URL="https://www.dndbeyond.com"
DDB_COOKIES="CobaltSession=...; __cf_bm=...; ..."
DDB_SECURITY_TOKEN="bf877cec19a71926736b4fc2826c3d9f"
DDB_AUTHENTICITY_TOKEN="a1b2c3d4e5f6..."
REQUEST_VERIFICATION_TOKEN="xyz123..."
DDB_USER_ID="110746825"
DDB_USERNAME="YourUsername"
```

### When to Use

Run this script whenever:
- 🆕 Setting up D&D Beyond sync for the first time
- ⚠️ Sync notebooks report "authentication failed"
- 🕐 Tokens have expired (typically every few days/weeks)
- 🔄 You've logged out and back in to D&D Beyond

### Security Notes

⚠️ **Important Security Reminders:**

1. **Never commit `.env` file** - Make sure it's in `.gitignore`
2. **Use environment variables** - Don't pass credentials as command-line arguments
3. **Tokens are sensitive** - Treat them like passwords
4. **Regular rotation** - Tokens expire; this is a security feature
5. **Secure storage** - The `.env` file contains your session credentials

### Troubleshooting

#### "playwright not installed"
```bash
poetry run playwright install chromium
```

#### "Login failed"
- Check your email/password are correct
- Try running without `--headless` to see what's happening
- Make sure you don't have 2FA enabled (not currently supported)

#### "Tokens not found"
- D&D Beyond may have changed their HTML structure
- Run without `--headless` to debug
- Check if you can manually access the create spell page

#### Browser opens but nothing happens
- Check your internet connection
- D&D Beyond may be down or slow
- Try running again with a longer timeout

### Example Workflow

```bash
# 1. First time setup
poetry run playwright install chromium

# 2. Set credentials
export DDB_EMAIL='your-email@example.com'
export DDB_PASSWORD='your-password'

# 3. Extract tokens
poetry run python DNDBeyond/scripts/get_ddb_tokens.py

# 4. Use the sync notebooks
poetry run jupyter notebook DNDBeyond/dnd_beyond_spells.ipynb
```

### Help

```bash
poetry run python DNDBeyond/scripts/get_ddb_tokens.py --help
```

---

## Scaling Extractor (`extract_scaling.py`)

Extracts scaling information from the "Scaling" column into separate structured columns for D&D Beyond sync.

### Usage

```bash
poetry run python DNDBeyond/scripts/extract_scaling.py
```

### What It Does

Parses the "Scaling" column and creates these new columns:

- **Scaling Level** - The spell level where scaling applies (e.g., "3", "5")
- **Scaling Modifier** - Additional modifier text
- **Scaling Effect** - Effect type ID (16=Damage, 9=Healing, 10=Temp HP)
- **Scaling Dice Count** - Number of dice (e.g., "2", "3")
- **Scaling Dice Type** - Dice type without 'd' (e.g., "6", "8", "10")
- **Fixed Value** - Fixed bonus (e.g., "3", "5")

### Supported Formats

**1. Structured Format (Recommended):**
```
3:2d6,5:3d6,7:4d6,9:5d6
```
This creates precise scaling entries for each level.

**2. Natural Language:**
```
The damage increases by 1d6 for each slot level above 1st
Add 2d8 fire damage at 5th level, and 3d8 at 9th level
Healing increases by 1d8 per spell level
```
The script will extract the first dice pattern found.

**3. Simple Dice Notation:**
```
2d6
3d8+5
1d10
```

### Output

Creates `DNDBeyond/Orimond_with_scaling.csv` with the new columns added.

### Examples

**Example 1: Natural Language**
```
Input:  "The damage increases by 1d6 for each slot level above 1st"
Output:
  Scaling Level: 1
  Scaling Dice Count: 1
  Scaling Dice Type: 6
  Scaling Effect: 16 (Damage)
```

**Example 2: Structured Format**
```
Input:  "3:2d6,5:3d6,7:4d6"
Output: (creates entry for first level)
  Scaling Level: 3
  Scaling Dice Count: 2
  Scaling Dice Type: 6
  Scaling Effect: 16 (Damage)
```

**Example 3: With Fixed Bonus**
```
Input:  "5:3d8+5"
Output:
  Scaling Level: 5
  Scaling Dice Count: 3
  Scaling Dice Type: 8
  Fixed Value: 5
  Scaling Effect: 16 (Damage)
```

### Effect Type IDs

The script automatically detects the effect type:

- `9` - Healing (detected from keywords: "heal", "healing", "hit point")
- `10` - Temporary Hit Points (detected from: "temp", "temporary")
- `16` - Damage (default for all other cases)

### Workflow

1. **Run the extraction:**
   ```bash
   poetry run python DNDBeyond/scripts/extract_scaling.py
   ```

2. **Review the output:**
   - Check `DNDBeyond/Orimond_with_scaling.csv`
   - Verify the extracted columns are correct

3. **Update Google Sheets:**
   - Import the new columns into your Google Sheets
   - Or manually copy the extracted values

4. **Update FiveETools:**
   - Re-export from Google Sheets if needed
   - The sync will automatically use the new structured columns

### Statistics

After running, the script shows:
- Total rows processed
- Number of spells with scaling data
- Successfully extracted entries
- Breakdown of dice types used (d4, d6, d8, etc.)

### Troubleshooting

**"Error: 'Scaling' column not found"**
- Make sure you're using the correct CSV file
- Check that the column is named exactly "Scaling"

**"No scaling data extracted"**
- Check the format of your Scaling column
- Use one of the supported formats listed above
- For structured format, use: `level:dice,level:dice`

**"Output file already exists"**
- The script will overwrite `Orimond_with_scaling.csv`
- Back up the old file if needed

---

## Modifier Extractor (`extract_modifiers.py` / `extract_modifiers_llm.py`)

Extracts modifier information from spell descriptions into structured columns for D&D Beyond sync.

**Two versions available:**
- **`extract_modifiers.py`** - Fast regex-based extraction (good for simple, common patterns)
- **`extract_modifiers_llm.py`** - LLM-powered extraction (more accurate, handles complex descriptions)

### Basic Usage (Regex)

```bash
poetry run python DNDBeyond/scripts/extract_modifiers.py
```

### LLM Usage (Recommended)

**Prerequisites:**
1. Ollama is already installed ✓
2. Model `llama3` is available ✓

**Run extraction:**
```bash
# Default (uses llama3 model)
poetry run python DNDBeyond/scripts/extract_modifiers_llm.py

# Use different model
poetry run python DNDBeyond/scripts/extract_modifiers_llm.py --model llama3.2

# Save progress every 5 spells (useful for testing)
poetry run python DNDBeyond/scripts/extract_modifiers_llm.py --batch-size 5
```

### Why Use LLM?

The LLM version provides significantly better results:

**Regex version:**
- ✓ Fast (processes all spells in seconds)
- ✓ No dependencies
- ✗ Misses complex or unusual phrasings
- ✗ Struggles with compound modifiers
- ✗ Can't understand context

**LLM version:**
- ✓ Understands natural language
- ✓ Handles complex/unusual descriptions
- ✓ Can extract multiple modifiers per spell
- ✓ Better at determining modifier types
- ✗ Slower (1-2 seconds per spell)
- ✗ Requires Ollama + model download

**Recommendation:** Use LLM version for initial extraction, then use regex version for incremental updates.

### What It Does

Parses spell descriptions and extracts these modifier columns:

- **Modifier Details** - Text snippet that matched the pattern
- **Modifier Type** - Effect type ID (1=AC, 2=Attack, 3=Damage, 4=Save, 7=Speed, 10=Temp HP)
- **Modifier Subtype** - Ability score for saves/checks (1=STR, 2=DEX, 3=CON, 4=INT, 5=WIS, 6=CHA)
- **Modifier Dice Count** - Number of dice (e.g., "1", "2", "3")
- **Modifier Dice Type** - Dice type without 'd' (e.g., "4", "6", "8")
- **Modifier Fixed Value** - Fixed bonus (e.g., "+2", "+5")
- **Modifier Duration** - Duration amount (e.g., "1", "10", "24")
- **Modifier Duration Unit** - Duration unit ID (1=rounds, 2=minutes, 3=hours, 4=days)

### Supported Patterns

**1. AC Bonuses:**
```
"gains a +2 bonus to AC"
"AC increases by 3"
"+1 to armor class"
```

**2. Attack Roll Bonuses:**
```
"+1 to attack rolls"
"bonus to hit equal to +2"
"attack rolls increase by 1d4"
```

**3. Damage Bonuses:**
```
"deals an extra 1d6 damage"
"additional 2d8 fire damage"
"bonus 3d10 damage"
```

**4. Saving Throw Bonuses:**
```
"+2 bonus to Dexterity saving throws"
"advantage on Wisdom saves"
"Constitution saves increase by 1d4"
```

**5. Speed Bonuses:**
```
"speed increases by 10 feet"
"gain 20 feet of movement"
```

**6. Temporary Hit Points:**
```
"gains 5 temporary hit points"
"1d8 temporary hp"
"2d6+3 temp hp"
```

### Output

Updates `DNDBeyond/Orimond.csv` in place with populated modifier columns.

### Examples

**Example 1: AC Bonus**
```
Input:  "Battle-Fury Ascension" - "...+2 bonus to AC..."
Output:
  Modifier Type: 1 (AC)
  Modifier Fixed Value: 2
  Modifier Details: "+2 bonus to ac"
```

**Example 2: Damage Bonus**
```
Input:  "Eyes Behind the Kiss" - "...extra 1d6 chiaric damage for 24 hours..."
Output:
  Modifier Type: 3 (Damage)
  Modifier Dice Count: 1
  Modifier Dice Type: 6
  Modifier Duration: 24
  Modifier Duration Unit: 3 (hours)
```

**Example 3: Temporary HP**
```
Input:  "Duinir's Respite of Flames" - "...gains 2d4 temporary hit points..."
Output:
  Modifier Type: 10 (Temp HP)
  Modifier Dice Count: 2
  Modifier Dice Type: 4
```

### Modifier Type IDs

The script automatically detects the modifier type:

- `1` - Armor Class (AC)
- `2` - Attack Roll
- `3` - Damage
- `4` - Saving Throw
- `5` - Ability Check
- `6` - Skill Check
- `7` - Speed
- `8` - Initiative
- `9` - Hit Points
- `10` - Temporary Hit Points

### Duration Unit IDs

- `1` - Rounds
- `2` - Minutes
- `3` - Hours
- `4` - Days

### Workflow

1. **Run the extraction:**
   ```bash
   poetry run python DNDBeyond/scripts/extract_modifiers.py
   ```

2. **Review the output:**
   - Check the console output for examples
   - Verify extracted modifiers are correct
   - Statistics show breakdown by modifier type

3. **Use in sync:**
   - The D&D Beyond sync notebooks will automatically use these columns
   - Modifiers are synced as separate API calls after spell creation

### Statistics

After running, the script shows:
- Total rows processed
- Number of modifiers found
- Breakdown by modifier type (AC, Attack, Damage, Save, Speed, Temp HP)

### Troubleshooting

**"Error: 'Description' column not found"**
- Make sure you're using the correct CSV file
- Check that the column is named exactly "Description"

**"No modifiers extracted"**
- Check that spell descriptions contain modifier language
- The script looks for keywords like "bonus", "increases", "gains"
- May need to add manual entries for complex modifiers

**"Wrong modifier type detected"**
- The script uses pattern matching which may misclassify edge cases
- Review and manually correct misclassified modifiers in the CSV
