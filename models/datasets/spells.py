from __future__ import annotations

from typing import cast

from Spreadsheet.core.lazy_exports import resolve_lazy_attr
from models.entities.spell import Spell
from Spreadsheet.core.converters.spell import SpellConverter

from models.datasets.registry import get_converter as get_registered_converter
from models.datasets.registry import load_dataset
from models.datasets.sources import DEFAULT_SOURCE

_attr_cache: dict[str, object] = {}


def get_converter() -> SpellConverter:
    return cast(SpellConverter, get_registered_converter("spells"))


def load_spells_pydantic(source_code: str = DEFAULT_SOURCE) -> list[Spell]:
    return cast(list[Spell], load_dataset("spells", source_code))


_RESOLVERS = {
    "converter": get_converter,
    "spells_pydantic": load_spells_pydantic,
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


__all__ = ["get_converter", "load_spells_pydantic", "converter", "spells_pydantic"]
