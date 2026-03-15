from __future__ import annotations

import importlib
from types import ModuleType
from typing import Any

_DATASET_MODULES: dict[str, str] = {
    "fantasy": "FiveETools.datasets.fantasy",
    "modern": "FiveETools.datasets.modern",
}


def normalize_setting(setting: str) -> str:
    key = str(setting).strip().lower()
    if key not in _DATASET_MODULES:
        raise ValueError(
            f"Unknown setting '{setting}'. Expected one of: {sorted(_DATASET_MODULES)}"
        )
    return key


def get_dataset_module(setting: str) -> ModuleType:
    return importlib.import_module(_DATASET_MODULES[normalize_setting(setting)])


def resolve_source_code(*, setting: str, source_code: str | None = None) -> str:
    dataset_module = get_dataset_module(setting)
    return dataset_module.resolve_source_code(source_code)


def load_entities(
    *,
    entity_type: str,
    setting: str,
    source_code: str | None = None,
) -> list[dict[str, Any]]:
    dataset_module = get_dataset_module(setting)
    return dataset_module.load_entities(entity_type, source_code=source_code)


def list_entity_types(setting: str | None = None) -> tuple[str, ...]:
    if setting is None:
        entity_types: set[str] = set()
        for setting_name in _DATASET_MODULES:
            entity_types.update(get_dataset_module(setting_name).list_entity_types())
        return tuple(sorted(entity_types))

    dataset_module = get_dataset_module(setting)
    return dataset_module.list_entity_types()


def get_source_catalog(setting: str) -> Any:
    dataset_module = get_dataset_module(setting)
    return dataset_module.get_source_catalog()


def __getattr__(name: str) -> ModuleType:
    module_path = _DATASET_MODULES.get(name)
    if module_path is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return importlib.import_module(module_path)


__all__ = [
    "fantasy",
    "modern",
    "normalize_setting",
    "get_dataset_module",
    "resolve_source_code",
    "load_entities",
    "list_entity_types",
    "get_source_catalog",
]
