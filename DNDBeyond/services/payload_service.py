from __future__ import annotations

from typing import Any

from DNDBeyond.datasets import load_entities
from DNDBeyond.mappers import map_entity_payload, map_spell_extras


class DnDBeyondPayloadService:
    def build_payloads(
        self,
        *,
        entity_type: str,
        setting: str,
        source_code: str | None = None,
        limit: int | None = None,
        include_spell_extras: bool = False,
    ) -> list[dict[str, Any]]:
        entities = load_entities(
            entity_type=entity_type,
            setting=setting,
            source_code=source_code,
        )
        if limit is not None and limit >= 0:
            entities = entities[:limit]

        payloads: list[dict[str, Any]] = []
        for entity in entities:
            payload = map_entity_payload(entity_type, entity)
            if include_spell_extras and str(entity_type).strip().lower() == "spell":
                payload["extras"] = map_spell_extras(entity)
            payloads.append(payload)

        return payloads

