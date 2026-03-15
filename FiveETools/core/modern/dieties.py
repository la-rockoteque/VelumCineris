from __future__ import annotations

from FiveETools.core.modern import sources as source_catalog
from FiveETools.datasets.json_loader import build_mapped_rows
from FiveETools.mappers.deity_mapper import map_modern_deity_row
from Spreadsheet.core.lazy_exports import resolve_lazy_attr

_cache: dict[str, object] = {}


def row_to_diety(row, *, json_source: str):
    return map_modern_deity_row(row, json_source=json_source)


def build_diety_list(source_code: str | None = None) -> list[dict]:
    return build_mapped_rows(
        sheets_client=source_catalog.modern_sheets,
        sheet_name="deities",
        source_code=source_code,
        default_source=source_catalog.DEFAULT_SOURCE,
        resolve_source_context=source_catalog.resolve_source_context,
        row_mapper=row_to_diety,
        name_column="Name",
        filter_by_source=False,
    )


_RESOLVERS = {
    "json_source": lambda: source_catalog.resolve_source_context(
        source_catalog.DEFAULT_SOURCE
    )[1],
    "diety_list": build_diety_list,
}
_CACHED_ATTRS = {"diety_list"}


def __getattr__(name: str):
    return resolve_lazy_attr(
        module_name=__name__,
        attr_name=name,
        cache=_cache,
        resolvers=_RESOLVERS,
        cached_attrs=_CACHED_ATTRS,
    )


__all__ = ["row_to_diety", "build_diety_list", "json_source", "diety_list"]
