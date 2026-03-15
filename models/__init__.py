"""
VelumCineris Pydantic Data Layer.

Type-safe domain models for D&D 5e homebrew content, providing:
- Validation at load time
- IDE autocomplete and type hints
- Backward compatibility with dict-based code
- Centralized schema definitions

Example:
    >>> from models import BaseEntity, Components
    >>> from models.entities.spell import Spell
    >>> from models.datasets import load_dataset
    >>>
    >>> # Load spells through the dataset ingestion layer
    >>> spell = load_dataset("spells")[0]
    >>>
    >>> # Type-safe attribute access
    >>> print(spell.name)
    >>> print(spell.components.v)  # IDE autocomplete!
    >>>
    >>> # Backward-compatible dict access
    >>> print(spell.get("name"))
    >>> print(spell["name"])
"""

from .base import BaseEntity, DictAccessMixin
from .fields import (
    Components,
    TimeAction,
    Distance,
    Range,
    Duration,
    Speed,
    AbilityScores,
    HP,
    AC,
    Skills,
    Saves,
)

__all__ = [
    # Base classes
    "BaseEntity",
    "DictAccessMixin",
    # Field types
    "Components",
    "TimeAction",
    "Distance",
    "Range",
    "Duration",
    "Speed",
    "AbilityScores",
    "HP",
    "AC",
    "Skills",
    "Saves",
]
