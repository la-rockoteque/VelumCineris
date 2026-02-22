"""
Magic Item entity model for D&D 5e.

Provides type-safe validation for magic item data from Google Sheets.
"""

from pydantic import Field
from typing import Optional, List
import pandas as pd
from ..base import BaseEntity


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
    def from_row(cls, row: pd.Series, source: str, json_source: str) -> 'MagicItem':
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
        if pd.notnull(row.get("Property")):
            props = [p.strip() for p in str(row.get("Property")).split(",")]
            # Add "VS" prefix as in original code
            properties = [f"VS{prop[2:]}" if len(prop) > 2 else prop for prop in props]

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
        if pd.isna(item_type) or not str(item_type).strip():
            item_type = "OTH"
        item_type = str(item_type)

        # Get rarity safely
        rarity = row.get("Rarity", "common")
        if pd.isna(rarity) or not str(rarity).strip():
            rarity = "common"
        rarity = str(rarity).lower()

        return cls(
            source=json_source,
            name=row.get("Name", "Unnamed Magic Item"),
            type=item_type,
            rarity=rarity,
            wondrous=True,
            value=opt_str("Value"),
            weight=opt_str("Weight"),
            page=0,
            entries=entries,
            # Weapon/armor fields
            properties=properties,
            weaponCategory=opt_str("Category"),
            dmg1=opt_str("Damage 1"),
            dmg2=opt_str("Damage 2"),
            dmgType=opt_str("Damage Type"),
            range=opt_str("Extracted Range"),
            # Magic fields
            recharge=opt_str("Recharge"),
            reqAttunement=opt_str("Require Attunement"),
            attachedSpells=attached_spells,
            baseItem=opt_str("Base Item"),
            tier=opt_str("Tier"),
        )
