#!/usr/bin/env python3
"""
batch_generate_lexemes.py

Batch-generates lexemes for all words in all languages.

Usage:
  python batch_generate_lexemes.py                    # Generate for all languages
  python batch_generate_lexemes.py --lang=Ashen       # Generate for specific language
  python batch_generate_lexemes.py --offline          # Use local XLSX file
  python batch_generate_lexemes.py --force            # Overwrite existing cells

  # Grammar deviation: Allow LLM to deviate from strict rules to prevent duplicates
  python batch_generate_lexemes.py --deviation=15     # Allow 15% deviation (default: 10%)

  # Creole: ALL words (except borrowed) use ALL creole words as blended inspiration
  python batch_generate_lexemes.py --creole-from=Brimic  # Blend Brimic words
  python batch_generate_lexemes.py --creole-from=Brimic --creole-from=Ancient  # Blend multiple creole languages

  # Proto-root: Randomly use ONE word as proto-root at specified rate
  python batch_generate_lexemes.py --root-from=Ancient --root-rate=30  # 30% of words use Ancient as proto
  python batch_generate_lexemes.py --root-from=Ancient --root-from=Brimic --root-rate=50  # 50% use either Ancient or Brimic

  # Borrowing: Randomly borrow X% of words verbatim from specified languages
  python batch_generate_lexemes.py --borrow-from=Concordian --borrow-rate=5  # Borrow 5% verbatim
  python batch_generate_lexemes.py --borrow-from=Concordian --borrow-from=Brimic --borrow-rate=10  # Borrow from multiple

  # Combined: Blend creole languages + occasionally use proto-roots
  python batch_generate_lexemes.py --creole-from=Brimic --creole-from=Ancient --root-from=Proto --root-rate=20 --borrow-from=Concordian --borrow-rate=10 --deviation=15
"""

import sys
import math
import random
from pathlib import Path

try:
  from Spreadsheet.sheets import gsheets, OfflineTranslatorSheetsClient as OfflineSheetsClient
except ModuleNotFoundError:
  for parent in Path(__file__).resolve().parents:
    if (parent / "Spreadsheet").is_dir():
      sys.path.append(str(parent))
      break
  from Spreadsheet.sheets import gsheets, OfflineTranslatorSheetsClient as OfflineSheetsClient
from generator import llm_lexeme
import pandas as pd

updates = []


def get_client():
  """Choose online or offline client based on flags."""
  offline = "--offline" in sys.argv
  if offline:
    print("Using OFFLINE XLSX client")
    return OfflineSheetsClient("Language.xlsx")
  else:
    print("Using ONLINE Google Sheets client")
    return gsheets


def get_target_languages(df: pd.DataFrame, lang_flag: str | None):
  """
  Determine which language columns to process.

  We treat Category, Word, key as non-language.
  Everything else is considered a language column.
  """
  non_lang = {"Category", "Word", "key"}
  all_langs = [c for c in df.columns if c not in non_lang]

  if lang_flag is None:
    return all_langs

  # Case-insensitive matching for language name
  lookup = {c.lower(): c for c in all_langs}
  wanted = lang_flag.lower()
  if wanted not in lookup:
    raise SystemExit(
      f"Language '{lang_flag}' not found. "
      f"Available: {', '.join(all_langs)}"
    )
  return [lang_flag]


def main():
  # Parse optional flags
  lang_flag = None
  force = False
  creole_from = []  # Blend ALL words from these languages
  root_from = []  # Use ONE random word as proto-root
  root_rate = 0.0
  borrow_from = []  # Changed to list to support multiple languages
  borrow_rate = 0.0
  deviation = 10.0  # Default 10% deviation from grammar rules
  args = sys.argv[1:]
  i = 0
  while i < len(args):
    arg = args[i]
    if arg.startswith("--lang="):
      lang_flag = arg.split("=", 1)[1].strip()
      i += 1
    elif arg == "--lang" and i + 1 < len(args):
      lang_flag = args[i + 1].strip()
      i += 2
    elif arg == "--force":
      force = True
      i += 1
    elif arg.startswith("--creole-from="):
      creole_from.append(arg.split("=", 1)[1].strip())
      i += 1
    elif arg == "--creole-from" and i + 1 < len(args):
      creole_from.append(args[i + 1].strip())
      i += 2
    elif arg.startswith("--root-from="):
      root_from.append(arg.split("=", 1)[1].strip())
      i += 1
    elif arg == "--root-from" and i + 1 < len(args):
      root_from.append(args[i + 1].strip())
      i += 2
    elif arg.startswith("--root-rate="):
      rate_str = arg.split("=", 1)[1].strip()
      rate_str = rate_str.rstrip("%")
      root_rate = float(rate_str) / 100.0
      i += 1
    elif arg == "--root-rate" and i + 1 < len(args):
      rate_str = args[i + 1].strip()
      rate_str = rate_str.rstrip("%")
      root_rate = float(rate_str) / 100.0
      i += 2
    elif arg.startswith("--borrow-from="):
      borrow_from.append(arg.split("=", 1)[1].strip())  # Append to list
      i += 1
    elif arg == "--borrow-from" and i + 1 < len(args):
      borrow_from.append(args[i + 1].strip())  # Append to list
      i += 2
    elif arg.startswith("--borrow-rate="):
      rate_str = arg.split("=", 1)[1].strip()
      # Support both "5" and "5%" formats
      rate_str = rate_str.rstrip("%")
      borrow_rate = float(rate_str) / 100.0
      i += 1
    elif arg == "--borrow-rate" and i + 1 < len(args):
      rate_str = args[i + 1].strip()
      rate_str = rate_str.rstrip("%")
      borrow_rate = float(rate_str) / 100.0
      i += 2
    elif arg.startswith("--deviation="):
      dev_str = arg.split("=", 1)[1].strip()
      dev_str = dev_str.rstrip("%")
      deviation = float(dev_str)
      i += 1
    elif arg == "--deviation" and i + 1 < len(args):
      dev_str = args[i + 1].strip()
      dev_str = dev_str.rstrip("%")
      deviation = float(dev_str)
      i += 2
    else:
      i += 1

  client = get_client()

  # Load dictionary
  df = client.get_df("dictionary")

  # Ensure 'key' column exists
  if "key" not in df.columns:
    df["key"] = df["Word"].astype(str).str.lower().str.replace(" ", "_")

  target_langs = get_target_languages(df, lang_flag)

  print("Target languages:", ", ".join(target_langs))
  print(f"Grammar deviation allowed: {deviation:.1f}% (to prevent duplicates)")
  if creole_from:
    print(f"Creole languages (blend all): {', '.join(creole_from)}")
  if root_from:
    print(f"Proto-root languages (use one randomly at {root_rate*100:.1f}% rate): {', '.join(root_from)}")
  if borrow_from:
    print(f"Borrowing from: {', '.join(borrow_from)} at {borrow_rate*100:.1f}% rate")

  # Walk through each word and each target language
  for idx, row in df.iterrows():
    word = str(row["Word"]).strip()
    if not word:
      continue

    # Sheet row index (header is row 1, df starts at row 0)
    row_index = idx + 2

    for lang in target_langs:
      current = row.get(lang, "")

      # Treat NaN as empty
      if isinstance(current, float) and math.isnan(current):
        print(f"[WARN] {word!r} [{lang}] → NaN detected")
        current = ""

      # Skip already-filled cells (unless --force is used)
      if isinstance(current, str) and current.strip():
        if not force:
          print(f"[SKIP] {word!r} [{lang}] → Already filled (use --force to overwrite)")
          continue
        else:
          print(f"[INFO] {word!r} [{lang}] → Overwriting existing value: {current!r}")

      # Check if we should borrow verbatim from another language
      lexeme = None
      if borrow_from and random.random() < borrow_rate:
        # Randomly select one of the borrow languages
        selected_borrow_lang = random.choice(borrow_from)
        borrowed_word = row.get(selected_borrow_lang, "")
        if isinstance(borrowed_word, str) and borrowed_word.strip():
          lexeme = borrowed_word.strip()
          print(f"[INFO] {word!r} [{lang}] → Borrowed verbatim from {selected_borrow_lang}: {lexeme!r}")
        else:
          print(f"[WARN] {word!r} [{lang}] → Cannot borrow: {selected_borrow_lang} not populated")

      # Generate lexeme via LLM if not borrowed
      if lexeme is None:
        try:
          root_words = {}

          # Creole behavior: Blend ALL words from ALL creole languages
          if creole_from:
            for creole_lang in creole_from:
              creole_val = row.get(creole_lang, "")
              if isinstance(creole_val, str) and creole_val.strip():
                root_words[creole_lang] = creole_val.strip()

          # Proto-root behavior: Use ONE random word as proto (either/or, not both)
          # Only applies with root_rate probability
          if root_from and random.random() < root_rate:
            # Randomly select ONE root language from the list
            selected_root_lang = random.choice(root_from)
            root_val = row.get(selected_root_lang, "")
            if isinstance(root_val, str) and root_val.strip():
              root_words[selected_root_lang] = root_val.strip()

          lexeme = llm_lexeme(word, lang, root_words=root_words if root_words else None, deviation=deviation)
          if root_words:
            root_str = ", ".join([f"{w!r} ({l})" for l, w in root_words.items()])
            print(f"[INFO] {word!r} [{lang}] → LLM generated {lexeme!r} (roots: {root_str})")
          else:
            print(f"[INFO] {word!r} [{lang}] → LLM generated {lexeme!r}")
        except Exception as e:
          print(f"[ERROR] {word!r} [{lang}] → LLM failed: {e}")
          continue

      # Compute sheet column (1-based)
      col_index = df.columns.get_loc(lang) + 1

      print(f"{word!r} [{lang}] → {lexeme!r}  (row {row_index}, col {col_index})")

      # Write back
      updates.append((row_index, col_index, lexeme))

  # Apply batched updates
  if updates:
    try:
      client.batch_update("dictionary", updates)
    except AttributeError:
      # Fallback if batch_update is not implemented: apply individually
      for r, c, v in updates:
        client.update_cell("dictionary", r, c, v)


if __name__ == "__main__":
  main()
