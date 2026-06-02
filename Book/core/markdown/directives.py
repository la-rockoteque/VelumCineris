PAGE_BREAK_MARKER = "<!-- PAGE_BREAK -->"


def page_break() -> str:
    """Stable markdown marker consumed by Google Docs and Homebrewery renderers."""
    return PAGE_BREAK_MARKER
