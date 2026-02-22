from FiveETools.fantasy.sources import source, json_source
try:
    from scripts.image_generator import generate_icon
except ImportError:
    generate_icon = None  # Optional dependency
from FiveETools.gsheets_client import fantasy_sheets
from Spreadsheet.converters.spell import SpellConverter
from models.entities.spell import Spell
from typing import List

df_spells = fantasy_sheets.get_sheet("625265890")
df_spells.head()

converter = SpellConverter(fantasy_sheets)
spells_pydantic: List[Spell] = converter.convert_all(
    source_filter=source,
    source=source,
    json_source=json_source
)
