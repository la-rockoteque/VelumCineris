"""
Book writers for different book types.
"""

from Book.writers.base import BaseWriter
from Book.writers.omnibook import OmnibookWriter
from Book.writers.phb import PHBWriter
from Book.writers.complete_phb import CompletePHBWriter
from Book.writers.dmg import DMGWriter
from Book.writers.monster_manual import MonsterManualWriter
from Book.writers.divine_codex import DivineCodexWriter

__all__ = [
    "BaseWriter",
    "OmnibookWriter",
    "PHBWriter",
    "CompletePHBWriter",
    "DMGWriter",
    "MonsterManualWriter",
    "DivineCodexWriter",
]
