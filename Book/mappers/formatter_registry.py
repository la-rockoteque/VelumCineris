from __future__ import annotations

from Book.core.formatters import (
    BackgroundFormatter,
    BaseFormatter,
    ClassFormatter,
    DiseaseFormatter,
    FeatFormatter,
    ItemFormatter,
    LanguageFormatter,
    MagicItemFormatter,
    MonsterFormatter,
    SpeciesFormatter,
    SpellFormatter,
    SubclassFormatter,
)

FormatterClass = type[BaseFormatter]

_FORMATTERS: dict[str, FormatterClass] = {
    "spell": SpellFormatter,
    "species": SpeciesFormatter,
    "race": SpeciesFormatter,
    "monster": MonsterFormatter,
    "background": BackgroundFormatter,
    "feat": FeatFormatter,
    "class": ClassFormatter,
    "subclass": SubclassFormatter,
    "item": ItemFormatter,
    "magicitem": MagicItemFormatter,
    "language": LanguageFormatter,
    "disease": DiseaseFormatter,
}


def get_formatter(entity_type: str) -> BaseFormatter:
    key = str(entity_type).strip().lower()
    if key not in _FORMATTERS:
        raise ValueError(
            f"Unknown entity type '{entity_type}'. Expected one of: {sorted(_FORMATTERS)}"
        )
    return _FORMATTERS[key]()


def list_entity_types() -> tuple[str, ...]:
    return tuple(_FORMATTERS.keys())
