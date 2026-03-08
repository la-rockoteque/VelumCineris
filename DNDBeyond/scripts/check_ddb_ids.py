#!/usr/bin/env python3
"""Check DDB ID status in spreadsheet."""

import sys
from pathlib import Path

# Add repository root to path
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from FiveETools.core.Helpers.gsheets_client import fantasy_sheets
from DNDBeyond.core.Helpers import normalize_ddb_id

SPELLS_GID = "625265890"

print("=" * 80)
print("DDB ID CHECK")
print("=" * 80)
print()

# Load spreadsheet
print("Loading spreadsheet...")
df = fantasy_sheets.get_sheet(SPELLS_GID)
print(f"✓ Loaded {len(df)} rows")
print()

# Check DDB column
if 'DDB' not in df.columns:
    print("❌ ERROR: 'DDB' column not found!")
    print(f"Available columns: {list(df.columns)[:20]}...")
    sys.exit(1)

# Count spells with/without DDB IDs
with_ddb = 0
without_ddb = 0
empty_names = 0

for _, row in df.iterrows():
    spell_name = row.get('Spell Name')
    if not spell_name or str(spell_name).strip() == "":
        empty_names += 1
        continue

    ddb_id = normalize_ddb_id(row.get('DDB'))
    if ddb_id:
        with_ddb += 1
    else:
        without_ddb += 1

print(f"Spells WITH DDB IDs:    {with_ddb}")
print(f"Spells WITHOUT DDB IDs: {without_ddb}")
print(f"Empty spell names:      {empty_names}")
print()

# Show first 10 spells without DDB IDs
print("First 10 spells WITHOUT DDB IDs:")
print("-" * 80)
count = 0
for _, row in df.iterrows():
    spell_name = row.get('Spell Name')
    if not spell_name or str(spell_name).strip() == "":
        continue

    ddb_id = normalize_ddb_id(row.get('DDB'))
    if not ddb_id:
        count += 1
        print(f"{count}. {spell_name}")
        if count >= 10:
            break

if without_ddb > 10:
    print(f"... and {without_ddb - 10} more")

print()
print("=" * 80)
print("If spells show as 'WITHOUT DDB IDs' but you just synced them,")
print("check the Cell 13 output for spreadsheet update errors.")
print("=" * 80)
