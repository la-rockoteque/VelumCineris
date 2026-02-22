# D&D Beyond Homebrew Sync

Sync homebrew content from Google Sheets to D&D Beyond using automated browser-based API interaction.

## Quick Start

### 1. Install Playwright (one-time setup)

```bash
poetry run playwright install chromium
```

### 2. Extract Authentication Tokens

**Automated (Recommended):**
```bash
# Will prompt for D&D Beyond credentials
poetry run python DNDBeyond/scripts/get_ddb_tokens.py
```

This will automatically:
- Log into your D&D Beyond account
- Extract session cookies
- Extract security tokens
- Save everything to `DNDBeyond/.env`

**Manual (Alternative):**
If you prefer, you can manually extract tokens:
1. Copy `.env.example` to `.env`
2. Log into D&D Beyond in your browser
3. Open DevTools → Network tab
4. Visit a homebrew creation page
5. Copy cookies and tokens from the request headers
6. Paste into `.env`

### 3. Sync Your Content

```bash
# Open a sync notebook
poetry run jupyter notebook DNDBeyond/dnd_beyond_spells.ipynb

# Or sync other entity types
poetry run jupyter notebook DNDBeyond/dnd_beyond_monsters.ipynb
poetry run jupyter notebook DNDBeyond/dnd_beyond_species.ipynb
poetry run jupyter notebook DNDBeyond/dnd_beyond_backgrounds.ipynb
poetry run jupyter notebook DNDBeyond/dnd_beyond_feats.ipynb
```

## Architecture

### Components

```
DNDBeyond/
├── scripts/
│   ├── get_ddb_tokens.py    # Automated token extraction
│   └── README.md             # Script documentation
├── helpers/
│   ├── client.py             # HTTP client for D&D Beyond API
│   ├── converter.py          # 5etools → D&D Beyond format conversion
│   ├── utils.py              # Utility functions
│   └── entities/             # Entity-specific handlers
│       ├── base.py           # Base entity class
│       ├── spells.py         # Spell sync logic
│       ├── monsters.py       # Monster sync logic
│       ├── species.py        # Species sync logic
│       ├── backgrounds.py    # Background sync logic
│       └── feats.py          # Feat sync logic
├── pages/                    # Saved HTML pages for reference
├── requests/                 # Sample request/response data
├── dnd_beyond_*.ipynb        # Sync notebooks (one per entity type)
├── .env                      # Authentication configuration (gitignored)
└── .env.example              # Template for .env file
```

### How It Works

1. **Data Source**: Reads homebrew content from `FiveETools` modules
2. **Format Conversion**: Converts 5etools JSON format → D&D Beyond API format
3. **Duplicate Detection**: Checks spreadsheet + D&D Beyond for existing content
4. **API Interaction**: Creates/updates content via HTTP POST requests
5. **ID Tracking**: Writes D&D Beyond IDs back to Google Sheets

### Authentication

D&D Beyond doesn't have a public API, so we use:
- **Session cookies** from browser login
- **Security tokens** from homebrew creation forms
- **Browser automation** (Playwright) to extract these automatically

Tokens expire periodically - re-run `get_ddb_tokens.py` when sync fails.

## Entity Types

Each entity type has its own sync notebook and handler:

| Entity       | Notebook                      | Spreadsheet Column | Notes                          |
|--------------|-------------------------------|--------------------|---------------------------------|
| Spells       | `dnd_beyond_spells.ipynb`     | `DDB`              | Includes AOE, save, attack     |
| Monsters     | `dnd_beyond_monsters.ipynb`   | `DDB`              | Full statblock sync            |
| Species      | `dnd_beyond_species.ipynb`    | `DDB`              | Races with traits              |
| Backgrounds  | `dnd_beyond_backgrounds.ipynb`| `DDB`              | Character backgrounds          |
| Feats        | `dnd_beyond_feats.ipynb`      | `DDB`              | Character feats                |

## Configuration Options

Each notebook supports these configuration variables:

```python
DRY_RUN = False              # Set True to test without creating
BATCH_SIZE = None            # Limit sync (None = all)
DELAY = 1                    # Seconds between requests (rate limiting)
VERBOSE = True               # Detailed logging
SKIP_EXISTING = True         # Skip items with DDB IDs
UPDATE_EXISTING = True       # Update items when IDs exist
```

## Features

### ✅ Duplicate Detection
- Primary: Checks spreadsheet for existing DDB IDs
- Secondary: Parses D&D Beyond HTML to find existing content
- Prevents duplicate creation

### ✅ Batch Updates
- Syncs multiple items in sequence
- Rate limiting to avoid throttling
- Batch writes DDB IDs back to spreadsheet

### ✅ Error Handling
- Detailed error logging with HTTP status codes
- Exception tracking with full tracebacks
- Continues processing on individual failures
- Saves results to JSON log files

### ✅ Update Support
- Can update existing content (e.g., after renaming)
- Preserves DDB IDs in spreadsheet
- Supports partial updates (e.g., AOE/save/attack fields)

## Troubleshooting

### Authentication Failed

```bash
# Re-extract tokens
poetry run python DNDBeyond/scripts/get_ddb_tokens.py
```

### "playwright not installed"

```bash
poetry run playwright install chromium
```

### Rate Limiting / 429 Errors

Increase the `DELAY` parameter in notebooks:
```python
DELAY = 2  # or higher
```

### Conversion Errors

Check `DNDBeyond/helpers/converter.py` for field mappings. D&D Beyond may have changed their API.

### Duplicate Creation

1. Check spreadsheet "DDB" column for existing IDs
2. Run with `SKIP_EXISTING = True` (default)
3. Use batch delete section in notebooks to clean up

## Security

⚠️ **Important:**
- `.env` file contains sensitive session credentials
- Never commit `.env` to git (it's in `.gitignore`)
- Tokens expire - treat them like temporary passwords
- Re-run token extraction when they expire

## Advanced Usage

### Custom Entity Handler

See `helpers/entities/base.py` for base class. Extend it:

```python
from helpers.entities.base import BaseEntity

class CustomEntity(BaseEntity):
    entity_type_id = "123456789"  # From D&D Beyond
    create_path = "/homebrew/creations/create-custom"
    # ... implement methods
```

### Direct API Client

```python
from helpers.client import DnDBeyondClient

client = DnDBeyondClient(cookies="...", security_token="...")
response = client.get("/my-creations")
```

### Format Converter

```python
from helpers.converter import convert_spell_to_ddb

ddb_data = convert_spell_to_ddb(fivetools_spell)
```

## API Reference

See `DNDBeyond/AGENTS.md` for detailed API endpoint documentation and field mappings.

## Contributing

When adding support for new entity types:

1. Create entity handler in `helpers/entities/`
2. Create sync notebook: `dnd_beyond_<entity>.ipynb`
3. Add converter functions to `helpers/converter.py`
4. Update spreadsheet with new "DDB" column
5. Document in this README

## Related Files

- `FiveETools/gsheets_client.py` - Google Sheets data access
- `FiveETools/{fantasy|modern}/*.py` - Source data converters
- `CLAUDE.md` - Project-wide documentation
