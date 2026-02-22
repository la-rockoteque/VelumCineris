import pandas as pd
from src.sources import source, json_source
from FiveETools.gsheets_client import modern_sheets
import inflection
import shutil

df_monster = modern_sheets.get_sheet("736393386")
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
