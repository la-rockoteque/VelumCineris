"""
Read structured sections from a Google Doc via the Docs API.
"""

from typing import Any, Dict, List, Tuple

_ORNAMENTAL_RULE = "─" * 30


def read_doc_sections(service, doc_id: str) -> List[Tuple[str, List[str]]]:
    """
    Fetch a Google Doc and return (section_title, content_lines) pairs.

    HEADING_1  → document title, skipped
    HEADING_2  → new section boundary
    HEADING_3  → converted to #### + ornamental rule
    HEADING_4  → converted to ####
    NORMAL_TEXT → body lines (bold/italic runs wrapped in ** / *)
    """
    doc = service.documents().get(documentId=doc_id).execute()
    body_content = doc.get("body", {}).get("content", [])

    sections: List[Tuple[str, List[str]]] = []
    current_title: str | None = None
    current_lines: List[str] = []

    for element in body_content:
        paragraph = element.get("paragraph")
        if not paragraph:
            continue

        style = paragraph.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
        text = _plain_text(paragraph)

        if not text.strip():
            if current_title is not None:
                current_lines.append("")
            continue

        if style == "HEADING_1":
            continue

        if style == "HEADING_2":
            if current_title is not None:
                sections.append((current_title, _trim_edges(current_lines)))
            current_title = text.strip()
            current_lines = []
            continue

        if current_title is None:
            continue

        if style == "HEADING_3":
            current_lines.append("#### " + text.strip())
            current_lines.append(_ORNAMENTAL_RULE)
            continue

        if style == "HEADING_4":
            current_lines.append("#### " + text.strip())
            continue

        current_lines.append(_inline_formatted(paragraph))

    if current_title is not None:
        sections.append((current_title, _trim_edges(current_lines)))

    return sections


def _plain_text(paragraph: Dict[str, Any]) -> str:
    parts = []
    for elem in paragraph.get("elements", []):
        text_run = elem.get("textRun")
        if text_run:
            parts.append(text_run.get("content", ""))
    return "".join(parts).rstrip("\n")


def _inline_formatted(paragraph: Dict[str, Any]) -> str:
    parts = []
    for elem in paragraph.get("elements", []):
        text_run = elem.get("textRun")
        if not text_run:
            continue
        content = text_run.get("content", "").rstrip("\n")
        if not content:
            continue
        ts = text_run.get("textStyle", {})
        bold = ts.get("bold", False)
        italic = ts.get("italic", False)
        if bold and content.strip():
            content = f"**{content}**"
        elif italic and content.strip():
            content = f"*{content}*"
        parts.append(content)
    return "".join(parts)


def _trim_edges(lines: List[str]) -> List[str]:
    result = list(lines)
    while result and result[0] == "":
        result.pop(0)
    while result and result[-1] == "":
        result.pop()
    return result