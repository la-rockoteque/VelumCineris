from __future__ import annotations

from pathlib import Path

import scripts.check_import_boundaries as boundaries


def _write_module(tmp_path: Path, relative_path: str, source: str) -> Path:
    path = tmp_path / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    return path


def test_top_level_sheet_call_is_flagged(monkeypatch, tmp_path: Path) -> None:
    _write_module(
        tmp_path,
        "FiveETools/core/modern/top_level.py",
        (
            "from Spreadsheet.sheets import modern_sheets\n"
            "DATA = modern_sheets.get_sheet_by_name('spells')\n"
            "\n"
            "def load() -> object:\n"
            "    return modern_sheets.get_sheet_by_name('spells')\n"
        ),
    )

    monkeypatch.setattr(boundaries, "ROOT", tmp_path)

    violations = boundaries.collect_top_level_sheet_call_violations()
    assert len(violations) == 1
    assert violations[0].file_path.name == "top_level.py"
    assert violations[0].call_name == "get_sheet_by_name"


def test_function_body_sheet_call_is_not_flagged(monkeypatch, tmp_path: Path) -> None:
    _write_module(
        tmp_path,
        "FiveETools/core/fantasy/in_function.py",
        (
            "from Spreadsheet.sheets import fantasy_sheets\n"
            "\n"
            "def load() -> object:\n"
            "    return fantasy_sheets.get_sheet('123')\n"
        ),
    )
    monkeypatch.setattr(boundaries, "ROOT", tmp_path)

    violations = boundaries.collect_top_level_sheet_call_violations()
    assert violations == []


def test_function_default_sheet_call_is_flagged(monkeypatch, tmp_path: Path) -> None:
    _write_module(
        tmp_path,
        "models/datasets/default_arg.py",
        (
            "from Spreadsheet.sheets import fantasy_sheets\n"
            "\n"
            "def load(data=fantasy_sheets.get_sheet('123')) -> object:\n"
            "    return data\n"
        ),
    )
    monkeypatch.setattr(boundaries, "ROOT", tmp_path)

    violations = boundaries.collect_top_level_sheet_call_violations()
    assert len(violations) == 1
    assert violations[0].file_path.name == "default_arg.py"
    assert violations[0].call_name == "get_sheet"


def test_path_specific_cross_app_internal_import_is_flagged(
    monkeypatch, tmp_path: Path
) -> None:
    _write_module(
        tmp_path,
        "DNDBeyond/datasets/entities.py",
        "from FiveETools.core.modern import spells\n",
    )

    monkeypatch.setattr(boundaries, "ROOT", tmp_path)

    violations = boundaries.collect_python_violations()
    assert len(violations) == 1
    assert violations[0].file_path.name == "entities.py"
    assert violations[0].forbidden_prefix == "FiveETools.core"


def test_path_specific_shim_import_is_flagged(monkeypatch, tmp_path: Path) -> None:
    _write_module(
        tmp_path,
        "Book/services/generation_service.py",
        "from Book.book_api import BookAPI\n",
    )

    monkeypatch.setattr(boundaries, "ROOT", tmp_path)

    violations = boundaries.collect_python_violations()
    assert len(violations) == 1
    assert violations[0].file_path.name == "generation_service.py"
    assert violations[0].forbidden_prefix == "Book.book_api"


def test_homebrewery_helper_core_import_is_flagged(monkeypatch, tmp_path: Path) -> None:
    _write_module(
        tmp_path,
        "Homebrewery/core/Helpers/classes.py",
        "from FiveETools.core.modern.sources import source\n",
    )

    monkeypatch.setattr(boundaries, "ROOT", tmp_path)

    violations = boundaries.collect_python_violations()
    assert len(violations) == 1
    assert violations[0].file_path.name == "classes.py"
    assert violations[0].forbidden_prefix == "FiveETools.core"
