from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pytest

import Spreadsheet.sheets as sheets


def _purge_modules(module_names: list[str]) -> None:
    for module_name in module_names:
        sys.modules.pop(module_name, None)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _discover_guardrail_modules() -> list[str]:
    root = _repo_root()
    module_roots = [
        root / "FiveETools/core/fantasy",
        root / "FiveETools/core/modern",
        root / "models/datasets",
    ]

    discovered: set[str] = {"models.datasets"}
    for module_root in module_roots:
        for path in module_root.glob("*.py"):
            if path.name == "__init__.py":
                continue
            discovered.add(".".join(path.relative_to(root).with_suffix("").parts))

    return sorted(discovered)


DATA_MODULES = _discover_guardrail_modules()


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _assert_export_shape(
    payload: dict,
    *,
    required_sections: dict[str, int],
) -> None:
    assert isinstance(payload.get("_meta"), dict)
    assert isinstance(payload.get("$schema"), str)

    for section, minimum_count in required_sections.items():
        section_payload = payload.get(section)
        assert isinstance(section_payload, list), f"{section} must be a list"
        assert len(section_payload) >= minimum_count, (
            f"{section} too small: got {len(section_payload)} expected >= {minimum_count}"
        )


def test_data_modules_import_without_sheet_reads(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_get_sheet(*args, **kwargs):
        raise AssertionError("Import-time sheet fetch detected via get_sheet")

    def fail_get_sheet_by_name(*args, **kwargs):
        raise AssertionError("Import-time sheet fetch detected via get_sheet_by_name")

    monkeypatch.setattr(sheets.ContentSheetsClient, "get_sheet", fail_get_sheet)
    monkeypatch.setattr(sheets.ContentSheetsClient, "get_sheet_by_name", fail_get_sheet_by_name)

    _purge_modules(DATA_MODULES)

    for module_name in DATA_MODULES:
        importlib.import_module(module_name)


def test_export_artifacts_have_expected_sections_and_volume() -> None:
    root = _repo_root()
    fantasy_path = root / "FiveETools/out/Velum_Cineris;guide_to_orimond.json"
    modern_path = root / "FiveETools/out/Velum_Cineris;everyday_guideto_concord_city.json"

    assert fantasy_path.exists(), f"Missing fantasy export: {fantasy_path}"
    assert modern_path.exists(), f"Missing modern export: {modern_path}"

    fantasy_payload = _load_json(fantasy_path)
    modern_payload = _load_json(modern_path)

    _assert_export_shape(
        fantasy_payload,
        required_sections={
            "race": 20,
            "spell": 100,
            "monster": 20,
            "condition": 10,
            "disease": 10,
            "language": 10,
            "deity": 10,
        },
    )

    _assert_export_shape(
        modern_payload,
        required_sections={
            "race": 20,
            "class": 5,
            "subclass": 5,
            "spell": 100,
            "item": 100,
            "monster": 50,
            "feat": 10,
            "background": 5,
            "condition": 10,
            "disease": 10,
            "language": 10,
            "deity": 10,
            "classFeature": 20,
            "subclassFeature": 10,
            "itemProperty": 10,
        },
    )


def test_models_datasets_public_api_surface() -> None:
    datasets = importlib.import_module("models.datasets")
    expected = {
        "sources",
        "spells",
        "monster",
        "diseases",
        "languages",
        "magic_items",
    }
    assert set(datasets.__all__) == expected

    for attr in expected:
        submodule = getattr(datasets, attr)
        assert getattr(submodule, "__name__", "").startswith("models.datasets.")
