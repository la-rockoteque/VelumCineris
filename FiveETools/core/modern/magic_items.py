from __future__ import annotations

from typing import cast

from FiveETools.core.modern import sources as source_catalog
from FiveETools.datasets.json_loader import build_mapped_rows
from FiveETools.mappers.magic_item_mapper import map_magic_item_row
from Spreadsheet.core.lazy_exports import resolve_lazy_attr
from Spreadsheet.core.converters.magic_item import MagicItemConverter
from models.datasets import get_converter as get_dataset_converter
from models.datasets import load_dataset
from models.entities.magic_item import MagicItem

_cache: dict[str, object] = {}


def row_to_magic_item(row, *, json_source: str):
    return map_magic_item_row(row, json_source=json_source)


def get_converter() -> MagicItemConverter:
    return cast(
        MagicItemConverter, get_dataset_converter("magic_items", setting="modern")
    )


def build_magic_items_list(source_code: str | None = None) -> list[dict]:
    return build_mapped_rows(
        sheets_client=source_catalog.modern_sheets,
        sheet_name="magic_items",
        source_code=source_code,
        default_source=source_catalog.DEFAULT_SOURCE,
        resolve_source_context=source_catalog.resolve_source_context,
        row_mapper=row_to_magic_item,
        name_column="Name",
        filter_by_source=True,
    )


def build_magic_items_pydantic(source_code: str | None = None) -> list[MagicItem]:
    return cast(
        list[MagicItem],
        load_dataset("magic_items", source_code=source_code, setting="modern"),
    )


_RESOLVERS = {
    "source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[0],
    "json_source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[1],
    "magic_items_list": build_magic_items_list,
    "converter": get_converter,
    "magic_items_pydantic": build_magic_items_pydantic,
}
_CACHED_ATTRS = {"magic_items_list", "magic_items_pydantic"}


def __getattr__(name: str):
    return resolve_lazy_attr(
        module_name=__name__,
        attr_name=name,
        cache=_cache,
        resolvers=_RESOLVERS,
        cached_attrs=_CACHED_ATTRS,
    )


__all__ = [
    "row_to_magic_item",
    "get_converter",
    "build_magic_items_list",
    "build_magic_items_pydantic",
    "source",
    "json_source",
    "magic_items_list",
    "converter",
    "magic_items_pydantic",
]
