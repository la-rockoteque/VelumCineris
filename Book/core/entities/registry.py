from __future__ import annotations

from functools import lru_cache
from typing import Any

from Book.core.entities.base import EntityMarkdownRenderer
from Book.core.entities.backgrounds import BackgroundMarkdownRenderer
from Book.core.entities.classes import ClassMarkdownRenderer
from Book.core.entities.diseases import DiseaseMarkdownRenderer
from Book.core.entities.feats import FeatMarkdownRenderer
from Book.core.entities.items import ItemMarkdownRenderer
from Book.core.entities.languages import LanguageMarkdownRenderer
from Book.core.entities.magic_items import MagicItemMarkdownRenderer
from Book.core.entities.monsters import MonsterMarkdownRenderer
from Book.core.entities.species import SpeciesMarkdownRenderer
from Book.core.entities.spells import SpellMarkdownRenderer
from Book.core.entities.subclasses import SubclassMarkdownRenderer

_RENDERER_CLASSES: dict[str, type[EntityMarkdownRenderer]] = {
    "spell": SpellMarkdownRenderer,
    "species": SpeciesMarkdownRenderer,
    "race": SpeciesMarkdownRenderer,
    "monster": MonsterMarkdownRenderer,
    "background": BackgroundMarkdownRenderer,
    "feat": FeatMarkdownRenderer,
    "class": ClassMarkdownRenderer,
    "subclass": SubclassMarkdownRenderer,
    "item": ItemMarkdownRenderer,
    "magicitem": MagicItemMarkdownRenderer,
    "language": LanguageMarkdownRenderer,
    "disease": DiseaseMarkdownRenderer,
}


@lru_cache(maxsize=None)
def get_entity_renderer(entity_type: str) -> EntityMarkdownRenderer:
    renderer_class = _RENDERER_CLASSES.get(entity_type.lower())
    if renderer_class is None:
        raise ValueError(f"No markdown renderer available for entity type: {entity_type}")
    return renderer_class()


def render_entity_markdown(entity_type: str, entity: dict[str, Any]) -> str:
    return get_entity_renderer(entity_type).render_markdown(entity)
