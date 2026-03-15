# Content Google Sheets Client

This folder contains a centralized Google Sheets client for accessing content data across fantasy and non-fantasy spreadsheets.

## Overview

All data access files now use the shared client in `Spreadsheet/sheets.py`, which provides:
- Centralized spreadsheet configuration
- Consistent data loading interface
- Built-in caching for performance
- Easy switching between fantasy and non-fantasy content

## Usage

### Export CLI

```bash
# Build modern export to default path (FiveETools/out/...)
python -m FiveETools.cli export --setting modern

# Build fantasy export with explicit source and output path
python -m FiveETools.cli export --setting fantasy --source ORIO --out FiveETools/out/custom.json
```

### Basic Usage

```python
from Spreadsheet.sheets import fantasy_sheets, modern_sheets

# Load fantasy content
df_monsters = fantasy_sheets.get_sheet("736393386")

# Load non-fantasy content
df_spells = modern_sheets.get_sheet("625265890")
```

### Using Named Sheets

```python
from Spreadsheet.sheets import ContentSheetsClient

# Create a client for fantasy content
client = ContentSheetsClient("fantasy")

# Load by name (if defined in SHEET_GIDS)
df = client.get_sheet_by_name("monsters")
```

### Direct Sheet Access

```python
# Access a sheet by GID directly
df = modern_sheets.get_sheet("1076107525")  # Feats
```

## Spreadsheet Configuration

### Non-Fantasy (Vestigium Guide to Concord City)
- Spreadsheet ID: `1I4FHncl40_xx1Udc_Q2rWWWvpL6xaMlpJyY90WBftag`
- Available sheets:
  - spells: `625265890`
  - monsters: `736393386`
  - species: `993815941`
  - magic_items: `695912920`
  - classes: `1924660120`
  - class_tables: `193036738`
  - class_features: `545140625`
  - subclasses: `338247460`
  - feats: `1076107525`
  - backgrounds: `1186398440`
  - item_properties: `1064461316`
  - items: `876046336`
  - conditions: `1321788284`
  - diseases: `1196270347`
  - deities: `1410134136` (legacy alias: `dieties`)
  - languages: `163123529`

### Fantasy (Orimond)
- Spreadsheet ID: `1NBZGu29IfE1ZfAWO1Z6ShR5GMLMMbaSyS0m-46PSYm4`
- Available sheets:
  - monsters: `736393386`
  - species: `993815941`
  - languages: `163123529`

## Migration Summary

All data access files have been migrated from:
```python
# OLD
url = "https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
df = pd.read_csv(url)
```

To:

```python
# NEW
from Spreadsheet.sheets import modern_sheets

df = modern_sheets.get_sheet("{gid}")
```

## Benefits

1. **No Reconfiguration**: Switch between fantasy and non-fantasy by importing the appropriate client
2. **Performance**: Built-in caching reduces API calls
3. **Maintainability**: Single source of truth for spreadsheet IDs
4. **Type Safety**: TypeScript-style literals for content types
5. **Convenience**: Named sheet access for commonly used sheets

## Special Cases

### Sheets with Custom Headers

For sheets that use `header=1` parameter (like `class_features` in classes.py and subclasses.py):

```python
import io
import requests

url = non_fantasy_sheets._build_csv_url("545140625")
response = requests.get(url)
df = pd.read_csv(io.StringIO(response.text), header=1)
```

## Files Updated

All data access files in `src/content/` have been updated:
- spells.py
- fantasy_spells.py
- monster.py
- fantasy_monster.py
- species.py
- fantasy_species.py
- languages.py
- fantasy_languages.py
- magic_items.py
- classes.py
- subclasses.py
- feats.py
- backgrounds.py
- items.py
- conditions.py
- diseases.py
- dieties.py (legacy filename for deities data)
- features.py
