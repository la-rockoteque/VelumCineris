import pandas as pd
from FiveETools.core.modern.sources import source, json_source
from FiveETools.core.Helpers.gsheets_client import modern_sheets

df_feat = modern_sheets.get_sheet_by_name("feats")
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

# NEW: Pydantic-based conversion for type safety
from Spreadsheet.core.converters.feat import FeatConverter
from models.entities.feat import Feat
from typing import List

converter = FeatConverter(modern_sheets)
feat_pydantic: List[Feat] = converter.convert_all(
    source_filter=source,
    source=source,
    json_source=json_source
)
