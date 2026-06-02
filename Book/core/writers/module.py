from __future__ import annotations

from typing import Any, Callable

from Book.core.markdown import normalize_markdown
from Book.core.writers.base import BaseWriter


class ModuleWriter(BaseWriter):
    """Standalone writer for one independently generated entity module."""

    def __init__(
        self,
        book_api: Any,
        *,
        entity_type: str,
        source: str = "fantasy",
        title: str | None = None,
        limit: int | None = None,
    ) -> None:
        super().__init__(book_api, source=source, cover_image_url=None)
        self.entity_type = entity_type
        self.title = title or self._default_title(entity_type)
        self.limit = limit

    def get_book_title(self) -> str:
        return self.title

    def get_sections(self) -> list[tuple[str, str, Callable | None]]:
        return [(self.title, self.entity_type, None)]

    def build_markdown(self) -> str:
        entities = self.book_api.load_entities(self.entity_type, source=self.source)
        if self.limit is not None:
            entities = entities[: self.limit]
        return normalize_markdown(
            self.write_section_with_error_handling(
                self.title,
                entities,
                self.entity_type,
            )
        )

    def _default_title(self, entity_type: str) -> str:
        words = entity_type.replace("_", " ").replace("-", " ").split()
        if not words:
            return "Module"
        return " ".join(word.capitalize() for word in words)
