import pandas as pd
from FiveETools.datasets.sources import get_default_source_context
from Spreadsheet.sheets import modern_sheets
import inflection
import shutil

source, json_source = get_default_source_context("modern")

df_monster = modern_sheets.get_sheet_by_name("monsters")
df_monster.head()


def placehold(row):
    src = f"../images/Monsters/Placeholder.png"
    dst = f"../images/Monsters/{row.get('Name')}.png"
    shutil.copyfile(src, dst)


[
    placehold(row)
    for index, row in df_monster.iterrows()
    if pd.notnull(row.get("Name")) and row.get("Source") == source
]
