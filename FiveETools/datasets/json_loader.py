from __future__ import annotations

import math
from collections.abc import Callable
from typing import Any

RowMapper = Callable[..., dict[str, Any]]
MapperKwargsBuilder = Callable[[str, str], dict[str, Any]]
SourceResolver = Callable[[str], tuple[str, str]]


def is_present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, float):
        return not math.isnan(value)
    try:
        return not bool(value != value)
    except Exception:
        return True


def build_mapped_rows(
    *,
    sheets_client: Any,
    sheet_name: str,
    source_code: str | None,
    default_source: str,
    resolve_source_context: SourceResolver,
    row_mapper: RowMapper,
    mapper_kwargs_builder: MapperKwargsBuilder | None = None,
    name_column: str = "Name",
    filter_by_source: bool = False,
) -> list[dict[str, Any]]:
    effective_source_code = str(source_code).strip() if source_code else default_source
    source, json_source = resolve_source_context(effective_source_code)
    mapper_kwargs = (
        mapper_kwargs_builder(source, json_source)
        if mapper_kwargs_builder is not None
        else {"json_source": json_source}
    )

    dataframe = sheets_client.get_sheet_by_name(sheet_name)
    entities: list[dict[str, Any]] = []
    for _, row in dataframe.iterrows():
        if not is_present(row.get(name_column)):
            continue
        if filter_by_source and row.get("Source") != source:
            continue
        entities.append(row_mapper(row, **mapper_kwargs))
    return entities


__all__ = ["build_mapped_rows", "is_present"]
