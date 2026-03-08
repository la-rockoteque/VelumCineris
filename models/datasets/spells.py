from models.datasets.sources import source, json_source, fantasy_sheets
try:
    from scripts.image_generator import generate_icon
except ImportError:
    generate_icon = None  # Optional dependency
from Spreadsheet.core.converters.spell import SpellConverter
from models.entities.spell import Spell
from typing import List

df_spells = fantasy_sheets.get_sheet_by_name("spells")
df_spells.head()

converter = SpellConverter(fantasy_sheets)
spells_pydantic: List[Spell] = converter.convert_all(
    source_filter=source,
    source=source,
    json_source=json_source
)
