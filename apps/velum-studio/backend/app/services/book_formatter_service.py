from __future__ import annotations

from datetime import datetime
from typing import Any


class BookFormatterService:
    def preview(
        self,
        *,
        sheet: str,
        row_number: int,
        row_data: dict[str, Any],
        targets: list[str],
        style_template: str | None = None,
        style_css: str | None = None,
    ) -> dict[str, Any]:
        title = _pick_title(row_data, fallback=f"{sheet} #{row_number}")
        markdown = _to_homebrewery_markdown(title=title, row_data=row_data)

        target_payloads: list[dict[str, Any]] = []
        normalized_targets = [_normalize(t) for t in targets] if targets else ["homebrewery"]
        if "homebrewery" in normalized_targets:
            target_payloads.append(
                {
                    "target": "homebrewery",
                    "status": "ready",
                    "artifact_type": "markdown",
                    "artifact_preview": _wrap_homebrewery_preview(markdown, style_css=style_css),
                }
            )

        if "googledocs" in normalized_targets or "google_docs" in normalized_targets:
            target_payloads.append(
                {
                    "target": "google_docs",
                    "status": "planned",
                    "document_title": f"{title} ({datetime.now().strftime('%Y-%m-%d')})",
                    "dry_run_steps": [
                        "Create Google Doc",
                        "Convert markdown-like structure to paragraphs",
                        "Apply heading and table styles",
                    ],
                }
            )

        if "5etools" in normalized_targets or "fivetools" in normalized_targets:
            target_payloads.append(
                {
                    "target": "fivetools",
                    "status": "ready",
                    "artifact_type": "json_fragment",
                    "artifact_preview": _to_fivetools_fragment(title=title, row_data=row_data),
                }
            )

        return {
            "sheet": sheet,
            "row_number": row_number,
            "title": title,
            "targets": target_payloads,
            "summary": _build_summary(len(target_payloads), style_template),
        }


def _wrap_homebrewery_preview(markdown: str, *, style_css: str | None) -> str:
    css = (style_css or "").strip()
    if not css:
        return markdown
    return "<style>\n" + css + "\n</style>\n\n" + markdown


def _build_summary(target_count: int, style_template: str | None) -> str:
    if style_template:
        return f"Generated formatter preview for {target_count} target(s) using style '{style_template}'."
    return f"Generated formatter preview for {target_count} target(s)."


def _pick_title(row_data: dict[str, Any], fallback: str) -> str:
    for key in ("Name", "Spell Name", "Condition Name", "Feature Name", "Title"):
        for row_key, value in row_data.items():
            if _normalize(row_key) == _normalize(key) and _has_value(value):
                return str(value).strip()
    return fallback


def _to_homebrewery_markdown(*, title: str, row_data: dict[str, Any]) -> str:
    lines = [f"## {title}", ""]
    for key, value in row_data.items():
        if key == "_sheet_row" or not _has_value(value):
            continue
        text = str(value).strip()
        if len(text) > 240:
            text = text[:237] + "..."
        lines.append(f"**{key}:** {text}")
    return "\n".join(lines)


def _to_fivetools_fragment(*, title: str, row_data: dict[str, Any]) -> str:
    fields: list[str] = []
    for key, value in row_data.items():
        if key == "_sheet_row" or not _has_value(value):
            continue
        text = str(value).strip()
        if len(text) > 160:
            text = text[:157] + "..."
        fields.append(f'    "{key}": "{text}"')

    body = ",\n".join(fields)
    return "{\n" + f'  "name": "{title}",\n' + '  "source": "VELUM",\n' + body + "\n}"


def _normalize(value: str) -> str:
    return "".join(ch for ch in str(value).lower() if ch.isalnum())


def _has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    return True
