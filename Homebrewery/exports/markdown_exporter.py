from __future__ import annotations

from pathlib import Path


def build_default_output_path(*, entity_type: str, setting: str) -> Path:
    return Path("Homebrewery/core/markdown") / f"{entity_type}_{setting}.txt"


def write_markdown(
    markdown: str,
    *,
    entity_type: str,
    setting: str,
    output_path: str | Path | None = None,
) -> Path:
    destination = (
        Path(output_path)
        if output_path is not None
        else build_default_output_path(entity_type=entity_type, setting=setting)
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(markdown, encoding="utf-8")
    return destination

