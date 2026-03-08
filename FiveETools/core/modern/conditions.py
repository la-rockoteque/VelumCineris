import pandas as pd
from FiveETools.core.modern.sources import source, json_source
from FiveETools.core.Helpers.gsheets_client import modern_sheets

df_condition = modern_sheets.get_sheet_by_name("conditions")
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
from Spreadsheet.core.converters.condition import ConditionConverter
from models.entities.condition import Condition
from typing import List

converter = ConditionConverter(modern_sheets)
condition_pydantic: List[Condition] = converter.convert_all(
    source_filter=None,
    source=source,
    json_source=json_source
)
