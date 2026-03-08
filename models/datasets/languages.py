from models.datasets.sources import source, json_source, fantasy_sheets
from Spreadsheet.core.converters.language import LanguageConverter
from models.entities.language import Language
from typing import List

df_language = fantasy_sheets.get_sheet_by_name("languages")
df_language.head()

# NEW: Pydantic-based conversion for type safety


converter = LanguageConverter(fantasy_sheets)
language_pydantic: List[Language] = converter.convert_all(
    source_filter=None,  # Languages don't have Source column
    source=source,
    json_source=json_source
)
