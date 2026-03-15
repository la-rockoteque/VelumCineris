from __future__ import annotations

from typing import cast

from FiveETools.core.modern import sources as source_catalog
from FiveETools.datasets.json_loader import build_mapped_rows
from FiveETools.mappers.item_mapper import map_item_property_row, map_item_row
from Spreadsheet.core.lazy_exports import resolve_lazy_attr
from Spreadsheet.core.converters.item import ItemConverter
from models.datasets import get_converter as get_dataset_converter
from models.datasets import load_dataset
from models.entities.item import Item

_cache: dict[str, object] = {}


def row_to_property(row, *, json_source: str):
    return map_item_property_row(row, json_source=json_source)


def row_to_item(row, *, json_source: str):
    return map_item_row(row, json_source=json_source)


def get_converter() -> ItemConverter:
    return cast(ItemConverter, get_dataset_converter("items", setting="modern"))


def build_item_property_list(source_code: str | None = None) -> list[dict]:
    return build_mapped_rows(
        sheets_client=source_catalog.modern_sheets,
        sheet_name="item_properties",
        source_code=source_code,
        default_source=source_catalog.DEFAULT_SOURCE,
        resolve_source_context=source_catalog.resolve_source_context,
        row_mapper=row_to_property,
        name_column="Name",
        filter_by_source=False,
    )


def build_items_list(source_code: str | None = None) -> list[dict]:
    return build_mapped_rows(
        sheets_client=source_catalog.modern_sheets,
        sheet_name="items",
        source_code=source_code,
        default_source=source_catalog.DEFAULT_SOURCE,
        resolve_source_context=source_catalog.resolve_source_context,
        row_mapper=row_to_item,
        name_column="Name",
        filter_by_source=True,
    )


def build_items_pydantic(source_code: str | None = None) -> list[Item]:
    return cast(
        list[Item], load_dataset("items", source_code=source_code, setting="modern")
    )


_RESOLVERS = {
    "source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[0],
    "json_source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[1],
    "item_property_list": build_item_property_list,
    "items_list": build_items_list,
    "converter": get_converter,
    "items_pydantic": build_items_pydantic,
}
_CACHED_ATTRS = {"item_property_list", "items_list", "items_pydantic"}


def __getattr__(name: str):
    return resolve_lazy_attr(
        module_name=__name__,
        attr_name=name,
        cache=_cache,
        resolvers=_RESOLVERS,
        cached_attrs=_CACHED_ATTRS,
    )


__all__ = [
    "row_to_property",
    "row_to_item",
    "get_converter",
    "build_item_property_list",
    "build_items_list",
    "build_items_pydantic",
    "source",
    "json_source",
    "item_property_list",
    "items_list",
    "converter",
    "items_pydantic",
]
