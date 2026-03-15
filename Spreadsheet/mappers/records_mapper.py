from __future__ import annotations

from typing import Any

import pandas as pd


def dataframe_preview(df: pd.DataFrame, *, limit: int = 10) -> list[dict[str, Any]]:
    frame = df.head(max(limit, 0)).copy()
    records: list[dict[str, Any]] = []
    for row in frame.to_dict(orient="records"):
        records.append(
            {
                str(key): (None if pd.isna(value) else value)
                for key, value in row.items()
            }
        )
    return records


def workbook_counts(records: dict[str, list[Any]]) -> dict[str, int]:
    return {sheet_name: len(rows) for sheet_name, rows in records.items()}
