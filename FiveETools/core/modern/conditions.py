from __future__ import annotations

from typing import cast

from FiveETools.core.modern import sources as source_catalog
from FiveETools.datasets.json_loader import build_mapped_rows
from FiveETools.mappers.condition_mapper import map_condition_row
from Spreadsheet.core.lazy_exports import resolve_lazy_attr
from Spreadsheet.core.converters.condition import ConditionConverter
from models.datasets import get_converter as get_dataset_converter
from models.datasets import load_dataset
from models.entities.condition import Condition

_cache: dict[str, object] = {}


def row_to_condition(row, *, json_source: str):
    return map_condition_row(row, json_source=json_source)


def get_converter() -> ConditionConverter:
    return cast(
        ConditionConverter, get_dataset_converter("conditions", setting="modern")
    )


def build_condition_list(source_code: str | None = None) -> list[dict]:
    return build_mapped_rows(
        sheets_client=source_catalog.modern_sheets,
        sheet_name="conditions",
        source_code=source_code,
        default_source=source_catalog.DEFAULT_SOURCE,
        resolve_source_context=source_catalog.resolve_source_context,
        row_mapper=row_to_condition,
        name_column="Condition Name",
        filter_by_source=False,
    )


def build_condition_pydantic(source_code: str | None = None) -> list[Condition]:
    return cast(
        list[Condition],
        load_dataset("conditions", source_code=source_code, setting="modern"),
    )


_RESOLVERS = {
    "source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[0],
    "json_source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[1],
    "condition_list": build_condition_list,
    "converter": get_converter,
    "condition_pydantic": build_condition_pydantic,
}
_CACHED_ATTRS = {"condition_list", "condition_pydantic"}


def __getattr__(name: str):
    return resolve_lazy_attr(
        module_name=__name__,
        attr_name=name,
        cache=_cache,
        resolvers=_RESOLVERS,
        cached_attrs=_CACHED_ATTRS,
    )


__all__ = [
    "row_to_condition",
    "get_converter",
    "build_condition_list",
    "build_condition_pydantic",
    "source",
    "json_source",
    "condition_list",
    "converter",
    "condition_pydantic",
]
