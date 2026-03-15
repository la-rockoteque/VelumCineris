import sys
from pathlib import Path

try:
  from Spreadsheet.sheets import gsheets
except ModuleNotFoundError:
  for parent in Path(__file__).resolve().parents:
    if (parent / "Spreadsheet").is_dir():
      sys.path.append(str(parent))
      break
  from Spreadsheet.sheets import gsheets

def load_dictionary():
  df = gsheets.get_df("dictionary")
  df["key"] = df["Word"].str.lower().str.replace(" ", "_")
  return df


if __name__ == "__main__":
  d = load_dictionary()
  print(list(d.keys())[:20])
