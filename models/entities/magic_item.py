"""
Magic Item entity model for D&D 5e.

Provides type-safe validation for magic item data from Google Sheets.
"""

from pydantic import Field
from typing import Optional, List
from ..base import BaseEntity
from ..row_access import is_missing, optional_text, row_value, split_csv


class MagicItem(BaseEntity):
    """
    D&D 5e Magic Item model.

    Represents a magical item in 5etools JSON format.
    """

    type: str = Field(..., description="Item type abbreviation")
    rarity: str = Field(..., description="Item rarity (common, uncommon, rare, etc.)")
    wondrous: bool = Field(default=True, description="Is a wondrous item")
    value: Optional[str] = Field(None, description="Item value/cost")
    weight: Optional[str] = Field(None, description="Item weight")

    # Optional weapon/armor fields
    properties: Optional[List[str]] = Field(None, description="Item properties")
    weaponCategory: Optional[str] = Field(None, description="Weapon category")
    dmg1: Optional[str] = Field(None, description="Primary damage")
    dmg2: Optional[str] = Field(None, description="Secondary damage")
    dmgType: Optional[str] = Field(None, description="Damage type")
    range: Optional[str] = Field(None, description="Weapon range")

    # Magic item specific fields
    recharge: Optional[str] = Field(None, description="Recharge condition")
    reqAttunement: Optional[str] = Field(None, description="Requires attunement")
    attachedSpells: Optional[List[str]] = Field(None, description="Attached spells")
    baseItem: Optional[str] = Field(None, description="Base item")
    tier: Optional[str] = Field(None, description="Item tier")

    @classmethod
    def from_row(cls, row, source: str, json_source: str) -> 'MagicItem':
        """
        Create MagicItem from DataFrame row.

        Args:
            row: DataFrame row from Google Sheets
            source: Source filter (e.g., "ORIO")
            json_source: JSON source identifier

        Returns:
            Validated MagicItem instance
        """
        # Parse properties
        properties = None
        property_values = split_csv(row_value(row, "Property"))
        if property_values:
            # Add "VS" prefix as in original code
            properties = [f"VS{prop[2:]}" if len(prop) > 2 else prop for prop in property_values]

        # Parse attached spells
        attached_spells = None
        attached_spells = split_csv(row_value(row, "Attached Spells")) or None

        # Parse description
        entries = []
        description = optional_text(row_value(row, "Description"))
        if description:
            entries.append(description)

        # Get type safely
        item_type = row_value(row, "Type ABRV")
        if is_missing(item_type):
            item_type = "OTH"
        item_type = str(item_type)

        # Get rarity safely
        rarity = row_value(row, "Rarity", "common")
        if is_missing(rarity):
            rarity = "common"
        rarity = str(rarity).lower()

        return cls(
            source=json_source,
            name=optional_text(row_value(row, "Name")) or "Unnamed Magic Item",
            type=item_type,
            rarity=rarity,
            wondrous=True,
            value=optional_text(row_value(row, "Value")),
            weight=optional_text(row_value(row, "Weight")),
            page=0,
            entries=entries,
            # Weapon/armor fields
            properties=properties,
            weaponCategory=optional_text(row_value(row, "Category")),
            dmg1=optional_text(row_value(row, "Damage 1")),
            dmg2=optional_text(row_value(row, "Damage 2")),
            dmgType=optional_text(row_value(row, "Damage Type")),
            range=optional_text(row_value(row, "Extracted Range")),
            # Magic fields
            recharge=optional_text(row_value(row, "Recharge")),
            reqAttunement=optional_text(row_value(row, "Require Attunement")),
            attachedSpells=attached_spells,
            baseItem=optional_text(row_value(row, "Base Item")),
            tier=optional_text(row_value(row, "Tier")),
        )
