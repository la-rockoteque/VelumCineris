# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Vestigium Foundry Spells** is a D&D 5e homebrew content management system for two campaign settings:
- **Vestigium Guide to Concord City** (non-fantasy/modern)
- **Orimond** (fantasy)

Content flows from **Google Sheets → Python converters → JSON exports → External platforms** (World Anvil, D&D Beyond, Foundry VTT).

## Development Commands

### Python Environment
```bash
# Install dependencies (uses Poetry)
poetry install

# Run Python scripts/notebooks
poetry run python <script.py>
poetry run jupyter notebook

# Download NLTK wordnet data (required for translator module)
poetry run download-wordnet
```

### Code Quality
```bash
# Format code
poetry run ruff format .

# Lint code
poetry run ruff check .

# Type checking
poetry run pyright
```

### JSON Validation
```bash
# Verify 5etools JSON format
npm run verify
```

## Architecture

### Data Flow Pipeline

```
Google Sheets (Source of Truth)
    ↓
src/content/*.py (Converters - 5etools format)
    ↓
*.json exports (Compendium files)
    ↓
Sync notebooks → External platforms
```

### Core Components

#### 1. Google Sheets Client (`src/content/gsheets_client.py`)
Centralized client for all data access with two modes:
- **Read-only**: CSV export URLs (fast, cached)
- **Read-write**: gspread with service account auth (`key.json`)

```python
from src.content.gsheets_client import fantasy_sheets, modern_sheets

# Read data
df = fantasy_sheets.get_sheet("625265890")  # By GID
df = modern_sheets.get_sheet_by_name("spells")  # By name

# Write data (requires credentials.json)
fantasy_sheets.ensure_column_exists("625265890", "DDB")
fantasy_sheets.update_cell_by_row_match(
    gid="625265890",
    match_column="Spell Name",
    match_value="Fireball",
    update_column="DDB",
    update_value="12345"
)
```

**Important GIDs:**
- Fantasy spells: `625265890`
- Non-fantasy spells: `625265890`
- Monsters: `736393386`
- Species: `993815941`

See `src/content/README.md` for complete GID mapping.

#### 2. Content Converters (`src/content/*.py`)
Each file converts raw Google Sheets data to **5etools JSON format**:
- `fantasy_spells.py` / `spells.py` - Spell data
- `fantasy_monster.py` / `monster.py` - Monster statblocks
- `fantasy_species.py` / `species.py` - Player races
- `classes.py`, `subclasses.py`, `features.py` - Class mechanics
- `magic_items.py`, `items.py` - Equipment and magic items

**Pattern:**
```python
# Load sheet
df = fantasy_sheets.get_sheet("GID")

# Define converter
def row_to_entity(row: pd.Series) -> dict:
    return {
        "name": row.get("Name"),
        "level": int(row.get("Level", 0)),
        # ... 5etools format fields
    }

# Generate list
entities_list = [row_to_entity(row) for _, row in df.iterrows()
                 if pd.notnull(row.get("Name"))]
```

**Key field mappings:**
- Components: `{"v": True, "s": True, "m": False}` format
- Time: `[{"number": 1, "unit": "action"}]` array format
- Range: `{"type": "point", "distance": {"type": "feet", "amount": 60}}`
- Duration: `[{"type": "instant", "concentration": False}]`

#### 3. Compendium Generators (Notebooks)
Generate final JSON exports:
- `compendium_fantasy.ipynb` → `Velum_Cineris;guide_to_orimond.json`
- `compendium_modern.ipynb` → `Velum_Cineris;everyday_guideto_concord_city.json`

These files are committed to git and can be imported into Foundry VTT.

#### 4. Sync Notebooks

**World Anvil Sync** (`world_anvil_sync.ipynb`):
- Uses internal web API (cookie-based auth, no API key)
- Helper class: `world_anvil/helpers/WorldAnvilAPI.py`
- Syncs species to World Anvil articles
- Tracks WA article IDs in spreadsheet "WA" column
- Features duplicate detection and batch updates

**D&D Beyond Sync** (`dnd_beyond_sync.ipynb`):
- Uses browser form submission (multipart/form-data)
- Requires security tokens from create form + session cookies
- Syncs spells to D&D Beyond homebrew
- Uses HTML parsing (BeautifulSoup) for duplicate detection
- Tracks DDB spell IDs in spreadsheet "DDB" column
- Features batch spreadsheet updates via gspread

Both sync notebooks:
1. Check spreadsheet for existing IDs first (primary)
2. Check platform for existing content (secondary)
3. Create new content if needed
4. Write IDs back to spreadsheet for future runs

#### 5. Translator Module (`translator/`)
Generates fictional language content using LLMs:
- `batch_generate_lexemes.py` - Word generation
- `batch_generate_phonetics.py` - Pronunciation generation
- `batch_generate_scripts.py` - Writing system generation
- `generator.py` - Core LLM interface (uses Ollama)
- `gsheets_client.py` - Separate client for translator sheets

Uses NLTK WordNet for linguistic analysis (requires `poetry run download-wordnet`).

### Source Configuration

The `src/sources.py` file defines campaign sources:
- `source = "VSTGCC"` - Vestigium Guide to Concord City
- Maps to Google Sheets row for full name and JSON identifiers
- Used to filter content by campaign in converters

### Image Management

Images stored in `images/` directory:
- `images/Monsters/{fantasy|modern}/` - Creature art
- `images/Species/{fantasy|modern}/` - Species portraits
- `images/Spell/` - Spell icons
- Referenced in JSON via GitHub raw URLs

Scripts in `scripts/`:
- `Placehold_monsters_images.py` - Generate placeholder images
- Image paths use `inflection.underscore()` for filename normalization

## Working with Jupyter Notebooks

All notebooks use the poetry environment kernel. To run:
```bash
poetry run jupyter notebook
```

**Common patterns:**
1. Import content modules: `import src.content.fantasy_spells`
2. Access data: `spells = src.content.fantasy_spells.spells_list`
3. Load sheets: `from src.content.gsheets_client import fantasy_sheets`

**Notebook purposes:**
- `world_anvil_sync.ipynb` - Sync to World Anvil
- `dnd_beyond_sync.ipynb` - Sync to D&D Beyond
- `compendium_fantasy.ipynb` - Generate JSON for Foundry VTT
- `compendium_modern.ipynb` - Generate JSON for Foundry VTT
- `markdown.ipynb` - Generate markdown documentation
- `ObsidiantoWorldAnvil.ipynb` - Convert Obsidian notes
- `Monsters.ipynb` - Monster data exploration

## Authentication & Credentials

### Google Sheets (Read-Write)
- File: `credentials.json` (service account)
- Used by: `gsheets_client.py` when writing data
- Scopes: `spreadsheets`, `drive`

### World Anvil
- Browser session cookies (no API key)
- Extract from Developer Tools → Network → Cookie header
- Configure in notebook: `WA_COOKIES` variable
- World ID: `47087` (Orimond)

### D&D Beyond
- Browser session cookies + security tokens
- Tokens from create form hidden fields: `security-token`, `authenticity-token`
- Configure in notebook: `DDB_COOKIES`, `DDB_SECURITY_TOKEN`, `DDB_AUTHENTICITY_TOKEN`
- Tokens expire periodically

## Key Patterns & Conventions

### 5etools JSON Format
This project generates content compatible with 5etools format:
- Spell schools: `"A"`, `"C"`, `"D"`, `"E"`, `"V"`, `"I"`, `"N"`, `"T"`
- Spell components: `{"v": bool, "s": bool, "m": bool}` (not strings)
- Nested time/range/duration structures (arrays and objects)

### Spreadsheet Column Tracking
External platform IDs are tracked in spreadsheet columns:
- `WA` column: World Anvil article IDs
- `DDB` column: D&D Beyond homebrew IDs
- Auto-created via `ensure_column_exists()` if missing
- Enables fast duplicate detection without API calls

### Content Type Switching
Two parallel content sets (fantasy vs non-fantasy):
```python
# Fantasy (Orimond)
from src.content.gsheets_client import fantasy_sheets
import src.content.fantasy_spells

# Non-fantasy (Concord City)
from src.content.gsheets_client import modern_sheets
import src.content.spells
```

### Error Handling in Sync Notebooks
Both sync notebooks track detailed results:
```python
results = {
    "created": 0,
    "skipped": 0,
    "errors": 0,
    "details": []  # List of dicts with per-item status
}
```

Results saved to JSON logs: `sync_log_YYYYMMDD_HHMMSS.json`

## Important Notes

- **Poetry environment**: Always use `poetry run` for Python commands
- **Credentials required**: `key.json` for writing to Google Sheets
- **Session cookies expire**: Re-extract from browser if sync fails
- **Rate limiting**: Both WA and DDB may throttle requests (use `DELAY` parameter)
- **5etools format**: Strictly follow nested dict/array structures for compatibility
- **Source filtering**: Most converters filter by `row.get("Source") == source`
