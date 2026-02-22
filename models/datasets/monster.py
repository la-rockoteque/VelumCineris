from FiveETools.fantasy.sources import json_source
from FiveETools.gsheets_client import fantasy_sheets
from Spreadsheet.converters.monster import MonsterConverter
from models.entities.monster import Monster
from typing import List

df_monster = fantasy_sheets.get_sheet("736393386")
df_monster.head()

converter = MonsterConverter(fantasy_sheets)
monster_pydantic: List[Monster] = converter.convert_all(
    source_filter=None,  # Monsters don't use source filter by default
    source="ORIO",
    json_source=json_source
)
