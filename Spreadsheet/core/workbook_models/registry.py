from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import re
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, ValidationError, create_model, model_validator

from .providers import GoogleSheetsProvider, SheetProvider, XlsxSheetProvider


ORIMOND_SPREADSHEET_ID = "1NBZGu29IfE1ZfAWO1Z6ShR5GMLMMbaSyS0m-46PSYm4"
VALIDATION_SHEET_MARKERS = ("validation", "validations", "validaiton", "validaitons")
INVALID_VALIDATION_VALUES = {"#n/a", "#ref!", "n/a", "na", "none", "null"}


@dataclass(frozen=True)
class ValidationRule:
    column_name: str
    values: tuple[str, ...]
    normalized_values: frozenset[str]


@dataclass
class ValidationCatalog:
    by_key: dict[str, ValidationRule]
    by_sheet: dict[str, dict[str, ValidationRule]]
    enums: dict[str, type[Enum]]

    def get(self, column_name: str) -> ValidationRule | None:
        return self.by_key.get(_normalize_key(column_name))

    def enum_for(self, column_name: str) -> type[Enum] | None:
        return self.enums.get(_normalize_key(column_name))


@dataclass(frozen=True)
class ColumnSchema:
    index: int
    source_header: str
    alias_header: str
    field_name: str
    annotation: Any
    is_list: bool


@dataclass
class SheetSchema:
    sheet_name: str
    model_name: str
    header_row: int
    columns: list[ColumnSchema]
    is_validation_sheet: bool

    @property
    def field_by_column_key(self) -> dict[str, str]:
        return {_normalize_key(col.source_header): col.field_name for col in self.columns}

    @property
    def columns_by_field(self) -> dict[str, ColumnSchema]:
        return {col.field_name: col for col in self.columns}


@dataclass(frozen=True)
class RelationRule:
    parent_sheet: str
    child_sheet: str
    parent_key: str
    child_key: str
    relation_name: str
    backref_name: str | None = None


class WorkbookSheetModel(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        validate_assignment=True,
        strict=False,
    )

    __sheet_name__: ClassVar[str] = ""
    __validation_rules__: ClassVar[dict[str, ValidationRule]] = {}
    __list_fields__: ClassVar[set[str]] = set()

    @model_validator(mode="after")
    def _validate_catalog_values(self) -> "WorkbookSheetModel":
        rules = type(self).__validation_rules__
        if not rules:
            return self

        for field_name, rule in rules.items():
            value = getattr(self, field_name, None)
            if value is None:
                continue

            if field_name in type(self).__list_fields__:
                values = value if isinstance(value, list) else [value]
                for item in values:
                    if not _is_allowed_value(item, rule.normalized_values):
                        raise ValueError(
                            f"{type(self).__name__}.{field_name}: '{item}' is not in validation "
                            f"set for '{rule.column_name}'"
                        )
                continue

            if not _is_allowed_value(value, rule.normalized_values):
                raise ValueError(
                    f"{type(self).__name__}.{field_name}: '{value}' is not in validation "
                    f"set for '{rule.column_name}'"
                )

        return self


class WorkbookRegistry:
    def __init__(self, provider: SheetProvider):
        self.provider = provider
        self.schemas = self._discover_schemas()
        self.validation_catalog = self._build_validation_catalog()
        self.models = self._build_models()

    @classmethod
    def from_xlsx(cls, workbook_path: str | Path) -> "WorkbookRegistry":
        return cls(XlsxSheetProvider(workbook_path))

    @classmethod
    def from_google(cls, spreadsheet_id: str, credentials_path: str | Path) -> "WorkbookRegistry":
        return cls(GoogleSheetsProvider(spreadsheet_id, credentials_path))

    def _discover_schemas(self) -> dict[str, SheetSchema]:
        schemas: dict[str, SheetSchema] = {}

        for sheet_name in self.provider.sheet_names():
            rows = self.provider.sheet_rows(sheet_name)
            header_row = _detect_header_row(rows)
            header_cells = rows[header_row - 1] if header_row - 1 < len(rows) else []
            columns = self._build_columns_for_sheet(rows, header_cells, header_row)

            schemas[sheet_name] = SheetSchema(
                sheet_name=sheet_name,
                model_name=_to_class_name(sheet_name),
                header_row=header_row,
                columns=columns,
                is_validation_sheet=_is_validation_sheet(sheet_name),
            )

        return schemas

    def _build_columns_for_sheet(
        self,
        rows: list[list[Any]],
        header_cells: list[Any],
        header_row: int,
    ) -> list[ColumnSchema]:
        raw_headers = [_cell_to_text(value) for value in header_cells]

        used_aliases: dict[str, int] = {}
        used_fields: dict[str, int] = {}
        values_by_column: dict[int, list[Any]] = {i: [] for i in range(1, len(raw_headers) + 1)}

        for row in rows[header_row:]:
            if not any(_clean_cell(v) is not None for v in row):
                continue

            for col_idx in values_by_column:
                value = row[col_idx - 1] if col_idx - 1 < len(row) else None
                clean = _clean_cell(value)
                if clean is not None:
                    values_by_column[col_idx].append(clean)

        columns: list[ColumnSchema] = []
        for idx, source_header in enumerate(raw_headers, start=1):
            if not source_header:
                continue

            alias_header = source_header
            alias_count = used_aliases.get(alias_header, 0) + 1
            used_aliases[alias_header] = alias_count
            if alias_count > 1:
                alias_header = f"{alias_header}_{alias_count}"

            base_field = _to_field_name(alias_header)
            field_count = used_fields.get(base_field, 0) + 1
            used_fields[base_field] = field_count
            field_name = base_field if field_count == 1 else f"{base_field}_{field_count}"

            values = values_by_column.get(idx, [])
            annotation, is_list = _infer_annotation(values, source_header)

            columns.append(
                ColumnSchema(
                    index=idx,
                    source_header=source_header,
                    alias_header=alias_header,
                    field_name=field_name,
                    annotation=annotation,
                    is_list=is_list,
                )
            )

        return columns

    def _build_validation_catalog(self) -> ValidationCatalog:
        by_key: dict[str, ValidationRule] = {}
        by_sheet: dict[str, dict[str, ValidationRule]] = {}
        enums: dict[str, type[Enum]] = {}

        for schema in self.schemas.values():
            if not schema.is_validation_sheet:
                continue

            rows = self.provider.sheet_rows(schema.sheet_name)
            rules_for_sheet: dict[str, ValidationRule] = {}
            columns_by_idx = {col.index: col for col in schema.columns}
            values_by_column: dict[str, set[str]] = {col.field_name: set() for col in schema.columns}

            for row in rows[schema.header_row:]:
                if not any(_clean_cell(v) is not None for v in row):
                    continue

                for col_idx, col in columns_by_idx.items():
                    value = row[col_idx - 1] if col_idx - 1 < len(row) else None
                    text = _cell_to_text(value)
                    if not text:
                        continue
                    if _normalize_key(text) in INVALID_VALIDATION_VALUES:
                        continue
                    values_by_column[col.field_name].add(text)

            for col in schema.columns:
                raw_values = sorted(values_by_column[col.field_name])
                if not raw_values:
                    continue

                rule = ValidationRule(
                    column_name=col.source_header,
                    values=tuple(raw_values),
                    normalized_values=frozenset(_normalize_key(v) for v in raw_values),
                )
                key = _normalize_key(col.source_header)
                rules_for_sheet[key] = rule

                existing = by_key.get(key)
                if existing is None or len(rule.values) > len(existing.values):
                    by_key[key] = rule

                enum_name = f"{_to_class_name(schema.sheet_name)}{_to_class_name(col.source_header)}Enum"
                enum_type = _make_str_enum(enum_name, raw_values)
                if enum_type is not None:
                    enums[key] = enum_type

            by_sheet[schema.sheet_name] = rules_for_sheet

        return ValidationCatalog(by_key=by_key, by_sheet=by_sheet, enums=enums)

    def _build_models(self) -> dict[str, type[WorkbookSheetModel]]:
        model_map: dict[str, type[WorkbookSheetModel]] = {}

        for schema in self.schemas.values():
            field_definitions: dict[str, tuple[Any, Field]] = {}
            validation_rules: dict[str, ValidationRule] = {}
            list_fields: set[str] = set()
            scoped_rules = self._validation_rules_for_sheet(schema.sheet_name)

            for col in schema.columns:
                field_definitions[col.field_name] = (
                    col.annotation | None,
                    Field(default=None, alias=col.alias_header),
                )
                if col.is_list:
                    list_fields.add(col.field_name)

                key = _normalize_key(col.source_header)
                validation = scoped_rules.get(key)
                if validation is not None:
                    validation_rules[col.field_name] = validation

            model_cls = create_model(schema.model_name, __base__=WorkbookSheetModel, **field_definitions)
            model_cls.__sheet_name__ = schema.sheet_name
            model_cls.__validation_rules__ = validation_rules
            model_cls.__list_fields__ = list_fields
            model_map[schema.sheet_name] = model_cls

        return model_map

    def _validation_rules_for_sheet(self, sheet_name: str) -> dict[str, ValidationRule]:
        target = _normalize_key(sheet_name)
        target_singular = _normalize_key(_singularize(sheet_name))
        scored_matches: list[tuple[int, str]] = []

        for validation_sheet in self.validation_catalog.by_sheet:
            base = _validation_base_name(validation_sheet)
            if not base:
                continue
            score = _sheet_match_score(target, target_singular, base)
            if score >= 2:
                scored_matches.append((score, validation_sheet))

        if not scored_matches:
            return {}

        best_score = max(score for score, _ in scored_matches)
        merged: dict[str, ValidationRule] = {}
        for score, validation_sheet in scored_matches:
            if score == best_score:
                merged.update(self.validation_catalog.by_sheet[validation_sheet])
        return merged

    def model_for(self, sheet_name: str) -> type[WorkbookSheetModel]:
        return self.models[sheet_name]

    def available_sheets(self) -> list[str]:
        return list(self.schemas.keys())

    def load_sheet(
        self,
        sheet_name: str,
        *,
        skip_validation_sheets: bool = False,
        continue_on_error: bool = False,
    ) -> list[WorkbookSheetModel]:
        schema = self.schemas[sheet_name]
        if skip_validation_sheets and schema.is_validation_sheet:
            return []

        rows = self.provider.sheet_rows(sheet_name)
        model_cls = self.models[sheet_name]
        records: list[WorkbookSheetModel] = []

        for row in rows[schema.header_row:]:
            payload: dict[str, Any] = {}
            for col in schema.columns:
                raw = row[col.index - 1] if col.index - 1 < len(row) else None
                parsed = _parse_value(raw, col.annotation, col.is_list)
                if parsed is not None:
                    payload[col.field_name] = parsed

            if not payload:
                continue

            try:
                records.append(model_cls.model_validate(payload))
            except (ValidationError, ValueError):
                if continue_on_error:
                    continue
                raise

        return records

    def load_all(
        self,
        *,
        include_validation_sheets: bool = False,
        continue_on_error: bool = False,
    ) -> dict[str, list[WorkbookSheetModel]]:
        records: dict[str, list[WorkbookSheetModel]] = {}
        for sheet_name, schema in self.schemas.items():
            if schema.is_validation_sheet and not include_validation_sheets:
                continue
            records[sheet_name] = self.load_sheet(sheet_name, continue_on_error=continue_on_error)
        return records

    def default_relations(self) -> list[RelationRule]:
        explicit = [
            RelationRule("Classes", "Subclasses", "Name", "Class", "subclasses", "class_ref"),
            RelationRule("Classes", "Class Table", "Name", "Class", "table_rows", "class_ref"),
            RelationRule("Classes", "Class Features", "Name", "Class", "features", "class_ref"),
            RelationRule("Subclasses", "Class Features", "Name", "Subclass", "features", "subclass_ref"),
            RelationRule("Species", "SpeciesAppearance", "Name", "Name", "appearances", "species_ref"),
        ]

        dynamic: list[RelationRule] = []
        for parent in self.schemas.values():
            if parent.is_validation_sheet:
                continue
            parent_key = self._choose_primary_key(parent)
            if parent_key is None:
                continue

            singular = _singularize(parent.sheet_name)
            singular_key = _normalize_key(singular)

            for child in self.schemas.values():
                if child.is_validation_sheet or child.sheet_name == parent.sheet_name:
                    continue
                if singular_key not in child.field_by_column_key:
                    continue

                relation_name = _to_field_name(child.sheet_name)
                if not relation_name.endswith("s"):
                    relation_name += "s"

                dynamic.append(
                    RelationRule(
                        parent_sheet=parent.sheet_name,
                        child_sheet=child.sheet_name,
                        parent_key=parent_key,
                        child_key=singular,
                        relation_name=relation_name,
                        backref_name=f"{_to_field_name(parent.sheet_name)}_ref",
                    )
                )

        dedup: dict[tuple[str, str, str, str], RelationRule] = {}
        for rule in [*explicit, *dynamic]:
            key = (
                rule.parent_sheet,
                rule.child_sheet,
                _normalize_key(rule.parent_key),
                _normalize_key(rule.child_key),
            )
            if key not in dedup:
                dedup[key] = rule
        return list(dedup.values())

    def attach_relations(
        self,
        records_by_sheet: dict[str, list[WorkbookSheetModel]],
        rules: list[RelationRule] | None = None,
    ) -> dict[str, list[WorkbookSheetModel]]:
        rules = rules or self.default_relations()

        for rule in rules:
            parent_records = records_by_sheet.get(rule.parent_sheet)
            child_records = records_by_sheet.get(rule.child_sheet)
            if not parent_records or not child_records:
                continue

            parent_schema = self.schemas[rule.parent_sheet]
            child_schema = self.schemas[rule.child_sheet]
            parent_field = self._resolve_field(parent_schema, rule.parent_key)
            child_field = self._resolve_field(child_schema, rule.child_key)
            if parent_field is None or child_field is None:
                continue

            for parent in parent_records:
                setattr(parent, rule.relation_name, [])

            index: dict[str, list[WorkbookSheetModel]] = {}
            for parent in parent_records:
                parent_value = getattr(parent, parent_field, None)
                if parent_value is None:
                    continue
                key = _normalize_key(_cell_to_text(parent_value))
                if key:
                    index.setdefault(key, []).append(parent)

            for child in child_records:
                child_value = getattr(child, child_field, None)
                if child_value is None:
                    continue

                keys = child_value if isinstance(child_value, list) else [child_value]
                for raw_key in keys:
                    key = _normalize_key(_cell_to_text(raw_key))
                    if not key:
                        continue
                    for parent in index.get(key, []):
                        getattr(parent, rule.relation_name).append(child)
                        if rule.backref_name and getattr(child, rule.backref_name, None) is None:
                            setattr(child, rule.backref_name, parent)

        return records_by_sheet

    def _choose_primary_key(self, schema: SheetSchema) -> str | None:
        preferred = ("Name", "Spell Name", "Condition Name", "Background")
        keys = schema.field_by_column_key
        for key in preferred:
            if _normalize_key(key) in keys:
                return key
        return schema.columns[0].source_header if schema.columns else None

    def _resolve_field(self, schema: SheetSchema, key_or_header: str) -> str | None:
        normalized = _normalize_key(key_or_header)
        if normalized in schema.field_by_column_key:
            return schema.field_by_column_key[normalized]
        if key_or_header in schema.columns_by_field:
            return key_or_header
        for field_name in schema.columns_by_field:
            if _normalize_key(field_name) == normalized:
                return field_name
        return None


def load_orimond_registry(
    *,
    source: str = "google",
    xlsx_path: str | Path = "Spreadsheet/Orimond.xlsx",
    spreadsheet_id: str = ORIMOND_SPREADSHEET_ID,
    credentials_path: str | Path | None = None,
) -> WorkbookRegistry:
    if credentials_path is None:
        spreadsheet_key = Path("Spreadsheet/key.json")
        fivetools_key = Path("FiveETools/key.json")
        if spreadsheet_key.exists():
            credentials_path = spreadsheet_key
        elif fivetools_key.exists():
            credentials_path = fivetools_key
        else:
            credentials_path = spreadsheet_key

    normalized_source = source.strip().lower()
    if normalized_source == "xlsx":
        return WorkbookRegistry.from_xlsx(xlsx_path)
    if normalized_source == "google":
        return WorkbookRegistry.from_google(spreadsheet_id, credentials_path)
    if normalized_source == "auto":
        try:
            return WorkbookRegistry.from_google(spreadsheet_id, credentials_path)
        except Exception:
            return WorkbookRegistry.from_xlsx(xlsx_path)

    raise ValueError("source must be one of: google, xlsx, auto")


def _normalize_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value).strip().lower())


def _cell_to_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def _clean_cell(value: Any) -> Any | None:
    if value is None:
        return None
    if isinstance(value, str):
        text = value.strip()
        return text if text else None
    return value


def _to_class_name(value: str) -> str:
    parts = re.split(r"[^a-zA-Z0-9]+", value)
    class_name = "".join(part[:1].upper() + part[1:] for part in parts if part)
    if not class_name:
        class_name = "Sheet"
    if class_name[0].isdigit():
        class_name = f"Sheet{class_name}"
    return class_name


def _to_field_name(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip()).strip("_").lower()
    if not slug:
        slug = "field"
    if slug[0].isdigit():
        slug = f"f_{slug}"
    if slug in set(dir(BaseModel)):
        slug = f"{slug}_field"
    return slug


def _is_validation_sheet(sheet_name: str) -> bool:
    normalized = _normalize_key(sheet_name)
    return any(marker in normalized for marker in VALIDATION_SHEET_MARKERS)


def _detect_header_row(rows: list[list[Any]], max_scan_rows: int = 12) -> int:
    best_row = 1
    best_count = -1
    for idx, row in enumerate(rows[:max_scan_rows], start=1):
        count = sum(1 for cell in row if _cell_to_text(cell))
        if count > best_count:
            best_count = count
            best_row = idx
    return best_row


def _infer_annotation(values: list[Any], source_header: str) -> tuple[Any, bool]:
    if not values:
        return str, False

    bool_like = 0
    numeric_like = 0
    numeric_all_int = True
    str_like = 0
    list_like = 0

    for value in values:
        if isinstance(value, bool):
            bool_like += 1
            continue

        if isinstance(value, (int, float)) and not isinstance(value, bool):
            numeric_like += 1
            if isinstance(value, float) and not value.is_integer():
                numeric_all_int = False
            continue

        text = _cell_to_text(value)
        if not text:
            continue

        lowered = text.lower()
        if lowered in {"true", "false", "yes", "no"}:
            bool_like += 1
            continue

        parsed_number = _parse_number(text)
        if parsed_number is not None:
            numeric_like += 1
            if not float(parsed_number).is_integer():
                numeric_all_int = False
            continue

        str_like += 1
        if _looks_like_list_value(text, source_header):
            list_like += 1

    total = max(1, len(values))
    if str_like > 0 and list_like >= 3 and (list_like / max(1, str_like)) >= 0.6:
        return list[str], True
    if bool_like == total:
        return bool, False
    if numeric_like == total or (numeric_like > 0 and str_like == 0):
        return (int if numeric_all_int else float), False
    return str, False


def _looks_like_list_value(value: str, source_header: str) -> bool:
    text = value.strip()
    if not text or re.search(r"https?://", text, re.IGNORECASE):
        return False

    if ";" in text:
        parts = [p.strip() for p in text.split(";") if p.strip()]
        return len(parts) >= 2

    header_key = _normalize_key(source_header)
    list_hint = any(
        hint in header_key
        for hint in ("tags", "choices", "languages", "proficiencies", "domains", "classes")
    )
    if "," in text and list_hint:
        parts = [p.strip() for p in text.split(",") if p.strip()]
        return len(parts) >= 2
    return False


def _parse_number(text: str) -> float | None:
    candidate = text.strip().replace(",", "")
    if not candidate:
        return None
    try:
        return float(candidate)
    except ValueError:
        return None


def _parse_value(value: Any, annotation: Any, is_list: bool) -> Any | None:
    clean = _clean_cell(value)
    if clean is None:
        return None

    if is_list:
        if isinstance(clean, list):
            values = [_cell_to_text(v) for v in clean]
            return [v for v in values if v] or None
        text = _cell_to_text(clean)
        parts = [part.strip() for part in re.split(r"[;,]", text) if part.strip()]
        return parts or None

    if annotation is bool:
        if isinstance(clean, bool):
            return clean
        lowered = _cell_to_text(clean).lower()
        if lowered in {"true", "yes", "1"}:
            return True
        if lowered in {"false", "no", "0"}:
            return False
        return None

    if annotation is int:
        if isinstance(clean, bool):
            return None
        if isinstance(clean, int):
            return clean
        if isinstance(clean, float):
            return int(clean)
        num = _parse_number(_cell_to_text(clean))
        return int(num) if num is not None else None

    if annotation is float:
        if isinstance(clean, bool):
            return None
        if isinstance(clean, (int, float)):
            return float(clean)
        num = _parse_number(_cell_to_text(clean))
        return float(num) if num is not None else None

    return _cell_to_text(clean)


def _make_str_enum(name: str, values: list[str]) -> type[Enum] | None:
    members: dict[str, str] = {}
    used: dict[str, int] = {}

    for value in values:
        candidate = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip()).strip("_").upper()
        if not candidate:
            candidate = "VALUE"
        if candidate[0].isdigit():
            candidate = f"V_{candidate}"

        count = used.get(candidate, 0) + 1
        used[candidate] = count
        member_name = candidate if count == 1 else f"{candidate}_{count}"
        members[member_name] = value

    if not members:
        return None
    return Enum(name, members, type=str)


def _is_allowed_value(value: Any, allowed: frozenset[str]) -> bool:
    key = _normalize_key(_cell_to_text(value))
    return not key or key in allowed


def _singularize(value: str) -> str:
    text = value.strip()
    lower = text.lower()
    if lower.endswith("species"):
        return text
    if lower.endswith("ies") and len(text) > 3:
        return text[:-3] + "y"
    if lower.endswith("s") and len(text) > 1:
        return text[:-1]
    return text


def _validation_base_name(sheet_name: str) -> str:
    base = _normalize_key(sheet_name)
    for marker in VALIDATION_SHEET_MARKERS:
        base = base.replace(marker, "")
    return base


def _sheet_match_score(target: str, target_singular: str, validation_base: str) -> int:
    base = validation_base
    base_singular = _normalize_key(_singularize(base))

    if base == target:
        return 4
    if base_singular == target_singular:
        return 3
    if target.startswith(base) or target.startswith(base_singular):
        return 2
    return 0
