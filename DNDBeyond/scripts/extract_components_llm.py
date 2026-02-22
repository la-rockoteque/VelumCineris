#!/usr/bin/env python3
"""
Extract Component Descriptions using LLM

This script uses a local LLM (Ollama) to infer component descriptions
that align with SRD conventions, based on spell mechanics and theme.

Usage:
    poetry run python DNDBeyond/scripts/extract_components_llm.py

Requirements:
    - Ollama installed and running (ollama.ai)
    - Model pulled: ollama pull llama3

Output:
    Updates Orimond.csv component description columns
"""

import sys
from pathlib import Path
from typing import Dict, Optional
import json

# Add project root to Python path
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pandas as pd
import ollama


def _parse_json_object(response_text: str) -> Optional[Dict]:
    json_start = response_text.find("{")
    json_end = response_text.rfind("}") + 1
    if json_start < 0 or json_end <= json_start:
        return None
    json_text = response_text[json_start:json_end]
    return json.loads(json_text)


def create_component_prompt(
    spell_name: str,
    description: str,
    components: str = "",
    components_abvr: str = "",
    theme: str = "",
    tag: str = "",
    school: str = "",
    level: str = "",
    casting_time: str = "",
    range_text: str = "",
    duration: str = "",
) -> str:
    return f"""You are writing SRD-aligned component descriptions for a D&D 5e spell.

Spell: {spell_name}
Description: {description}
Theme: {theme}
Tag: {tag}
School: {school}
Level: {level}
Casting Time: {casting_time}
Range: {range_text}
Duration: {duration}
Components: {components}
Components ABVR: {components_abvr}

Rules:
- If a component is NOT listed, its description must be empty.
- Keep descriptions short and SRD-style (typically a brief phrase).
- Material components should be a specific item or focus wording.
- Somatic should be a simple gesture phrase.
- Verbal should be a brief incantation phrase.

Return ONLY valid JSON:
{{"material_desc":"","somatic_desc":"","verbal_desc":""}}

JSON:"""


def extract_components_with_llm(
    spell_name: str,
    description: str,
    components: str = "",
    components_abvr: str = "",
    theme: str = "",
    tag: str = "",
    school: str = "",
    level: str = "",
    casting_time: str = "",
    range_text: str = "",
    duration: str = "",
    model: str = "llama3",
) -> Dict[str, str]:
    if not description or pd.isna(description):
        return {"material_desc": "", "somatic_desc": "", "verbal_desc": ""}

    prompt = create_component_prompt(
        spell_name=spell_name,
        description=str(description),
        components=str(components or ""),
        components_abvr=str(components_abvr or ""),
        theme=str(theme or ""),
        tag=str(tag or ""),
        school=str(school or ""),
        level=str(level or ""),
        casting_time=str(casting_time or ""),
        range_text=str(range_text or ""),
        duration=str(duration or ""),
    )

    try:
        response = ollama.generate(
            model=model,
            prompt=prompt,
            options={
                "temperature": 0.2,
                "top_p": 0.9,
            }
        )
        response_text = response["response"].strip()
        parsed = _parse_json_object(response_text)
        if not parsed:
            return {"material_desc": "", "somatic_desc": "", "verbal_desc": ""}

        material_desc = str(parsed.get("material_desc", "")).strip()
        somatic_desc = str(parsed.get("somatic_desc", "")).strip()
        verbal_desc = str(parsed.get("verbal_desc", "")).strip()

        return {
            "material_desc": material_desc,
            "somatic_desc": somatic_desc,
            "verbal_desc": verbal_desc,
        }

    except json.JSONDecodeError as e:
        print(f"  ⚠ JSON parse error for '{spell_name}': {e}")
        print(f"  Response: {response_text[:200]}...")
        return {"material_desc": "", "somatic_desc": "", "verbal_desc": ""}
    except Exception as e:
        print(f"  ⚠ LLM error for '{spell_name}': {e}")
        return {"material_desc": "", "somatic_desc": "", "verbal_desc": ""}


def _save_to_google_sheets(df, fantasy_sheets, gid, columns_to_update):
    updates_by_column = {col: [] for col in columns_to_update}

    for _, row in df.iterrows():
        spell_name = row.get("Spell Name")
        if not spell_name or pd.isna(spell_name):
            continue
        for column in columns_to_update:
            value = row.get(column)
            if pd.notna(value) and str(value).strip():
                updates_by_column[column].append({
                    "match_value": spell_name,
                    "update_column": column,
                    "update_value": str(value)
                })

    total_updated = 0
    for column, updates in updates_by_column.items():
        if not updates:
            continue
        try:
            result = fantasy_sheets.batch_update_cells_by_row_match(
                gid, "Spell Name", updates
            )
            success_count = sum(1 for v in result.values() if v)
            total_updated = max(total_updated, success_count)
            print(f"  ✓ Updated {column}: {success_count} spells")
        except Exception as e:
            print(f"  ✗ Failed to update {column}: {e}")

    print(f"  ✓ Total spells updated: {total_updated}")


def extract_components_from_csv(
    input_csv: str,
    output_csv: str = None,
    model: str = "llama3",
    batch_size: int = 10,
    use_google_sheets: bool = False,
    gid: str = None,
    overwrite: bool = False,
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

    if "Description" not in df.columns:
        print("Error: 'Description' column not found")
        return

    material_col = "Component Description (Material)"
    somatic_col = "Component Description (Somatic)"
    verbal_col = "Component Description (Verbal)"

    for col in (material_col, somatic_col, verbal_col):
        if col not in df.columns:
            df[col] = ""
        df[col] = df[col].astype(object)

    processed = 0
    updated = 0
    skipped = 0

    for idx, row in df.iterrows():
        has_material = pd.notna(row.get(material_col)) and str(row.get(material_col)).strip()
        has_somatic = pd.notna(row.get(somatic_col)) and str(row.get(somatic_col)).strip()
        has_verbal = pd.notna(row.get(verbal_col)) and str(row.get(verbal_col)).strip()

        if not overwrite and (has_material or has_somatic or has_verbal):
            skipped += 1
            continue

        spell_name = row.get("Spell Name", "Unknown")
        description = row.get("Description", "")
        components = row.get("Components", "")
        components_abvr = row.get("Components ABVR", "")
        theme = row.get("Theme", "")
        tag = row.get("Tag", "")
        school = row.get("School", "")
        level = row.get("Level", "")
        casting_time = f"{row.get('Casting Time','')} {row.get('Casting Unit','')}".strip()
        range_text = f"{row.get('Range Distance','')} {row.get('Range Unit','')}".strip()
        duration = row.get("Duration", "")

        print(f"\n[{processed + 1}] Processing: {spell_name}")

        inferred = extract_components_with_llm(
            spell_name=spell_name,
            description=description,
            components=components,
            components_abvr=components_abvr,
            theme=theme,
            tag=tag,
            school=school,
            level=level,
            casting_time=casting_time,
            range_text=range_text,
            duration=duration,
            model=model,
        )

        df.at[idx, material_col] = inferred["material_desc"]
        df.at[idx, somatic_col] = inferred["somatic_desc"]
        df.at[idx, verbal_col] = inferred["verbal_desc"]

        if inferred["material_desc"] or inferred["somatic_desc"] or inferred["verbal_desc"]:
            updated += 1
            if inferred["material_desc"]:
                print(f"  ✓ Material: {inferred['material_desc']}")
            if inferred["somatic_desc"]:
                print(f"  ✓ Somatic: {inferred['somatic_desc']}")
            if inferred["verbal_desc"]:
                print(f"  ✓ Verbal: {inferred['verbal_desc']}")
        else:
            print("  - No component descriptions inferred")

        processed += 1

        if processed % batch_size == 0:
            if use_google_sheets:
                print("\n💾 Saving progress to Google Sheets...")
                _save_to_google_sheets(
                    df, fantasy_sheets, gid,
                    [material_col, somatic_col, verbal_col]
                )
            else:
                output_path = output_csv or input_csv
                print(f"\n💾 Saving progress to {output_path}...")
                df.to_csv(output_path, index=False)

    if use_google_sheets:
        print("\n💾 Saving final results to Google Sheets...")
        _save_to_google_sheets(
            df, fantasy_sheets, gid,
            [material_col, somatic_col, verbal_col]
        )
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

    parser = argparse.ArgumentParser(description="Infer component descriptions using LLM")
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

    extract_components_from_csv(
        str(input_csv),
        model=args.model,
        batch_size=args.batch_size,
        use_google_sheets=use_google_sheets,
        gid=gid,
        overwrite=args.overwrite,
    )
    return 0


if __name__ == "__main__":
    exit(main())
