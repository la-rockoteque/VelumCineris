from __future__ import annotations

import re
from typing import Any, cast

from FiveETools.core.modern import sources as source_catalog
from FiveETools.datasets.json_loader import build_mapped_rows
from FiveETools.mappers.monster_mapper import map_modern_monster_row
from Spreadsheet.core.lazy_exports import resolve_lazy_attr
from Spreadsheet.core.converters.monster import MonsterConverter
from models.datasets import get_converter as get_dataset_converter
from models.datasets import load_dataset
from models.entities.monster import Monster

_cache: dict[str, object] = {}


def _text(value, default: str = "") -> str:
    if pd.isnull(value):
        return default
    return str(value)


def parse_speed(value):
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        match = re.search(r"(\d+)", value)
        return int(match.group(1)) if match else None
    return None


def parse_entries(raw_text):
    if pd.isnull(raw_text):
        return []
    raw_text = str(raw_text)
    pattern = re.compile(r"([A-Z][^.]+?)\.\s+(.*?)(?=(?:[A-Z][^.]+?\.)|$)", re.S)
    entries = []

    for text in raw_text.split("\n"):
        name, entry = (text.split(":: ") + ["", ""])[:2]
        entries.append({"name": name, "entries": [entry]})
    return entries


DMG = {
    "acid",
    "cold",
    "fire",
    "force",
    "lightning",
    "necrotic",
    "poison",
    "psychic",
    "radiant",
    "thunder",
}

BPS = {"bludgeoning", "piercing", "slashing"}


def parse_immunities(raw_text):
    if pd.isnull(raw_text):
        return []
    raw_text = str(raw_text)
    immunities = []
    for immunity in DMG:
        if immunity in raw_text.lower():
            immunities.append(immunity)

    if "from" in raw_text.lower():
        special_immunities = []
        fluff = raw_text.split(" from ")[1]
        for immunity in BPS:
            if immunity in raw_text.lower():
                special_immunities.append(immunity)
        immunities.append(
            {"immune": special_immunities, "note": f"from {fluff.lower()}"}
        )
    # Preserve legacy behavior: historical exports serialized this as null.
    return None


def parse_skills(raw_text):
    if pd.isnull(raw_text):
        return {}
    raw_text = str(raw_text)
    pattern = re.compile(
        r"(?:^|[,\n;]\s*)"
        r"([A-Z]{3}|[A-Za-z][A-Za-z'/-]*(?:\s+[A-Za-z'/-]+)*)"
        r"\s*([+-]\d+)",
        re.IGNORECASE,
    )

    skills = {}
    for match in pattern.finditer(raw_text):
        name = match.group(1).strip().lower()
        skills[name] = match.group(2)
    return skills


def parse_saves(raw_text):
    if pd.isnull(raw_text):
        return {}
    raw_text = str(raw_text)
    pattern = re.compile(r"([A-Z]{3})\s*([+-]\d+)")
    saves = {}

    key_map = {
        "STR": "str",
        "DEX": "dex",
        "CON": "con",
        "INT": "int",
        "WIS": "wis",
        "CHA": "cha",
    }

    for stat, value in pattern.findall(raw_text):
        if stat in key_map:
            saves[key_map[stat]] = value

    return saves


def row_to_monster(row, *, json_source: str) -> dict[str, Any]:
    return map_modern_monster_row(
        row,
        json_source=json_source,
        text_fn=_text,
        parse_speed_fn=parse_speed,
        parse_entries_fn=parse_entries,
        parse_saves_fn=parse_saves,
        parse_skills_fn=parse_skills,
        parse_immunities_fn=parse_immunities,
    )


def get_converter() -> MonsterConverter:
    return cast(MonsterConverter, get_dataset_converter("monster", setting="modern"))


def build_monster_list(source_code: str | None = None) -> list[dict[str, Any]]:
    return build_mapped_rows(
        sheets_client=source_catalog.modern_sheets,
        sheet_name="monsters",
        source_code=source_code,
        default_source=source_catalog.DEFAULT_SOURCE,
        resolve_source_context=source_catalog.resolve_source_context,
        row_mapper=row_to_monster,
        name_column="Name",
        filter_by_source=False,
    )


def build_monster_pydantic(source_code: str | None = None) -> list[Monster]:
    return cast(
        list[Monster],
        load_dataset("monster", source_code=source_code, setting="modern"),
    )


_RESOLVERS = {
    "source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[0],
    "json_source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[1],
    "monster_list": build_monster_list,
    "converter": get_converter,
    "monster_pydantic": build_monster_pydantic,
}
_CACHED_ATTRS = {"monster_list", "monster_pydantic"}


def __getattr__(name: str):
    return resolve_lazy_attr(
        module_name=__name__,
        attr_name=name,
        cache=_cache,
        resolvers=_RESOLVERS,
        cached_attrs=_CACHED_ATTRS,
    )


__all__ = [
    "parse_speed",
    "parse_entries",
    "parse_immunities",
    "parse_skills",
    "parse_saves",
    "row_to_monster",
    "get_converter",
    "build_monster_list",
    "build_monster_pydantic",
    "source",
    "json_source",
    "monster_list",
    "converter",
    "monster_pydantic",
]
