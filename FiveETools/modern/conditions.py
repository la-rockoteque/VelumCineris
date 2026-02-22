import pandas as pd
from FiveETools.modern.sources import source, json_source
from FiveETools.gsheets_client import modern_sheets

df_condition = modern_sheets.get_sheet("1321788284")
df_condition.head()

condition_list = [
    {
        "name": row.get("Condition Name"),
        "source": json_source,
        "entries": [
            *row.get("Condition Text").split(";"),
        ],
    }
    for index, row in df_condition.iterrows()
    if pd.notnull(row.get("Condition Name"))
]

# NEW: Pydantic-based conversion for type safety
from Spreadsheet.converters.condition import ConditionConverter
from models.entities.condition import Condition
from typing import List

converter = ConditionConverter(modern_sheets)
condition_pydantic: List[Condition] = converter.convert_all(
    source_filter=None,
    source=source,
    json_source=json_source
)
