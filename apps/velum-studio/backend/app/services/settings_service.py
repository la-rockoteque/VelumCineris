from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any


DEFAULT_SETTINGS: dict[str, Any] = {
    "version": 1,
    "default_source": "auto",
    "compendium": {
        "minimal_columns_default": True,
        "minimal_column_count": 8,
        "cell_char_limit": 150,
    },
    "formatter": {
        "style_template": "",
        "style_css": "",
    },
    "column_visibility": {},
}


class SettingsService:
    def __init__(self, settings_path: Path):
        self.settings_path = settings_path

    def get(self) -> dict[str, Any]:
        loaded = self._load_file()
        merged = _merge_dicts(deepcopy(DEFAULT_SETTINGS), loaded)
        return merged

    def update(self, patch: dict[str, Any]) -> dict[str, Any]:
        current = self.get()
        merged = _merge_dicts(current, patch)
        self._save_file(merged)
        return merged

    def set_sheet_columns(self, source: str, sheet: str, visible_columns: list[str]) -> dict[str, Any]:
        current = self.get()
        key = _sheet_key(source, sheet)
        current.setdefault("column_visibility", {})[key] = list(visible_columns)
        self._save_file(current)
        return current

    def reset_sheet_columns(self, source: str, sheet: str) -> dict[str, Any]:
        current = self.get()
        key = _sheet_key(source, sheet)
        current.setdefault("column_visibility", {}).pop(key, None)
        self._save_file(current)
        return current

    def _load_file(self) -> dict[str, Any]:
        file_path = self._resolve_file_path()
        if not file_path.exists():
            return {}

        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}

        return data if isinstance(data, dict) else {}

    def _save_file(self, settings: dict[str, Any]) -> None:
        file_path = self._resolve_file_path()
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(settings, indent=2, ensure_ascii=True), encoding="utf-8")

    def _resolve_file_path(self) -> Path:
        # If path points to a directory (legacy layout), store settings as settings.json inside.
        if self.settings_path.exists() and self.settings_path.is_dir():
            return self.settings_path / "settings.json"

        if self.settings_path.suffix:
            return self.settings_path

        if self.settings_path.name == ".velum":
            return self.settings_path

        return self.settings_path / "settings.json"


def _sheet_key(source: str, sheet: str) -> str:
    return f"{source.strip().lower()}::{sheet.strip()}"


def _merge_dicts(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            base[key] = _merge_dicts(base[key], value)
        else:
            base[key] = value
    return base
