from __future__ import annotations

from typing import cast

from FiveETools.core.modern import sources as source_catalog
from FiveETools.datasets.json_loader import build_mapped_rows
from FiveETools.mappers.disease_mapper import map_disease_row
from Spreadsheet.core.lazy_exports import resolve_lazy_attr
from Spreadsheet.core.converters.disease import DiseaseConverter
from models.datasets import get_converter as get_dataset_converter
from models.datasets import load_dataset
from models.entities.disease import Disease

_cache: dict[str, object] = {}


def row_to_disease(row, *, json_source: str):
    return map_disease_row(row, json_source=json_source)


def get_converter() -> DiseaseConverter:
    return cast(DiseaseConverter, get_dataset_converter("diseases", setting="modern"))


def build_disease_list(source_code: str | None = None) -> list[dict]:
    return build_mapped_rows(
        sheets_client=source_catalog.modern_sheets,
        sheet_name="diseases",
        source_code=source_code,
        default_source=source_catalog.DEFAULT_SOURCE,
        resolve_source_context=source_catalog.resolve_source_context,
        row_mapper=row_to_disease,
        name_column="Name",
        filter_by_source=False,
    )


def build_disease_pydantic(source_code: str | None = None) -> list[Disease]:
    return cast(
        list[Disease],
        load_dataset("diseases", source_code=source_code, setting="modern"),
    )


_RESOLVERS = {
    "source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[0],
    "json_source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[1],
    "disease_list": build_disease_list,
    "converter": get_converter,
    "disease_pydantic": build_disease_pydantic,
}
_CACHED_ATTRS = {"disease_list", "disease_pydantic"}


def __getattr__(name: str):
    return resolve_lazy_attr(
        module_name=__name__,
        attr_name=name,
        cache=_cache,
        resolvers=_RESOLVERS,
        cached_attrs=_CACHED_ATTRS,
    )


__all__ = [
    "row_to_disease",
    "get_converter",
    "build_disease_list",
    "build_disease_pydantic",
    "source",
    "json_source",
    "disease_list",
    "converter",
    "disease_pydantic",
]
