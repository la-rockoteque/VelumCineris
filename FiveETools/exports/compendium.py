from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

import inflection

SCHEMA_URL = "https://raw.githubusercontent.com/TheGiddyLimit/5etools-utils/master/schema/brew-fast/homebrew.json"
DATE_ADDED = 1743879729
CURRENCY_CONVERSIONS = {
    "credit": [
        {
            "coin": "credit",
            "mult": 0.001,
            "isFallback": True,
        }
    ]
}


def _generate_date_last_modified_hash(document: dict[str, Any]) -> str:
    payload = dict(document)
    meta = dict(payload.get("_meta", {}))
    meta.pop("_dateLastModifiedHash", None)
    payload["_meta"] = meta
    json_str = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        default=lambda value: list(value) if isinstance(value, set) else value,
    )
    return hashlib.md5(json_str.encode("utf-8")).hexdigest()


def build_compendium_document(
    *,
    sources: list[dict[str, Any]],
    sections: dict[str, list[dict[str, Any]]],
    timestamp: int | None = None,
) -> dict[str, Any]:
    now = int(timestamp if timestamp is not None else time.time())
    document: dict[str, Any] = {
        "_meta": {
            "sources": sources,
            "unlisted": True,
            "dateAdded": DATE_ADDED,
            "dateLastModified": now,
            "_dateLastModifiedHash": "",
            "edition": "classic",
            "currencyConversions": CURRENCY_CONVERSIONS,
        },
        "$schema": SCHEMA_URL,
        **sections,
    }
    document["_meta"]["_dateLastModifiedHash"] = _generate_date_last_modified_hash(document)
    return document


def build_default_output_filename(json_source: str) -> str:
    slug = inflection.underscore(str(json_source).strip() or "output")
    return f"Velum_Cineris;{slug}.json"


def write_compendium_document(document: dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path
