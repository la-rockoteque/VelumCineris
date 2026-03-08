from __future__ import annotations

from dataclasses import dataclass
import json
import os
import re
from typing import Any

from .spreadsheet_service import RegistryManager


@dataclass(frozen=True)
class IntegrationSpec:
    key: str
    label: str
    description: str
    sheet_targets: tuple[str, ...]
    required_env: tuple[str, ...] = ()


INTEGRATION_SPECS: dict[str, IntegrationSpec] = {
    "worldanvil": IntegrationSpec(
        key="worldanvil",
        label="WorldAnvil",
        description="Publish selected entities and lore pages to WorldAnvil.",
        sheet_targets=(
            "Species",
            "Spells",
            "Monsters",
            "Magic Items",
            "Languages",
            "Dieties",
            "Conditions",
            "Diseases",
            "Backgrounds",
            "Feats",
        ),
        required_env=("WA_COOKIES", "WA_WORLD_ID", "WA_WORLD_SLUG"),
    ),
    "dndbeyond": IntegrationSpec(
        key="dndbeyond",
        label="D&D Beyond",
        description="Push classes, spells, items, and monsters to D&D Beyond drafts.",
        sheet_targets=(
            "Spells",
            "Species",
            "Monsters",
            "Backgrounds",
            "Feats",
            "Magic Items",
            "Items",
            "Classes",
            "Subclasses",
            "Class Features",
            "Class Table",
            "Conditions",
            "Diseases",
        ),
        required_env=("DDB_SECURITY_TOKEN", "DDB_AUTHENTICITY_TOKEN", "REQUEST_VERIFICATION_TOKEN"),
    ),
    "homebrewery": IntegrationSpec(
        key="homebrewery",
        label="Homebrewery",
        description="Render markdown/style pipelines into Homebrewery documents.",
        sheet_targets=(
            "Classes",
            "Subclasses",
            "Spells",
            "Species",
            "Backgrounds",
            "Feats",
            "Magic Items",
            "Items",
            "Languages",
            "Dieties",
            "Conditions",
            "Diseases",
        ),
    ),
    "fivetools": IntegrationSpec(
        key="fivetools",
        label="5eTools",
        description="Generate and validate 5eTools-compatible JSON bundles.",
        sheet_targets=(
            "Sources",
            "Classes",
            "Subclasses",
            "Class Features",
            "Class Table",
            "Spells",
            "Species",
            "Monsters",
            "Backgrounds",
            "Feats",
            "Magic Items",
            "Items",
            "Languages",
            "Dieties",
            "Conditions",
            "Diseases",
        ),
    ),
    "obsidianportal": IntegrationSpec(
        key="obsidianportal",
        label="Obsidian Portal",
        description="Sync campaign pages and timeline entries to Obsidian Portal.",
        sheet_targets=(
            "Sources",
            "Species",
            "Classes",
            "Subclasses",
            "Backgrounds",
            "Feats",
            "Items",
            "Magic Items",
            "Spells",
            "Monsters",
            "Dieties",
            "Languages",
        ),
        required_env=("OBSIDIANPORTAL_API_KEY",),
    ),
}


class IntegrationManager:
    def __init__(self, registry_manager: RegistryManager):
        self.registry_manager = registry_manager

    def list_cards(self, *, source: str = "auto") -> list[dict[str, Any]]:
        resolved_source = self._best_source(source)
        cards: list[dict[str, Any]] = []
        for key in INTEGRATION_SPECS:
            status = self.status(key, source=resolved_source)
            cards.append(
                {
                    "key": status["key"],
                    "label": status["label"],
                    "status": status["status"],
                    "description": status["description"],
                    "missing_env": status["missing_env"],
                    "target_sheets": status["resolved_target_sheets"],
                }
            )
        return cards

    def status(self, key: str, *, source: str = "auto") -> dict[str, Any]:
        spec = self._spec_for(key)
        resolved_source = self._best_source(source)
        missing_env = [name for name in spec.required_env if not _env_present(name)]

        available_sheets = self.registry_manager.list_sheets(resolved_source)
        resolved = self._resolve_targets(available_sheets, spec.sheet_targets)
        resolved_set = {_normalize_name(item) for item in resolved}
        missing_targets = [
            target for target in spec.sheet_targets if _normalize_name(target) not in resolved_set
        ]

        if missing_env:
            status = "disabled"
        elif resolved:
            status = "connected"
        else:
            status = "planned"

        return {
            "key": spec.key,
            "label": spec.label,
            "description": spec.description,
            "status": status,
            "source": resolved_source,
            "required_env": list(spec.required_env),
            "missing_env": missing_env,
            "target_sheets": list(spec.sheet_targets),
            "resolved_target_sheets": resolved,
            "missing_target_sheets": missing_targets,
        }

    def preview(
        self,
        key: str,
        *,
        source: str = "auto",
        limit_per_sheet: int = 100,
        include_samples: int = 3,
    ) -> dict[str, Any]:
        spec = self._spec_for(key)
        resolved_source = self._best_source(source)
        registry = self.registry_manager.get_registry(resolved_source)
        available_sheets = registry.available_sheets()
        resolved_targets = self._resolve_targets(available_sheets, spec.sheet_targets)

        sheet_previews: list[dict[str, Any]] = []
        total_rows = 0
        total_sync_candidates = 0

        for sheet_name in resolved_targets:
            sheet_preview = self._sheet_preview(
                integration_key=key,
                registry=registry,
                sheet_name=sheet_name,
                limit_per_sheet=limit_per_sheet,
                include_samples=include_samples,
            )
            sheet_previews.append(sheet_preview)
            total_rows += sheet_preview["total_rows"]
            total_sync_candidates += sheet_preview["sync_candidates"]

        status = self.status(key, source=resolved_source)
        return {
            "integration": {
                "key": spec.key,
                "label": spec.label,
                "description": spec.description,
            },
            "source": resolved_source,
            "status": status["status"],
            "missing_env": status["missing_env"],
            "sheet_preview": sheet_previews,
            "totals": {
                "sheets": len(sheet_previews),
                "rows": total_rows,
                "sync_candidates": total_sync_candidates,
            },
        }

    def sync(
        self,
        key: str,
        *,
        source: str = "auto",
        dry_run: bool = True,
        limit_per_sheet: int = 100,
        include_samples: int = 3,
    ) -> dict[str, Any]:
        preview = self.preview(
            key,
            source=source,
            limit_per_sheet=limit_per_sheet,
            include_samples=include_samples,
        )

        if not dry_run:
            raise NotImplementedError(
                "Live sync is not wired yet in Velum Studio. Use dry_run=true for execution planning."
            )

        planned_ops: list[dict[str, Any]] = []
        for sheet in preview["sheet_preview"]:
            if sheet["sync_candidates"] <= 0:
                continue
            planned_ops.append(
                {
                    "sheet": sheet["sheet"],
                    "action": f"sync_{key}",
                    "estimated_operations": sheet["sync_candidates"],
                    "estimated_skips": max(0, sheet["total_rows"] - sheet["sync_candidates"]),
                }
            )

        return {
            "integration": preview["integration"],
            "source": preview["source"],
            "dry_run": dry_run,
            "planned_operations": planned_ops,
            "totals": preview["totals"],
            "message": "Dry-run planning complete. No external API calls were made.",
        }

    def item_action(
        self,
        key: str,
        *,
        source: str,
        sheet_name: str,
        row_number: int,
        row_data: dict[str, Any],
        requested_operation: str | None = None,
        dry_run: bool = True,
    ) -> dict[str, Any]:
        status = self.status(key, source=source)
        normalized_targets = {_normalize_name(name) for name in status["resolved_target_sheets"]}
        sheet_supported = _normalize_name(sheet_name) in normalized_targets

        if not sheet_supported:
            return {
                "integration_key": key,
                "status": "skipped",
                "sheet_supported": False,
                "sheet": sheet_name,
                "row_number": row_number,
                "name": _best_name(row_data),
                "reason": f"Sheet '{sheet_name}' is not mapped for {status['label']}.",
                "dry_run": dry_run,
                "missing_env": status["missing_env"],
                "execution_detail": None,
            }

        if status["missing_env"]:
            return {
                "integration_key": key,
                "status": "blocked",
                "sheet_supported": True,
                "sheet": sheet_name,
                "row_number": row_number,
                "name": _best_name(row_data),
                "reason": "Missing required environment variables.",
                "dry_run": dry_run,
                "missing_env": status["missing_env"],
                "execution_detail": None,
            }

        id_markers = _id_column_markers_for(key)
        id_column, item_id = _find_existing_id(row_data, id_markers)
        operation = _resolve_item_operation(requested_operation=requested_operation, existing_id=item_id)

        if operation == "delete" and not item_id:
            return {
                "integration_key": key,
                "integration_label": status["label"],
                "status": "skipped",
                "sheet_supported": True,
                "sheet": sheet_name,
                "row_number": row_number,
                "name": _best_name(row_data),
                "existing_external_id": item_id,
                "existing_id_column": id_column,
                "operation": operation,
                "requested_operation": requested_operation,
                "dry_run": dry_run,
                "reason": "Delete requested but no external id was found on this row.",
                "missing_env": [],
                "execution_detail": None,
            }

        if not dry_run and operation == "delete":
            return {
                "integration_key": key,
                "integration_label": status["label"],
                "status": "unsupported",
                "sheet_supported": True,
                "sheet": sheet_name,
                "row_number": row_number,
                "name": _best_name(row_data),
                "existing_external_id": item_id,
                "existing_id_column": id_column,
                "operation": operation,
                "requested_operation": requested_operation,
                "dry_run": dry_run,
                "reason": "Live delete is not wired yet. Run in dry-run to plan the operation.",
                "missing_env": [],
                "execution_detail": None,
            }

        if not dry_run and key == "worldanvil":
            return self._execute_worldanvil_item_action(
                status=status,
                sheet_name=sheet_name,
                row_number=row_number,
                row_data=row_data,
                operation=operation,
                existing_id=item_id,
                existing_id_column=id_column,
            )
        if not dry_run:
            return {
                "integration_key": key,
                "integration_label": status["label"],
                "status": "unsupported",
                "sheet_supported": True,
                "sheet": sheet_name,
                "row_number": row_number,
                "name": _best_name(row_data),
                "existing_external_id": item_id,
                "existing_id_column": id_column,
                "operation": operation,
                "requested_operation": requested_operation,
                "dry_run": dry_run,
                "reason": "Live item action is implemented only for WorldAnvil right now.",
                "missing_env": [],
                "execution_detail": None,
            }

        return {
            "integration_key": key,
            "integration_label": status["label"],
            "status": "planned",
            "sheet_supported": True,
            "sheet": sheet_name,
            "row_number": row_number,
            "name": _best_name(row_data),
            "existing_external_id": item_id,
            "existing_id_column": id_column,
            "operation": operation,
            "requested_operation": requested_operation,
            "dry_run": dry_run,
            "reason": "Dry-run item action planned.",
            "missing_env": [],
            "execution_detail": {
                "target": "worldanvil" if key == "worldanvil" else key,
                "proposed_operation": operation,
                "requested_operation": requested_operation or "publish",
            },
        }

    def _execute_worldanvil_item_action(
        self,
        *,
        status: dict[str, Any],
        sheet_name: str,
        row_number: int,
        row_data: dict[str, Any],
        operation: str,
        existing_id: str | None,
        existing_id_column: str | None,
    ) -> dict[str, Any]:
        import requests

        from WorldAnvil.core.Helpers.WorldAnvilAPI import WorldAnvilAPI

        cookies = os.getenv("WA_COOKIES", "").strip()
        world_id = os.getenv("WA_WORLD_ID", "").strip()
        world_slug = os.getenv("WA_WORLD_SLUG", "").strip()

        session = requests.Session()
        session.headers.update(
            {
                "Cookie": cookies,
                "User-Agent": "VelumStudio/0.2",
                "Accept": "application/json, text/plain, */*",
                "Origin": "https://www.worldanvil.com",
                "Referer": f"https://www.worldanvil.com/w/{world_slug}",
            }
        )

        category_id = _worldanvil_category_for_sheet(sheet_name)
        payload = _build_worldanvil_payload(
            sheet_name=sheet_name,
            row_data=row_data,
            category_id=category_id,
        )

        api = WorldAnvilAPI(session, world_id=world_id, world_slug=world_slug)
        if existing_id:
            response = api.update_article(existing_id, payload)
            actual_operation = "update"
        else:
            response = api.create_article(payload)
            actual_operation = "create"

        if response is None:
            return {
                "integration_key": "worldanvil",
                "integration_label": status["label"],
                "status": "error",
                "sheet_supported": True,
                "sheet": sheet_name,
                "row_number": row_number,
                "name": _best_name(row_data),
                "existing_external_id": existing_id,
                "existing_id_column": existing_id_column,
                "operation": actual_operation,
                "requested_operation": operation,
                "dry_run": False,
                "reason": "WorldAnvil request failed.",
                "missing_env": [],
                "execution_detail": {
                    "last_error": api.last_error,
                    "category_id": category_id,
                    "payload_preview": _truncate_dict(payload, max_items=8),
                },
            }

        article_id = existing_id or _extract_worldanvil_article_id(response)
        return {
            "integration_key": "worldanvil",
            "integration_label": status["label"],
            "status": "executed",
            "sheet_supported": True,
            "sheet": sheet_name,
            "row_number": row_number,
            "name": _best_name(row_data),
            "existing_external_id": article_id,
            "existing_id_column": existing_id_column,
            "operation": actual_operation,
            "requested_operation": operation,
            "dry_run": False,
            "reason": f"WorldAnvil {actual_operation} request completed.",
            "missing_env": [],
            "execution_detail": {
                "article_id": article_id,
                "category_id": category_id,
                "response_preview": _truncate_dict(response, max_items=12),
            },
        }

    def _sheet_preview(
        self,
        *,
        integration_key: str,
        registry,
        sheet_name: str,
        limit_per_sheet: int,
        include_samples: int,
    ) -> dict[str, Any]:
        schema = registry.schemas[sheet_name]
        rows = registry.provider.sheet_rows(sheet_name)[schema.header_row :]

        name_col = _pick_name_column([col.alias_header for col in schema.columns])
        id_markers = _id_column_markers_for(integration_key)
        id_columns = [
            col.alias_header
            for col in schema.columns
            if _matches_any_marker(col.alias_header, id_markers)
        ]

        non_empty_rows = 0
        truncated = False
        sync_candidates = 0
        already_synced = 0
        samples: list[str] = []
        processed_limit = max(1, limit_per_sheet)

        for row in rows:
            rendered = _row_by_alias(schema.columns, row)
            if not any(value is not None for value in rendered.values()):
                continue

            non_empty_rows += 1

            id_present = any(_has_value(rendered.get(column)) for column in id_columns)
            if id_present:
                already_synced += 1
            else:
                sync_candidates += 1

            if len(samples) < include_samples:
                sample_value = rendered.get(name_col) if name_col else None
                if _has_value(sample_value):
                    samples.append(str(sample_value).strip())

            if non_empty_rows >= processed_limit:
                truncated = True
                break

        return {
            "sheet": sheet_name,
            "name_column": name_col,
            "id_columns": id_columns,
            "total_rows": non_empty_rows,
            "truncated": truncated,
            "already_synced": already_synced,
            "sync_candidates": sync_candidates,
            "sample_names": samples,
        }

    def _spec_for(self, key: str) -> IntegrationSpec:
        normalized = key.strip().lower()
        if normalized not in INTEGRATION_SPECS:
            raise KeyError(normalized)
        return INTEGRATION_SPECS[normalized]

    def _resolve_targets(self, available_sheets: list[str], targets: tuple[str, ...]) -> list[str]:
        by_norm = {_normalize_name(name): name for name in available_sheets}
        resolved: list[str] = []

        for target in targets:
            target_norm = _normalize_name(target)
            direct = by_norm.get(target_norm)
            if direct:
                resolved.append(direct)
                continue

            fuzzy = [name for name in available_sheets if target_norm in _normalize_name(name)]
            if fuzzy:
                resolved.extend(fuzzy)

        deduped: list[str] = []
        seen: set[str] = set()
        for sheet in resolved:
            if sheet in seen:
                continue
            seen.add(sheet)
            deduped.append(sheet)
        return deduped

    def _best_source(self, source: str) -> str:
        normalized = source.strip().lower()
        if normalized != "auto":
            return normalized

        availability = self.registry_manager.available_sources()
        if availability.get("xlsx", (False,))[0]:
            return "xlsx"
        return "auto"


def _normalize_name(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "", str(value).lower())
    aliases = {
        "dieties": "deities",
        "diety": "deity",
        "sciptures": "scriptures",
    }
    return aliases.get(normalized, normalized)


def _has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    return True


def _matches_any_marker(column_name: str, markers: tuple[str, ...]) -> bool:
    normalized = _normalize_name(column_name)
    return any(_normalize_name(marker) in normalized for marker in markers)


def _row_by_alias(columns, row: list[Any]) -> dict[str, Any]:
    rendered: dict[str, Any] = {}
    for col in columns:
        value = row[col.index - 1] if col.index - 1 < len(row) else None
        if isinstance(value, str):
            clean = value.strip()
            rendered[col.alias_header] = clean if clean else None
        else:
            rendered[col.alias_header] = value
    return rendered


def _env_present(name: str) -> bool:
    value = os.getenv(name)
    return bool(value and value.strip())


def _pick_name_column(columns: list[str]) -> str | None:
    preferred = (
        "Name",
        "Spell Name",
        "Condition Name",
        "Feature Name",
        "Class",
        "Background",
        "Item",
    )
    normalized_map = {_normalize_name(name): name for name in columns}
    for column in preferred:
        match = normalized_map.get(_normalize_name(column))
        if match:
            return match
    return columns[0] if columns else None


def _id_column_markers_for(integration_key: str) -> tuple[str, ...]:
    mapping = {
        "dndbeyond": ("ddb", "dnd beyond", "dndbeyond", "homebrew id"),
        "worldanvil": ("worldanvil", "world anvil", "wa", "article id"),
        "homebrewery": ("homebrewery", "markdown", "doc id"),
        "fivetools": ("5etools", "5e tools", "json", "foundry"),
        "obsidianportal": ("obsidian", "portal", "op", "article id"),
    }
    return mapping.get(integration_key, ())


def _best_name(row_data: dict[str, Any]) -> str:
    for candidate in ("Name", "Spell Name", "Condition Name", "Feature Name", "Title"):
        for key, value in row_data.items():
            if _normalize_name(key) == _normalize_name(candidate) and _has_value(value):
                return str(value).strip()
    for value in row_data.values():
        if _has_value(value):
            return str(value).strip()
    return "Unnamed Item"


def _find_existing_id(
    row_data: dict[str, Any], markers: tuple[str, ...]
) -> tuple[str | None, str | None]:
    for key, value in row_data.items():
        if not _has_value(value):
            continue
        if _matches_any_marker(key, markers):
            return key, str(value).strip()
    return None, None


def _resolve_item_operation(*, requested_operation: str | None, existing_id: str | None) -> str:
    requested = _normalize_name(requested_operation or "")

    if requested in {"delete", "remove"}:
        return "delete"
    if requested in {"create", "new"}:
        return "create"
    if requested in {"update", "edit"}:
        return "update"
    # "publish" maps to create/update depending on existing id.
    return "update" if existing_id else "create"


def _build_worldanvil_payload(
    *,
    sheet_name: str,
    row_data: dict[str, Any],
    category_id: str | None,
) -> dict[str, Any]:
    title = _best_name(row_data)
    content_lines = [f"# {title}", ""]

    for key, value in row_data.items():
        if key == "_sheet_row" or not _has_value(value):
            continue
        value_text = str(value).strip()
        if len(value_text) > 3000:
            value_text = value_text[:2997] + "..."
        content_lines.append(f"**{key}:**")
        content_lines.append(value_text)
        content_lines.append("")

    payload = {
        "title": title,
        "templateType": "article",
        "state": "private",
        "content": "\n".join(content_lines).strip(),
        "tags": [sheet_name, "velum-studio"],
    }
    if category_id:
        payload["folderId"] = category_id
    return payload


def _extract_worldanvil_article_id(response: Any) -> str | None:
    if isinstance(response, dict):
        for key in ("id", "_id", "articleId", "article_id"):
            value = response.get(key)
            if _has_value(value):
                return str(value).strip()

        article = response.get("article")
        if isinstance(article, dict):
            for key in ("id", "_id", "articleId", "article_id"):
                value = article.get(key)
                if _has_value(value):
                    return str(value).strip()
    return None


def _truncate_dict(value: Any, *, max_items: int) -> Any:
    if isinstance(value, dict):
        output: dict[str, Any] = {}
        for idx, (key, item) in enumerate(value.items()):
            if idx >= max_items:
                output["..."] = f"truncated after {max_items} fields"
                break
            output[key] = _truncate_value(item)
        return output
    if isinstance(value, list):
        sliced = value[:max_items]
        output = [_truncate_value(item) for item in sliced]
        if len(value) > max_items:
            output.append(f"... truncated after {max_items} items")
        return output
    return _truncate_value(value)


def _truncate_value(value: Any) -> Any:
    if isinstance(value, str):
        if len(value) > 500:
            return value[:497] + "..."
        return value
    if isinstance(value, (dict, list)):
        return _truncate_dict(value, max_items=8)
    return value


def _worldanvil_category_for_sheet(sheet_name: str) -> str | None:
    mapping = _json_env_object("WA_CATEGORY_MAP_JSON")
    normalized_sheet = _normalize_name(sheet_name)

    for key, value in mapping.items():
        if _normalize_name(key) == normalized_sheet and _has_value(value):
            return str(value).strip()

    fallback = os.getenv("WA_CATEGORY_ID", "").strip()
    if fallback:
        return fallback
    return None


def _json_env_object(name: str) -> dict[str, Any]:
    raw = os.getenv(name, "").strip()
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}
