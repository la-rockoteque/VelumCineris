from __future__ import annotations

from pathlib import Path
import re
from typing import Any


_CSS_VAR_RE = re.compile(r"(--[a-zA-Z0-9_-]+)\s*:\s*([^;]+);")
_CSS_COLOR_RE = re.compile(r"#(?:[0-9a-fA-F]{3,8})\b|rgba?\([^)]+\)|hsla?\([^)]+\)")


class FormatterStyleService:
    def __init__(self, styles_dir: Path):
        self.styles_dir = styles_dir

    def list_templates(self) -> list[dict[str, str]]:
        if not self.styles_dir.exists():
            return []

        templates: list[dict[str, str]] = []
        for path in sorted(self.styles_dir.glob("*.css")):
            if path.name.startswith("_"):
                continue
            templates.append(
                {
                    "name": path.name,
                    "label": _label_for_template(path.name),
                }
            )
        return templates

    def load_template(self, template_name: str) -> dict[str, Any]:
        if not template_name:
            raise ValueError("template_name is required")

        safe_name = Path(template_name).name
        path = self.styles_dir / safe_name
        if not path.exists() or path.suffix.lower() != ".css":
            raise FileNotFoundError(f"Unknown template '{template_name}'")

        css = path.read_text(encoding="utf-8")
        palette = _extract_palette(css)
        return {
            "name": safe_name,
            "label": _label_for_template(safe_name),
            "css": css,
            "palette": palette,
        }


def _label_for_template(name: str) -> str:
    stem = Path(name).stem.replace("_", " ").replace("-", " ").strip()
    return " ".join(part.capitalize() for part in stem.split()) or name


def _extract_palette(css: str) -> list[dict[str, str]]:
    palette: list[dict[str, str]] = []
    seen: set[str] = set()

    for token, value in _CSS_VAR_RE.findall(css):
        color = _extract_first_color(value)
        if not color:
            continue
        key = f"{token.lower()}::{color.lower()}"
        if key in seen:
            continue
        seen.add(key)
        palette.append({"token": token, "value": color})
        if len(palette) >= 20:
            return palette

    for idx, color in enumerate(_CSS_COLOR_RE.findall(css), start=1):
        key = f"color{idx}::{color.lower()}"
        if key in seen:
            continue
        seen.add(key)
        palette.append({"token": f"color_{idx}", "value": color})
        if len(palette) >= 20:
            break

    return palette


def _extract_first_color(value: str) -> str | None:
    match = _CSS_COLOR_RE.search(value)
    if not match:
        return None
    return match.group(0)
