# Book Generator

Generate D&D sourcebooks in Google Docs or Homebrewery with PHB-style formatting.

## Overview

The Book Generator consolidates homebrew content from Google Sheets into professional-looking books with two-column PHB-style layout. It supports multiple book types (Omnibook, PHB, DMG, Monster Manual, Divine Codex) and two campaign settings (Fantasy/Orimond and Modern/Concord City). Writer profiles now produce canonical markdown first; Google Docs and Homebrewery exports are derived from that markdown.

## Architecture

```
Book/
├── cli.py                         # Normalized CLI entrypoint
├── datasets/                      # Source/sheets selection adapters
├── exports/                       # Writer profile registry
├── mappers/                       # Compatibility registry adapters
├── services/                      # Generation orchestration service
├── core/                          # Book rendering internals
│   ├── Helpers/
│   ├── entities/                  # Entity-owned markdown renderers
│   ├── markdown/                  # Jinja, helpers, Docs markdown renderer
│   ├── formatters/                # Compatibility wrappers during migration
│   └── writers/
├── book_api.py                    # Compatibility shim to core Helpers
├── google_docs_client.py          # Compatibility shim to core Helpers
└── book_generation.ipynb          # Jupyter notebook interface
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

CLI:

```bash
poetry run python -m Book.cli generate --book-type omnibook --source fantasy --doc-id YOUR_GOOGLE_DOC_ID
```

Homebrewery export:

```bash
poetry run python -m Book.cli export-homebrewery --book-type campaign_handbook --source fantasy --output Book/exports/orimond-campaign-handbook.homebrewery.md
```

Canonical markdown export:

```bash
poetry run python -m Book.cli export-markdown --book-type campaign_handbook --source fantasy --output Book/exports/orimond-campaign-handbook.md
```

Standalone module export:

```bash
poetry run python -m Book.cli export-module-markdown --entity-type spell --source fantasy --title "Starter Spells" --limit 20 --output Book/exports/starter-spells.md
poetry run python -m Book.cli export-module-homebrewery --entity-type monster --source fantasy --output Book/exports/monsters.homebrewery.md
```

Standalone Google Docs module:

```bash
poetry run python -m Book.cli generate-module --entity-type species --source fantasy --doc-id YOUR_GOOGLE_DOC_ID
```

Python service:

```python
from Book.services import BookGenerationService

service = BookGenerationService()
service.generate_book(
    book_type="omnibook",
    source="fantasy",
    doc_id="YOUR_GOOGLE_DOC_ID",
    credentials_path="FiveETools/key.json",
)

service.export_homebrewery(
    book_type="campaign_handbook",
    source="fantasy",
    output_path="Book/exports/orimond-campaign-handbook.homebrewery.md",
)

service.export_markdown(
    book_type="campaign_handbook",
    source="fantasy",
    output_path="Book/exports/orimond-campaign-handbook.md",
)

service.export_module_markdown(
    entity_type="spell",
    source="fantasy",
    title="Starter Spells",
    limit=20,
    output_path="Book/exports/starter-spells.md",
)
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

### Creating a New Entity Markdown Renderer

1. Create an entity package under `Book/core/entities/<entity_type>/` with a context builder and Jinja-backed renderer:

```python
# Book/core/entities/backgrounds/renderer.py
from typing import Any

from Book.core.entities.base import EntityMarkdownRenderer


class BackgroundMarkdownRenderer(EntityMarkdownRenderer):
    template_name = "entities/backgrounds/template.md.j2"

    def build_context(self, background: dict[str, Any]) -> dict[str, Any]:
        return {
            "name": background.get("name", "Unknown Background"),
            "entries": background.get("entries", []),
        }
```

2. Add the renderer to `Book/core/entities/registry.py`:

```python
_RENDERER_CLASSES = {
    ...
    "background": BackgroundMarkdownRenderer,
}
```

3. Add a Jinja markdown template:

```jinja
### {{ name }}

{{ entries | render_entries }}
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
    def _build_requests_for_markdown(markdown: str, index: int)
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

### EntityMarkdownRenderer

```python
class EntityMarkdownRenderer(ABC):
    template_name: str
    def build_context(entity: dict) -> dict
    def render_markdown(entity: dict) -> str
```

### BaseWriter

```python
class BaseWriter(ABC):
    def get_sections() -> List[Tuple[str, str, Optional[Callable]]]  # Abstract
    def get_book_title() -> str  # Abstract
    def build_markdown() -> str
    def get_entity_renderer(entity_type: str) -> EntityMarkdownRenderer
    def write_cover_page() -> str
    def write_table_of_contents() -> str
    def write_section(section_name: str, entities: List[Dict], entity_type: str) -> str
```

## Future Enhancements

- [ ] Replace remaining formatter-backed entity adapters with native context builders.
- [x] Add image support for markdown and cover image directives.
- [ ] Implement automatic table of contents with page numbers
- [ ] Add custom styling options (fonts, colors, margins)
- [ ] Support for exporting to PDF directly
- [ ] Batch processing for multiple documents
- [ ] Progress indicators for long-running generations
- [ ] Error recovery and partial generation

## License

Part of the Vestigium Foundry Spells project.
