from __future__ import annotations

from collections.abc import Iterable


class HomebreweryRenderer:
    """Render book writer lines as Homebrewery source markdown."""

    def render(self, lines: Iterable[str]) -> str:
        rendered_lines: list[str] = []
        previous_empty = False

        for line in lines:
            rendered = self._render_line(line)

            if rendered == "":
                if previous_empty:
                    continue
                rendered_lines.append("")
                previous_empty = True
                continue

            rendered_lines.extend(rendered.splitlines())
            previous_empty = False

        while rendered_lines and rendered_lines[-1] == "":
            rendered_lines.pop()

        return "\n".join(rendered_lines) + "\n"

    def _render_line(self, line: str) -> str:
        if line == "---":
            return "\\page"
        if line.startswith("COVER_TAGLINE: "):
            return f"##### {line[15:]}"
        if line.startswith("COVER_TITLE: "):
            return f"# {line[13:]}"
        if line.startswith("COVER_SUBTITLE: "):
            return f"### {line[16:]}"
        if line.startswith("COVER_IMAGE: "):
            url = line[13:].strip()
            return (
                f"![cover image]({url})"
                "{position:absolute;left:0;top:0;width:100%;z-index:-1}"
            )
        if self._is_ornamental_rule(line):
            return "___"
        return line

    def _is_ornamental_rule(self, line: str) -> bool:
        stripped = line.strip()
        return bool(stripped) and set(stripped) == {"─"}
