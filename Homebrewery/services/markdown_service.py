from __future__ import annotations

from Homebrewery.datasets import load_entities
from Homebrewery.mappers import map_entity_markdown


class HomebreweryMarkdownService:
    def build_markdown(
        self,
        *,
        entity_type: str,
        setting: str = "modern",
        source_code: str | None = None,
        limit: int | None = None,
        title: str | None = None,
    ) -> str:
        entities = load_entities(
            entity_type=entity_type,
            setting=setting,
            source_code=source_code,
        )
        if limit is not None and limit >= 0:
            entities = entities[:limit]

        blocks = [map_entity_markdown(entity_type, entity) for entity in entities]
        body = "\n\n---\n\n".join(block for block in blocks if block.strip())
        if title:
            return f"# {title}\n\n{body}".strip()
        return body

