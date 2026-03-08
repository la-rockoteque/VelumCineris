from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from threading import Lock
import re
from typing import Any

from Spreadsheet.core.workbook_models.providers import GoogleSheetsProvider, SheetProvider, XlsxSheetProvider
from Spreadsheet.core.workbook_models.registry import (
    WorkbookRegistry,
    _cell_to_text,
    _detect_header_row,
    _is_validation_sheet,
    load_orimond_registry,
)


VALID_SOURCES = {"auto", "google", "xlsx"}
INVALID_VALIDATION_VALUES = {"#n/a", "#ref!", "n/a", "na", "none", "null"}

NON_COMPENDIUM_SHEETS = {
    "speciesappearance",
    "speciescompatibility",
    "cults",
    "sciptures",
    "scriptures",
    "classtable",
    "classfeatures",
    "vehicleupgrades",
    "mispelled",
    "spellssrd",
    "spellsrepartition",
    "spellsmodifiers",
    "spellsscaling",
    "spellsconditions",
    "money",
    "moneymatrix",
}

NON_COMPENDIUM_PATTERNS = (
    ":phonetics",
    ":grammar",
    ":script",
    "dictionary",
)

VALIDATION_EXTRA_SHEETS = {
    "itemproperty",
    "sources",
}

RELATION_RULES = (
    {
        "parent_sheet": "Species",
        "child_sheet": "SpeciesAppearance",
        "parent_key": "Name",
        "child_key": "Name",
        "section": "Appearance",
    },
    {
        "parent_sheet": "Species",
        "child_sheet": "Species:Compatibility",
        "parent_key": "Name",
        "child_key": "Species",
        "section": "Compatibility",
    },
    {
        "parent_sheet": "Dieties",
        "child_sheet": "Cults",
        "parent_key": "Name",
        "child_key": "Dieties",
        "section": "Cults",
    },
    {
        "parent_sheet": "Dieties",
        "child_sheet": "Sciptures",
        "parent_key": "Name",
        "child_key": "Diety",
        "section": "Scriptures",
    },
    {
        "parent_sheet": "Class",
        "child_sheet": "Class Table",
        "parent_key": "Name",
        "child_key": "Class",
        "section": "Class Table",
    },
    {
        "parent_sheet": "Class",
        "child_sheet": "Class Features",
        "parent_key": "Name",
        "child_key": "Class",
        "section": "Class Features",
    },
    {
        "parent_sheet": "Class",
        "child_sheet": "Class Table",
        "parent_key": "Class",
        "child_key": "Class",
        "section": "Class Table",
    },
    {
        "parent_sheet": "Class",
        "child_sheet": "Class Features",
        "parent_key": "Class",
        "child_key": "Class",
        "section": "Class Features",
    },
    {
        "parent_sheet": "Classes",
        "child_sheet": "Class Table",
        "parent_key": "Name",
        "child_key": "Class",
        "section": "Class Table",
    },
    {
        "parent_sheet": "Classes",
        "child_sheet": "Class Features",
        "parent_key": "Name",
        "child_key": "Class",
        "section": "Class Features",
    },
    {
        "parent_sheet": "Classes",
        "child_sheet": "Class Table",
        "parent_key": "Class",
        "child_key": "Class",
        "section": "Class Table",
    },
    {
        "parent_sheet": "Classes",
        "child_sheet": "Class Features",
        "parent_key": "Class",
        "child_key": "Class",
        "section": "Class Features",
    },
    {
        "parent_sheet": "Vehicles",
        "child_sheet": "Vehicle Upgrades",
        "parent_key": "Name",
        "child_key": "Vehicle",
        "section": "Upgrades",
    },
    {
        "parent_sheet": "Vehicles",
        "child_sheet": "Vehicle Upgrades",
        "parent_key": "Vehicle",
        "child_key": "Vehicle",
        "section": "Upgrades",
    },
    {
        "parent_sheet": "Spells",
        "child_sheet": "Spells:Modifiers",
        "parent_key": "Name",
        "child_key": "Spell",
        "section": "Modifiers",
    },
    {
        "parent_sheet": "Spells",
        "child_sheet": "Spells:Modifiers",
        "parent_key": "Name",
        "child_key": "Spell Name",
        "section": "Modifiers",
    },
    {
        "parent_sheet": "Spells",
        "child_sheet": "Spells:Modifiers",
        "parent_key": "Name",
        "child_key": "Name",
        "section": "Modifiers",
    },
    {
        "parent_sheet": "Spells",
        "child_sheet": "Spells:Scaling",
        "parent_key": "Name",
        "child_key": "Spell",
        "section": "Scaling",
    },
    {
        "parent_sheet": "Spells",
        "child_sheet": "Spells:Scaling",
        "parent_key": "Name",
        "child_key": "Spell Name",
        "section": "Scaling",
    },
    {
        "parent_sheet": "Spells",
        "child_sheet": "Spells:Scaling",
        "parent_key": "Name",
        "child_key": "Name",
        "section": "Scaling",
    },
    {
        "parent_sheet": "Spells",
        "child_sheet": "Spells:Conditions",
        "parent_key": "Name",
        "child_key": "Spell",
        "section": "Conditions",
    },
    {
        "parent_sheet": "Spells",
        "child_sheet": "Spells:Conditions",
        "parent_key": "Name",
        "child_key": "Spell Name",
        "section": "Conditions",
    },
    {
        "parent_sheet": "Spells",
        "child_sheet": "Spells:Conditions",
        "parent_key": "Name",
        "child_key": "Name",
        "section": "Conditions",
    },
    {
        "parent_sheet": "Spells",
        "child_sheet": "Spells:Modifiers",
        "parent_key": "Spell Name",
        "child_key": "Spell",
        "section": "Modifiers",
    },
    {
        "parent_sheet": "Spells",
        "child_sheet": "Spells:Scaling",
        "parent_key": "Spell Name",
        "child_key": "Spell",
        "section": "Scaling",
    },
    {
        "parent_sheet": "Spells",
        "child_sheet": "Spells:Conditions",
        "parent_key": "Spell Name",
        "child_key": "Spell",
        "section": "Conditions",
    },
)


@dataclass(frozen=True)
class SpreadsheetRuntimeConfig:
    spreadsheet_id: str
    xlsx_path: Path
    credentials_path: Path


class RegistryManager:
    def __init__(self, cfg: SpreadsheetRuntimeConfig):
        self.cfg = cfg
        self._lock = Lock()
        self._cache: dict[str, WorkbookRegistry] = {}
        self._provider_cache: dict[str, SheetProvider] = {}

    def available_sources(self) -> dict[str, tuple[bool, str | None]]:
        xlsx_exists = self.cfg.xlsx_path.exists()
        credentials_exists = self.cfg.credentials_path.exists()

        return {
            "auto": (xlsx_exists or credentials_exists, None),
            "google": (
                credentials_exists,
                None if credentials_exists else f"Missing credentials at {self.cfg.credentials_path}",
            ),
            "xlsx": (
                xlsx_exists,
                None if xlsx_exists else f"Missing workbook at {self.cfg.xlsx_path}",
            ),
        }

    def get_registry(self, source: str) -> WorkbookRegistry:
        normalized = source.strip().lower()
        if normalized not in VALID_SOURCES:
            raise ValueError(f"Invalid source '{source}'. Use one of: auto, google, xlsx")
        if normalized == "auto" and self.cfg.xlsx_path.exists():
            normalized = "xlsx"

        with self._lock:
            cached = self._cache.get(normalized)
            if cached is not None:
                return cached

            registry = load_orimond_registry(
                source=normalized,
                xlsx_path=self.cfg.xlsx_path,
                spreadsheet_id=self.cfg.spreadsheet_id,
                credentials_path=self.cfg.credentials_path,
            )
            self._cache[normalized] = registry
            return registry

    def list_sheets(self, source: str) -> list[str]:
        _, provider = self._provider_for(source)
        return provider.sheet_names()

    def list_compendium_sheets(self, source: str) -> list[str]:
        sheets = self.list_sheets(source)
        return [sheet for sheet in sheets if _is_compendium_sheet(sheet)]

    def list_validation_sheets(self, source: str) -> list[str]:
        sheets = self.list_sheets(source)
        return [sheet for sheet in sheets if _is_validation_like_sheet(sheet)]

    def list_money_sheets(self, source: str) -> list[str]:
        sheets = self.list_sheets(source)
        return [sheet for sheet in sheets if _is_money_sheet(sheet)]

    def schema_for(self, source: str, sheet_name: str) -> tuple[list[str], int, bool, list[str]]:
        _, provider = self._provider_for(source)
        rows = provider.sheet_rows(sheet_name)
        header_row = _detect_header_row(rows)

        header_cells = rows[header_row - 1] if header_row - 1 < len(rows) else []
        columns = _normalized_headers(header_cells)
        is_validation_sheet = _is_validation_sheet(sheet_name)
        validation_columns = list(columns) if is_validation_sheet else []

        return columns, header_row, is_validation_sheet, validation_columns

    def rows_for(
        self,
        source: str,
        sheet_name: str,
        *,
        offset: int = 0,
        limit: int = 100,
        query: str | None = None,
    ) -> tuple[list[str], list[dict[str, Any]], int]:
        _, provider = self._provider_for(source)
        rows = provider.sheet_rows(sheet_name)
        header_row = _detect_header_row(rows)

        header_cells = rows[header_row - 1] if header_row - 1 < len(rows) else []
        columns_with_index = _indexed_headers(header_cells)
        columns = [item["alias"] for item in columns_with_index]

        data_rows = rows[header_row:]
        needle = (query or "").strip().lower()

        filtered: list[tuple[int, list[Any]]] = []

        for idx, row in enumerate(data_rows):
            if not any(
                _clean_cell(row[col["index"] - 1] if col["index"] - 1 < len(row) else None) is not None
                for col in columns_with_index
            ):
                continue

            if needle:
                joined = " | ".join(
                    _as_text(row[col["index"] - 1] if col["index"] - 1 < len(row) else None).lower()
                    for col in columns_with_index
                )
                if needle not in joined:
                    continue

            filtered.append((idx + header_row + 1, row))

        total = len(filtered)
        window = filtered[offset : offset + limit]

        result_rows: list[dict[str, Any]] = []
        for sheet_row_number, row in window:
            rendered: dict[str, Any] = {"_sheet_row": sheet_row_number}
            for col in columns_with_index:
                value = row[col["index"] - 1] if col["index"] - 1 < len(row) else None
                rendered[col["alias"]] = _clean_cell(value)
            result_rows.append(rendered)

        return columns, result_rows, total

    def row_for(
        self,
        source: str,
        sheet_name: str,
        *,
        row_number: int,
    ) -> tuple[list[str], dict[str, Any], int]:
        if row_number < 1:
            raise ValueError("row_number must be >= 1")

        _, provider = self._provider_for(source)
        rows = provider.sheet_rows(sheet_name)
        if row_number > len(rows):
            raise KeyError(f"Row {row_number} is out of range for sheet '{sheet_name}'")

        header_row = _detect_header_row(rows)
        header_cells = rows[header_row - 1] if header_row - 1 < len(rows) else []
        columns_with_index = _indexed_headers(header_cells)
        columns = [item["alias"] for item in columns_with_index]

        row = rows[row_number - 1]
        rendered: dict[str, Any] = {"_sheet_row": row_number}
        for col in columns_with_index:
            value = row[col["index"] - 1] if col["index"] - 1 < len(row) else None
            rendered[col["alias"]] = _clean_cell(value)

        return columns, rendered, header_row

    def row_sections_for(
        self,
        source: str,
        sheet_name: str,
        row_data: dict[str, Any],
    ) -> list[dict[str, Any]]:
        _, provider = self._provider_for(source)
        grouped_sections: dict[tuple[str, str], dict[str, Any]] = {}

        for rule in RELATION_RULES:
            if _normalize_key(rule["parent_sheet"]) != _normalize_key(sheet_name):
                continue

            target_sheet = _resolve_sheet_name(provider.sheet_names(), rule["child_sheet"])
            if target_sheet is None:
                continue

            parent_value = _first_matching_value(row_data, rule["parent_key"])
            if parent_value is None:
                continue

            child_rows = provider.sheet_rows(target_sheet)
            child_header_row = _detect_header_row(child_rows)
            child_headers = child_rows[child_header_row - 1] if child_header_row - 1 < len(child_rows) else []
            child_columns = _indexed_headers(child_headers)

            matches: list[dict[str, Any]] = []
            for row in child_rows[child_header_row:]:
                rendered = _render_row(child_columns, row)
                if not any(v is not None for v in rendered.values()):
                    continue

                child_value = _first_matching_value(rendered, rule["child_key"])
                if child_value is None:
                    continue

                if _value_matches(parent_value, child_value):
                    matches.append(rendered)

            if not matches:
                continue

            section_key = (rule["section"], target_sheet)
            bucket = grouped_sections.get(section_key)
            if bucket is None:
                bucket = {
                    "section": rule["section"],
                    "sheet": target_sheet,
                    "count": 0,
                    "rows": [],
                    "_seen": set(),
                }
                grouped_sections[section_key] = bucket

            for match in matches:
                signature = _row_signature(match)
                if signature in bucket["_seen"]:
                    continue
                bucket["_seen"].add(signature)
                bucket["rows"].append(match)

            bucket["count"] = len(bucket["rows"])

        sections = list(grouped_sections.values())
        for section in sections:
            section.pop("_seen", None)

        if _normalize_key(sheet_name) in {"spell", "spells"}:
            existing_names = {_normalize_key(section["section"]) for section in sections}
            for virtual in _build_virtual_spell_sections(row_data):
                if _normalize_key(virtual["section"]) in existing_names:
                    continue
                sections.append(virtual)

        return sections

    def records_for(
        self,
        source: str,
        sheet_name: str,
        *,
        limit: int = 5000,
    ) -> tuple[list[str], list[dict[str, Any]]]:
        _, provider = self._provider_for(source)
        rows = provider.sheet_rows(sheet_name)
        header_row = _detect_header_row(rows)
        header_cells = rows[header_row - 1] if header_row - 1 < len(rows) else []
        columns_with_index = _indexed_headers(header_cells)
        columns = [item["alias"] for item in columns_with_index]

        records: list[dict[str, Any]] = []
        for row in rows[header_row:]:
            rendered: dict[str, Any] = {}
            for col in columns_with_index:
                value = row[col["index"] - 1] if col["index"] - 1 < len(row) else None
                rendered[col["alias"]] = _clean_cell(value)
            if any(value is not None for value in rendered.values()):
                records.append(rendered)
            if len(records) >= limit:
                break

        return columns, records

    def validation_catalog(self, source: str) -> dict[str, Any]:
        _, provider = self._provider_for(source)
        catalog: dict[str, dict[str, Any]] = {}
        by_sheet: dict[str, dict[str, list[str]]] = {}

        for sheet in self.list_validation_sheets(source):
            rows = provider.sheet_rows(sheet)
            header_row = _detect_header_row(rows)
            header_cells = rows[header_row - 1] if header_row - 1 < len(rows) else []
            columns = _indexed_headers(header_cells)
            values_per_column: dict[str, set[str]] = {col["alias"]: set() for col in columns}

            for row in rows[header_row:]:
                if not any(_clean_cell(v) is not None for v in row):
                    continue

                for col in columns:
                    raw = row[col["index"] - 1] if col["index"] - 1 < len(row) else None
                    text = _as_text(raw)
                    if not text:
                        continue
                    if _normalize_key(text) in INVALID_VALIDATION_VALUES:
                        continue
                    values_per_column[col["alias"]].add(text)

            sheet_values: dict[str, list[str]] = {}
            for col in columns:
                alias = col["alias"]
                ordered = sorted(values_per_column.get(alias, set()))
                sheet_values[alias] = ordered
                if not ordered:
                    continue

                key = _normalize_key(col["source"])
                existing = catalog.get(key)
                if existing is None or len(ordered) > len(existing["values"]):
                    catalog[key] = {
                        "field": col["source"],
                        "values": ordered,
                        "sheet": sheet,
                    }

            by_sheet[sheet] = sheet_values

        return {
            "sheets": self.list_validation_sheets(source),
            "options_by_field": catalog,
            "options_by_sheet": by_sheet,
        }

    def money_catalog(self, source: str) -> dict[str, Any]:
        _, provider = self._provider_for(source)
        names = provider.sheet_names()
        money_sheet = _resolve_sheet_name(names, "Money") or _resolve_first_sheet(names, ("money",))
        matrix_sheet = _resolve_sheet_name(names, "Money Matrix") or _resolve_sheet_name(
            names, "MoneyMatrix"
        ) or _resolve_first_sheet(names, ("moneymatrix",))

        currencies: list[str] = []
        matrix: dict[str, dict[str, float]] = {}

        if money_sheet:
            cols, records = self.records_for(source, money_sheet, limit=5000)
            currency_col = _pick_currency_column(cols)
            seen: set[str] = set()
            for record in records:
                value = _as_text(record.get(currency_col))
                if not value:
                    continue
                if value.lower() in seen:
                    continue
                seen.add(value.lower())
                currencies.append(value)

        if matrix_sheet:
            rows = provider.sheet_rows(matrix_sheet)
            header_row = _detect_header_row(rows)
            header_cells = rows[header_row - 1] if header_row - 1 < len(rows) else []
            columns = _indexed_headers(header_cells)

            if columns:
                row_key = columns[0]["alias"]
                target_cols = [col["alias"] for col in columns[1:]]

                for raw_row in rows[header_row:]:
                    rendered = _render_row(columns, raw_row)
                    base_currency = _as_text(rendered.get(row_key))
                    if not base_currency:
                        continue

                    rates: dict[str, float] = {}
                    for target in target_cols:
                        numeric = _to_float(rendered.get(target))
                        if numeric is not None:
                            rates[target] = numeric
                    if rates:
                        matrix[base_currency] = rates

                if not currencies:
                    deduped = set(matrix.keys())
                    for row_rates in matrix.values():
                        deduped.update(row_rates.keys())
                    currencies = sorted(deduped)

        return {
            "money_sheet": money_sheet,
            "matrix_sheet": matrix_sheet,
            "currencies": currencies,
            "matrix": matrix,
        }

    def _provider_for(self, source: str) -> tuple[str, SheetProvider]:
        normalized = source.strip().lower()
        if normalized not in VALID_SOURCES:
            raise ValueError(f"Invalid source '{source}'. Use one of: auto, google, xlsx")

        resolved = normalized
        if normalized == "auto":
            if self.cfg.xlsx_path.exists():
                resolved = "xlsx"
            elif self.cfg.credentials_path.exists():
                resolved = "google"

        key = f"{resolved}:{self.cfg.spreadsheet_id}:{self.cfg.xlsx_path}:{self.cfg.credentials_path}"

        with self._lock:
            cached = self._provider_cache.get(key)
            if cached is not None:
                return resolved, cached

            if resolved == "xlsx":
                provider = XlsxSheetProvider(self.cfg.xlsx_path)
            elif resolved == "google":
                provider = GoogleSheetsProvider(self.cfg.spreadsheet_id, self.cfg.credentials_path)
            else:
                raise ValueError("No available source for auto mode. Provide xlsx or google credentials.")

            self._provider_cache[key] = provider
            return resolved, provider


def _indexed_headers(header_cells: list[Any]) -> list[dict[str, Any]]:
    used_aliases: dict[str, int] = {}
    columns: list[dict[str, Any]] = []

    for idx, raw in enumerate(header_cells, start=1):
        source = _cell_to_text(raw)
        if not source:
            continue

        alias = source
        alias_count = used_aliases.get(alias, 0) + 1
        used_aliases[alias] = alias_count
        if alias_count > 1:
            alias = f"{alias}_{alias_count}"

        columns.append({"index": idx, "source": source, "alias": alias})

    return columns


def _render_row(columns: list[dict[str, Any]], row: list[Any]) -> dict[str, Any]:
    rendered: dict[str, Any] = {}
    for col in columns:
        value = row[col["index"] - 1] if col["index"] - 1 < len(row) else None
        rendered[col["alias"]] = _clean_cell(value)
    return rendered


def _row_signature(row: dict[str, Any]) -> str:
    normalized = []
    for key in sorted(row.keys()):
        normalized.append(f"{_normalize_key(key)}={_as_text(row[key])}")
    return "|".join(normalized)


def _build_virtual_spell_sections(row_data: dict[str, Any]) -> list[dict[str, Any]]:
    spell_name = (
        _first_matching_value(row_data, "Name")
        or _first_matching_value(row_data, "Spell Name")
        or _first_matching_value(row_data, "Spell")
        or "Spell"
    )

    buckets: dict[str, list[str]] = {
        "Modifiers": [],
        "Scaling": [],
        "Conditions": [],
    }

    for field, value in row_data.items():
        normalized = _normalize_key(field)
        if "modifier" in normalized:
            buckets["Modifiers"].extend(_split_multi_values(value))
        elif "scaling" in normalized:
            buckets["Scaling"].extend(_split_multi_values(value))
        elif "condition" in normalized:
            buckets["Conditions"].extend(_split_multi_values(value))

    sections: list[dict[str, Any]] = []
    for label, values in buckets.items():
        deduped = []
        seen = set()
        for item in values:
            key = item.lower()
            if key in seen:
                continue
            seen.add(key)
            deduped.append(item)

        if not deduped:
            continue

        sections.append(
            {
                "section": label,
                "sheet": "Spells (virtual)",
                "count": len(deduped),
                "rows": [{"Spell": _as_text(spell_name), "Value": item} for item in deduped],
            }
        )

    return sections


def _normalized_headers(header_cells: list[Any]) -> list[str]:
    return [item["alias"] for item in _indexed_headers(header_cells)]


def _as_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _clean_cell(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, str):
        text = value.strip()
        return text if text else None
    return value


def _normalize_key(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "", str(value).lower())
    aliases = {
        "dieties": "deities",
        "diety": "deity",
        "sciptures": "scriptures",
    }
    return aliases.get(normalized, normalized)


def _resolve_sheet_name(sheet_names: list[str], target: str) -> str | None:
    target_norm = _normalize_key(target)
    for name in sheet_names:
        if _normalize_key(name) == target_norm:
            return name
    return None


def _resolve_first_sheet(sheet_names: list[str], patterns: tuple[str, ...]) -> str | None:
    for name in sheet_names:
        normalized = _normalize_key(name)
        if any(pattern in normalized for pattern in patterns):
            return name
    return None


def _first_matching_value(row: dict[str, Any], key: str) -> Any:
    wanted = _normalize_key(key)
    for row_key, value in row.items():
        if _normalize_key(row_key) == wanted:
            return value
    return None


def _value_matches(parent_value: Any, child_value: Any) -> bool:
    parent_norm = _normalize_key(_as_text(parent_value))
    if not parent_norm:
        return False

    child_text = _as_text(child_value)
    parts = [segment.strip() for segment in re.split(r"[,;/|]", child_text) if segment.strip()]
    if not parts:
        parts = [child_text]

    return any(_normalize_key(part) == parent_norm for part in parts)


def _split_multi_values(value: Any) -> list[str]:
    text = _as_text(value)
    if not text:
        return []

    values = [part.strip() for part in re.split(r"[\n,;/|]+", text) if part.strip()]
    if values:
        return values
    return [text]


def _is_compendium_sheet(sheet_name: str) -> bool:
    if _is_validation_like_sheet(sheet_name):
        return False

    normalized = _normalize_key(sheet_name)
    if normalized in NON_COMPENDIUM_SHEETS:
        return False

    lowered = sheet_name.strip().lower()
    if any(marker in lowered for marker in NON_COMPENDIUM_PATTERNS):
        return False

    return True


def _is_validation_like_sheet(sheet_name: str) -> bool:
    if _is_validation_sheet(sheet_name):
        return True
    normalized = _normalize_key(sheet_name)
    if normalized in VALIDATION_EXTRA_SHEETS:
        return True
    if "validation" in normalized:
        return True
    return False


def _is_money_sheet(sheet_name: str) -> bool:
    normalized = _normalize_key(sheet_name)
    return normalized == "money" or normalized == "moneymatrix"


def _pick_currency_column(columns: list[str]) -> str:
    if not columns:
        return ""

    markers = ("currency", "name", "code", "short")
    for column in columns:
        normalized = _normalize_key(column)
        if any(marker in normalized for marker in markers):
            return column
    return columns[0]


def _to_float(value: Any) -> float | None:
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    text = _as_text(value).replace(",", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None
