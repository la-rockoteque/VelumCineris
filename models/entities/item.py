"""
Item entity model for D&D 5e.

Provides type-safe validation for item data from Google Sheets.
"""

from pydantic import Field
from typing import Optional, List
from ..base import BaseEntity
from ..row_access import is_missing, optional_int, optional_text, row_value, split_csv


class Item(BaseEntity):
    """
    D&D 5e Item model.

    Represents a mundane or enhanced item in 5etools JSON format.
    """

    type: str = Field(..., description="Item type abbreviation")
    rarity: str = Field(default="none", description="Item rarity")
    value: Optional[str] = Field(None, description="Item value/cost")
    weight: Optional[str] = Field(None, description="Item weight")

    # Optional weapon fields
    property: Optional[List[str]] = Field(None, description="Weapon properties")
    weaponCategory: Optional[str] = Field(None, description="Weapon category")
    dmg1: Optional[str] = Field(None, description="Primary damage")
    dmg2: Optional[str] = Field(None, description="Secondary damage")
    dmgType: Optional[str] = Field(None, description="Damage type")
    range: Optional[str] = Field(None, description="Weapon range")
    bonusWeapon: Optional[str] = Field(None, description="Weapon bonus")

    # Optional magic fields
    recharge: Optional[str] = Field(None, description="Recharge condition")
    reqAttunement: Optional[str] = Field(None, description="Requires attunement")
    attachedSpells: Optional[List[str]] = Field(None, description="Attached spells")
    baseItem: Optional[str] = Field(None, description="Base item")
    tier: Optional[str] = Field(None, description="Item tier")

    @classmethod
    def from_row(cls, row, source: str, json_source: str) -> 'Item':
        """
        Create Item from DataFrame row.

        Args:
            row: DataFrame row from Google Sheets
            source: Source filter (e.g., "VSTGCC")
            json_source: JSON source identifier

        Returns:
            Validated Item instance
        """
        # Parse properties
        properties = None
        properties = split_csv(row_value(row, "Property ABRV")) or None

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

        return cls(
            source=json_source,
            name=optional_text(row_value(row, "Name")) or "Unnamed Item",
            type=item_type,
            rarity="none",
            value=optional_text(row_value(row, "Value")),
            weight=optional_text(row_value(row, "Weight")),
            page=optional_int(row_value(row, "Page"), 0),
            entries=entries,
            # Weapon fields
            property=properties,
            weaponCategory=optional_text(row_value(row, "Category")),
            dmg1=optional_text(row_value(row, "Damage 1")),
            dmg2=optional_text(row_value(row, "Damage 2")),
            dmgType=optional_text(row_value(row, "Damage Type")),
            range=optional_text(row_value(row, "Range")),
            bonusWeapon=optional_text(row_value(row, "Bonus Weapon")),
            # Magic fields
            recharge=optional_text(row_value(row, "Recharge")),
            reqAttunement=optional_text(row_value(row, "Require Attunement")),
            attachedSpells=attached_spells,
            baseItem=optional_text(row_value(row, "Base Item")),
            tier=optional_text(row_value(row, "Tier")),
        )
