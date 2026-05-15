from __future__ import annotations

import csv
from pathlib import Path

from .schemas import LoadingTriviaItem


def _normalize_header(value: str) -> str:
    return value.strip().lower()


def _row_value(row: list[str], index: int | None) -> str | None:
    if index is None or index >= len(row):
        return None
    value = row[index].strip()
    return value or None


def _parse_headered_rows(rows: list[list[str]]) -> list[LoadingTriviaItem]:
    headers = {_normalize_header(value): index for index, value in enumerate(rows[0])}
    items: list[LoadingTriviaItem] = []

    for row in rows[1:]:
        tidbit = _row_value(row, headers.get("tidbit"))
        if not tidbit:
            continue
        items.append(
            LoadingTriviaItem(
                tidbit=tidbit,
                entity_type=_row_value(row, headers.get("entity_type")),
                entity_name=_row_value(row, headers.get("entity_name")),
                source=_row_value(row, headers.get("source")),
            )
        )

    return items


def _parse_headerless_row(row: list[str]) -> LoadingTriviaItem | None:
    if len(row) >= 5:
        entity_type = _row_value(row, 1)
        entity_name = _row_value(row, 2)
        source = _row_value(row, 3)
        tidbit = _row_value(row, 4)
    elif len(row) >= 4:
        entity_type = _row_value(row, 0)
        entity_name = _row_value(row, 1)
        source = _row_value(row, 2)
        tidbit = _row_value(row, 3)
    else:
        return None

    if not tidbit:
        return None

    return LoadingTriviaItem(
        tidbit=tidbit,
        entity_type=entity_type,
        entity_name=entity_name,
        source=source,
    )


def load_loading_trivia_items(trivia_path: Path) -> list[LoadingTriviaItem]:
    if not trivia_path.exists():
        return []

    with trivia_path.open("r", newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.reader(handle) if any(cell.strip() for cell in row)]

    if not rows:
        return []

    normalized_headers = {_normalize_header(value) for value in rows[0]}
    if "tidbit" in normalized_headers:
        return _parse_headered_rows(rows)

    items: list[LoadingTriviaItem] = []
    for row in rows:
        item = _parse_headerless_row(row)
        if item:
            items.append(item)
    return items
