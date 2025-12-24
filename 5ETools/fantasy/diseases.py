import pandas as pd
from src.sources import source, json_source
from src.content.gsheets_client import fantasy_sheets

df_disease = fantasy_sheets.get_sheet("1196270347")
df_disease.head()

def row_to_disease(row):
  return     {
    "name": row.get("Name"),
    "source": json_source,
    "entries": [
      row.get("Symptoms"),
      row.get("In-Game Effects"),
      row.get("Cure"),
      row.get("Prognosis"),
    ],
    "page": 0,
  }

disease_list = [
  row_to_disease(row)
  for index, row in df_disease.iterrows()
  if pd.notnull(row.get("Name"))
]
