"""
Generic converter base class for transforming Google Sheets data to Pydantic models.

Provides type-safe conversion pattern using Python generics.
"""

from typing import TypeVar, Generic, List, Type
import pandas as pd
from models.base import BaseEntity

# Generic type variable bound to BaseEntity
T = TypeVar('T', bound=BaseEntity)


class BaseConverter(Generic[T]):
    """
    Generic converter for transforming DataFrame rows to entity models.

    Type-safe converter pattern that ensures consistency across all entity types.

    Attributes:
        entity_class: The Pydantic model class to convert to
        sheet_gid: Google Sheets GID for this entity type
        name_column: Column name containing entity name (default: "Name")

    Example:
        >>> class SpellConverter(BaseConverter[Spell]):
        ...     entity_class = Spell
        ...     sheet_gid = "625265890"
        ...     name_column = "Spell Name"
        ...
        ...     def convert_row(self, row: pd.Series, **kwargs) -> Spell:
        ...         return Spell.from_row(row, **kwargs)
        >>>
        >>> converter = SpellConverter(fantasy_sheets)
        >>> spells = converter.convert_all(source_filter="ORIO")
    """

    # Subclasses must define these
    entity_class: Type[T]
    sheet_gid: str
    name_column: str = "Name"  # Can be overridden by subclasses

    def __init__(self, sheets_client):
        """
        Initialize converter with Google Sheets client.

        Args:
            sheets_client: Google Sheets client (fantasy_sheets or modern_sheets)
        """
        self.sheets_client = sheets_client

    def load_sheet(self) -> pd.DataFrame:
        """
        Load DataFrame from Google Sheets.

        Returns:
            DataFrame with entity data

        Raises:
            Exception: If sheet loading fails
        """
        return self.sheets_client.get_sheet(self.sheet_gid)

    def convert_row(self, row: pd.Series, **kwargs) -> T:
        """
        Convert single DataFrame row to entity model.

        Default implementation calls entity_class.from_row().
        Subclasses can override for custom logic.

        Args:
            row: DataFrame row with entity data
            **kwargs: Additional context passed to from_row()

        Returns:
            Entity instance

        Raises:
            Exception: If conversion fails
        """
        return self.entity_class.from_row(row, **kwargs)

    def convert_all(self, source_filter: str = None, **kwargs) -> List[T]:
        """
        Convert all rows to entity models.

        Args:
            source_filter: Optional source identifier to filter by (e.g., "ORIO")
            **kwargs: Additional context passed to convert_row()

        Returns:
            List of entity instances

        Example:
            >>> converter.convert_all(source_filter="ORIO", source="ORIO", json_source="ORIO")
        """
        df = self.load_sheet()
        entities = []

        for _, row in df.iterrows():
            # Skip empty rows (use configured name column)
            name_value = row.get(self.name_column)
            if pd.isnull(name_value) or str(name_value).strip() == "":
                continue

            # Apply source filter if provided
            if source_filter and row.get("Source") != source_filter:
                continue

            try:
                entity = self.convert_row(row, **kwargs)
                entities.append(entity)
            except Exception as e:
                # Log error but continue processing
                print(f"Error converting row '{name_value}': {e}")
                continue

        return entities

    def to_list_dict(self, entities: List[T]) -> List[dict]:
        """
        Convert entity list to list of dictionaries for JSON export.

        Args:
            entities: List of entity instances

        Returns:
            List of dictionaries in 5etools format
        """
        return [entity.to_dict() for entity in entities]
