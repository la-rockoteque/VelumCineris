from __future__ import annotations

import pandas as pd

from FiveETools.datasets.json_loader import build_mapped_rows


class FakeSheetsClient:
    def __init__(self, dataframe: pd.DataFrame):
        self._dataframe = dataframe

    def get_sheet_by_name(self, sheet_name: str) -> pd.DataFrame:
        assert sheet_name == "spells"
        return self._dataframe


def test_build_mapped_rows_filters_blank_names_and_source() -> None:
    dataframe = pd.DataFrame(
        [
            {"Spell Name": "Fireball", "Source": "ORIO", "Level": 3},
            {"Spell Name": " ", "Source": "ORIO", "Level": 1},
            {"Spell Name": "Sleep", "Source": "OTHER", "Level": 1},
        ]
    )
    calls: list[tuple[str, str, str]] = []

    def row_mapper(row, *, json_source: str):
        calls.append((row["Spell Name"], row["Source"], json_source))
        return {"name": row["Spell Name"], "json_source": json_source}

    entities = build_mapped_rows(
        sheets_client=FakeSheetsClient(dataframe),
        sheet_name="spells",
        source_code="ORIO",
        default_source="ORIO",
        resolve_source_context=lambda source_code: (source_code, f"{source_code}_JSON"),
        row_mapper=row_mapper,
        name_column="Spell Name",
        filter_by_source=True,
    )

    assert entities == [{"name": "Fireball", "json_source": "ORIO_JSON"}]
    assert calls == [("Fireball", "ORIO", "ORIO_JSON")]


def test_build_mapped_rows_supports_custom_mapper_kwargs() -> None:
    dataframe = pd.DataFrame(
        [
            {"Background": "Scholar", "Source": "VSTGCC"},
        ]
    )
    calls: list[tuple[str, str, str]] = []

    def row_mapper(row, *, source: str, json_source: str):
        calls.append((row["Background"], source, json_source))
        return {"name": row["Background"], "source": source, "json_source": json_source}

    entities = build_mapped_rows(
        sheets_client=FakeSheetsClient(
            dataframe.rename(columns={"Background": "Spell Name"})
        ),
        sheet_name="spells",
        source_code="VSTGCC",
        default_source="VSTGCC",
        resolve_source_context=lambda source_code: (
            f"{source_code}_SRC",
            f"{source_code}_JSON",
        ),
        row_mapper=lambda row, **kwargs: row_mapper(
            row.rename({"Spell Name": "Background"}), **kwargs
        ),
        mapper_kwargs_builder=lambda source, json_source: {
            "source": source,
            "json_source": json_source,
        },
        name_column="Spell Name",
        filter_by_source=False,
    )

    assert entities == [
        {
            "name": "Scholar",
            "source": "VSTGCC_SRC",
            "json_source": "VSTGCC_JSON",
        }
    ]
    assert calls == [("Scholar", "VSTGCC_SRC", "VSTGCC_JSON")]
