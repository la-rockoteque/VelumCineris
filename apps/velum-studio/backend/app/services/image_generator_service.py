from __future__ import annotations

import os
from typing import Any


class ImageGeneratorService:
    def generate(
        self,
        *,
        entity_name: str,
        entity_type: str,
        style: str,
        description: str,
        provider: str = "chatgpt",
        dry_run: bool = True,
    ) -> dict[str, Any]:
        if not entity_name.strip():
            raise ValueError("entity_name cannot be empty")

        prompt = self._build_prompt(
            entity_name=entity_name.strip(),
            entity_type=entity_type.strip() or "entity",
            style=style.strip() or "cinematic concept art",
            description=description.strip(),
        )

        normalized_provider = provider.strip().lower() or "chatgpt"
        if normalized_provider == "chatgpt":
            api_key = os.getenv("OPENAI_API_KEY")
            status = "ready" if api_key else "disabled"
            reason = None if api_key else "Missing OPENAI_API_KEY"
        else:
            status = "planned"
            reason = f"Provider '{provider}' is not wired yet"

        return {
            "provider": normalized_provider,
            "status": status,
            "reason": reason,
            "dry_run": dry_run,
            "prompt": prompt,
            "output_path": f"out/images/{_slug(entity_name)}.png",
            "image_url": None,
        }

    def _build_prompt(self, *, entity_name: str, entity_type: str, style: str, description: str) -> str:
        core = [
            f"Dungeons & Dragons 5e {entity_type} illustration of {entity_name}.",
            f"Style: {style}.",
            "High detail, atmospheric lighting, publication-quality fantasy art.",
        ]
        if description:
            core.append(f"Description cues: {description}")
        return " ".join(core)


def _slug(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")
