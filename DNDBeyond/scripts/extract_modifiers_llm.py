#!/usr/bin/env python3
"""
Extract Modifier Information using LLM

This script uses a local LLM (Ollama) to parse spell descriptions and extract
structured modifier data with higher accuracy than regex pattern matching.

Usage:
    poetry run python DNDBeyond/scripts/extract_modifiers_llm.py

Requirements:
    - Ollama installed and running (ollama.ai)
    - Model pulled: ollama pull llama3

Output:
    Updates Orimond.csv with extracted modifier columns
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pandas as pd
import json
from typing import Dict, List, Optional
import ollama


# D&D Beyond Modifier Type IDs
MODIFIER_TYPES = {
    "ac": "1",
    "armor class": "1",
    "attack": "2",
    "attack roll": "2",
    "damage": "3",
    "save": "4",
    "saving throw": "4",
    "ability check": "5",
    "skill": "6",
    "speed": "7",
    "initiative": "8",
    "hp": "9",
    "hit points": "9",
    "temp hp": "10",
    "temporary hit points": "10",
}

MODIFIER_SUBTYPES = {
    "strength": "1",
    "dexterity": "2",
    "constitution": "3",
    "intelligence": "4",
    "wisdom": "5",
    "charisma": "6",
}

DURATION_UNITS = {
    "round": "1",
    "minute": "2",
    "hour": "3",
    "day": "4",
}


def create_extraction_prompt(spell_name: str, description: str, duration: str = "") -> str:
    """Create a prompt for the LLM to extract modifier information."""
    return f"""You are analyzing D&D 5e spell descriptions to extract game mechanical modifiers.

Spell: {spell_name}
Description: {description}
Duration: {duration}

Extract ALL modifiers from this spell. A modifier is any bonus or penalty that affects:
- AC (Armor Class)
- Attack rolls
- Damage
- Saving throws
- Ability checks
- Skills
- Speed
- Initiative
- Hit points
- Temporary hit points

For each modifier found, provide:
1. **type**: The modifier type (ac, attack, damage, save, ability check, skill, speed, initiative, hp, temp hp)
2. **subtype**: For saves/checks, specify which ability (strength, dexterity, constitution, intelligence, wisdom, charisma)
3. **dice_count**: Number of dice (e.g., "1", "2", "3") or empty if fixed value only
4. **dice_type**: Dice type (e.g., "4", "6", "8", "10", "12") or empty if fixed value only
5. **fixed_value**: Fixed bonus/penalty (e.g., "2", "5") or empty if dice only
6. **duration_amount**: How long the modifier lasts (e.g., "1", "10", "24") or empty for spell duration
7. **duration_unit**: Unit of time (round, minute, hour, day) or empty for spell duration

Respond ONLY with valid JSON array. If no modifiers found, return empty array [].

Example output format:
[
  {{
    "type": "ac",
    "subtype": "",
    "dice_count": "",
    "dice_type": "",
    "fixed_value": "2",
    "duration_amount": "",
    "duration_unit": "",
    "details": "gains a +2 bonus to AC"
  }},
  {{
    "type": "damage",
    "subtype": "",
    "dice_count": "1",
    "dice_type": "6",
    "fixed_value": "",
    "duration_amount": "",
    "duration_unit": "",
    "details": "deals an extra 1d6 fire damage"
  }}
]

JSON:"""


def _save_to_google_sheets(df, fantasy_sheets, gid):
    """Save modifier data back to Google Sheets.

    Args:
        df: DataFrame with modifier columns
        fantasy_sheets: Google Sheets client
        gid: Sheet GID
    """
    # Update each modifier column separately
    columns_to_update = [
        "Modifiers JSON",
        "Modifier Type",
        "Modifier Subtype",
        "Modifier Dice Count",
        "Modifier Dice Type",
        "Modifier Fixed Value",
        "Modifier Duration",
        "Modifier Duration Unit",
        "Modifier Details"
    ]

    total_updated = 0
    for column in columns_to_update:
        if column not in df.columns:
            continue

        # Get all rows with non-empty values for this column
        updates = []
        for idx, row in df.iterrows():
            spell_name = row.get("Spell Name")
            value = row.get(column)
            if spell_name and pd.notna(value) and str(value).strip():
                updates.append({
                    'match_value': spell_name,
                    'update_column': column,
                    'update_value': str(value)
                })

        if updates:
            try:
                result = fantasy_sheets.batch_update_cells_by_row_match(gid, "Spell Name", updates)
                success_count = sum(1 for v in result.values() if v)
                total_updated = max(total_updated, success_count)
                print(f"  ✓ Updated {column}: {success_count} spells")
            except Exception as e:
                print(f"  ✗ Failed to update {column}: {e}")

    print(f"  ✓ Total spells updated: {total_updated}")


def extract_modifiers_with_llm(
    spell_name: str,
    description: str,
    duration: str = "",
    model: str = "llama3"
) -> List[Dict]:
    """Extract modifiers using LLM.

    Args:
        spell_name: Name of the spell
        description: Spell description text
        duration: Duration string (optional)
        model: Ollama model to use

    Returns:
        List of modifier dicts
    """
    if not description or pd.isna(description):
        return []

    prompt = create_extraction_prompt(spell_name, str(description), str(duration))

    try:
        # Call Ollama
        response = ollama.generate(
            model=model,
            prompt=prompt,
            options={
                "temperature": 0.1,  # Low temperature for consistent extraction
                "top_p": 0.9,
            }
        )

        response_text = response['response'].strip()

        # Try to extract JSON from response
        # Sometimes the model includes explanation before/after JSON
        json_start = response_text.find('[')
        json_end = response_text.rfind(']') + 1

        if json_start >= 0 and json_end > json_start:
            json_text = response_text[json_start:json_end]
            modifiers = json.loads(json_text)

            # Validate and normalize the extracted data
            normalized = []
            for mod in modifiers:
                # Map type to ID
                mod_type = mod.get("type", "").lower().strip()
                type_id = MODIFIER_TYPES.get(mod_type, "")

                if not type_id:
                    continue  # Skip invalid types

                # Map subtype to ID
                subtype = mod.get("subtype", "").lower().strip()
                subtype_id = MODIFIER_SUBTYPES.get(subtype, "")

                # Map duration unit to ID
                duration_unit = mod.get("duration_unit", "").lower().strip()
                duration_unit_id = DURATION_UNITS.get(duration_unit, "")

                normalized.append({
                    "type": type_id,
                    "subtype": subtype_id,
                    "dice_count": str(mod.get("dice_count", "")).strip(),
                    "dice_type": str(mod.get("dice_type", "")).strip(),
                    "fixed_value": str(mod.get("fixed_value", "")).strip(),
                    "duration": str(mod.get("duration_amount", "")).strip(),
                    "duration_unit": duration_unit_id,
                    "details": str(mod.get("details", ""))[:100]
                })

            return normalized

        return []

    except json.JSONDecodeError as e:
        print(f"  ⚠ JSON parse error for '{spell_name}': {e}")
        print(f"  Response: {response_text[:200]}...")
        return []
    except Exception as e:
        print(f"  ⚠ LLM error for '{spell_name}': {e}")
        return []


def extract_modifiers_from_csv(
    input_csv: str,
    output_csv: str = None,
    model: str = "llama3",
    batch_size: int = 10,
    use_google_sheets: bool = False,
    gid: str = None
):
    """Extract modifier information from CSV or Google Sheets using LLM.

    Args:
        input_csv: Path to input CSV (or sheet name if use_google_sheets=True)
        output_csv: Path to output CSV (defaults to input file)
        model: Ollama model name
        batch_size: How often to save progress
        use_google_sheets: Read/write directly to Google Sheets
        gid: Google Sheet GID (required if use_google_sheets=True)
    """
    if use_google_sheets:
        if not gid:
            print("Error: gid is required when use_google_sheets=True")
            return

        print(f"Reading from Google Sheets (GID: {gid})...")
        from FiveETools.core.Helpers.gsheets_client import fantasy_sheets
        df = fantasy_sheets.get_sheet(gid)
    else:
        print(f"Reading {input_csv}...")
        df = pd.read_csv(input_csv)

    print(f"Loaded {len(df)} rows")
    print(f"Using model: {model}")

    # Check required columns
    if "Description" not in df.columns:
        print("Error: 'Description' column not found")
        return

    # Ensure modifier columns exist with proper string dtype
    modifier_columns = {
        "Modifier Details": "",
        "Modifier Type": "",
        "Modifier Subtype": "",
        "Modifier Dice Count": "",
        "Modifier Dice Type": "",
        "Modifier Fixed Value": "",
        "Modifier Duration": "",
        "Modifier Duration Unit": "",
        "Modifiers JSON": "",  # NEW: Store all modifiers as JSON
    }

    for col, default in modifier_columns.items():
        if col not in df.columns:
            df[col] = default
        df[col] = df[col].astype(object)

    # Process each row
    processed = 0
    found_modifiers = 0
    skipped = 0

    for idx, row in df.iterrows():
        # Skip if already has modifier data
        if pd.notna(row.get("Modifier Type")) and str(row.get("Modifier Type")).strip():
            skipped += 1
            continue

        spell_name = row.get("Spell Name", "Unknown")
        description = row.get("Description", "")
        duration = row.get("Duration", "")

        print(f"\n[{processed + 1}] Processing: {spell_name}")

        # Extract modifiers using LLM
        modifiers = extract_modifiers_with_llm(spell_name, description, duration, model)

        if modifiers:
            # Store ALL modifiers as JSON
            df.at[idx, "Modifiers JSON"] = json.dumps(modifiers)

            # Also store first modifier in individual columns (for readability)
            mod = modifiers[0]
            df.at[idx, "Modifier Details"] = mod["details"]
            df.at[idx, "Modifier Type"] = mod["type"]
            df.at[idx, "Modifier Subtype"] = mod["subtype"]
            df.at[idx, "Modifier Dice Count"] = mod["dice_count"]
            df.at[idx, "Modifier Dice Type"] = mod["dice_type"]
            df.at[idx, "Modifier Fixed Value"] = mod["fixed_value"]
            df.at[idx, "Modifier Duration"] = mod["duration"]
            df.at[idx, "Modifier Duration Unit"] = mod["duration_unit"]

            found_modifiers += 1

            # Show what was found
            type_names = ["", "AC", "Attack", "Damage", "Save", "Ability Check",
                         "Skill", "Speed", "Initiative", "HP", "Temp HP"]
            type_idx = int(mod['type']) if mod['type'] else 0
            type_name = type_names[type_idx] if type_idx < len(type_names) else "Unknown"

            print(f"  ✓ Found {type_name}: {mod['details'][:60]}...")
            if len(modifiers) > 1:
                print(f"    ✓ Stored {len(modifiers)} total modifiers in JSON")
                # Show all modifiers
                for i, m in enumerate(modifiers[1:], 2):
                    m_type_idx = int(m['type']) if m['type'] else 0
                    m_type_name = type_names[m_type_idx] if m_type_idx < len(type_names) else "Unknown"
                    print(f"      {i}. {m_type_name}: {m['details'][:50]}...")
        else:
            print(f"  - No modifiers found")

        processed += 1

        # Save progress periodically
        if processed % batch_size == 0:
            if use_google_sheets:
                print(f"\n💾 Saving progress to Google Sheets...")
                _save_to_google_sheets(df, fantasy_sheets, gid)
            else:
                output_path = output_csv or input_csv
                print(f"\n💾 Saving progress to {output_path}...")
                df.to_csv(output_path, index=False)

    # Final save
    if use_google_sheets:
        print(f"\n💾 Saving final results to Google Sheets...")
        _save_to_google_sheets(df, fantasy_sheets, gid)
    else:
        output_path = output_csv or input_csv
        print(f"\n💾 Saving final results to {output_path}...")
        df.to_csv(output_path, index=False)

    print(f"\n✓ Complete!")
    print(f"  Total rows: {len(df)}")
    print(f"  Already processed (skipped): {skipped}")
    print(f"  Newly processed: {processed}")
    print(f"  Modifiers found: {found_modifiers}")
    print(f"  Output: {output_path}")

    # Statistics
    if found_modifiers > 0:
        print(f"\n=== Modifier Statistics ===")
        type_counts = df[df["Modifier Type"] != ""]["Modifier Type"].value_counts()
        type_names = ["", "AC", "Attack", "Damage", "Save", "Ability Check",
                     "Skill", "Speed", "Initiative", "HP", "Temp HP"]
        for type_id, count in type_counts.items():
            type_id_int = int(type_id) if str(type_id).isdigit() else 0
            type_name = type_names[type_id_int] if type_id_int < len(type_names) else "Unknown"
            print(f"  {type_name}: {count} spells")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Extract spell modifiers using LLM")
    parser.add_argument(
        "--model",
        default="llama3",
        help="Ollama model to use (default: llama3)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=10,
        help="Save progress every N spells (default: 10)"
    )
    parser.add_argument(
        "--input",
        help="Input CSV path (default: DNDBeyond/Orimond.csv)"
    )
    parser.add_argument(
        "--google-sheets",
        action="store_true",
        help="Read/write directly to Google Sheets instead of CSV"
    )
    parser.add_argument(
        "--gid",
        default="625265890",
        help="Google Sheet GID (default: 625265890 for fantasy spells)"
    )

    args = parser.parse_args()

    # Default paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    input_csv = args.input or (project_root / "DNDBeyond" / "Orimond.csv")
    use_google_sheets = args.google_sheets
    gid = args.gid if use_google_sheets else None

    if not Path(input_csv).exists():
        print(f"Error: {input_csv} not found")
        print("\nMake sure Ollama is running:")
        print("  ollama serve")
        print("\nAnd pull the model:")
        print(f"  ollama pull {args.model}")
        return 1

    # Check if Ollama is available
    try:
        ollama.list()
        print("✓ Ollama is running")
    except Exception as e:
        print(f"Error: Cannot connect to Ollama")
        print(f"Make sure Ollama is running: ollama serve")
        print(f"Error details: {e}")
        return 1

    if use_google_sheets:
        print("✓ Google Sheets mode enabled")
        print(f"  GID: {gid}")

    extract_modifiers_from_csv(
        str(input_csv),
        model=args.model,
        batch_size=args.batch_size,
        use_google_sheets=use_google_sheets,
        gid=gid
    )
    return 0


if __name__ == "__main__":
    exit(main())
