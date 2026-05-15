"""
Book writers for different book types.
"""

from Book.core.writers.base import BaseWriter
from Book.core.writers.omnibook import OmnibookWriter
from Book.core.writers.phb import PHBWriter
from Book.core.writers.complete_phb import CompletePHBWriter
from Book.core.writers.campaign_handbook import CampaignHandbookWriter
from Book.core.writers.dmg import DMGWriter
from Book.core.writers.monster_manual import MonsterManualWriter
from Book.core.writers.divine_codex import DivineCodexWriter

__all__ = [
    "BaseWriter",
    "OmnibookWriter",
    "PHBWriter",
    "CompletePHBWriter",
    "CampaignHandbookWriter",
    "DMGWriter",
    "MonsterManualWriter",
    "DivineCodexWriter",
]
