import pandas as pd
from FiveETools.core.modern.sources import source, json_source
from FiveETools.core.Helpers.gsheets_client import modern_sheets

df_diety = modern_sheets.get_sheet_by_name("deities")
df_diety.head()

def row_to_diety(row):
    return     {
        "name": row.get("Name"),
        "source": json_source,
        "pantheon": "None",
        "symbol": row.get("Symbol") if pd.notnull(row.get("Symbol")) else "",
        "entries": [
            row.get("Description") if pd.notnull(row.get("Description")) else "",
        ],
        "page": 0,
        "alignment": [row.get("Alignment")[:1].upper()],
        **({"altNames": row.get("Epithet").split(", ")} if pd.notnull(row.get("Epithet")) else {}),
        # "domains": row.get("Domains").split(", ") if pd.notnull(row.get("Domains")) else [],
        "customProperties": {
            "Plane": row.get("Plane") if pd.notnull(row.get("Plane")) else "",
            "Followers": row.get("Followers") if pd.notnull(row.get("Followers")) else "",
            "Slogan": row.get("Slogan") if pd.notnull(row.get("Slogan")) else "",
            "Lore": row.get("Lore") if pd.notnull(row.get("Lore")) else "",
            "Quote": row.get("Quote") if pd.notnull(row.get("Quote")) else "",
        }
    }

diety_list = [
    row_to_diety(row)
    for index, row in df_diety.iterrows()
    if pd.notnull(row.get("Name"))
]
