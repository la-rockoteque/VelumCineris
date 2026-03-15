from __future__ import annotations

from pathlib import Path

from models.entities.spell import Spell


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_models_package_has_no_pandas_imports() -> None:
    root = _repo_root() / "models"
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if "import pandas as pd" in text or "pd.Series" in text or "pd.isna" in text:
            offenders.append(str(path.relative_to(_repo_root())))

    assert offenders == []


def test_spell_ddb_metadata_survives_as_extra_fields() -> None:
    row = {
        "Spell Name": "Ashen Breath",
        "Level": "2",
        "School ABRV": "E",
        "Components ABVR": "V, S",
        "Casting Unit": "1",
        "Casting Type": "action",
        "Range Type": "point",
        "Range Distance": "self",
        "Duration Type": "timed",
        "Duration Unit": "minute",
        "Duration Amount": "1",
        "Description": "A wave of cinders rushes forward.",
        "Class": "Wizard, Sorcerer",
        "Success": "Half damage",
        "Fail": "Full damage",
        "Area Type": "cone",
        "Area Distance": "15",
        "Damage": "2d6 fire",
        "Condition": "blinded",
        "Scaling": "1d6 per slot",
        "Modifier Type": "bonus",
        "Modifier Subtype": "speed",
        "Modifier Dice Count": "1",
        "Modifier Dice Type": "6",
        "Modifier Fixed Value": "0",
        "Modifier Duration": "1",
        "Modifier Duration Unit": "round",
    }

    spell = Spell.from_row(row, source="ORIO", json_source="ORIO")
    payload = spell.to_dict()

    assert payload["name"] == "Ashen Breath"
    assert payload["ddb_save_success"] == "Half damage"
    assert payload["ddb_condition"] == "blinded"
    assert payload["ddb_modifier_type"] == "bonus"
