from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from markdown_it import MarkdownIt

from Book.core.markdown.directives import PAGE_BREAK_MARKER
from Book.core.markdown.helpers import normalize_markdown


@dataclass(frozen=True)
class InlineStyle:
    start: int
    end: int
    bold: bool = False
    italic: bool = False
    code: bool = False


@dataclass(frozen=True)
class Block:
    kind: str
    text: str = ""
    level: int | None = None
    rows: tuple[tuple[str, ...], ...] = ()
    src: str | None = None
    alt: str = ""
    inline_styles: tuple[InlineStyle, ...] = ()


class GoogleDocsMarkdownRenderer:
    """Render canonical book markdown into Google Docs batch-update requests."""

    def __init__(self, gdocs: Any) -> None:
        self.gdocs = gdocs
        self._markdown = MarkdownIt("commonmark").enable("table")

    def build_requests(self, markdown: str, *, index: int = 1) -> tuple[list[dict[str, Any]], int]:
        requests: list[dict[str, Any]] = []
        current_layout: str | None = None
        pending_layout: str | None = None

        for block in self._parse_blocks(markdown):
            if block.kind == "blank":
                line_start = index
                requests.append({"insertText": {"location": {"index": index}, "text": "\n"}})
                index += 1
                if pending_layout is not None:
                    requests.append(
                        self.gdocs.create_section_style_request(
                            start_index=line_start,
                            end_index=index,
                            columns=1 if pending_layout == "one_column" else 2,
                        )
                    )
                    current_layout = pending_layout
                    pending_layout = None
                continue

            if block.kind == "page_break":
                requests.append({"insertPageBreak": {"location": {"index": index}}})
                index += 1
                continue

            if block.kind == "heading" and block.level in {1, 2, 3}:
                if index > 1:
                    requests.append(
                        {
                            "insertSectionBreak": {
                                "sectionType": "CONTINUOUS",
                                "location": {"index": index},
                            }
                        }
                    )
                    index += 2

                line_start = index
                text = block.text + "\n"
                requests.append({"insertText": {"location": {"index": index}, "text": text}})
                index += len(text)
                requests.extend(
                    self.gdocs.create_heading_style_requests(
                        start_index=line_start,
                        end_index=index,
                        level=block.level or 2,
                    )
                )
                requests.append(
                    self.gdocs.create_section_style_request(
                        start_index=line_start,
                        end_index=index,
                        columns=1,
                    )
                )
                requests.append(
                    {
                        "insertSectionBreak": {
                            "sectionType": "CONTINUOUS",
                            "location": {"index": index},
                        }
                    }
                )
                index += 2
                current_layout = None
                pending_layout = "two_column"
                continue

            desired_layout = pending_layout or self._layout_for_block(block)
            layout_switched = desired_layout is not None and desired_layout != current_layout
            if layout_switched and current_layout is not None:
                requests.append(
                    {
                        "insertSectionBreak": {
                            "sectionType": "CONTINUOUS",
                            "location": {"index": index},
                        }
                    }
                )
                index += 2

            line_start = index
            if block.kind == "heading":
                text = block.text + "\n"
                requests.append({"insertText": {"location": {"index": index}, "text": text}})
                index += len(text)
                requests.extend(
                    self.gdocs.create_heading_style_requests(
                        start_index=line_start,
                        end_index=index,
                        level=block.level or 4,
                    )
                )
            elif block.kind == "cover_tagline":
                index = self._insert_styled_cover_line(
                    requests, index, block.text, self.gdocs.create_cover_tagline_style_requests
                )
            elif block.kind == "cover_title":
                index = self._insert_styled_cover_line(
                    requests, index, block.text, self.gdocs.create_cover_title_style_requests
                )
            elif block.kind == "cover_subtitle":
                index = self._insert_styled_cover_line(
                    requests, index, block.text, self.gdocs.create_cover_subtitle_style_requests
                )
            elif block.kind == "image":
                index = self._insert_image(requests, index, line_start, block)
            elif block.kind == "rule":
                text = block.text + "\n"
                requests.append({"insertText": {"location": {"index": index}, "text": text}})
                index += len(text)
                requests.extend(self.gdocs.create_rule_style_requests(start_index=line_start, end_index=index))
            elif block.kind == "table":
                text = self._table_to_text(block) + "\n"
                requests.append({"insertText": {"location": {"index": index}, "text": text}})
                index += len(text)
                requests.extend(self.gdocs.create_body_style_requests(start_index=line_start, end_index=index))
            else:
                text = block.text + "\n"
                requests.append({"insertText": {"location": {"index": index}, "text": text}})
                index += len(text)
                requests.extend(self.gdocs.create_body_style_requests(start_index=line_start, end_index=index))
                for style in block.inline_styles:
                    requests.append(
                        self.gdocs.create_inline_text_style_request(
                            start_index=line_start + style.start,
                            end_index=line_start + style.end,
                            bold=style.bold or style.code,
                            italic=style.italic,
                        )
                    )

            if layout_switched:
                requests.append(
                    self.gdocs.create_section_style_request(
                        start_index=line_start,
                        end_index=index,
                        columns=1 if desired_layout == "one_column" else 2,
                    )
                )
            if desired_layout is not None:
                current_layout = desired_layout
                if pending_layout == desired_layout:
                    pending_layout = None

        return requests, index

    def _parse_blocks(self, markdown: str) -> list[Block]:
        blocks: list[Block] = []
        lines = normalize_markdown(markdown).splitlines()
        index = 0
        while index < len(lines):
            line = lines[index]
            if line == "":
                blocks.append(Block("blank"))
                index += 1
                continue
            if line == PAGE_BREAK_MARKER or line == "---":
                blocks.append(Block("page_break"))
                index += 1
                continue
            if line.startswith("COVER_TAGLINE: "):
                blocks.append(Block("cover_tagline", text=line[15:]))
                index += 1
                continue
            if line.startswith("COVER_TITLE: "):
                blocks.append(Block("cover_title", text=line[13:]))
                index += 1
                continue
            if line.startswith("COVER_SUBTITLE: "):
                blocks.append(Block("cover_subtitle", text=line[16:]))
                index += 1
                continue
            if line.startswith("COVER_IMAGE: "):
                blocks.append(Block("image", src=line[13:].strip(), alt="cover image"))
                index += 1
                continue
            if match := re.match(r"^(#{1,4})\s+(.+)$", line):
                blocks.append(Block("heading", text=match.group(2), level=len(match.group(1))))
                index += 1
                continue
            if self._is_rule(line):
                blocks.append(Block("rule", text=line))
                index += 1
                continue
            if line.startswith("| "):
                table_lines: list[str] = []
                while index < len(lines) and lines[index].startswith("| "):
                    table_lines.append(lines[index])
                    index += 1
                blocks.append(self._parse_table(table_lines))
                continue
            if image := re.match(r"^!\[([^]]*)]\(([^)]+)\)", line):
                blocks.append(Block("image", src=image.group(2), alt=image.group(1)))
                index += 1
                continue

            paragraph_lines = [line]
            index += 1
            while index < len(lines) and lines[index] and not self._starts_new_block(lines[index]):
                paragraph_lines.append(lines[index])
                index += 1
            blocks.append(self._parse_text_block("\n".join(paragraph_lines)))

        return blocks

    def _starts_new_block(self, line: str) -> bool:
        return (
            line == PAGE_BREAK_MARKER
            or line == "---"
            or line.startswith(("COVER_", "#", "| ", "!["))
            or self._is_rule(line)
        )

    def _parse_text_block(self, text: str) -> Block:
        plain = ""
        styles: list[InlineStyle] = []
        tokens = self._markdown.parseInline(text, {})[0].children or []
        stack: list[tuple[str, int]] = []
        for token in tokens:
            if token.type == "text":
                plain += token.content
            elif token.type == "code_inline":
                start = len(plain)
                plain += token.content
                styles.append(InlineStyle(start, len(plain), code=True))
            elif token.type in {"strong_open", "em_open"}:
                stack.append((token.type, len(plain)))
            elif token.type in {"strong_close", "em_close"}:
                open_type = "strong_open" if token.type == "strong_close" else "em_open"
                for stack_index in range(len(stack) - 1, -1, -1):
                    if stack[stack_index][0] == open_type:
                        _, start = stack.pop(stack_index)
                        styles.append(
                            InlineStyle(
                                start,
                                len(plain),
                                bold=open_type == "strong_open",
                                italic=open_type == "em_open",
                            )
                        )
                        break
            elif token.type == "softbreak":
                plain += "\n"
        return Block("paragraph", text=plain, inline_styles=tuple(styles))

    def _parse_table(self, lines: list[str]) -> Block:
        rows = []
        for line in lines:
            cells = tuple(cell.strip() for cell in line.strip("|").split("|"))
            if cells and all(set(cell) <= {"-", ":"} for cell in cells):
                continue
            rows.append(cells)
        return Block("table", rows=tuple(rows))

    def _table_to_text(self, block: Block) -> str:
        return "\n".join(" | ".join(row) for row in block.rows)

    def _layout_for_block(self, block: Block) -> str | None:
        if block.kind in {"cover_tagline", "cover_title", "cover_subtitle", "image"}:
            return "one_column"
        if block.kind == "page_break":
            return None
        return "two_column"

    def _insert_styled_cover_line(self, requests: list[dict[str, Any]], index: int, text: str, style_factory: Any) -> int:
        start = index
        insert_text = text + "\n"
        requests.append({"insertText": {"location": {"index": index}, "text": insert_text}})
        index += len(insert_text)
        requests.extend(style_factory(start_index=start, end_index=index))
        return index

    def _insert_image(self, requests: list[dict[str, Any]], index: int, line_start: int, block: Block) -> int:
        from Book.core.Helpers.styles import COVER_IMAGE_HEIGHT_PT, COVER_IMAGE_WIDTH_PT

        requests.append(
            {
                "insertInlineImage": {
                    "uri": block.src or "",
                    "location": {"index": index},
                    "objectSize": {
                        "height": {"magnitude": COVER_IMAGE_HEIGHT_PT, "unit": "PT"},
                        "width": {"magnitude": COVER_IMAGE_WIDTH_PT, "unit": "PT"},
                    },
                }
            }
        )
        index += 1
        requests.append({"insertText": {"location": {"index": index}, "text": "\n"}})
        index += 1
        requests.append(
            self.gdocs.create_paragraph_style_request(
                start_index=line_start,
                end_index=index,
                paragraph_style={
                    "alignment": "CENTER",
                    "spaceAbove": {"magnitude": 8, "unit": "PT"},
                    "spaceBelow": {"magnitude": 8, "unit": "PT"},
                },
                fields=["alignment", "spaceAbove", "spaceBelow"],
            )
        )
        return index

    def _is_rule(self, line: str) -> bool:
        stripped = line.strip()
        return bool(stripped) and set(stripped) == {"─"}
