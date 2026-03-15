from __future__ import annotations

import importlib
from types import ModuleType

from .registry import (
    clear_dataset_cache,
    get_converter,
    get_dataset_spec,
    list_datasets,
    load_dataset,
    resolve_dataset_name,
)

_MODULES = {
    "sources": "models.datasets.sources",
    "spells": "models.datasets.spells",
    "monster": "models.datasets.monster",
    "diseases": "models.datasets.diseases",
    "languages": "models.datasets.languages",
    "magic_items": "models.datasets.magic_items",
}

__all__ = list(_MODULES.keys())


def __getattr__(name: str) -> ModuleType:
    module_path = _MODULES.get(name)
    if module_path is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return importlib.import_module(module_path)


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
