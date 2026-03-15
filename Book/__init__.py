"""
Book Generator Module

Generates D&D sourcebooks in Google Docs with PHB-style formatting.
Consolidates homebrew content from Google Sheets into professional-looking books.
"""

from Book.book_api import BookAPI
from Book.services import BookGenerationService

__all__ = ["BookAPI", "GoogleDocsClient", "BookGenerationService"]


def __getattr__(name: str):
    if name == "GoogleDocsClient":
        from Book.google_docs_client import GoogleDocsClient

        return GoogleDocsClient
    raise AttributeError(name)
