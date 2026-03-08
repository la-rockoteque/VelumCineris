from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import pandas as pd

from Spreadsheet.core.converters.spell import SpellConverter
from models.entities.spell import Spell


def _base_spell_row() -> pd.Series:
    return pd.Series(
        {
            "Spell Name": "Arc Flash",
            "Source": "ORIO",
            "Level": "3rd",
            "School": "Evocation",
            "Components ABVR": "V, S",
            "Class": "Wizard, Sorcerer",
            "Description": "A flash of crackling force.",
            "Range Type": "Point",
            "Range Distance": "Feet",
            "Range Unit": 60,
            "Duration Type": "Timed",
            "Duration Unit": "Minutes",
            "Duration Amount": 1,
            "Casting Unit": 1,
            "Casting Type": "Action",
            "Up To": "TRUE",
            "Concentration": "TRUE",
        }
    )


def test_spell_from_row_uses_child_sheet_fallbacks() -> None:
    row = _base_spell_row()
    modifiers_rows = [
        {
            "Spell": "Arc Flash",
            "Modifier Type": "bonus",
            "Modifier Subtype": "magic",
            "Modifier Dice Count": "1",
            "Modifier Dice Type": "6",
            "Modifier Duration": "1",
            "Modifier Duration Unit": "minute",
            "Modifier Details": "Extra force damage",
            "Modifier Use Primary Stat": "true",
        }
    ]
    scaling_rows = [
        {"Spell": "Arc Flash", "Scaling": "At higher levels, damage increases.", "Scaling Effect": "+1d6 force"}
    ]
    condition_rows = [
        {
            "Spell": "Arc Flash",
            "Condition": "Blinded",
            "Saving Throw": "Dexterity",
            "Success": "half damage",
            "Fail": "full damage",
        }
    ]

    spell = Spell.from_row(
        row,
        source="ORIO",
        json_source="ORIO",
        modifiers_rows=modifiers_rows,
        scaling_rows=scaling_rows,
        condition_rows=condition_rows,
    )

    assert spell.level == 3
    assert spell.school == "V"
    assert spell.savingThrow == ["dexterity"]
    assert spell.ddb_condition == "Blinded"
    assert spell.ddb_save_success == "half damage"
    assert spell.ddb_save_fail == "full damage"
    assert spell.ddb_scaling and "higher levels" in spell.ddb_scaling.lower()
    assert spell.entriesHigherLevel and "higher levels" in spell.entriesHigherLevel[0]["entries"][0].lower()

    payload = json.loads(spell.ddb_modifiers_json or "[]")
    assert len(payload) == 1
    assert payload[0]["type"] == "bonus"
    assert payload[0]["details"] == "Extra force damage"


def test_spell_from_row_handles_nan_numeric_cells() -> None:
    row = _base_spell_row()
    row["Level"] = float("nan")
    row["Casting Unit"] = float("nan")
    row["Range Unit"] = float("nan")
    row["Duration Amount"] = float("nan")
    row["School"] = "Evocation"
    row["School ABRV"] = float("nan")

    spell = Spell.from_row(row, source="ORIO", json_source="ORIO")
    assert spell.level == 0
    assert spell.school == "V"
    assert spell.time[0].number == 1
    assert spell.range.distance.amount is None
    assert spell.duration[0].duration and spell.duration[0].duration["amount"] == 1


def test_spell_from_row_maps_school_names_and_level_text() -> None:
    row = _base_spell_row()
    row["Level"] = "9th"
    row["School"] = "Necromancy"
    row["School ABRV"] = None
    spell = Spell.from_row(row, source="ORIO", json_source="ORIO")

    assert spell.level == 9
    assert spell.school == "N"


@dataclass
class FakeSheetsClient:
    spells_df: pd.DataFrame
    sheet_rows_by_title: dict[str, list[list[Any]]]

    def get_sheet(self, gid: str, *, header: int = 0) -> pd.DataFrame:
        return self.spells_df.copy()

    def list_sheet_names(self) -> list[str]:
        return list(self.sheet_rows_by_title.keys())

    def get_rows_by_title(self, title: str) -> list[list[Any]]:
        return self.sheet_rows_by_title[title]


def _build_child_rows_sheet(headers: list[str], rows: list[list[Any]]) -> list[list[Any]]:
    return [headers, *rows]


def test_spell_converter_supports_sanitized_child_sheet_names() -> None:
    spells_df = pd.DataFrame(
        [
            {"Spell Name": "Arc Flash", "Source": "ORIO", "Level": "3rd", "School": "Evocation", "Description": "desc"},
            {"Spell Name": "Ignore Me", "Source": "OTHER", "Level": "1st", "School": "Abjuration", "Description": "desc"},
        ]
    )
    client = FakeSheetsClient(
        spells_df=spells_df,
        sheet_rows_by_title={
            "Spells": _build_child_rows_sheet(["Spell Name"], [["Arc Flash"], ["Ignore Me"]]),
            "SpellsModifiers": _build_child_rows_sheet(
                ["Spell", "Modifier Type", "Modifier Details"],
                [["Arc Flash", "bonus", "Extra force damage"]],
            ),
            "SpellsScaling": _build_child_rows_sheet(
                ["Spell", "Scaling"],
                [["Arc Flash", "At higher levels, +1d6"]],
            ),
            "SpellsConditions": _build_child_rows_sheet(
                ["Spell", "Condition", "Saving Throw"],
                [["Arc Flash", "Blinded", "Dexterity"]],
            ),
        },
    )

    converter = SpellConverter(client)
    converted = converter.convert_all(source_filter="ORIO", source="ORIO", json_source="ORIO")

    assert len(converted) == 1
    spell = converted[0]
    assert spell.name == "Arc Flash"
    assert spell.ddb_condition == "Blinded"
    assert spell.ddb_scaling == "At higher levels, +1d6"
    assert spell.ddb_modifiers_json and "Extra force damage" in spell.ddb_modifiers_json


def test_spell_converter_supports_colon_child_sheet_names() -> None:
    spells_df = pd.DataFrame(
        [{"Spell Name": "Arc Flash", "Source": "ORIO", "Level": "3rd", "School": "Evocation", "Description": "desc"}]
    )
    client = FakeSheetsClient(
        spells_df=spells_df,
        sheet_rows_by_title={
            "Spells:Modifiers": _build_child_rows_sheet(
                ["Spell Name", "Modifier Type", "Modifier Details"],
                [["Arc Flash", "bonus", "details"]],
            ),
            "Spells:Scaling": _build_child_rows_sheet(["Spell Name", "Scaling"], [["Arc Flash", "scale"]]),
            "Spells:Conditions": _build_child_rows_sheet(["Spell Name", "Condition"], [["Arc Flash", "Prone"]]),
        },
    )

    converter = SpellConverter(client)
    converted = converter.convert_all(source_filter="ORIO", source="ORIO", json_source="ORIO")

    assert len(converted) == 1
    spell = converted[0]
    assert spell.ddb_condition == "Prone"
    assert spell.ddb_scaling == "scale"
    assert spell.ddb_modifiers_json and "details" in spell.ddb_modifiers_json
