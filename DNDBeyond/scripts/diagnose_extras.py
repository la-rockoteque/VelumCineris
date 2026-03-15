#!/usr/bin/env python3
"""Diagnostic script to check why modifiers/conditions/scaling are failing."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from Spreadsheet.sheets import fantasy_sheets
from FiveETools.core.fantasy.spells import spells_list
from DNDBeyond.core.Helpers import (
    extract_spell_conditions,
    extract_spell_modifiers,
    extract_spell_scaling,
    parse_dice_scaling,
    normalize_ddb_id
)

SPELLS_GID = "625265890"

print("=" * 80)
print("MODIFIERS/CONDITIONS/SCALING DIAGNOSTIC")
print("=" * 80)
print()

# Check spreadsheet columns
print("1. Checking Google Sheets columns...")
print("-" * 80)
df = fantasy_sheets.get_sheet(SPELLS_GID)
required_columns = [
    "Condition",
    "Scaling",
    "Modifiers JSON",
    "Modifier Type",
    "Modifier Subtype",
    "Modifier Dice Count",
    "Modifier Dice Type",
    "Modifier Fixed Value",
    "Modifier Duration",
    "Modifier Duration Unit"
]

missing_columns = []
present_columns = []
for col in required_columns:
    if col in df.columns:
        # Count non-empty values
        non_empty = df[col].notna().sum()
        filled_count = (df[col].astype(str).str.strip() != "").sum()
        present_columns.append(col)
        status = "✓ PRESENT"
        if filled_count == 0:
            status += " (but all empty)"
        else:
            status += f" ({filled_count} filled)"
        print(f"  {status:50s} - {col}")
    else:
        missing_columns.append(col)
        print(f"  ✗ MISSING{'':<40s} - {col}")

print()
if missing_columns:
    print(f"⚠️  Missing {len(missing_columns)} columns. These need to be added to your spreadsheet.")
    print()

# Check spell data
print("2. Checking loaded spell data...")
print("-" * 80)
print(f"Total spells loaded: {len(spells_list)}")

# Sample a few spells to check data structure
sample_spells = spells_list[:5]
for i, spell in enumerate(sample_spells, 1):
    spell_name = spell.get("name", "Unknown")
    print(f"\nSpell {i}: {spell_name}")

    # Check for DDB-specific fields
    has_condition = "ddb_condition" in spell and spell.get("ddb_condition", "").strip()
    has_modifiers_json = "ddb_modifiers_json" in spell and spell.get("ddb_modifiers_json", "").strip()
    has_modifier_type = "ddb_modifier_type" in spell and spell.get("ddb_modifier_type", "").strip()
    has_scaling = "ddb_scaling" in spell and spell.get("ddb_scaling", "").strip()

    print(f"  Condition field: {'✓ Present' if has_condition else '✗ Empty/Missing'}")
    if has_condition:
        print(f"    Value: {spell.get('ddb_condition', '')[:100]}")

    print(f"  Modifiers JSON: {'✓ Present' if has_modifiers_json else '✗ Empty/Missing'}")
    if has_modifiers_json:
        print(f"    Value: {spell.get('ddb_modifiers_json', '')[:100]}")

    print(f"  Modifier Type: {'✓ Present' if has_modifier_type else '✗ Empty/Missing'}")
    if has_modifier_type:
        print(f"    Value: {spell.get('ddb_modifier_type', '')[:100]}")

    print(f"  Scaling field: {'✓ Present' if has_scaling else '✗ Empty/Missing'}")
    if has_scaling:
        print(f"    Value: {spell.get('ddb_scaling', '')[:100]}")

print()
print("3. Testing extraction functions...")
print("-" * 80)

# Test with a spell that has data
for spell in spells_list[:10]:
    spell_name = spell.get("name", "Unknown")

    # Try extracting
    conditions = extract_spell_conditions(spell)
    modifiers = extract_spell_modifiers(spell)
    scaling_text = extract_spell_scaling(spell)
    higher_levels = parse_dice_scaling(scaling_text) if scaling_text else []

    if conditions or modifiers or higher_levels:
        print(f"\n✓ {spell_name}")
        if conditions:
            print(f"  → {len(conditions)} condition(s)")
            for cond in conditions:
                print(f"     - Condition ID: {cond.get('condition')}")
        if modifiers:
            print(f"  → {len(modifiers)} modifier(s)")
            for mod in modifiers:
                print(f"     - Type: {mod.get('type')}, Subtype: {mod.get('subtype')}")
        if higher_levels:
            print(f"  → {len(higher_levels)} higher level(s)")

print()
print("4. Checking spells with DDB IDs...")
print("-" * 80)

# Get spells with DDB IDs
df_spells = fantasy_sheets.get_sheet(SPELLS_GID)
spells_with_ddb = 0
spells_with_extras_data = 0

for _, row in df_spells.iterrows():
    spell_name = row.get('Spell Name')
    ddb_id = normalize_ddb_id(row.get('DDB'))

    if ddb_id:
        spells_with_ddb += 1

        # Check if this spell has any extras data
        has_condition = row.get('Condition', '') and str(row.get('Condition', '')).strip()
        has_modifiers_json = row.get('Modifiers JSON', '') and str(row.get('Modifiers JSON', '')).strip()
        has_modifier_type = row.get('Modifier Type', '') and str(row.get('Modifier Type', '')).strip()
        has_scaling = row.get('Scaling', '') and str(row.get('Scaling', '')).strip()

        if has_condition or has_modifiers_json or has_modifier_type or has_scaling:
            spells_with_extras_data += 1

print(f"Spells with DDB IDs: {spells_with_ddb}")
print(f"Spells with extras data (conditions/modifiers/scaling): {spells_with_extras_data}")

if spells_with_ddb > 0 and spells_with_extras_data == 0:
    print()
    print("⚠️  WARNING: You have spells synced to DDB but no extras data!")
    print("   This means your spreadsheet is missing the required columns")
    print("   or the columns are empty.")

print()
print("=" * 80)
print("SUMMARY")
print("=" * 80)

if missing_columns:
    print("❌ MISSING COLUMNS:")
    print(f"   Add these columns to your Google Sheets: {', '.join(missing_columns)}")
    print()

if spells_with_extras_data == 0:
    print("❌ NO EXTRAS DATA:")
    print("   Your spreadsheet columns exist but are empty.")
    print("   You need to:")
    print("   1. Run the LLM extraction script to populate modifiers:")
    print("      poetry run python DNDBeyond/scripts/extract_modifiers_llm.py --google-sheets")
    print("   2. Manually fill in Condition and Scaling columns for spells that need them")
    print()
else:
    print(f"✓ {spells_with_extras_data} spells have extras data")
    print()

print("TIP: To add missing columns, the sync will create them automatically")
print("     on the next run, but they will be empty initially.")
