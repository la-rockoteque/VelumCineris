from __future__ import annotations

import math
import re
from collections.abc import Iterable, Mapping
from typing import Any

RowLike = Mapping[str, Any] | Any


def row_value(row: RowLike, key: str, default: Any = None) -> Any:
    getter = getattr(row, "get", None)
    if callable(getter):
        return getter(key, default)
    try:
        return row[key]
    except Exception:
        return default


def is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, float):
        return math.isnan(value)
    try:
        return bool(value != value)
    except Exception:
        return False


def optional_text(value: Any) -> str | None:
    if is_missing(value):
        return None
    text = str(value).strip()
    return text or None


def optional_int(value: Any, default: int = 0) -> int:
    if is_missing(value):
        return default
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    text = optional_text(value)
    if not text:
        return default
    match = re.search(r"-?\d+", text)
    return int(match.group(0)) if match else default


def split_csv(value: Any) -> list[str]:
    text = optional_text(value)
    if not text:
        return []
    return [item.strip() for item in text.split(",") if item.strip()]


def ordered_row_keys(row: RowLike) -> list[str]:
    keys = getattr(row, "keys", None)
    if callable(keys):
        try:
            return [str(key) for key in keys()]
        except TypeError:
            return [str(key) for key in keys]
    if isinstance(row, Mapping):
        return [str(key) for key in row.keys()]
    return []


def values_after_key(row: RowLike, key: str) -> list[Any]:
    keys = ordered_row_keys(row)
    try:
        index = keys.index(key)
    except ValueError:
        return []
    return [row_value(row, next_key) for next_key in keys[index:]]


def iter_present_values(values: Iterable[Any]) -> list[Any]:
    return [value for value in values if not is_missing(value)]
