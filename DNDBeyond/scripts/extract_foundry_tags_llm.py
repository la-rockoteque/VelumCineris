#!/usr/bin/env python3
"""
Extract Foundry Tags using LLM

This script uses a local LLM (Ollama) to infer Foundry Tags
based on spell description and a fixed allowed tag list.

Usage:
    poetry run python DNDBeyond/scripts/extract_foundry_tags_llm.py

Requirements:
    - Ollama installed and running (ollama.ai)
    - Model pulled: ollama pull llama3

Output:
    Updates Orimond.csv Foundry Tag column
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional
import json

# Add project root to Python path
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pandas as pd
import ollama


ALLOWED_TAGS = [
    "Healing",
    "Grants Temporary Hit Points",
    "Requires Sight",
    "Permanent Effects",
    "Summons Creature",
    "Modifies AC",
    "Teleportation",
    "Creates Sunlight",
    "Creates Light",
    "Uses Bonus Action",
    "Plane Shifting",
    "Difficult Terrain",
    "Affects Objects",
    "Grants Advantage",
]


def _parse_json_object(response_text: str) -> Optional[Dict]:
    json_start = response_text.find("{")
    json_end = response_text.rfind("}") + 1
    if json_start < 0 or json_end <= json_start:
        return None
    json_text = response_text[json_start:json_end]
    return json.loads(json_text)


def create_foundry_tags_prompt(
    spell_name: str,
    description: str,
    theme: str = "",
    tag: str = "",
    school: str = "",
    level: str = "",
    casting_time: str = "",
    duration: str = "",
    allowed_tags: List[str] = None,
) -> str:
    allowed_tags = allowed_tags or ALLOWED_TAGS
    return f"""You are classifying D&D 5e spells into Foundry tags.

Spell: {spell_name}
Description: {description}
Theme: {theme}
Tag: {tag}
School: {school}
Level: {level}
Casting Time: {casting_time}
Duration: {duration}

Choose ONLY from the allowed tags below. Select all that clearly apply.
Allowed tags:
{", ".join(allowed_tags)}

Return ONLY valid JSON:
{{"tags":["Tag A","Tag B"]}}

JSON:"""


def extract_tags_with_llm(
    spell_name: str,
    description: str,
    theme: str = "",
    tag: str = "",
    school: str = "",
    level: str = "",
    casting_time: str = "",
    duration: str = "",
    model: str = "llama3",
    allowed_tags: List[str] = None,
) -> List[str]:
    if not description or pd.isna(description):
        return []

    prompt = create_foundry_tags_prompt(
        spell_name=spell_name,
        description=str(description),
        theme=str(theme or ""),
        tag=str(tag or ""),
        school=str(school or ""),
        level=str(level or ""),
        casting_time=str(casting_time or ""),
        duration=str(duration or ""),
        allowed_tags=allowed_tags or ALLOWED_TAGS,
    )

    try:
        response = ollama.generate(
            model=model,
            prompt=prompt,
            options={
                "temperature": 0.1,
                "top_p": 0.9,
            }
        )
        response_text = response["response"].strip()
        parsed = _parse_json_object(response_text)
        if not parsed:
            return []

        tags = parsed.get("tags", [])
        allowed = set(allowed_tags or ALLOWED_TAGS)
        normalized = []
        seen = set()
        for t in tags:
            tag_clean = str(t).strip()
            if tag_clean in allowed and tag_clean not in seen:
                seen.add(tag_clean)
                normalized.append(tag_clean)
        return normalized

    except json.JSONDecodeError as e:
        print(f"  ⚠ JSON parse error for '{spell_name}': {e}")
        print(f"  Response: {response_text[:200]}...")
        return []
    except Exception as e:
        print(f"  ⚠ LLM error for '{spell_name}': {e}")
        return []


def _save_to_google_sheets(df, fantasy_sheets, gid, column_to_update: str):
    updates = []
    for _, row in df.iterrows():
        spell_name = row.get("Spell Name")
        value = row.get(column_to_update)
        if spell_name and pd.notna(value) and str(value).strip():
            updates.append({
                "match_value": spell_name,
                "update_column": column_to_update,
                "update_value": str(value)
            })

    if updates:
        try:
            result = fantasy_sheets.batch_update_cells_by_row_match(
                gid, "Spell Name", updates
            )
            success_count = sum(1 for v in result.values() if v)
            print(f"  ✓ Updated {column_to_update}: {success_count} spells")
        except Exception as e:
            print(f"  ✗ Failed to update {column_to_update}: {e}")


def extract_tags_from_csv(
    input_csv: str,
    output_csv: str = None,
    model: str = "llama3",
    batch_size: int = 10,
    use_google_sheets: bool = False,
    gid: str = None,
    overwrite: bool = False,
    source_column: str = "Description",
):
    if use_google_sheets:
        if not gid:
            print("Error: gid is required when use_google_sheets=True")
            return
        print(f"Reading from Google Sheets (GID: {gid})...")
        from FiveETools.gsheets_client import fantasy_sheets
        df = fantasy_sheets.get_sheet(gid)
    else:
        print(f"Reading {input_csv}...")
        df = pd.read_csv(input_csv)

    print(f"Loaded {len(df)} rows")
    print(f"Using model: {model}")

    if source_column not in df.columns:
        print(f"Error: '{source_column}' column not found")
        return

    tag_column = "Foundry Tag"
    if tag_column not in df.columns:
        df[tag_column] = ""
    df[tag_column] = df[tag_column].astype(object)

    processed = 0
    updated = 0
    skipped = 0

    for idx, row in df.iterrows():
        has_tag = pd.notna(row.get(tag_column)) and str(row.get(tag_column)).strip()
        if not overwrite and has_tag:
            skipped += 1
            continue

        spell_name = row.get("Spell Name", "Unknown")
        description = row.get(source_column, "")
        theme = row.get("Theme", "")
        tag = row.get("Tag", "")
        school = row.get("School", "")
        level = row.get("Level", "")
        casting_time = f"{row.get('Casting Time','')} {row.get('Casting Unit','')}".strip()
        duration = row.get("Duration", "")

        print(f"\n[{processed + 1}] Processing: {spell_name}")

        tags = extract_tags_with_llm(
            spell_name=spell_name,
            description=description,
            theme=theme,
            tag=tag,
            school=school,
            level=level,
            casting_time=casting_time,
            duration=duration,
            model=model,
            allowed_tags=ALLOWED_TAGS,
        )

        df.at[idx, tag_column] = ", ".join(tags)

        if tags:
            updated += 1
            print(f"  ✓ Tags: {', '.join(tags)}")
        else:
            print("  - No tags inferred")

        processed += 1

        if processed % batch_size == 0:
            if use_google_sheets:
                print("\n💾 Saving progress to Google Sheets...")
                _save_to_google_sheets(df, fantasy_sheets, gid, tag_column)
            else:
                output_path = output_csv or input_csv
                print(f"\n💾 Saving progress to {output_path}...")
                df.to_csv(output_path, index=False)

    if use_google_sheets:
        print("\n💾 Saving final results to Google Sheets...")
        _save_to_google_sheets(df, fantasy_sheets, gid, tag_column)
    else:
        output_path = output_csv or input_csv
        print(f"\n💾 Saving final results to {output_path}...")
        df.to_csv(output_path, index=False)

    print("\n✓ Complete!")
    print(f"  Total rows: {len(df)}")
    print(f"  Already processed (skipped): {skipped}")
    print(f"  Newly processed: {processed}")
    print(f"  Rows updated: {updated}")
    if not use_google_sheets:
        print(f"  Output: {output_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Infer Foundry tags using LLM")
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
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing values (default: skip rows already filled)"
    )
    parser.add_argument(
        "--source-column",
        default="Description",
        help="Column to analyze (default: Description)"
    )

    args = parser.parse_args()

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

    try:
        ollama.list()
        print("✓ Ollama is running")
    except Exception as e:
        print("Error: Cannot connect to Ollama")
        print("Make sure Ollama is running: ollama serve")
        print(f"Error details: {e}")
        return 1

    if use_google_sheets:
        print("✓ Google Sheets mode enabled")
        print(f"  GID: {gid}")

    extract_tags_from_csv(
        str(input_csv),
        model=args.model,
        batch_size=args.batch_size,
        use_google_sheets=use_google_sheets,
        gid=gid,
        overwrite=args.overwrite,
        source_column=args.source_column,
    )
    return 0


if __name__ == "__main__":
    exit(main())
