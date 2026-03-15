from __future__ import annotations

from typing import cast

from Spreadsheet.core.lazy_exports import resolve_lazy_attr
from models.entities.monster import Monster
from Spreadsheet.core.converters.monster import MonsterConverter

from models.datasets.registry import get_converter as get_registered_converter
from models.datasets.registry import load_dataset
from models.datasets.sources import DEFAULT_SOURCE

_attr_cache: dict[str, object] = {}


def get_converter() -> MonsterConverter:
    return cast(MonsterConverter, get_registered_converter("monster"))


def load_monster_pydantic(source_code: str = DEFAULT_SOURCE) -> list[Monster]:
    return cast(list[Monster], load_dataset("monster", source_code))


_RESOLVERS = {
    "converter": get_converter,
    "monster_pydantic": load_monster_pydantic,
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


__all__ = ["get_converter", "load_monster_pydantic", "converter", "monster_pydantic"]
