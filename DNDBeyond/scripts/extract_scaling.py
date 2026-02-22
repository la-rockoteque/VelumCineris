#!/usr/bin/env python3
"""
Extract Scaling Information to Separate Columns

This script parses the "Scaling" column from Orimond.csv and extracts
structured scaling data into separate columns:
- Scaling Level (e.g., "3", "5", "7")
- Scaling Modifier
- Scaling Effect (e.g., "16" for damage, "9" for healing)
- Scaling Dice Count (e.g., "2", "3")
- Scaling Dice Type (e.g., "6", "8", "10", "12")
- Fixed Value (e.g., "3", "5")

Usage:
    poetry run python DNDBeyond/scripts/extract_scaling.py

Output:
    Creates DNDBeyond/Orimond_with_scaling.csv with extracted columns
"""

import pandas as pd
import re
from pathlib import Path


def parse_dice(dice_str):
    """Parse dice notation like '2d6', '3d8+5' into components.

    Args:
        dice_str: String like "2d6", "3d8+5", "1d10"

    Returns:
        Tuple of (dice_count, dice_type, fixed_value)
    """
    if not dice_str or pd.isna(dice_str):
        return None, None, None

    # Match patterns like: 2d6, 3d8+5, 1d10, d6, d8+3
    match = re.match(r'(\d+)?d(\d+)(?:\+(\d+))?', str(dice_str).strip(), re.IGNORECASE)
    if match:
        dice_count = match.group(1) or "1"  # Default to 1 if not specified
        dice_type = match.group(2)
        fixed_value = match.group(3) or ""
        return dice_count, dice_type, fixed_value

    return None, None, None


def parse_scaling_text(scaling_text):
    """Parse scaling text to extract structured data.

    Handles patterns like:
    - "The damage increases by 1d6 for each slot level above 1st"
    - "Add 2d8 fire damage at 5th level, and 3d8 at 9th level"
    - "Healing increases by 1d8 for each slot level"
    - "3:2d6,5:3d6,7:4d6" (structured format)

    Returns:
        List of dicts with keys: level, modifier, effect, dice_count, dice_type, fixed_value
    """
    if not scaling_text or pd.isna(scaling_text):
        return []

    scaling_text = str(scaling_text).strip()
    results = []

    # Pattern 1: Structured format like "3:2d6,5:3d6,7:4d6"
    if ":" in scaling_text and ("," in scaling_text or "d" in scaling_text):
        # Try to parse structured format
        for pair in scaling_text.split(","):
            pair = pair.strip()
            if ":" in pair:
                try:
                    level_str, dice_str = pair.split(":", 1)
                    level = level_str.strip()
                    dice_count, dice_type, fixed_value = parse_dice(dice_str.strip())

                    if dice_count and dice_type:
                        results.append({
                            "level": level,
                            "modifier": "",
                            "effect": "16",  # Damage (default)
                            "dice_count": dice_count,
                            "dice_type": dice_type,
                            "fixed_value": fixed_value
                        })
                except (ValueError, AttributeError):
                    continue

    # Pattern 2: Text with dice notation
    # Look for patterns like "1d6", "2d8+3", etc.
    dice_matches = list(re.finditer(r'(\d+)?d(\d+)(?:\+(\d+))?', scaling_text, re.IGNORECASE))

    if dice_matches and not results:
        # Use the first dice match found
        match = dice_matches[0]
        dice_count = match.group(1) or "1"
        dice_type = match.group(2)
        fixed_value = match.group(3) or ""

        # Try to detect effect type from text
        effect = "16"  # Default: damage
        lower_text = scaling_text.lower()
        if "heal" in lower_text or "hit point" in lower_text:
            effect = "9"  # Healing
        elif "temp" in lower_text:
            effect = "10"  # Temporary hit points

        # Try to detect starting level
        level_match = re.search(r'(?:at |above |from )(\d+)(?:st|nd|rd|th)', scaling_text, re.IGNORECASE)
        level = level_match.group(1) if level_match else "1"

        results.append({
            "level": level,
            "modifier": "",
            "effect": effect,
            "dice_count": dice_count,
            "dice_type": dice_type,
            "fixed_value": fixed_value
        })

    return results


def extract_scaling_columns(input_csv, output_csv=None):
    """Extract scaling information from CSV into separate columns.

    Args:
        input_csv: Path to input CSV file
        output_csv: Path to output CSV file (defaults to input_with_scaling.csv)
    """
    # Read CSV
    print(f"Reading {input_csv}...")
    df = pd.read_csv(input_csv)

    print(f"Loaded {len(df)} rows")
    print(f"Columns: {len(df.columns)}")

    # Check if Scaling column exists
    if "Scaling" not in df.columns:
        print("Error: 'Scaling' column not found in CSV")
        return

    # Add new columns if they don't exist
    new_columns = [
        "Scaling Level",
        "Scaling Modifier",
        "Scaling Effect",
        "Scaling Dice Count",
        "Scaling Dice Type",
        "Fixed Value"
    ]

    for col in new_columns:
        if col not in df.columns:
            df[col] = ""

    # Process each row
    processed_count = 0
    spells_with_scaling = 0

    for idx, row in df.iterrows():
        scaling_text = row.get("Scaling")

        if pd.notna(scaling_text) and str(scaling_text).strip():
            # Parse scaling
            parsed = parse_scaling_text(scaling_text)

            if parsed:
                # Use the first parsed entry
                entry = parsed[0]
                df.at[idx, "Scaling Level"] = entry["level"]
                df.at[idx, "Scaling Modifier"] = entry["modifier"]
                df.at[idx, "Scaling Effect"] = entry["effect"]
                df.at[idx, "Scaling Dice Count"] = entry["dice_count"]
                df.at[idx, "Scaling Dice Type"] = entry["dice_type"]
                df.at[idx, "Fixed Value"] = entry["fixed_value"]

                processed_count += 1

                # Print examples of the first few
                if processed_count <= 5:
                    spell_name = row.get("Spell Name", "Unknown")
                    print(f"\nExample {processed_count}: {spell_name}")
                    print(f"  Original: {scaling_text[:80]}...")
                    print(f"  Extracted: Level {entry['level']}, {entry['dice_count']}d{entry['dice_type']}" +
                          (f"+{entry['fixed_value']}" if entry['fixed_value'] else ""))

            spells_with_scaling += 1

    # Save output
    if output_csv is None:
        output_csv = str(Path(input_csv).parent / (Path(input_csv).stem + "_with_scaling.csv"))

    print(f"\nSaving to {output_csv}...")
    df.to_csv(output_csv, index=False)

    print(f"\n✓ Complete!")
    print(f"  Total rows: {len(df)}")
    print(f"  Spells with Scaling column: {spells_with_scaling}")
    print(f"  Successfully extracted: {processed_count}")
    print(f"  Output: {output_csv}")

    # Show summary statistics
    if processed_count > 0:
        print(f"\n=== Scaling Statistics ===")
        print(f"Dice types used:")
        dice_types = df[df["Scaling Dice Type"] != ""]["Scaling Dice Type"].value_counts()
        for dice_type, count in dice_types.items():
            print(f"  d{dice_type}: {count} spells")


def main():
    """Main entry point."""
    # Default paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    input_csv = project_root / "DNDBeyond" / "Orimond.csv"

    if not input_csv.exists():
        print(f"Error: {input_csv} not found")
        print("\nUsage:")
        print("  poetry run python DNDBeyond/scripts/extract_scaling.py")
        print("\nMake sure you're running from the project root directory")
        return 1

    extract_scaling_columns(input_csv)
    return 0


if __name__ == "__main__":
    exit(main())
