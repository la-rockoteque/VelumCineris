from __future__ import annotations

from Book.core.writers import (
    BaseWriter,
    CampaignHandbookWriter,
    CompletePHBWriter,
    DMGWriter,
    DivineCodexWriter,
    MonsterManualWriter,
    OmnibookWriter,
    PHBWriter,
)

WriterClass = type[BaseWriter]

_WRITERS: dict[str, WriterClass] = {
    "omnibook": OmnibookWriter,
    "phb": PHBWriter,
    "complete_phb": CompletePHBWriter,
    "campaign_handbook": CampaignHandbookWriter,
    "full_handbook": CampaignHandbookWriter,
    "dmg": DMGWriter,
    "monster_manual": MonsterManualWriter,
    "divine_codex": DivineCodexWriter,
}


def normalize_book_type(book_type: str) -> str:
    normalized = str(book_type).strip().lower()
    if normalized not in _WRITERS:
        raise ValueError(
            f"Unknown book type '{book_type}'. Expected one of: {sorted(_WRITERS)}"
        )
    return normalized


def get_writer_class(book_type: str) -> WriterClass:
    return _WRITERS[normalize_book_type(book_type)]


def list_book_types() -> tuple[str, ...]:
    return tuple(_WRITERS.keys())
