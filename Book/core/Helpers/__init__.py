"""Book helper modules used by notebooks and scripts."""

from Book.core.Helpers.book_api import BookAPI

__all__ = [
    "BookAPI",
    "GoogleDocsClient",
]


def __getattr__(name: str):
    if name == "GoogleDocsClient":
        from Book.core.Helpers.google_docs_client import GoogleDocsClient

        return GoogleDocsClient
    raise AttributeError(name)
