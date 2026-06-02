from __future__ import annotations

from abc import ABC
from typing import Any

from Book.core.markdown.helpers import normalize_markdown
from Book.core.markdown.templates import render_template


class EntityMarkdownRenderer(ABC):
    """Entity-owned markdown renderer backed by a Jinja template."""

    template_name: str

    def build_context(self, entity: dict[str, Any]) -> dict[str, Any]:
        return {"entity": entity}

    def render_markdown(self, entity: dict[str, Any]) -> str:
        return normalize_markdown(render_template(self.template_name, self.build_context(entity)))
