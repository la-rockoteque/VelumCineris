"""
Item entity model for D&D 5e.

Provides type-safe validation for item data from Google Sheets.
"""

from pydantic import Field
from typing import Optional, List
import pandas as pd
from ..base import BaseEntity


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
    def from_row(cls, row: pd.Series, source: str, json_source: str) -> 'Item':
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
        if pd.notnull(row.get("Property ABRV")):
            properties = [p.strip() for p in row.get("Property ABRV").split(",")]

        # Parse attached spells
        attached_spells = None
        if pd.notnull(row.get("Attached Spells")):
            attached_spells = [s.strip() for s in row.get("Attached Spells").split(",")]

        # Parse description
        entries = []
        if pd.notnull(row.get("Description")):
            entries.append(row.get("Description"))

        # Helper for optional string fields
        def opt_str(field_name: str) -> Optional[str]:
            value = row.get(field_name)
            if pd.isna(value):
                return None
            stripped = str(value).strip()
            return stripped if stripped else None

        # Get type safely
        item_type = row.get("Type ABRV")
        if pd.isna(item_type):
            item_type = "OTH"
        item_type = str(item_type)

        return cls(
            source=json_source,
            name=row.get("Name", "Unnamed Item"),
            type=item_type,
            rarity="none",
            value=opt_str("Value"),
            weight=opt_str("Weight"),
            page=int(row.get("Page", 0)) if pd.notnull(row.get("Page")) else 0,
            entries=entries,
            # Weapon fields
            property=properties,
            weaponCategory=opt_str("Category"),
            dmg1=opt_str("Damage 1"),
            dmg2=opt_str("Damage 2"),
            dmgType=opt_str("Damage Type"),
            range=opt_str("Range"),
            bonusWeapon=opt_str("Bonus Weapon"),
            # Magic fields
            recharge=opt_str("Recharge"),
            reqAttunement=opt_str("Require Attunement"),
            attachedSpells=attached_spells,
            baseItem=opt_str("Base Item"),
            tier=opt_str("Tier"),
        )
