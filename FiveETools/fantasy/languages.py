import pandas as pd
from FiveETools.fantasy.sources import source, json_source
from FiveETools.gsheets_client import fantasy_sheets
import inflection

df_language = fantasy_sheets.get_sheet("163123529")
df_language.head()

language_list = [
    {
        "name": row.get("Name"),
        "source": json_source,
        "type": row.get("Type").lower(),
        **(
            {
                "typicalSpeakers": [
                    f"{{@filter {inflection.pluralize(speaker)}|bestiary|type=humanoid|tag= any race;{speaker}}}"
                    for speaker in row.get("Races").split(", ")
                ]
            }
            if pd.notnull(row.get("Races"))
            else {}
        ),
        **(
            {"script": row.get("Script").lower()}
            if pd.notnull(row.get("Script"))
            else {}
        ),
        "page": 0,
        "entries": [
            row.get("Description"),
        ],
    }
    for index, row in df_language.iterrows()
    if pd.notnull(row.get("Name"))
]

# NEW: Pydantic-based conversion for type safety
from Spreadsheet.converters.language import LanguageConverter
from models.entities.language import Language
from typing import List

converter = LanguageConverter(fantasy_sheets)
language_pydantic: List[Language] = converter.convert_all(
    source_filter=None,  # Languages don't have Source column
    source=source,
    json_source=json_source
)
