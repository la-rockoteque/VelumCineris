import pandas as pd
from src.sources import source, json_source
from src.content.gsheets_client import modern_sheets

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
