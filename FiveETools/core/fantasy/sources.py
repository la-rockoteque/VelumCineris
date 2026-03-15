from __future__ import annotations

from FiveETools.datasets import sources as dataset_sources
from Spreadsheet.core.lazy_exports import resolve_lazy_attr

DEFAULT_SOURCE = dataset_sources.DEFAULT_SOURCES["fantasy"]
DEFAULT_JSON_SOURCE = dataset_sources.DEFAULT_JSON_SOURCES["fantasy"]
SOURCES_SHEET_NAME = dataset_sources.SOURCES_SHEET_NAME
fantasy_sheets = dataset_sources.fantasy_sheets
_attr_cache: dict[str, object] = {}


def get_sources_sheet():
    return dataset_sources.get_sources_sheet("fantasy")


def resolve_source_context(source_code: str = DEFAULT_SOURCE) -> tuple[str, str]:
    return dataset_sources.resolve_source_context(
        setting="fantasy", source_code=source_code
    )


def get_full_source(source_code: str = DEFAULT_SOURCE) -> str:
    return dataset_sources.get_full_source(setting="fantasy", source_code=source_code)


def list_sources():
    return dataset_sources.list_sources(setting="fantasy")


_RESOLVERS = {
    "source": lambda: resolve_source_context(DEFAULT_SOURCE)[0],
    "json_source": lambda: resolve_source_context(DEFAULT_SOURCE)[1],
    "full_source": lambda: get_full_source(DEFAULT_SOURCE),
    "sources": list_sources,
}
_CACHED_ATTRS = {"source", "json_source", "full_source", "sources"}


def __getattr__(name: str):
    return resolve_lazy_attr(
        module_name=__name__,
        attr_name=name,
        cache=_attr_cache,
        resolvers=_RESOLVERS,
        cached_attrs=_CACHED_ATTRS,
    )


__all__ = [
    "DEFAULT_SOURCE",
    "DEFAULT_JSON_SOURCE",
    "SOURCES_SHEET_NAME",
    "fantasy_sheets",
    "get_sources_sheet",
    "resolve_source_context",
    "get_full_source",
    "list_sources",
    "source",
    "json_source",
    "full_source",
    "sources",
]
