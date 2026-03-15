# grammar_context.py
"""
Loads grammar descriptions for each language from the Google Sheets
'Grammar' tab and formats them into a text block for LLM prompting.

This file parallels load_dictionary.py but for grammar instead of lexicon.
"""

from functools import lru_cache
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
import pandas as pd


@lru_cache(maxsize=None)
def _load_grammar_df() -> pd.DataFrame:
  df = gsheets.get_df("grammar")

  # Normalize column names
  df.columns = [str(c).strip() for c in df.columns]

  return df


@lru_cache(maxsize=None)
def _load_language_df() -> pd.DataFrame:
  df = gsheets.get_df("languages")

  # Normalize column names
  df.columns = [str(c).strip() for c in df.columns]

  return df


def build_language_metadata(language: str) -> str:
  """
  Load metadata about the language from the Language sheet.

  Returns a formatted string with language properties like:
  - Type
  - Script
  - Description
  - Spoken By
  - etc.
  """
  df = _load_language_df()

  # Find the row where Name matches the language
  row = df[df["Name"] == language]

  if row.empty:
    return f"(No Language metadata found for '{language}')"

  row_data = row.iloc[0]
  lines = []

  # Define which columns to include and their display labels
  fields = [
    ("Type", "Language Type"),
    ("Script", "Script"),
    ("Description", "Description"),
    ("Spoken By", "Spoken By"),
    ("Longer description", "Longer Description"),
    ("Additional Notes", "Additional Notes"),
    ("Example", "Example Words"),
    ("Notation", "Notation"),
  ]

  for col_name, display_label in fields:
    value = row_data.get(col_name)
    if pd.notna(value) and isinstance(value, str) and value.strip():
      lines.append(f"{display_label}: {value.strip()}")

  return "\n".join(lines) if lines else "(No metadata available)"


# ---------------------------------------------------------
# PUBLIC FUNCTION
# ---------------------------------------------------------

def build_grammar_info(language: str, max_lines: int = None) -> str:
  """
  Create a block of grammar text for a given language to feed the LLM.

  Reads the grammar sheet and includes ALL grammar categories (no filtering).

  The sheet should contain columns:
      "Unnamed: 0" (optional section header)
      "Grammar Category"
      "<language>" columns (Brimic, Concordian, etc.)
  """

  df = _load_grammar_df()

  if language not in df.columns:
    return f"(No Grammar Sheet column exists for '{language}')"

  lines = []
  current_section = None

  for _, row in df.iterrows():
    section = row.get("Unnamed: 0")
    category = row.get("Grammar Category")
    value = row.get(language)

    # Track PHONOLOGY, MORPHOLOGY, SYNTAX, etc.
    if isinstance(section, str) and section.strip():
      current_section = section.strip()

    # Skip empty cells
    if not isinstance(value, str) or not value.strip():
      continue

    prefix = f"[{current_section}] " if current_section else ""

    if isinstance(category, str) and category.strip():
      line = f"{prefix}{category}: {value.strip()}"
    else:
      line = f"{prefix}{value.strip()}"

    lines.append(line)

  # Only limit lines if max_lines is specified
  if max_lines and len(lines) > max_lines:
    lines = lines[:max_lines]

  return "\n".join(lines)
