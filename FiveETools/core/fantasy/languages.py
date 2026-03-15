from __future__ import annotations

from typing import cast

from FiveETools.core.fantasy import sources as source_catalog
from FiveETools.datasets.json_loader import build_mapped_rows
from FiveETools.mappers.language_mapper import map_language_row
from Spreadsheet.core.lazy_exports import resolve_lazy_attr
from Spreadsheet.core.converters.language import LanguageConverter
from models.datasets import get_converter as get_dataset_converter
from models.datasets import load_dataset
from models.entities.language import Language

_cache: dict[str, object] = {}


def row_to_language(row, *, json_source: str):
    return map_language_row(row, json_source=json_source)


def get_converter() -> LanguageConverter:
    return cast(
        LanguageConverter, get_dataset_converter("languages", setting="fantasy")
    )


def build_language_list(source_code: str | None = None) -> list[dict]:
    return build_mapped_rows(
        sheets_client=source_catalog.fantasy_sheets,
        sheet_name="languages",
        source_code=source_code,
        default_source=source_catalog.DEFAULT_SOURCE,
        resolve_source_context=source_catalog.resolve_source_context,
        row_mapper=row_to_language,
        name_column="Name",
        filter_by_source=False,
    )


def build_language_pydantic(source_code: str | None = None) -> list[Language]:
    return cast(
        list[Language],
        load_dataset("languages", source_code=source_code, setting="fantasy"),
    )


_RESOLVERS = {
    "source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[0],
    "json_source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[1],
    "language_list": build_language_list,
    "converter": get_converter,
    "language_pydantic": build_language_pydantic,
}
_CACHED_ATTRS = {"language_list", "language_pydantic"}


def __getattr__(name: str):
    return resolve_lazy_attr(
        module_name=__name__,
        attr_name=name,
        cache=_cache,
        resolvers=_RESOLVERS,
        cached_attrs=_CACHED_ATTRS,
    )


__all__ = [
    "row_to_language",
    "get_converter",
    "build_language_list",
    "build_language_pydantic",
    "source",
    "json_source",
    "language_list",
    "converter",
    "language_pydantic",
]
