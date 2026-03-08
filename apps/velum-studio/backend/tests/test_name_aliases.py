from __future__ import annotations

from app.services.integration_service import _normalize_name
from app.services.spreadsheet_service import _first_matching_value, _normalize_key, _resolve_sheet_name


def test_normalize_aliases_in_integration_service() -> None:
    assert _normalize_name("Dieties") == "deities"
    assert _normalize_name("Deities") == "deities"
    assert _normalize_name("Diety") == "deity"
    assert _normalize_name("Sciptures") == "scriptures"


def test_normalize_aliases_in_spreadsheet_service() -> None:
    assert _normalize_key("Dieties") == "deities"
    assert _normalize_key("Deities") == "deities"
    assert _normalize_key("Diety") == "deity"
    assert _normalize_key("Sciptures") == "scriptures"


def test_resolve_sheet_name_supports_legacy_and_canonical_variants() -> None:
    sheet_names = ["Deities", "Scriptures", "Species"]

    assert _resolve_sheet_name(sheet_names, "Dieties") == "Deities"
    assert _resolve_sheet_name(sheet_names, "Dieties ") == "Deities"
    assert _resolve_sheet_name(sheet_names, "Sciptures") == "Scriptures"


def test_first_matching_value_supports_deity_alias() -> None:
    row = {"Deity": "Aerith", "Other": "ignored"}
    assert _first_matching_value(row, "Diety") == "Aerith"
