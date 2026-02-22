#!/usr/bin/env python3
"""
Extract Modifier Information from Spell Descriptions

This script parses spell descriptions and extracts structured modifier data:
- Modifier Type (AC bonus, attack bonus, saving throw bonus, etc.)
- Modifier Subtype (specific ability/stat affected)
- Dice values (e.g., 1d4, 2d6)
- Fixed values (e.g., +2, +5)
- Duration information
- Usage restrictions

Usage:
    poetry run python DNDBeyond/scripts/extract_modifiers.py

Output:
    Updates Orimond.csv with extracted modifier columns
"""

import pandas as pd
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# D&D Beyond Modifier Type IDs
# These map to the form fields on D&D Beyond
MODIFIER_TYPES = {
    "ac": "1",  # Armor Class
    "armor class": "1",
    "attack": "2",  # Attack Roll
    "attack roll": "2",
    "damage": "3",  # Damage
    "save": "4",  # Saving Throw
    "saving throw": "4",
    "ability check": "5",  # Ability Check
    "skill": "6",  # Skill Check
    "speed": "7",  # Speed
    "initiative": "8",  # Initiative
    "hp": "9",  # Hit Points
    "hit points": "9",
    "temp hp": "10",  # Temporary Hit Points
    "temporary hit points": "10",
}

# Modifier Subtypes (abilities/stats)
MODIFIER_SUBTYPES = {
    "strength": "1",
    "str": "1",
    "dexterity": "2",
    "dex": "2",
    "constitution": "3",
    "con": "3",
    "intelligence": "4",
    "int": "4",
    "wisdom": "5",
    "wis": "5",
    "charisma": "6",
    "cha": "6",
}

# Duration units
DURATION_UNITS = {
    "round": "1",
    "rounds": "1",
    "minute": "2",
    "minutes": "2",
    "hour": "3",
    "hours": "3",
    "day": "4",
    "days": "4",
}


def parse_bonus_value(text: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Parse bonus value from text like '+2', '+1d4', '1d6+3'.

    Returns:
        Tuple of (dice_count, dice_type, fixed_value)
    """
    # Pattern: +1d4, 1d6, 2d8+3, +5, etc.
    bonus_pattern = r'\+?\s*(\d+)?d(\d+)(?:\s*\+\s*(\d+))?|\+(\d+)'
    match = re.search(bonus_pattern, text)

    if match:
        if match.group(4):  # Just a fixed bonus like "+2"
            return None, None, match.group(4)
        else:  # Dice notation
            dice_count = match.group(1) or "1"
            dice_type = match.group(2)
            fixed_value = match.group(3) or ""
            return dice_count, dice_type, fixed_value

    return None, None, None


def extract_duration(text: str) -> Tuple[Optional[str], Optional[str]]:
    """Extract duration from text like '1 minute', '10 rounds', '1 hour'.

    Returns:
        Tuple of (duration_amount, duration_unit_id)
    """
    duration_pattern = r'(?:for|lasts?)\s+(\d+)\s+(round|minute|hour|day)s?'
    match = re.search(duration_pattern, text.lower())

    if match:
        amount = match.group(1)
        unit = match.group(2)
        unit_id = DURATION_UNITS.get(unit, "")
        return amount, unit_id

    # Check for "until the spell ends" or "for the duration"
    if "until the spell ends" in text.lower() or "for the duration" in text.lower():
        return "", ""  # Empty means spell duration

    return None, None


def extract_modifiers_from_description(description: str) -> List[Dict]:
    """Extract modifier data from spell description.

    Args:
        description: The spell description text

    Returns:
        List of modifier dicts with extracted data
    """
    if not description or pd.isna(description):
        return []

    description = str(description).lower()
    modifiers = []

    # Pattern 1: AC bonus
    # "gains a +2 bonus to AC", "bonus to AC equal to", "+1 to AC"
    ac_patterns = [
        r'(\+?\d+d?\d*)\s+(?:bonus\s+)?to\s+(?:armor\s+class|ac)',
        r'(?:armor\s+class|ac).*?(?:increases?|bonus).*?by\s+(\+?\d+d?\d*)',
        r'gain(?:s)?\s+(\+?\d+d?\d*)\s+(?:to\s+)?(?:armor\s+class|ac)',
    ]

    for pattern in ac_patterns:
        match = re.search(pattern, description)
        if match:
            bonus_text = match.group(1)
            dice_count, dice_type, fixed_value = parse_bonus_value(bonus_text)
            duration_amount, duration_unit = extract_duration(description)

            modifiers.append({
                "type": "1",  # AC
                "subtype": "",
                "dice_count": dice_count or "",
                "dice_type": dice_type or "",
                "fixed_value": fixed_value or "",
                "duration": duration_amount or "",
                "duration_unit": duration_unit or "",
                "details": match.group(0)[:100]
            })
            break  # Take first match

    # Pattern 2: Attack roll bonus
    # "bonus to attack rolls", "+1 to hit"
    attack_patterns = [
        r'(\+?\d+d?\d*)\s+(?:bonus\s+)?to\s+(?:attack\s+rolls?|hit)',
        r'attack\s+rolls?.*?(?:increases?|bonus).*?by\s+(\+?\d+d?\d*)',
    ]

    for pattern in attack_patterns:
        match = re.search(pattern, description)
        if match:
            bonus_text = match.group(1)
            dice_count, dice_type, fixed_value = parse_bonus_value(bonus_text)
            duration_amount, duration_unit = extract_duration(description)

            modifiers.append({
                "type": "2",  # Attack
                "subtype": "",
                "dice_count": dice_count or "",
                "dice_type": dice_type or "",
                "fixed_value": fixed_value or "",
                "duration": duration_amount or "",
                "duration_unit": duration_unit or "",
                "details": match.group(0)[:100]
            })
            break

    # Pattern 3: Damage bonus
    # "deals an extra 1d6 damage", "additional 2d8"
    damage_patterns = [
        r'(?:extra|additional|bonus)\s+(\d+d\d+(?:\+\d+)?)\s+(?:\w+\s+)?damage',
        r'(\d+d\d+(?:\+\d+)?)\s+(?:extra|additional|bonus)\s+damage',
    ]

    for pattern in damage_patterns:
        match = re.search(pattern, description)
        if match:
            bonus_text = match.group(1)
            dice_count, dice_type, fixed_value = parse_bonus_value(bonus_text)
            duration_amount, duration_unit = extract_duration(description)

            modifiers.append({
                "type": "3",  # Damage
                "subtype": "",
                "dice_count": dice_count or "",
                "dice_type": dice_type or "",
                "fixed_value": fixed_value or "",
                "duration": duration_amount or "",
                "duration_unit": duration_unit or "",
                "details": match.group(0)[:100]
            })
            break

    # Pattern 4: Saving throw bonus
    # "bonus to Dexterity saving throws", "advantage on Wisdom saves"
    save_patterns = [
        r'(\+?\d+d?\d*)\s+(?:bonus\s+)?to\s+(strength|dexterity|constitution|intelligence|wisdom|charisma|str|dex|con|int|wis|cha)\s+sav(?:ing|es?)',
        r'(strength|dexterity|constitution|intelligence|wisdom|charisma|str|dex|con|int|wis|cha)\s+sav(?:ing|es?).*?(?:bonus|increases?).*?(\+?\d+d?\d*)',
    ]

    for pattern in save_patterns:
        match = re.search(pattern, description)
        if match:
            if match.lastindex == 2:
                bonus_text = match.group(1) if match.group(1).startswith('+') or 'd' in match.group(1) else match.group(2)
                ability = match.group(2) if match.group(1).startswith('+') or 'd' in match.group(1) else match.group(1)
            else:
                bonus_text = match.group(1)
                ability = match.group(2)

            dice_count, dice_type, fixed_value = parse_bonus_value(bonus_text) if bonus_text else (None, None, None)
            subtype_id = MODIFIER_SUBTYPES.get(ability.lower(), "")
            duration_amount, duration_unit = extract_duration(description)

            modifiers.append({
                "type": "4",  # Saving Throw
                "subtype": subtype_id,
                "dice_count": dice_count or "",
                "dice_type": dice_type or "",
                "fixed_value": fixed_value or "",
                "duration": duration_amount or "",
                "duration_unit": duration_unit or "",
                "details": match.group(0)[:100]
            })
            break

    # Pattern 5: Speed bonus
    # "speed increases by 10 feet", "gain 20 feet of movement"
    speed_patterns = [
        r'speed.*?(?:increases?|bonus).*?by\s+(\d+)\s*(?:feet|ft)',
        r'gain(?:s)?\s+(\d+)\s*(?:feet|ft).*?(?:speed|movement)',
    ]

    for pattern in speed_patterns:
        match = re.search(pattern, description)
        if match:
            fixed_value = match.group(1)
            duration_amount, duration_unit = extract_duration(description)

            modifiers.append({
                "type": "7",  # Speed
                "subtype": "",
                "dice_count": "",
                "dice_type": "",
                "fixed_value": fixed_value,
                "duration": duration_amount or "",
                "duration_unit": duration_unit or "",
                "details": match.group(0)[:100]
            })
            break

    # Pattern 6: Temporary HP
    # "gains 5 temporary hit points", "1d8 temporary hp"
    temp_hp_patterns = [
        r'gain(?:s)?\s+(\d+d?\d*(?:\+\d+)?)\s+temporary\s+hit\s+points',
        r'(\d+d?\d*(?:\+\d+)?)\s+temp(?:orary)?\s+hp',
    ]

    for pattern in temp_hp_patterns:
        match = re.search(pattern, description)
        if match:
            bonus_text = match.group(1)
            dice_count, dice_type, fixed_value = parse_bonus_value(bonus_text)

            modifiers.append({
                "type": "10",  # Temporary HP
                "subtype": "",
                "dice_count": dice_count or "",
                "dice_type": dice_type or "",
                "fixed_value": fixed_value or "",
                "duration": "",
                "duration_unit": "",
                "details": match.group(0)[:100]
            })
            break

    return modifiers


def extract_modifiers_from_csv(input_csv: str, output_csv: str = None):
    """Extract modifier information from CSV and add to modifier columns.

    Args:
        input_csv: Path to input CSV
        output_csv: Path to output CSV (defaults to input file)
    """
    print(f"Reading {input_csv}...")
    df = pd.read_csv(input_csv)

    print(f"Loaded {len(df)} rows")

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
        "Modifiers JSON": "",  # Store all modifiers as JSON
    }

    for col, default in modifier_columns.items():
        if col not in df.columns:
            df[col] = default
        # Convert to object dtype to avoid dtype warnings
        df[col] = df[col].astype(object)

    # Process each row
    processed = 0
    found_modifiers = 0

    for idx, row in df.iterrows():
        description = row.get("Description", "")

        # Skip if already has modifier data
        if pd.notna(row.get("Modifier Type")) and str(row.get("Modifier Type")).strip():
            continue

        # Extract modifiers
        modifiers = extract_modifiers_from_description(description)

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

            # Show first few examples
            if found_modifiers <= 5:
                spell_name = row.get("Spell Name", "Unknown")
                print(f"\nExample {found_modifiers}: {spell_name}")
                print(f"  Type: {mod['type']} ({['', 'AC', 'Attack', 'Damage', 'Save', 'Ability Check', 'Skill', 'Speed', 'Initiative', 'HP', 'Temp HP'][int(mod['type']) if mod['type'] else 0]})")
                if mod['subtype']:
                    print(f"  Subtype: {mod['subtype']}")
                if mod['dice_count'] and mod['dice_type']:
                    print(f"  Dice: {mod['dice_count']}d{mod['dice_type']}" + (f"+{mod['fixed_value']}" if mod['fixed_value'] else ""))
                elif mod['fixed_value']:
                    print(f"  Fixed: +{mod['fixed_value']}")
                if mod['duration']:
                    print(f"  Duration: {mod['duration']} ({mod['duration_unit']})")
                print(f"  Matched: {mod['details']}")

        processed += 1

    # Save
    if output_csv is None:
        output_csv = input_csv

    print(f"\nSaving to {output_csv}...")
    df.to_csv(output_csv, index=False)

    print(f"\n✓ Complete!")
    print(f"  Total rows: {len(df)}")
    print(f"  Rows processed: {processed}")
    print(f"  Modifiers found: {found_modifiers}")
    print(f"  Output: {output_csv}")

    # Statistics
    if found_modifiers > 0:
        print(f"\n=== Modifier Statistics ===")
        type_counts = df[df["Modifier Type"] != ""]["Modifier Type"].value_counts()
        type_names = ["", "AC", "Attack", "Damage", "Save", "Ability Check", "Skill", "Speed", "Initiative", "HP", "Temp HP"]
        for type_id, count in type_counts.items():
            type_id_int = int(type_id) if str(type_id).isdigit() else 0
            type_name = type_names[type_id_int] if type_id_int < len(type_names) else "Unknown"
            print(f"  {type_name}: {count} spells")


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    input_csv = project_root / "DNDBeyond" / "Orimond.csv"

    if not input_csv.exists():
        print(f"Error: {input_csv} not found")
        return 1

    extract_modifiers_from_csv(str(input_csv))
    return 0


if __name__ == "__main__":
    exit(main())
