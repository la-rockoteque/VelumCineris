"""Divine Codex writer containing deities and reference appendices."""

from __future__ import annotations

import math
import re
import unicodedata
from collections import defaultdict
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any

from Book.core.markdown import normalize_markdown
from Book.core.writers.base import BaseWriter

Section = tuple[str, str, Callable | None]
PAGE_BREAK = "\\page"
PAGE_HEIGHT_ESTIMATE = 1320


def _clean_value(value: Any, default: str = "") -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return default
    return str(value).strip() or default


def _alphabetical_key(value: Any) -> str:
    normalized = unicodedata.normalize("NFKD", _clean_value(value))
    return "".join(character for character in normalized if not unicodedata.combining(character)).casefold()


class DivineCodexWriter(BaseWriter):
    """Writer for the alphabetized Divine Codex and its reference appendices."""

    def get_book_title(self) -> str:
        return "Orimond Divine Codex" if self.source == "fantasy" else "Vestigium Divine Codex"

    def get_sections(self) -> list[Section]:
        return [("Deities", "deity", None)]

    def build_markdown(self) -> str:
        deities = sorted(
            self.book_api.load_entities("deity", source=self.source),
            key=lambda deity: _alphabetical_key(deity.get("name")),
        )
        parts = [
            self._opening_pages(),
            self._render_deities(deities),
            self._render_flat_appendix(
                "D",
                "Deities by domain",
                self._group_by_domains(deities),
            ),
            self._render_alignment_appendix(deities),
            self._render_flat_appendix(
                "F",
                "Deities by pantheon",
                self._group_by_value(deities, "pantheon"),
                include_page_break=False,
            ),
        ]
        return normalize_markdown("\n".join(parts))

    def _opening_pages(self) -> str:
        legacy_path = (
            Path(__file__).resolve().parents[3]
            / "Homebrewery"
            / "core"
            / "markdown"
            / "Divine Codex 2.0.txt"
        )
        legacy = legacy_path.read_text(encoding="utf-8")
        opening_start = legacy.index("{{frontCover}}")
        opening_end = legacy.index("\n# Church of Omnis")
        return normalize_markdown(legacy[opening_start:opening_end])

    def _render_deities(self, deities: Iterable[dict[str, Any]]) -> str:
        renderer = self.get_entity_renderer("deity")
        parts = ["# Deities", ""]
        used_height = 50
        success_count = 0
        error_count = 0
        deity_list = list(deities)

        for index, deity in enumerate(deity_list):
            try:
                if index > 0:
                    parts.extend([PAGE_BREAK, ""])
                    used_height = 0
                if index % 2 == 0:
                    parts.extend(["\\column", ""])
                renderable_deity = {
                    **deity,
                    "_image_side": "left" if index % 2 == 0 else "right",
                }
                rendered = renderer.render_markdown(renderable_deity)
                paginated, used_height = self._paginate_markdown(rendered, used_height)
                parts.append(paginated)
                success_count += 1
                if (index + 1) % 50 == 0:
                    print(f"  Formatted {index + 1}/{len(deity_list)} entities...")
            except Exception as error:
                error_count += 1
                print(f"  Warning: Error formatting {deity.get('name', 'unknown')}: {error}")

        parts.extend(["", PAGE_BREAK, ""])
        print(f"  Added {success_count} entities ({error_count} errors)")
        return normalize_markdown("\n".join(parts))

    def _paginate_markdown(self, markdown: str, used_height: int) -> tuple[str, int]:
        parts: list[str] = []
        blocks = re.split(r"\n\s*\n", markdown.strip())
        for index, block in enumerate(blocks):
            if block.strip() == PAGE_BREAK:
                continue
            block_height = self._estimate_block_height(block)
            opening_height = block_height
            if block.startswith("## ") and index + 1 < len(blocks):
                next_block = blocks[index + 1]
                if next_block.startswith("{{imageMaskEdge"):
                    opening_height += self._estimate_block_height(next_block)
            if used_height and used_height + opening_height > PAGE_HEIGHT_ESTIMATE:
                parts.extend([PAGE_BREAK, ""])
                used_height = 0
            parts.extend([block, ""])
            used_height += block_height
        return normalize_markdown("\n".join(parts)), used_height

    def _estimate_block_height(self, block: str) -> int:
        lines = block.splitlines()
        if block.startswith("{{imageMaskEdge"):
            return 0
        if all(line.startswith("|") for line in lines):
            return 24 + (len(lines) * 18)
        if block.startswith("{{quote"):
            return 45 + self._wrapped_line_count(block, 48) * 13
        if block.startswith("#"):
            return sum(34 if line.startswith("## ") else 22 for line in lines)
        return 12 + self._wrapped_line_count(block, 48) * 13

    def _wrapped_line_count(self, block: str, width: int) -> int:
        return sum(max(1, math.ceil(len(line) / width)) for line in block.splitlines())

    def _group_by_domains(self, deities: Iterable[dict[str, Any]]) -> dict[str, list[str]]:
        groups: defaultdict[str, list[str]] = defaultdict(list)
        for deity in deities:
            name = _clean_value(deity.get("name"), "Unknown Deity")
            raw_domains = deity.get("domains") or []
            domains = raw_domains if isinstance(raw_domains, list) else [raw_domains]
            normalized_domains = [
                domain.strip()
                for value in domains
                for domain in re.split(r"[;,]", _clean_value(value))
                if domain.strip()
            ]
            for domain in normalized_domains or ["Unspecified"]:
                groups[domain].append(name)
        return dict(groups)

    def _group_by_value(
        self,
        deities: Iterable[dict[str, Any]],
        key: str,
    ) -> dict[str, list[str]]:
        groups: defaultdict[str, list[str]] = defaultdict(list)
        for deity in deities:
            group = _clean_value(deity.get(key), "Unspecified")
            groups[group].append(_clean_value(deity.get("name"), "Unknown Deity"))
        return dict(groups)

    def _render_flat_appendix(
        self,
        letter: str,
        title: str,
        groups: dict[str, list[str]],
        *,
        include_page_break: bool = True,
    ) -> str:
        lines = [
            f"# APPENDIX {letter}",
            f"## {title}",
            "",
            "<div class='wide' style='column-count:3'>",
            "",
        ]
        for group in sorted(groups, key=_alphabetical_key):
            lines.extend([f"### {group}", ""])
            lines.extend(f"- {name}" for name in sorted(groups[group], key=_alphabetical_key))
            lines.append("")
        lines.extend(["</div>", "", "{{pageNumber,auto}}"])
        if include_page_break:
            lines.extend([PAGE_BREAK, ""])
        return normalize_markdown("\n".join(lines))

    def _render_alignment_appendix(self, deities: Iterable[dict[str, Any]]) -> str:
        groups: defaultdict[str, defaultdict[str, list[str]]] = defaultdict(
            lambda: defaultdict(list)
        )
        for deity in deities:
            moral, ethical = self._alignment_parts(deity.get("alignment"))
            groups[moral][ethical].append(_clean_value(deity.get("name"), "Unknown Deity"))

        lines = [
            "# APPENDIX E",
            "## Deities by alignment",
            "",
            "<div class='wide' style='column-count:3'>",
            "",
        ]
        moral_order = ("Lawful", "Neutral", "Chaotic", "Unspecified")
        ethical_order = ("Good", "Neutral", "Evil", "Unspecified")
        included_morals = [moral for moral in moral_order if moral in groups]
        for moral_index, moral in enumerate(included_morals):
            lines.extend([f"### {moral}", ""])
            for ethical in ethical_order:
                if ethical not in groups[moral]:
                    continue
                lines.extend([f"#### {ethical}", ""])
                lines.extend(
                    f"- {name}"
                    for name in sorted(groups[moral][ethical], key=_alphabetical_key)
                )
                lines.append("")
            if moral_index < len(included_morals) - 1:
                lines.extend(["\\column", ""])
        lines.extend(["</div>", "", "{{pageNumber,auto}}", PAGE_BREAK, ""])
        return normalize_markdown("\n".join(lines))

    def _alignment_parts(self, value: Any) -> tuple[str, str]:
        alignment = _clean_value(value)
        if not alignment:
            return "Unspecified", "Unspecified"

        words = re.findall(r"[A-Za-z]+", alignment.casefold())
        moral = next(
            (label for label in ("Lawful", "Neutral", "Chaotic") if label.casefold() in words),
            "Unspecified",
        )
        ethical = next(
            (label for label in ("Good", "Evil") if label.casefold() in words),
            "Neutral" if moral != "Unspecified" else "Unspecified",
        )
        return moral, ethical
