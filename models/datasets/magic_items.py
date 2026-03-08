from models.datasets.sources import source, json_source, fantasy_sheets
try:
    from scripts.image_generator import generate_icon
except ImportError:
    generate_icon = None  # Optional dependency
from Spreadsheet.core.converters.magic_item import MagicItemConverter
from models.entities.magic_item import MagicItem
from typing import List

df_magic_items = fantasy_sheets.get_sheet_by_name("magic_items")
df_magic_items.head()




converter = MagicItemConverter(fantasy_sheets)
magic_items_pydantic: List[MagicItem] = converter.convert_all(
    source_filter=source,
    source=source,
    json_source=json_source
)
