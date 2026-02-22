import pandas as pd
import inflection
from FiveETools.gsheets_client import fantasy_sheets

pd.options.display.float_format = "{:,.0f}".format
df_source = fantasy_sheets.get_sheet("340852453")
df_source.head()

source = "ORIO"
source_row = df_source[df_source["Source"] == source].iloc[0]

full_source = source_row["Full"]
json_source = source_row["json"]

sources = [
    {
        "json": row["json"],
        "abbreviation": row["Source"],
        "full": row["Full"],
        "url": f"https://raw.githubusercontent.com/la-rockoteque/Vestigium/refs/heads/main/Velum_Cineris;{inflection.underscore(json_source)}.json",
        "authors": ["Velum Cineris"],
        "version": "1.0",
    }
    for index, row in df_source.iterrows()
    if pd.notnull(row.get("Full"))
]
