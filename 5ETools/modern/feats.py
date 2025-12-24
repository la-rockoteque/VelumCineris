import pandas as pd
from src.sources import source, json_source
from src.content.gsheets_client import modern_sheets

df_feat = modern_sheets.get_sheet("1076107525")
df_feat.head()

def row_to_feat(row):
    feat_pos = row.index.get_loc("Feat")
    return     {
        "name": row.get("Name").lower(),
        "source": json_source,
        "entries": [
            row.get("Flavor Text"),
            *row.iloc[feat_pos:].dropna().tolist()
        ],
    }

feat_list = [
    row_to_feat(row)
    for index, row in df_feat.iterrows()
    if pd.notnull(row.get("Name")) and row.get("Source") == source
]
