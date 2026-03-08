# Book Generator

Generate D&D sourcebooks in Google Docs with PHB-style formatting.

## Overview

The Book Generator consolidates homebrew content from Google Sheets into professional-looking books with two-column PHB-style layout. It supports multiple book types (Omnibook, PHB, DMG, Monster Manual, Divine Codex) and two campaign settings (Fantasy/Orimond and Modern/Concord City).

## Architecture

```
Book/
├── book_api.py                    # Main orchestrator
├── google_docs_client.py          # Google Docs API wrapper
├── styles.py                      # PHB-style constants
├── formatters/                    # Entity-specific formatters
│   ├── base.py                   # Base formatter class
│   ├── spells.py                 # Spell formatter
│   ├── species.py                # Race/Species formatter
│   ├── monsters.py               # Monster formatter
│   └── ...                       # Additional formatters
├── writers/                      # Book-specific writers
│   ├── base.py                   # Base writer class
│   ├── omnibook.py               # Complete book (all entities)
│   ├── phb.py                    # Player's Handbook
│   ├── dmg.py                    # Dungeon Master's Guide
│   ├── monster_manual.py         # Monster Manual
│   └── divine_codex.py           # Divine Codex
└── book_generation.ipynb         # Jupyter notebook interface
```

## Quick Start

### 1. Install Dependencies

```bash
poetry add google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib
```

### 2. Configure Google Docs API

Ensure your `FiveETools/key.json` service account has Google Docs API permissions:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Google Docs API
3. Grant service account access to your document

### 3. Run the Notebook

```bash
poetry run jupyter notebook Book/book_generation.ipynb
```

### 4. Generate a Book

```python
from Book.book_api import BookAPI
from Book.google_docs_client import GoogleDocsClient
from Book.core.writers import OmnibookWriter
from FiveETools.gsheets_client import fantasy_sheets

# Initialize
DOC_ID = "YOUR_GOOGLE_DOC_ID"
gdocs = GoogleDocsClient(DOC_ID, "FiveETools/key.json")
book_api = BookAPI(gdocs, fantasy_sheets)

# Generate Omnibook
writer = OmnibookWriter(book_api, source="fantasy")
book_api.generate_book(writer, DOC_ID)
```

## Supported Book Types

### 1. Omnibook
Complete book with all entity types:
- Races/Species
- Classes & Subclasses (modern only)
- Backgrounds
- Feats
- Spells
- Items & Magic Items
- Monsters
- Languages
- Diseases

```python
writer = OmnibookWriter(book_api, source="fantasy")
```

### 2. Player's Handbook (PHB)
Player-facing content only:
- Races
- Classes & Subclasses (modern only)
- Backgrounds
- Feats
- Spells
- Equipment (modern only)

```python
writer = PHBWriter(book_api, source="fantasy")
```

### 3. Monster Manual
Creatures only, sorted by CR:
- Monsters

```python
writer = MonsterManualWriter(book_api, source="fantasy")
```

### 4. Dungeon Master's Guide (DMG)
DM-facing content:
- Magic Items
- Diseases
- Languages

```python
writer = DMGWriter(book_api, source="fantasy")
```

### 5. Divine Codex
Deity and religious content (placeholder):
- Deities (not yet implemented)

```python
writer = DivineCodexWriter(book_api, source="fantasy")
```

## Campaign Settings

### Fantasy (Orimond)
```python
book_api = BookAPI(gdocs, fantasy_sheets)
writer = OmnibookWriter(book_api, source="fantasy")
```

### Modern (Concord City)
```python
book_api = BookAPI(gdocs, modern_sheets)
writer = OmnibookWriter(book_api, source="modern")
```

## Formatters

Formatters convert 5etools format entities into formatted text for Google Docs.

### Implemented Formatters
- ✅ **SpellFormatter** - Formats spell entries with properties and descriptions
- ✅ **SpeciesFormatter** - Formats race/species with traits and abilities
- ✅ **MonsterFormatter** - Formats monster stat blocks

### Stub Formatters (To Be Implemented)
- ⏳ **BackgroundFormatter** - Backgrounds with features
- ⏳ **FeatFormatter** - Feats with prerequisites and benefits
- ⏳ **ClassFormatter** - Classes with features and tables
- ⏳ **SubclassFormatter** - Subclasses with features
- ⏳ **ItemFormatter** - Equipment and items
- ⏳ **MagicItemFormatter** - Magic items with properties
- ⏳ **LanguageFormatter** - Languages with scripts
- ⏳ **DiseaseFormatter** - Diseases with effects

### Creating a New Formatter

1. Create a new file in `Book/core/formatters/`:

```python
# Book/core/formatters/backgrounds.py
from typing import Dict, List, Any
from Book.core.formatters.base import BaseFormatter

class BackgroundFormatter(BaseFormatter):
    def format_entity(self, background: Dict[str, Any]) -> List[str]:
        lines = []

        # Format background name
        name = background.get("name", "Unknown Background")
        lines.extend(self.format_heading(name, level=3))

        # Format description
        entries = background.get("entries", [])
        lines.extend(self.format_entries(entries))

        # Format features
        if "feature" in background:
            for feature in background["feature"]:
                lines.extend(self._format_feature(feature))

        return lines

    def _format_feature(self, feature: Dict[str, Any]) -> List[str]:
        lines = []
        name = feature.get("name", "")
        if name:
            lines.extend(self.format_text(name, bold=True))
        entries = feature.get("entries", [])
        lines.extend(self.format_entries(entries))
        return lines
```

2. Update `Book/core/formatters/__init__.py`:

```python
from Book.core.formatters.backgrounds import BackgroundFormatter

__all__ = [..., "BackgroundFormatter"]
```

3. Update `Book/core/writers/base.py` formatter map:

```python
formatter_map = {
    ...
    "background": BackgroundFormatter(),
}
```

## Google Docs API

### Key Methods

```python
# Clear document
gdocs.clear_document()

# Add heading
gdocs.add_heading("Chapter 1", level=1)

# Add paragraph
gdocs.add_paragraph("This is a paragraph.", bold=False, italic=False)

# Add page break
gdocs.add_page_break()

# Apply two-column layout
gdocs.apply_two_column_layout()
```

### Batch Updates

For efficiency, use batch updates:

```python
requests = [
    {"insertText": {"location": {"index": 1}, "text": "Hello\n"}},
    {"updateTextStyle": {...}},
]
gdocs.batch_update(requests)
```

## Styling

PHB-style constants are defined in `Book/styles.py`:

```python
# Fonts
FONT_NAME = "Georgia"  # PHB alternative
BODY_FONT_SIZE = 9
HEADING_1_SIZE = 24

# Colors (PHB burgundy)
HEADING_COLOR = {"red": 0.58, "green": 0.0, "blue": 0.0}

# Layout
COLUMN_GAP = 36
MARGIN_TOP = 72
```

## Troubleshooting

### Import Errors
Ensure you're running from the project root or add parent directory to path:

```python
import sys
sys.path.insert(0, '..')
```

### Authentication Errors
- Check that `key.json` exists at the specified path
- Verify Google Docs API is enabled in Google Cloud Console
- Ensure service account has access to the target document

### Missing Entities
- Verify entity converters exist in `FiveETools/core/fantasy/` or `FiveETools/core/modern/`
- Check that the entity type is supported (see `book_api.entity_modules`)

### Formatting Issues
- Preview formatting with `book_api.preview_section()` before full generation
- Check formatter implementation for the specific entity type
- Verify 5etools format data structure matches formatter expectations

## Development

### Adding a New Book Type

1. Create a new writer in `Book/core/writers/`:

```python
# Book/core/writers/my_book.py
from Book.core.writers.base import BaseWriter

class MyBookWriter(BaseWriter):
    def get_book_title(self) -> str:
        return "My Custom Book"

    def get_sections(self):
        return [
            ("Chapter 1", "spell", None),
            ("Chapter 2", "monster", lambda m: m[:10]),  # First 10 monsters
        ]
```

2. Update `Book/core/writers/__init__.py`
3. Use in notebook: `writer = MyBookWriter(book_api, source="fantasy")`

### Testing

Preview specific sections before generating full books:

```python
# Preview 5 spells
book_api.preview_section("spell", source="fantasy", limit=5)

# Preview 3 monsters
book_api.preview_section("monster", source="fantasy", limit=3)
```

## API Reference

### BookAPI

```python
class BookAPI:
    def load_entities(entity_type: str, source: str = "fantasy") -> List[Dict]
    def generate_book(writer: BaseWriter, doc_id: str = None)
    def preview_section(entity_type: str, source: str = "fantasy", limit: int = 5)
```

### GoogleDocsClient

```python
class GoogleDocsClient:
    def clear_document()
    def add_heading(text: str, level: int = 1, index: int = None)
    def add_paragraph(text: str, bold: bool = False, italic: bool = False, index: int = None)
    def add_page_break(index: int = None)
    def apply_two_column_layout()
    def batch_update(requests: List[Dict])
```

### BaseFormatter

```python
class BaseFormatter(ABC):
    def format_entity(entity: Dict) -> List[str]  # Abstract method
    def format_heading(text: str, level: int = 2) -> List[str]
    def format_property(label: str, value: Any, bold_label: bool = True) -> List[str]
    def format_list_item(text: str, level: int = 0) -> List[str]
    def format_text(text: str, bold: bool = False, italic: bool = False) -> List[str]
    def format_table(headers: List[str], rows: List[List[str]]) -> List[str]
    def format_entries(entries: List[Any]) -> List[str]
```

### BaseWriter

```python
class BaseWriter(ABC):
    def get_sections() -> List[Tuple[str, str, Optional[Callable]]]  # Abstract
    def get_book_title() -> str  # Abstract
    def get_formatter(entity_type: str) -> BaseFormatter
    def write_cover_page() -> List[str]
    def write_table_of_contents() -> List[str]
    def write_section(section_name: str, entities: List[Dict], formatter: BaseFormatter) -> List[str]
```

## Future Enhancements

- [ ] Implement remaining formatters (backgrounds, feats, items, etc.)
- [ ] Add image support via Google Docs `inlineObjects` API
- [ ] Implement automatic table of contents with page numbers
- [ ] Add custom styling options (fonts, colors, margins)
- [ ] Support for exporting to PDF directly
- [ ] Batch processing for multiple documents
- [ ] Progress indicators for long-running generations
- [ ] Error recovery and partial generation

## License

Part of the Vestigium Foundry Spells project.
