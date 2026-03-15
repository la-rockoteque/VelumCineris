from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Literal

from Spreadsheet.core.converters.disease import DiseaseConverter
from Spreadsheet.core.converters.background import BackgroundConverter
from Spreadsheet.core.converters.condition import ConditionConverter
from Spreadsheet.core.converters.feat import FeatConverter
from Spreadsheet.core.converters.item import ItemConverter
from Spreadsheet.core.converters.language import LanguageConverter
from Spreadsheet.core.converters.magic_item import MagicItemConverter
from Spreadsheet.core.converters.monster import MonsterConverter
from Spreadsheet.core.converters.spell import SpellConverter

from .sources import (
    DEFAULT_SETTING,
    DEFAULT_SOURCES,
    fantasy_sheets,
    modern_sheets,
    normalize_setting as normalize_source_setting,
    resolve_source_context_for_setting,
)

SourceFilterMode = Literal["source", "none"]


@dataclass(frozen=True)
class DatasetSpec:
    name: str
    converter_factory: Any
    source_filter_mode: SourceFilterMode = "source"


def _normalize_dataset_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(name).strip().lower()).strip("_")


_DATASET_SPECS: dict[str, DatasetSpec] = {
    "spells": DatasetSpec(
        name="spells",
        converter_factory=lambda: SpellConverter(fantasy_sheets),
        source_filter_mode="source",
    ),
    "monster": DatasetSpec(
        name="monster",
        converter_factory=lambda: MonsterConverter(fantasy_sheets),
        source_filter_mode="none",
    ),
    "diseases": DatasetSpec(
        name="diseases",
        converter_factory=lambda: DiseaseConverter(fantasy_sheets),
        source_filter_mode="none",
    ),
    "languages": DatasetSpec(
        name="languages",
        converter_factory=lambda: LanguageConverter(fantasy_sheets),
        source_filter_mode="none",
    ),
    "magic_items": DatasetSpec(
        name="magic_items",
        converter_factory=lambda: MagicItemConverter(fantasy_sheets),
        source_filter_mode="source",
    ),
}
_MODERN_DATASET_SPECS: dict[str, DatasetSpec] = {
    "backgrounds": DatasetSpec(
        name="backgrounds",
        converter_factory=lambda: BackgroundConverter(modern_sheets),
        source_filter_mode="source",
    ),
    "conditions": DatasetSpec(
        name="conditions",
        converter_factory=lambda: ConditionConverter(modern_sheets),
        source_filter_mode="none",
    ),
    "feats": DatasetSpec(
        name="feats",
        converter_factory=lambda: FeatConverter(modern_sheets),
        source_filter_mode="source",
    ),
    "items": DatasetSpec(
        name="items",
        converter_factory=lambda: ItemConverter(modern_sheets),
        source_filter_mode="source",
    ),
    "spells": DatasetSpec(
        name="spells",
        converter_factory=lambda: SpellConverter(modern_sheets),
        source_filter_mode="source",
    ),
    "monster": DatasetSpec(
        name="monster",
        converter_factory=lambda: MonsterConverter(modern_sheets),
        source_filter_mode="none",
    ),
    "diseases": DatasetSpec(
        name="diseases",
        converter_factory=lambda: DiseaseConverter(modern_sheets),
        source_filter_mode="none",
    ),
    "languages": DatasetSpec(
        name="languages",
        converter_factory=lambda: LanguageConverter(modern_sheets),
        source_filter_mode="none",
    ),
    "magic_items": DatasetSpec(
        name="magic_items",
        converter_factory=lambda: MagicItemConverter(modern_sheets),
        source_filter_mode="source",
    ),
}
_SETTING_DATASET_SPECS = {
    "fantasy": _DATASET_SPECS,
    "modern": _MODERN_DATASET_SPECS,
}
_DATASET_ALIASES = {
    "background": "backgrounds",
    "backgrounds": "backgrounds",
    "condition": "conditions",
    "conditions": "conditions",
    "feat": "feats",
    "feats": "feats",
    "item": "items",
    "items": "items",
    "spell": "spells",
    "monster": "monster",
    "monsters": "monster",
    "disease": "diseases",
    "diseases": "diseases",
    "language": "languages",
    "languages": "languages",
    "magic_item": "magic_items",
    "magic_items": "magic_items",
}
_SETTING_DEFAULT_SOURCES = {
    "fantasy": DEFAULT_SOURCES["fantasy"],
    "modern": DEFAULT_SOURCES["modern"],
}
_SOURCE_CONTEXT_RESOLVERS = {
    "fantasy": lambda source_code: resolve_source_context_for_setting(
        "fantasy", source_code
    ),
    "modern": lambda source_code: resolve_source_context_for_setting(
        "modern", source_code
    ),
}
_CACHE: dict[tuple[str, str, str], list[Any]] = {}


def normalize_setting(setting: str | None = None) -> str:
    return normalize_source_setting(setting or DEFAULT_SETTING)


def resolve_dataset_name(name: str, *, setting: str | None = None) -> str:
    setting_key = normalize_setting(setting)
    normalized = _normalize_dataset_name(name)
    canonical = _DATASET_ALIASES.get(normalized, normalized)
    if canonical not in _SETTING_DATASET_SPECS[setting_key]:
        raise KeyError(f"Unknown dataset: {name}")
    return canonical


def list_datasets(setting: str | None = None) -> list[str]:
    if setting is None:
        dataset_names: set[str] = set()
        for setting_specs in _SETTING_DATASET_SPECS.values():
            dataset_names.update(setting_specs)
        return sorted(dataset_names)
    return sorted(_SETTING_DATASET_SPECS[normalize_setting(setting)])


def get_dataset_spec(name: str, *, setting: str | None = None) -> DatasetSpec:
    setting_key = normalize_setting(setting)
    return _SETTING_DATASET_SPECS[setting_key][
        resolve_dataset_name(name, setting=setting_key)
    ]


def get_converter(name: str, *, setting: str | None = None) -> Any:
    return get_dataset_spec(name, setting=setting).converter_factory()


def load_dataset(
    name: str,
    source_code: str | None = None,
    *,
    setting: str | None = None,
) -> list[Any]:
    setting_key = normalize_setting(setting)
    dataset_name = resolve_dataset_name(name, setting=setting_key)
    default_source = _SETTING_DEFAULT_SOURCES[setting_key]
    normalized_source_code = str(source_code).strip() if source_code else default_source
    cache_key = (setting_key, dataset_name, normalized_source_code)
    if cache_key in _CACHE:
        return _CACHE[cache_key]

    spec = get_dataset_spec(dataset_name, setting=setting_key)
    source, json_source = _SOURCE_CONTEXT_RESOLVERS[setting_key](normalized_source_code)
    source_filter = source if spec.source_filter_mode == "source" else None
    entities = spec.converter_factory().convert_all(
        source_filter=source_filter,
        source=source,
        json_source=json_source,
    )
    _CACHE[cache_key] = entities
    return entities


def clear_dataset_cache(setting: str | None = None) -> None:
    if setting is None:
        _CACHE.clear()
        return

    setting_key = normalize_setting(setting)
    for key in [cache_key for cache_key in _CACHE if cache_key[0] == setting_key]:
        _CACHE.pop(key, None)


__all__ = [
    "DEFAULT_SETTING",
    "DatasetSpec",
    "clear_dataset_cache",
    "get_converter",
    "get_dataset_spec",
    "list_datasets",
    "load_dataset",
    "normalize_setting",
    "resolve_dataset_name",
]
