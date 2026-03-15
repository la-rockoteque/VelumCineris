from __future__ import annotations

from typing import cast

from Spreadsheet.core.lazy_exports import resolve_lazy_attr
from models.entities.magic_item import MagicItem
from Spreadsheet.core.converters.magic_item import MagicItemConverter

from models.datasets.registry import get_converter as get_registered_converter
from models.datasets.registry import load_dataset
from models.datasets.sources import DEFAULT_SOURCE

_attr_cache: dict[str, object] = {}


def get_converter() -> MagicItemConverter:
    return cast(MagicItemConverter, get_registered_converter("magic_items"))


def load_magic_items_pydantic(source_code: str = DEFAULT_SOURCE) -> list[MagicItem]:
    return cast(list[MagicItem], load_dataset("magic_items", source_code))


_RESOLVERS = {
    "converter": get_converter,
    "magic_items_pydantic": load_magic_items_pydantic,
}
_CACHED_ATTRS: set[str] = set()


def __getattr__(name: str):
    return resolve_lazy_attr(
        module_name=__name__,
        attr_name=name,
        cache=_attr_cache,
        resolvers=_RESOLVERS,
        cached_attrs=_CACHED_ATTRS,
    )


__all__ = ["get_converter", "load_magic_items_pydantic", "converter", "magic_items_pydantic"]
