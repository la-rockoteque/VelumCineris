from FiveETools.fantasy.sources import source, json_source
try:
    from scripts.image_generator import generate_icon
except ImportError:
    generate_icon = None  # Optional dependency
from FiveETools.gsheets_client import fantasy_sheets
from Spreadsheet.converters.magic_item import MagicItemConverter
from models.entities.magic_item import MagicItem
from typing import List

df_magic_items = fantasy_sheets.get_sheet("695912920")
df_magic_items.head()




converter = MagicItemConverter(fantasy_sheets)
magic_items_pydantic: List[MagicItem] = converter.convert_all(
    source_filter=source,
    source=source,
    json_source=json_source
)
