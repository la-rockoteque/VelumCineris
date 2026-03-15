from __future__ import annotations

from typing import cast

from FiveETools.core.modern import sources as source_catalog
from FiveETools.datasets.json_loader import build_mapped_rows
from FiveETools.mappers.background_mapper import map_background_row
from Spreadsheet.core.lazy_exports import resolve_lazy_attr
from Spreadsheet.core.converters.background import BackgroundConverter
from models.datasets import get_converter as get_dataset_converter
from models.datasets import load_dataset
from models.entities.background import Background

_cache: dict[str, object] = {}


def row_to_background(row, *, source: str, json_source: str):
    return map_background_row(row, source=source, json_source=json_source)


def get_converter() -> BackgroundConverter:
    return cast(
        BackgroundConverter, get_dataset_converter("backgrounds", setting="modern")
    )


def build_background_list(source_code: str | None = None) -> list[dict]:
    return build_mapped_rows(
        sheets_client=source_catalog.modern_sheets,
        sheet_name="backgrounds",
        source_code=source_code,
        default_source=source_catalog.DEFAULT_SOURCE,
        resolve_source_context=source_catalog.resolve_source_context,
        row_mapper=row_to_background,
        mapper_kwargs_builder=lambda source, json_source: {
            "source": source,
            "json_source": json_source,
        },
        name_column="Background",
        filter_by_source=True,
    )


def build_background_pydantic(source_code: str | None = None) -> list[Background]:
    return cast(
        list[Background],
        load_dataset("backgrounds", source_code=source_code, setting="modern"),
    )


_RESOLVERS = {
    "source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[0],
    "json_source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[1],
    "background_list": build_background_list,
    "converter": get_converter,
    "background_pydantic": build_background_pydantic,
}
_CACHED_ATTRS = {"background_list", "background_pydantic"}


def __getattr__(name: str):
    return resolve_lazy_attr(
        module_name=__name__,
        attr_name=name,
        cache=_cache,
        resolvers=_RESOLVERS,
        cached_attrs=_CACHED_ATTRS,
    )


__all__ = [
    "row_to_background",
    "get_converter",
    "build_background_list",
    "build_background_pydantic",
    "source",
    "json_source",
    "background_list",
    "converter",
    "background_pydantic",
]
