"""
Base entity classes for VelumCineris D&D 5e content models.

Provides BaseEntity with dict-like access for backward compatibility.
"""

from collections.abc import Mapping
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DictAccessMixin:
    """Provides .get() access for backward compatibility with dict-based code."""

    def get(self, key: str, default=None):
        """Get attribute by name, returning default if not found (dict-like interface)."""
        return getattr(self, key, default)

    def __getitem__(self, key: str):
        """Get attribute by key (dict-like interface)."""
        return getattr(self, key)

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary suitable for JSON export."""
        return self.model_dump(exclude_none=True, by_alias=True, mode='json')


class BaseEntity(BaseModel, DictAccessMixin):
    """
    Base class for all D&D 5e entity models.

    Provides common fields and utilities for all content types.
    Supports both Pydantic attribute access and dict-like .get() access.
    """

    model_config = ConfigDict(
        extra='allow',  # Allow additional fields not in schema
        validate_assignment=True,  # Validate on attribute assignment
        populate_by_name=True,  # Allow both field name and alias
        strict=False,  # Allow type coercion (str to int, etc.)
    )

    # Core fields present in all 5etools entities
    name: str = Field(..., description="Entity name")
    source: str = Field(..., description="Source identifier (e.g., 'ORIO', 'VSTGCC')")
    page: Optional[int] = Field(None, description="Source page number")
    entries: Optional[List[Any]] = Field(default_factory=list, description="Description entries")
    fluff: Optional[Dict[str, Any]] = Field(None, description="Flavor text and lore")

    @classmethod
    def from_row(cls, row: Mapping[str, Any] | Any, **kwargs):
        """
        Create entity from a tabular row mapping.

        Must be implemented by subclasses with entity-specific logic.

        Args:
            row: Row-like mapping with entity data
            **kwargs: Additional context (source, json_source, etc.)

        Returns:
            Entity instance

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement from_row()")

    def to_5etools(self) -> Dict[str, Any]:
        """
        Export entity in 5etools JSON format.

        By default, returns dict representation. Subclasses can override
        for custom transformations.

        Returns:
            Dictionary in 5etools format
        """
        return self.to_dict()
