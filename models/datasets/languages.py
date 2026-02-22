from FiveETools.fantasy.sources import source, json_source
from FiveETools.gsheets_client import fantasy_sheets
from Spreadsheet.converters.language import LanguageConverter
from models.entities.language import Language
from typing import List

df_language = fantasy_sheets.get_sheet("163123529")
df_language.head()

# NEW: Pydantic-based conversion for type safety


converter = LanguageConverter(fantasy_sheets)
language_pydantic: List[Language] = converter.convert_all(
    source_filter=None,  # Languages don't have Source column
    source=source,
    json_source=json_source
)
