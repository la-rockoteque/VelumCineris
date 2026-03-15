from __future__ import annotations

from typing import Any, cast

from FiveETools.core.fantasy import sources as source_catalog
from FiveETools.datasets.json_loader import build_mapped_rows
from FiveETools.mappers.spell_mapper import map_fantasy_spell_row
from Spreadsheet.core.lazy_exports import resolve_lazy_attr
from Spreadsheet.core.converters.spell import SpellConverter
from models.datasets import get_converter as get_dataset_converter
from models.datasets import load_dataset
from models.entities.spell import Spell

_cache: dict[str, object] = {}


def row_to_spell(row, *, json_source: str) -> dict[str, Any]:
    return map_fantasy_spell_row(row, json_source=json_source)


def get_converter() -> SpellConverter:
    return cast(SpellConverter, get_dataset_converter("spells", setting="fantasy"))


def build_spells_list(source_code: str | None = None) -> list[dict[str, Any]]:
    return build_mapped_rows(
        sheets_client=source_catalog.fantasy_sheets,
        sheet_name="spells",
        source_code=source_code,
        default_source=source_catalog.DEFAULT_SOURCE,
        resolve_source_context=source_catalog.resolve_source_context,
        row_mapper=row_to_spell,
        name_column="Spell Name",
        filter_by_source=True,
    )


def build_spells_pydantic(source_code: str | None = None) -> list[Spell]:
    return cast(
        list[Spell], load_dataset("spells", source_code=source_code, setting="fantasy")
    )


_RESOLVERS = {
    "source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[0],
    "json_source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[1],
    "spells_list": build_spells_list,
    "converter": get_converter,
    "spells_pydantic": build_spells_pydantic,
}
_CACHED_ATTRS = {"spells_list", "spells_pydantic"}


def __getattr__(name: str):
    return resolve_lazy_attr(
        module_name=__name__,
        attr_name=name,
        cache=_cache,
        resolvers=_RESOLVERS,
        cached_attrs=_CACHED_ATTRS,
    )


__all__ = [
    "row_to_spell",
    "get_converter",
    "build_spells_list",
    "build_spells_pydantic",
    "source",
    "json_source",
    "spells_list",
    "converter",
    "spells_pydantic",
]
