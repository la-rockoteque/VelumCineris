"""Spreadsheet package."""

__all__ = ["SpreadsheetService"]


def __getattr__(name: str):
    if name == "SpreadsheetService":
        from Spreadsheet.services import SpreadsheetService

        return SpreadsheetService
    raise AttributeError(f"module 'Spreadsheet' has no attribute {name!r}")
