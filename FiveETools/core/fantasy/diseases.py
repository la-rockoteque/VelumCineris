import pandas as pd
from FiveETools.core.fantasy.sources import source, json_source
from FiveETools.core.Helpers.gsheets_client import fantasy_sheets

df_disease = fantasy_sheets.get_sheet_by_name("diseases")
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

# NEW: Pydantic-based conversion for type safety
from Spreadsheet.core.converters.disease import DiseaseConverter
from models.entities.disease import Disease
from typing import List

converter = DiseaseConverter(fantasy_sheets)
disease_pydantic: List[Disease] = converter.convert_all(
    source_filter=None,  # Diseases don't use source filter
    source=source,
    json_source=json_source
)
