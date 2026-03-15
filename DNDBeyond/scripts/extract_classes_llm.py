#!/usr/bin/env python3
"""
Extract Class Information using LLM

This script uses a local LLM (Ollama) to infer D&D class suitability
from spell descriptions and related metadata.

Usage:
    poetry run python DNDBeyond/scripts/extract_classes_llm.py

Requirements:
    - Ollama installed and running (ollama.ai)
    - Model pulled: ollama pull llama3

Output:
    Updates Orimond.csv with inferred class columns
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


DEFAULT_CLASSES = [
    "Artificer",
    "Bard",
    "Cleric",
    "Druid",
    "Paladin",
    "Ranger",
    "Sorcerer",
    "Warlock",
    "Wizard",
]

DEFAULT_NEW_CLASSES = [
    "Anomalous",
    "Architect",
    "Celebrity",
    "Cultist",
    "Hacker",
    "Judge",
    "Medic",
    "Operative",
    "Parascientist",
    "Psychomancer",
    "Runner",
    "Scourge",
]

CLASS_SYNONYMS = {
    "sorcerer": "Sorcerer",
    "sorceror": "Sorcerer",
    "artificier": "Artificer",
}


def _build_allowed_map(allowed: List[str]) -> Dict[str, str]:
    allowed_map = {c.lower(): c for c in allowed}
    for k, v in CLASS_SYNONYMS.items():
        if v in allowed:
            allowed_map[k] = v
    return allowed_map


def _normalize_list(raw_list: List[str], allowed: List[str]) -> List[str]:
    allowed_map = _build_allowed_map(allowed)
    seen = set()
    normalized = []
    for item in raw_list or []:
        key = str(item).strip().lower()
        if not key:
            continue
        canonical = allowed_map.get(key)
        if not canonical:
            continue
        if canonical in seen:
            continue
        seen.add(canonical)
        normalized.append(canonical)
    return normalized


def _parse_json_object(response_text: str) -> Optional[Dict]:
    json_start = response_text.find("{")
    json_end = response_text.rfind("}") + 1
    if json_start < 0 or json_end <= json_start:
        return None
    json_text = response_text[json_start:json_end]
    return json.loads(json_text)


def create_class_prompt(
    spell_name: str,
    description: str,
    theme: str = "",
    tag: str = "",
    school: str = "",
    level: str = "",
    target: str = "class",
    allowed_classes: List[str] = None,
    allowed_new_classes: List[str] = None,
) -> str:
    allowed_classes = allowed_classes or DEFAULT_CLASSES
    allowed_new_classes = allowed_new_classes or DEFAULT_NEW_CLASSES

    target_text = "D&D class list" if target == "class" else "new class list"
    if target == "both":
        target_text = "D&D class list and new class list"

    return f"""You are classifying a D&D 5e spell into the most appropriate classes.

Spell: {spell_name}
Description: {description}
Theme: {theme}
Tag: {tag}
School: {school}
Level: {level}

Choose classes ONLY from the allowed lists below. Use mechanics, theme, and spell flavor.
Target: {target_text}

Allowed D&D classes:
{", ".join(allowed_classes)}

Allowed new classes:
{", ".join(allowed_new_classes)}

Return ONLY valid JSON object with these fields:
- "classes": array of D&D classes (may be empty)
- "new_classes": array of new classes (may be empty)

If Target is "D&D class list", set "new_classes" to [].
If Target is "new class list", set "classes" to [].

Example:
{{"classes":["Wizard","Warlock"],"new_classes":[]}}

JSON:"""


def extract_classes_with_llm(
    spell_name: str,
    description: str,
    theme: str = "",
    tag: str = "",
    school: str = "",
    level: str = "",
    target: str = "class",
    model: str = "llama3",
    allowed_classes: List[str] = None,
    allowed_new_classes: List[str] = None,
) -> Dict[str, List[str]]:
    if not description or pd.isna(description):
        return {"classes": [], "new_classes": []}

    prompt = create_class_prompt(
        spell_name=spell_name,
        description=str(description),
        theme=str(theme or ""),
        tag=str(tag or ""),
        school=str(school or ""),
        level=str(level or ""),
        target=target,
        allowed_classes=allowed_classes,
        allowed_new_classes=allowed_new_classes,
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
            return {"classes": [], "new_classes": []}

        classes_raw = parsed.get("classes", [])
        new_classes_raw = parsed.get("new_classes", [])

        normalized = {
            "classes": _normalize_list(classes_raw, allowed_classes or DEFAULT_CLASSES),
            "new_classes": _normalize_list(new_classes_raw, allowed_new_classes or DEFAULT_NEW_CLASSES),
        }

        if target == "class":
            normalized["new_classes"] = []
        elif target == "new_class":
            normalized["classes"] = []

        # Enforce at least one class when targeting D&D classes
        if target in ("class", "both") and not normalized["classes"]:
            fallback = (allowed_classes or DEFAULT_CLASSES)[-1]
            normalized["classes"] = [fallback]

        return normalized

    except json.JSONDecodeError as e:
        print(f"  ⚠ JSON parse error for '{spell_name}': {e}")
        print(f"  Response: {response_text[:200]}...")
        return {"classes": [], "new_classes": []}
    except Exception as e:
        print(f"  ⚠ LLM error for '{spell_name}': {e}")
        return {"classes": [], "new_classes": []}


def _save_to_google_sheets(df, fantasy_sheets, gid, columns_to_update: List[str]):
    updates_by_column = {col: [] for col in columns_to_update}

    for idx, row in df.iterrows():
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


def extract_classes_from_csv(
    input_csv: str,
    output_csv: str = None,
    model: str = "llama3",
    batch_size: int = 10,
    use_google_sheets: bool = False,
    gid: str = None,
    target: str = "class",
    overwrite: bool = False,
    allowed_classes: List[str] = None,
    allowed_new_classes: List[str] = None,
):
    if use_google_sheets:
        if not gid:
            print("Error: gid is required when use_google_sheets=True")
            return
        print(f"Reading from Google Sheets (GID: {gid})...")
        from Spreadsheet.sheets import fantasy_sheets
        df = fantasy_sheets.get_sheet(gid)
    else:
        print(f"Reading {input_csv}...")
        df = pd.read_csv(input_csv)

    print(f"Loaded {len(df)} rows")
    print(f"Using model: {model}")

    if "Description" not in df.columns:
        print("Error: 'Description' column not found")
        return

    class_column = "LLM Class"
    new_class_column = "New Class"
    if class_column not in df.columns:
        df[class_column] = ""
    if new_class_column not in df.columns:
        df[new_class_column] = ""

    df[class_column] = df[class_column].astype(object)
    df[new_class_column] = df[new_class_column].astype(object)

    processed = 0
    updated = 0
    skipped = 0

    for idx, row in df.iterrows():
        has_class = pd.notna(row.get(class_column)) and str(row.get(class_column)).strip()
        has_new_class = pd.notna(row.get(new_class_column)) and str(row.get(new_class_column)).strip()

        if not overwrite:
            if target == "class" and has_class:
                skipped += 1
                continue
            if target == "new_class" and has_new_class:
                skipped += 1
                continue
            if target == "both" and has_class and has_new_class:
                skipped += 1
                continue

        spell_name = row.get("Spell Name", "Unknown")
        description = row.get("Description", "")
        theme = row.get("Theme", "")
        tag = row.get("Tag", "")
        school = row.get("School", "")
        level = row.get("Level", "")

        print(f"\n[{processed + 1}] Processing: {spell_name}")

        inferred = extract_classes_with_llm(
            spell_name=spell_name,
            description=description,
            theme=theme,
            tag=tag,
            school=school,
            level=level,
            target=target,
            model=model,
            allowed_classes=allowed_classes or DEFAULT_CLASSES,
            allowed_new_classes=allowed_new_classes or DEFAULT_NEW_CLASSES,
        )

        classes = inferred.get("classes", [])
        new_classes = inferred.get("new_classes", [])

        if target in ("class", "both"):
            df.at[idx, class_column] = ", ".join(classes)
        if target in ("new_class", "both"):
            df.at[idx, new_class_column] = ", ".join(new_classes)

        if classes or new_classes:
            updated += 1
            if classes:
                print(f"  ✓ Classes: {', '.join(classes)}")
            if new_classes:
                print(f"  ✓ New Classes: {', '.join(new_classes)}")
        else:
            print("  - No classes inferred")

        processed += 1

        if processed % batch_size == 0:
            if use_google_sheets:
                print("\n💾 Saving progress to Google Sheets...")
                columns = []
                if target in ("class", "both"):
                    columns.append(class_column)
                if target in ("new_class", "both"):
                    columns.append(new_class_column)
                _save_to_google_sheets(df, fantasy_sheets, gid, columns)
            else:
                output_path = output_csv or input_csv
                print(f"\n💾 Saving progress to {output_path}...")
                df.to_csv(output_path, index=False)

    if use_google_sheets:
        print("\n💾 Saving final results to Google Sheets...")
        columns = []
        if target in ("class", "both"):
            columns.append(class_column)
        if target in ("new_class", "both"):
            columns.append(new_class_column)
        _save_to_google_sheets(df, fantasy_sheets, gid, columns)
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


def _parse_list_arg(value: Optional[str], fallback: List[str]) -> List[str]:
    if not value:
        return fallback
    return [v.strip() for v in value.split(",") if v.strip()]


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Infer spell classes using LLM")
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
        "--target",
        choices=["class", "new_class", "both"],
        default="class",
        help="Which column(s) to fill (default: class)"
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing values (default: skip rows already filled)"
    )
    parser.add_argument(
        "--class-list",
        help="Comma-separated list of allowed D&D classes"
    )
    parser.add_argument(
        "--new-class-list",
        help="Comma-separated list of allowed new classes"
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

    allowed_classes = _parse_list_arg(args.class_list, DEFAULT_CLASSES)
    allowed_new_classes = _parse_list_arg(args.new_class_list, DEFAULT_NEW_CLASSES)

    if use_google_sheets:
        print("✓ Google Sheets mode enabled")
        print(f"  GID: {gid}")

    extract_classes_from_csv(
        str(input_csv),
        model=args.model,
        batch_size=args.batch_size,
        use_google_sheets=use_google_sheets,
        gid=gid,
        target=args.target,
        overwrite=args.overwrite,
        allowed_classes=allowed_classes,
        allowed_new_classes=allowed_new_classes,
    )
    return 0


if __name__ == "__main__":
    exit(main())
