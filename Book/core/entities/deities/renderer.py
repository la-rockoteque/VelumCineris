from __future__ import annotations

import math
import re
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any
from urllib.parse import quote

from Book.core.entities.base import EntityMarkdownRenderer

_RAW_ART_ROOT = (
    "https://raw.githubusercontent.com/la-rockoteque/Vestigium/refs/heads/main/"
    "assets/art/Dieties"
)
_DEITY_ART_ALIASES = {
    "the justificator": "Justicator",
    "sarruinn": "Sarruin",
}


def _value(value: Any, default: Any = "") -> Any:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return default
    return value


def _normalized_name(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_name = "".join(
        character for character in normalized if not unicodedata.combining(character)
    )
    return re.sub(r"[^a-z0-9]", "", ascii_name.casefold())


@lru_cache(maxsize=1)
def _art_filenames() -> dict[str, str]:
    art_directory = Path(__file__).resolve().parents[4] / "assets" / "art" / "Dieties"
    return {
        _normalized_name(path.stem): path.stem
        for path in art_directory.glob("*")
        if path.is_file()
    }


def deity_image_url(name: str) -> str:
    alias = _DEITY_ART_ALIASES.get(name.casefold())
    candidates = [alias, name, re.sub(r"^The ", "", name, flags=re.IGNORECASE)]
    filenames = _art_filenames()
    stem = next(
        (
            filenames[_normalized_name(candidate)]
            for candidate in candidates
            if candidate and _normalized_name(candidate) in filenames
        ),
        name,
    )
    return f"{_RAW_ART_ROOT}/{quote(stem, safe='')}.png"


class DeityMarkdownRenderer(EntityMarkdownRenderer):
    template_name = "entities/deities/template.md.j2"

    def build_context(self, entity: dict[str, Any]) -> dict[str, Any]:
        properties = _value(entity.get("customProperties"), {})
        alt_names = _value(entity.get("altNames"), [])
        entries = _value(entity.get("entries"), [])
        epithet = _value(entity.get("epithet")) or ", ".join(alt_names)
        pantheon = _value(entity.get("pantheon"))
        domains = _value(entity.get("domains"), [])
        plane = _value(entity.get("plane")) or _value(properties.get("Plane"))
        alignment = _value(entity.get("alignment"))
        followers = _value(entity.get("followers")) or _value(properties.get("Followers"))
        symbol = _value(entity.get("symbol"))
        slogan = _value(entity.get("slogan")) or _value(properties.get("Slogan"))

        name = _value(entity.get("name"), "Unknown Deity")
        image_side = _value(entity.get("_image_side"), "right")
        return {
            "name": name,
            "image_url": deity_image_url(name),
            "image_mask": "imageMaskEdge3" if image_side == "right" else "imageMaskEdge5",
            "image_rotation": 270 if image_side == "right" else 90,
            "image_position": "right:-20%" if image_side == "right" else "left:-20%",
            "epithet": epithet,
            "metadata": [
                ("Alignment", alignment),
                ("Symbol", symbol),
                ("Pantheon", pantheon),
                ("Domains", ", ".join(domains) if isinstance(domains, list) else domains),
                ("Plane", plane),
                ("Followers", followers),
                ("Slogan", slogan),
            ],
            "description": _value(entity.get("description")),
            "entries": entries,
            "lore": _value(entity.get("lore")) or _value(properties.get("Lore")),
            "quote": _value(entity.get("quote")) or _value(properties.get("Quote")),
        }
