"""
Spell converter for transforming Google Sheets spell data to Pydantic models.
"""

from __future__ import annotations

import re
from typing import Any

from .base import BaseConverter
from models.entities.spell import Spell


class SpellConverter(BaseConverter[Spell]):
    """
    Converter for spell entities.

    Transforms DataFrame rows to validated Spell instances.
    """

    entity_class = Spell
    sheet_gid = "625265890"  # Spells sheet GID
    name_column = "Spell Name"  # Spells use "Spell Name" column
    _CHILD_SHEET_CANDIDATES = {
        "modifiers": ("Spells:Modifiers", "SpellsModifiers"),
        "scaling": ("Spells:Scaling", "SpellsScaling"),
        "conditions": ("Spells:Conditions", "SpellsConditions"),
    }

    def __init__(self, sheets_client):
        super().__init__(sheets_client)
        self._child_rows_index: dict[str, dict[str, list[dict[str, Any]]]] | None = None

    def _normalize_key(self, value: Any) -> str:
        return re.sub(r"[^a-z0-9]+", "", str(value or "").lower())

    def _load_rows_by_title(self, title: str) -> list[dict[str, Any]]:
        rows_getter = getattr(self.sheets_client, "get_rows_by_title", None)
        if rows_getter is None:
            return []

        rows = rows_getter(title)
        if not rows:
            return []

        headers = [str(cell).strip() for cell in rows[0]]
        parsed: list[dict[str, Any]] = []
        for row in rows[1:]:
            record: dict[str, Any] = {}
            for index, header in enumerate(headers):
                if not header:
                    continue
                record[header] = row[index] if index < len(row) else ""
            parsed.append(record)
        return parsed

    def _resolve_sheet_title(self, candidates: tuple[str, ...]) -> str | None:
        names_getter = getattr(self.sheets_client, "list_sheet_names", None)
        if names_getter is None:
            return candidates[0]

        try:
            sheet_names = names_getter()
        except Exception:
            return candidates[0]

        lookup = {self._normalize_key(name): name for name in sheet_names}
        for candidate in candidates:
            matched = lookup.get(self._normalize_key(candidate))
            if matched:
                return matched
        return None

    def _index_rows_by_spell(self, rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        index: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            spell_name = ""
            for key in ("Spell", "Spell Name", "Name"):
                value = str(row.get(key, "")).strip()
                if value:
                    spell_name = value
                    break
            if not spell_name:
                continue
            normalized = self._normalize_key(spell_name)
            if not normalized:
                continue
            index.setdefault(normalized, []).append(row)
        return index

    def _build_child_rows_index(self) -> dict[str, dict[str, list[dict[str, Any]]]]:
        result: dict[str, dict[str, list[dict[str, Any]]]] = {}
        for key, candidates in self._CHILD_SHEET_CANDIDATES.items():
            title = self._resolve_sheet_title(candidates)
            if not title:
                result[key] = {}
                continue
            try:
                rows = self._load_rows_by_title(title)
            except Exception:
                rows = []
            result[key] = self._index_rows_by_spell(rows)
        return result

    def _child_rows_for_spell(self, spell_name: Any, key: str) -> list[dict[str, Any]]:
        if self._child_rows_index is None:
            self._child_rows_index = self._build_child_rows_index()
        normalized = self._normalize_key(spell_name)
        if not normalized:
            return []
        return self._child_rows_index.get(key, {}).get(normalized, [])

    def convert_row(self, row, source: str, json_source: str, **kwargs) -> Spell:
        """
        Convert single spell row.

        Args:
            row: DataFrame row with spell data
            source: Source filter (e.g., "ORIO")
            json_source: JSON source identifier (e.g., "ORIO")

        Returns:
            Validated Spell instance
        """
        spell_name = row.get(self.name_column) or row.get("Name") or row.get("Spell")
        return Spell.from_row(
            row,
            source=source,
            json_source=json_source,
            modifiers_rows=self._child_rows_for_spell(spell_name, "modifiers"),
            scaling_rows=self._child_rows_for_spell(spell_name, "scaling"),
            condition_rows=self._child_rows_for_spell(spell_name, "conditions"),
        )
