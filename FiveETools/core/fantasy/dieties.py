import pandas as pd
from FiveETools.core.Helpers.gsheets_client import fantasy_sheets

df_dieties = fantasy_sheets.get_sheet_by_name("deities")
df_dieties.head()


def _split_list(value):
    if pd.isnull(value):
        return []
    return [item.strip() for item in str(value).split(",") if item.strip()]


def row_to_diety(row):
    return {
        "name": row.get("Name"),
        "epithet": row.get("Epithet"),
        "pantheon": row.get("Pantheon"),
        "image": row.get("Image"),
        "domains": _split_list(row.get("Domains")),
        "plane": row.get("Plane"),
        "vstg": row.get("VSTG"),
        "alignment": row.get("Alignment"),
        "followers": row.get("Followers"),
        "symbol": row.get("Symbol"),
        "slogan": row.get("Slogan"),
        "link": row.get("Link"),
        "description": row.get("Description"),
        "lore": row.get("Lore"),
        "quote": row.get("Quote"),
    }


diety_list = [
    row_to_diety(row)
    for _, row in df_dieties.iterrows()
    if pd.notnull(row.get("Name"))
]
