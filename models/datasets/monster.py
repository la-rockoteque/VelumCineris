from models.datasets.sources import json_source, fantasy_sheets
from Spreadsheet.core.converters.monster import MonsterConverter
from models.entities.monster import Monster
from typing import List

df_monster = fantasy_sheets.get_sheet_by_name("monsters")
df_monster.head()

converter = MonsterConverter(fantasy_sheets)
monster_pydantic: List[Monster] = converter.convert_all(
    source_filter=None,  # Monsters don't use source filter by default
    source="ORIO",
    json_source=json_source
)
