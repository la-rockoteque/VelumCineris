#!/usr/bin/env python3
"""
Generate D&D loading-screen tidbits with a local Ollama model.

The script loads monsters, spells, and species data, then continuously asks a
local model for one short trivia line at a time and appends each result to a
CSV file. It runs until interrupted (Ctrl+C) unless --max-items is provided.
"""

from __future__ import annotations

import argparse
import csv
import re
import signal
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from random import choice
from typing import Any, Iterable, Optional

import ollama


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


CSV_HEADERS = [
    "created_at_utc",
    "entity_type",
    "entity_name",
    "source",
    "tidbit",
    "model",
]
SCHOOL_NAMES = {
    "A": "Abjuration",
    "C": "Conjuration",
    "D": "Divination",
    "E": "Enchantment",
    "V": "Evocation",
    "I": "Illusion",
    "N": "Necromancy",
    "T": "Transmutation",
}
SIZE_NAMES = {
    "T": "Tiny",
    "S": "Small",
    "M": "Medium",
    "L": "Large",
    "H": "Huge",
    "G": "Gargantuan",
}
STOP_REQUESTED = False


@dataclass(frozen=True)
class TriviaEntity:
    entity_type: str
    name: str
    source: str
    facts: list[str]


def _signal_stop_handler(signum, frame):
    del frame
    global STOP_REQUESTED
    STOP_REQUESTED = True
    print(f"\nReceived signal {signum}. Stopping after this iteration...")


def _install_signal_handlers() -> None:
    signal.signal(signal.SIGINT, _signal_stop_handler)
    signal.signal(signal.SIGTERM, _signal_stop_handler)


def _trim(text: str, max_len: int) -> str:
    clean = re.sub(r"\s+", " ", str(text or "")).strip()
    if len(clean) <= max_len:
        return clean
    return clean[: max_len - 1].rstrip() + "..."


def _normalized_dedupe_key(text: str) -> str:
    return re.sub(r"\W+", "", text.lower())


def _model_dump(entity: Any) -> dict[str, Any]:
    if hasattr(entity, "model_dump"):
        return entity.model_dump(exclude_none=True, by_alias=True)
    if isinstance(entity, dict):
        return entity
    return {}


def _collect_text_fragments(value: Any, limit: int = 4) -> list[str]:
    fragments: list[str] = []

    def walk(node: Any) -> None:
        if len(fragments) >= limit:
            return
        if isinstance(node, str):
            text = _trim(node, 140)
            if text:
                fragments.append(text)
            return
        if isinstance(node, list):
            for child in node:
                walk(child)
                if len(fragments) >= limit:
                    return
            return
        if isinstance(node, dict):
            for key in ("name", "entries", "entry", "text", "note"):
                if key in node:
                    walk(node[key])
                    if len(fragments) >= limit:
                        return

    walk(value)
    return fragments


def _monster_to_entity(monster: Any) -> Optional[TriviaEntity]:
    data = _model_dump(monster)
    name = str(data.get("name", "")).strip()
    if not name:
        return None

    source = str(data.get("source", "")).strip() or "UNKNOWN"
    size = data.get("size") or []
    size_name = SIZE_NAMES.get(size[0], "") if size else ""
    creature_type_raw = data.get("type")
    creature_type = (
        str(creature_type_raw.get("type", "")).strip()
        if isinstance(creature_type_raw, dict)
        else str(creature_type_raw or "").strip()
    )
    cr = str(data.get("cr", "")).strip()

    ac = ""
    if isinstance(data.get("ac"), list) and data["ac"]:
        ac = str(data["ac"][0].get("ac", "")).strip()
    hp = ""
    if isinstance(data.get("hp"), dict):
        hp = str(data["hp"].get("average", "")).strip()
    speed = ""
    if isinstance(data.get("speed"), dict) and data["speed"]:
        speed_pairs = [f"{mode} {value}" for mode, value in data["speed"].items()]
        speed = ", ".join(speed_pairs)
    languages = ""
    if isinstance(data.get("languages"), list):
        languages = ", ".join(str(x) for x in data["languages"][:3])
    trait_names = [
        str(item.get("name", "")).strip()
        for item in data.get("trait", [])[:2]
        if isinstance(item, dict) and item.get("name")
    ]
    action_names = [
        str(item.get("name", "")).strip()
        for item in data.get("action", [])[:2]
        if isinstance(item, dict) and item.get("name")
    ]
    lore = _collect_text_fragments(
        [data.get("entries"), data.get("trait"), data.get("action")],
        limit=2,
    )

    combat_parts = []
    if ac:
        combat_parts.append(f"AC {ac}")
    if hp:
        combat_parts.append(f"HP {hp}")

    facts = [
        f"{size_name} {creature_type} (CR {cr})".strip(),
        "; ".join(combat_parts),
        f"Speed: {speed}" if speed else "",
        f"Languages: {languages}" if languages else "",
        f"Traits: {', '.join(trait_names)}" if trait_names else "",
        f"Actions: {', '.join(action_names)}" if action_names else "",
        *lore,
    ]
    return TriviaEntity("monster", name, source, [f for f in facts if f])


def _spell_to_entity(spell: Any) -> Optional[TriviaEntity]:
    data = _model_dump(spell)
    name = str(data.get("name", "")).strip()
    if not name:
        return None

    source = str(data.get("source", "")).strip() or "UNKNOWN"
    level = int(data.get("level", 0) or 0)
    level_text = "Cantrip" if level == 0 else f"Level {level}"
    school = SCHOOL_NAMES.get(str(data.get("school", "")).upper(), str(data.get("school", "")))

    cast = ""
    if isinstance(data.get("time"), list) and data["time"]:
        first = data["time"][0]
        if isinstance(first, dict):
            number = first.get("number")
            unit = first.get("unit")
            cast = f"{number} {unit}".strip()

    spell_range = ""
    if isinstance(data.get("range"), dict):
        range_type = str(data["range"].get("type", "")).strip()
        distance = data["range"].get("distance")
        if isinstance(distance, dict):
            dist_type = str(distance.get("type", "")).strip()
            amount = distance.get("amount")
            if amount:
                spell_range = f"{range_type} ({amount} {dist_type})".strip()
            else:
                spell_range = f"{range_type} ({dist_type})".strip()

    duration = ""
    if isinstance(data.get("duration"), list) and data["duration"]:
        first = data["duration"][0]
        if isinstance(first, dict):
            duration = str(first.get("type", "")).strip()
            inner = first.get("duration")
            if isinstance(inner, dict):
                amount = inner.get("amount")
                unit = inner.get("type")
                if amount and unit:
                    duration = f"{duration} ({amount} {unit})".strip()

    class_names: list[str] = []
    classes = data.get("classes")
    if isinstance(classes, dict):
        from_class_list = classes.get("fromClassList", [])
        if isinstance(from_class_list, list):
            for row in from_class_list[:4]:
                if isinstance(row, dict):
                    class_name = row.get("name")
                    if class_name:
                        class_names.append(str(class_name))

    damage_types = ""
    if isinstance(data.get("damageInflict"), list):
        damage_types = ", ".join(str(x) for x in data["damageInflict"][:3])
    saves = ""
    if isinstance(data.get("savingThrow"), list):
        saves = ", ".join(str(x) for x in data["savingThrow"][:2])
    lore = _collect_text_fragments(
        [data.get("entries"), data.get("entriesHigherLevel")],
        limit=2,
    )

    facts = [
        f"{level_text} {school}".strip(),
        f"Casting time: {cast}" if cast else "",
        f"Range: {spell_range}" if spell_range else "",
        f"Duration: {duration}" if duration else "",
        f"Classes: {', '.join(class_names)}" if class_names else "",
        f"Damage types: {damage_types}" if damage_types else "",
        f"Saving throws: {saves}" if saves else "",
        *lore,
    ]
    return TriviaEntity("spell", name, source, [f for f in facts if f])


def _species_to_entity(species: dict[str, Any]) -> Optional[TriviaEntity]:
    name = str(species.get("name", "")).strip()
    if not name:
        return None

    source = str(species.get("source", "")).strip() or "UNKNOWN"
    size = species.get("size")
    size_text = ", ".join(SIZE_NAMES.get(code, str(code)) for code in size) if size else ""
    speed = species.get("speed")
    speed_text = str(speed).strip() if speed is not None else ""

    ability_text = ""
    if isinstance(species.get("ability"), list) and species["ability"]:
        first = species["ability"][0]
        if isinstance(first, dict):
            ability_text = ", ".join(
                f"{stat.upper()} {value:+d}"
                for stat, value in first.items()
                if isinstance(value, int)
            )

    trait_names: list[str] = []
    entries = species.get("entries")
    if isinstance(entries, list):
        for item in entries:
            if isinstance(item, dict):
                trait_name = str(item.get("name", "")).strip()
                if trait_name and trait_name not in {"Age", "Size", "Speed", "Vision", "Languages"}:
                    trait_names.append(trait_name)
            if len(trait_names) >= 3:
                break

    lore = _collect_text_fragments(species.get("entries"), limit=2)
    facts = [
        f"Size: {size_text}" if size_text else "",
        f"Speed: {speed_text}" if speed_text else "",
        f"Ability bonuses: {ability_text}" if ability_text else "",
        f"Traits: {', '.join(trait_names)}" if trait_names else "",
        *lore,
    ]
    return TriviaEntity("species", name, source, [f for f in facts if f])


def _csv_name(row: dict[str, str]) -> str:
    for key in ("name", "Name", "Spell Name", "title", "Title"):
        value = row.get(key)
        if value and str(value).strip():
            return str(value).strip()
    return ""


def _csv_source(row: dict[str, str], fallback: str = "UNKNOWN") -> str:
    for key in ("source", "Source"):
        value = row.get(key)
        if value and str(value).strip():
            return str(value).strip()
    return fallback


def _load_entities_from_csv(path: Path, entity_type: str) -> list[TriviaEntity]:
    entities: list[TriviaEntity] = []
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            name = _csv_name(row)
            if not name:
                continue
            facts: list[str] = []
            for key, value in row.items():
                if not key or not value:
                    continue
                stripped_value = str(value).strip()
                if not stripped_value:
                    continue
                if key in {"name", "Name", "Spell Name", "source", "Source"}:
                    continue
                facts.append(f"{key}: {_trim(stripped_value, 120)}")
                if len(facts) >= 6:
                    break
            entities.append(
                TriviaEntity(
                    entity_type=entity_type,
                    name=name,
                    source=_csv_source(row),
                    facts=facts,
                )
            )
    return entities


def _load_repository_entities(
    requested_types: set[str],
    source_code: str,
) -> tuple[list[TriviaEntity], list[str]]:
    entities: list[TriviaEntity] = []
    warnings: list[str] = []

    if "monster" in requested_types:
        try:
            from models.datasets import load_dataset

            monsters = load_dataset("monster", source_code=source_code)
            for monster in monsters:
                entity = _monster_to_entity(monster)
                if entity is not None:
                    entities.append(entity)
        except Exception as exc:
            warnings.append(f"Could not load monsters from repository data: {exc}")

    if "spell" in requested_types:
        try:
            from models.datasets import load_dataset

            spells = load_dataset("spells", source_code=source_code)
            for spell in spells:
                entity = _spell_to_entity(spell)
                if entity is not None:
                    entities.append(entity)
        except Exception as exc:
            warnings.append(f"Could not load spells from repository data: {exc}")

    if "species" in requested_types:
        try:
            try:
                from models.datasets.species import load_species_list

                species_list = load_species_list(source_code=source_code)
            except ModuleNotFoundError:
                from FiveETools.core.fantasy.species import build_species_list

                species_list = build_species_list(source_code=source_code)
            for species in species_list:
                entity = _species_to_entity(species)
                if entity is not None:
                    entities.append(entity)
        except Exception as exc:
            warnings.append(f"Could not load species from repository data: {exc}")

    return entities, warnings


def _build_prompt(entity: TriviaEntity) -> str:
    facts_block = "\n".join(f"- {fact}" for fact in entity.facts[:8]) or "- No extra facts."
    return f"""You write one-line loading-screen trivia for a D&D 5e setting.

Entity type: {entity.entity_type}
Entity name: {entity.name}
Source: {entity.source}

Known facts:
{facts_block}

Rules:
- Write exactly one sentence.
- Start with "Did you know".
- Use 14 to 28 words.
- Mention the entity name exactly once.
- Keep the sentence anchored in the known facts.
- Do not invent mechanics or lore not present above.
- Plain text only, no list markers or quotes.

Never output meta text like:
- "here is your one-line loading-screen trivia"
- "here is a one-line loading-screen trivia for..."
- "for a D&D 5e setting"
"""


def _normalize_tidbit(text: str) -> str:
    candidate = text.strip().splitlines()[0] if text.strip() else ""
    candidate = re.sub(r'^[>\-*"\']+\s*', "", candidate).strip()
    candidate = re.sub(r"\s+", " ", candidate).strip()
    if not candidate:
        return ""
    if not candidate.lower().startswith("did you know"):
        candidate = f"Did you know {candidate[0].lower() + candidate[1:]}"
    if candidate[-1] not in ".!?":
        candidate += "."
    return candidate


def _is_valid_tidbit(tidbit: str, entity: TriviaEntity) -> bool:
    if not tidbit:
        return False

    lowered = tidbit.lower()
    name_lower = entity.name.lower()
    banned_phrases = (
        "here is your one-line loading-screen trivia",
        "here is a one-line loading-screen trivia",
        "here is one-line loading-screen trivia",
        "for a d&d 5e setting",
        "your requested one-line",
        "one-line loading-screen trivia:",
    )
    if any(phrase in lowered for phrase in banned_phrases):
        return False

    if not lowered.startswith("did you know"):
        return False
    if lowered.endswith(":.") or lowered.endswith(":"):
        return False
    if lowered.count(name_lower) != 1:
        return False

    words = re.findall(r"[A-Za-z0-9'-]+", tidbit)
    if len(words) < 12 or len(words) > 36:
        return False

    return True


def _load_existing_tidbits(output_csv: Path) -> set[str]:
    if not output_csv.exists():
        return set()
    keys: set[str] = set()
    with output_csv.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            text = row.get("tidbit", "")
            if text:
                keys.add(_normalized_dedupe_key(text))
    return keys


def _append_tidbit_row(
    output_csv: Path,
    *,
    entity: TriviaEntity,
    tidbit: str,
    model: str,
) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    file_exists = output_csv.exists()
    with output_csv.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_HEADERS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(
            {
                "created_at_utc": datetime.now(timezone.utc).isoformat(),
                "entity_type": entity.entity_type,
                "entity_name": entity.name,
                "source": entity.source,
                "tidbit": tidbit,
                "model": model,
            }
        )


def _generate_tidbit(entity: TriviaEntity, model: str, temperature: float) -> str:
    response = ollama.generate(
        model=model,
        prompt=_build_prompt(entity),
        options={
            "temperature": temperature,
            "top_p": 0.9,
        },
    )
    return _normalize_tidbit(response.get("response", ""))


def _generate_valid_tidbit(
    entity: TriviaEntity,
    model: str,
    temperature: float,
    max_retries: int,
) -> str:
    retries = max(1, max_retries)
    for _ in range(retries):
        tidbit = _generate_tidbit(entity=entity, model=model, temperature=temperature)
        if _is_valid_tidbit(tidbit, entity):
            return tidbit
    return ""


def _extract_available_model_names(list_response: Any) -> list[str]:
    names: set[str] = set()
    models: Any = []

    if isinstance(list_response, dict):
        models = list_response.get("models", [])
    elif isinstance(list_response, list):
        models = list_response

    if isinstance(models, list):
        for item in models:
            if not isinstance(item, dict):
                continue
            for key in ("name", "model"):
                value = item.get(key)
                if isinstance(value, str) and value.strip():
                    names.add(value.strip())

    return sorted(names)


def _normalize_model_name(model_name: str) -> str:
    return model_name.strip().lower()


def _model_base(model_name: str) -> str:
    return _normalize_model_name(model_name).split(":", 1)[0]


def _resolve_model_name(requested: str, available: list[str]) -> Optional[str]:
    if not available:
        return requested

    normalized_to_actual = {_normalize_model_name(name): name for name in available}
    requested_norm = _normalize_model_name(requested)
    if requested_norm in normalized_to_actual:
        return normalized_to_actual[requested_norm]

    latest_key = f"{requested_norm}:latest"
    if latest_key in normalized_to_actual:
        return normalized_to_actual[latest_key]

    requested_base = _model_base(requested_norm)
    base_matches = [name for name in available if _model_base(name) == requested_base]
    if len(base_matches) == 1:
        return base_matches[0]

    return None


def _parse_type_list(raw: str) -> set[str]:
    values = {item.strip().lower() for item in raw.split(",") if item.strip()}
    allowed = {"monster", "spell", "species"}
    unknown = sorted(values - allowed)
    if unknown:
        unknown_text = ", ".join(unknown)
        raise ValueError(
            f"Unsupported entity type(s): {unknown_text}. "
            f"Use only: {', '.join(sorted(allowed))}."
        )
    if not values:
        raise ValueError("At least one entity type is required.")
    return values


def _merge_entities(groups: Iterable[list[TriviaEntity]]) -> list[TriviaEntity]:
    merged: list[TriviaEntity] = []
    for group in groups:
        merged.extend(group)
    return merged


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate loading-screen trivia with a local Ollama model."
    )
    parser.add_argument(
        "--model",
        default="llama3",
        help="Ollama model name (default: llama3).",
    )
    parser.add_argument(
        "--source",
        default="ORIO",
        help="Source code for repository datasets (default: ORIO).",
    )
    parser.add_argument(
        "--types",
        default="monster,spell,species",
        help="Comma-separated entity types (monster,spell,species).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("assets/loading_trivia.csv"),
        help="Output CSV path (default: assets/loading_trivia.csv).",
    )
    parser.add_argument(
        "--interval-seconds",
        type=float,
        default=0.0,
        help="Pause between generated rows (default: 0).",
    )
    parser.add_argument(
        "--max-items",
        type=int,
        default=None,
        help="Stop after this many newly generated rows (default: run until stopped).",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.6,
        help="Sampling temperature for generation (default: 0.6).",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=5,
        help="Generation retries per entity when output format is invalid (default: 5).",
    )
    parser.add_argument(
        "--monster-csv",
        type=Path,
        default=None,
        help="Optional monster CSV input.",
    )
    parser.add_argument(
        "--spell-csv",
        type=Path,
        default=None,
        help="Optional spell CSV input.",
    )
    parser.add_argument(
        "--species-csv",
        type=Path,
        default=None,
        help="Optional species CSV input.",
    )
    parser.add_argument(
        "--skip-repository-data",
        action="store_true",
        help="Use only provided CSV inputs and skip repository dataset loaders.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    _install_signal_handlers()

    try:
        requested_types = _parse_type_list(args.types)
    except ValueError as exc:
        print(f"Error: {exc}")
        return 2

    csv_groups: list[list[TriviaEntity]] = []
    for csv_path in (args.monster_csv, args.spell_csv, args.species_csv):
        if csv_path is not None and not csv_path.exists():
            print(f"Error: CSV file not found: {csv_path}")
            return 2

    if args.monster_csv and "monster" in requested_types:
        csv_groups.append(_load_entities_from_csv(args.monster_csv, "monster"))
    if args.spell_csv and "spell" in requested_types:
        csv_groups.append(_load_entities_from_csv(args.spell_csv, "spell"))
    if args.species_csv and "species" in requested_types:
        csv_groups.append(_load_entities_from_csv(args.species_csv, "species"))

    repository_entities: list[TriviaEntity] = []
    warnings: list[str] = []
    if not args.skip_repository_data:
        repository_entities, warnings = _load_repository_entities(
            requested_types=requested_types,
            source_code=args.source,
        )

    for warning in warnings:
        print(f"Warning: {warning}")

    entities = _merge_entities([repository_entities, *csv_groups])
    if not entities:
        print("Error: no entities available. Check source data or CSV inputs.")
        return 1

    try:
        list_response = ollama.list()
    except Exception as exc:
        print(f"Error: cannot reach Ollama: {exc}")
        print("Start Ollama first (example: ollama serve).")
        return 1

    available_models = _extract_available_model_names(list_response)
    resolved_model = _resolve_model_name(args.model, available_models)
    if resolved_model is None:
        print(f"Error: model '{args.model}' is not installed in Ollama.")
        if available_models:
            print("Installed models:")
            for model_name in available_models:
                print(f"  - {model_name}")
        print(f"Install it with: ollama pull {args.model}")
        return 1
    if resolved_model != args.model:
        print(f"Model '{args.model}' not found exactly; using '{resolved_model}' instead.")

    existing_keys = _load_existing_tidbits(args.output)
    generated = 0
    duplicates = 0
    rejected = 0
    attempts = 0

    print(
        f"Loaded {len(entities)} entities. "
        f"Writing to {args.output}. Press Ctrl+C to stop."
    )

    while not STOP_REQUESTED:
        if args.max_items is not None and generated >= args.max_items:
            break

        attempts += 1
        entity = choice(entities)
        try:
            tidbit = _generate_valid_tidbit(
                entity=entity,
                model=resolved_model,
                temperature=args.temperature,
                max_retries=args.max_retries,
            )
        except Exception as exc:
            print(f"LLM error for '{entity.name}': {exc}")
            if args.interval_seconds > 0:
                time.sleep(args.interval_seconds)
            continue

        if not tidbit:
            rejected += 1
            continue

        key = _normalized_dedupe_key(tidbit)
        if key in existing_keys:
            duplicates += 1
            continue

        _append_tidbit_row(
            args.output,
            entity=entity,
            tidbit=tidbit,
            model=resolved_model,
        )
        existing_keys.add(key)
        generated += 1
        print(f"[{generated}] {tidbit}")

        if args.interval_seconds > 0:
            time.sleep(args.interval_seconds)

    print(
        "Stopped. "
        f"Generated {generated} new row(s), skipped {duplicates} duplicate(s), "
        f"rejected {rejected} format failure(s), attempted {attempts} generation(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
