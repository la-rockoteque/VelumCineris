"""
Parser for Homebrewery markdown files — strips layout markup and extracts sections.
"""

from pathlib import Path
from typing import List, Tuple

_ORNAMENTAL_RULE = "─" * 30


def load_cosmology_sections(path: Path | str) -> List[Tuple[str, List[str]]]:
    """
    Parse a Homebrewery .txt file and return (section_title, content_lines) pairs.

    Strips: metadata/CSS code blocks, \\page markers, {{...}} template blocks,
    image lines, and the top-level # title. Converts ### to #### + ornamental rule.
    Only content after the first # heading is considered.
    """
    raw_lines = Path(path).read_text(encoding="utf-8").splitlines()

    sections: List[Tuple[str, List[str]]] = []
    current_title: str | None = None
    current_lines: List[str] = []
    in_code_block = False
    in_brace_block = False
    content_started = False

    for line in raw_lines:
        stripped = line.strip()

        # Toggle fenced code blocks (metadata, CSS)
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Wait for the real H1 title to mark content start
        if not content_started:
            if stripped.startswith("# ") and not stripped.startswith("## "):
                content_started = True
            continue

        # Strip \page markers
        if stripped == "\\page":
            continue

        # Strip {{ ... }} template blocks (possibly multi-line)
        if stripped.startswith("{{"):
            if "}}" in stripped:
                continue
            in_brace_block = True
            continue
        if in_brace_block:
            if "}}" in stripped:
                in_brace_block = False
            continue

        # Strip Homebrewery inline image lines
        if stripped.startswith("!["):
            continue

        # New ## section boundary
        if stripped.startswith("## ") and not stripped.startswith("### "):
            if current_title is not None:
                sections.append((current_title, _trim_blank_edges(current_lines)))
            current_title = stripped[3:].strip()
            current_lines = []
            continue

        if current_title is None:
            continue

        # Convert ### subsection → #### + ornamental rule
        if stripped.startswith("### "):
            current_lines.append("#### " + stripped[4:].strip())
            current_lines.append(_ORNAMENTAL_RULE)
            continue

        current_lines.append(line.rstrip())

    if current_title is not None:
        sections.append((current_title, _trim_blank_edges(current_lines)))

    return sections


def _trim_blank_edges(lines: List[str]) -> List[str]:
    result = list(lines)
    while result and result[0] == "":
        result.pop(0)
    while result and result[-1] == "":
        result.pop()
    return result