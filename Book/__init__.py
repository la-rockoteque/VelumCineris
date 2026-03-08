"""
Book Generator Module

Generates D&D sourcebooks in Google Docs with PHB-style formatting.
Consolidates homebrew content from Google Sheets into professional-looking books.
"""

from Book.core.Helpers.book_api import BookAPI
from Book.core.Helpers.google_docs_client import GoogleDocsClient

__all__ = ["BookAPI", "GoogleDocsClient"]
