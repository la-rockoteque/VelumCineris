from __future__ import annotations

from models.datasets import registry


class FakeConverter:
    def __init__(self, result, calls):
        self._result = result
        self._calls = calls

    def convert_all(self, **kwargs):
        self._calls.append(kwargs)
        return self._result


def test_load_dataset_uses_source_filter_when_required(monkeypatch):
    calls = []
    registry.clear_dataset_cache()
    monkeypatch.setitem(
        registry._SETTING_DATASET_SPECS["fantasy"],
        "spells",
        registry.DatasetSpec(
            name="spells",
            converter_factory=lambda: FakeConverter(["spell"], calls),
            source_filter_mode="source",
        ),
    )
    monkeypatch.setitem(
        registry._SOURCE_CONTEXT_RESOLVERS,
        "fantasy",
        lambda source_code: (source_code, f"{source_code}_JSON"),
    )

    result = registry.load_dataset("spell", source_code="ORIO")

    assert result == ["spell"]
    assert calls == [
        {
            "source_filter": "ORIO",
            "source": "ORIO",
            "json_source": "ORIO_JSON",
        }
    ]


def test_load_dataset_skips_source_filter_for_global_datasets(monkeypatch):
    calls = []
    registry.clear_dataset_cache()
    monkeypatch.setitem(
        registry._SETTING_DATASET_SPECS["fantasy"],
        "monster",
        registry.DatasetSpec(
            name="monster",
            converter_factory=lambda: FakeConverter(["monster"], calls),
            source_filter_mode="none",
        ),
    )
    monkeypatch.setitem(
        registry._SOURCE_CONTEXT_RESOLVERS,
        "fantasy",
        lambda source_code: (source_code, f"{source_code}_JSON"),
    )

    result = registry.load_dataset("monsters", source_code="ORIO")

    assert result == ["monster"]
    assert calls == [
        {
            "source_filter": None,
            "source": "ORIO",
            "json_source": "ORIO_JSON",
        }
    ]


def test_load_dataset_caches_by_dataset_and_source(monkeypatch):
    calls = []
    registry.clear_dataset_cache()
    monkeypatch.setitem(
        registry._SETTING_DATASET_SPECS["fantasy"],
        "languages",
        registry.DatasetSpec(
            name="languages",
            converter_factory=lambda: FakeConverter(["language"], calls),
            source_filter_mode="none",
        ),
    )
    monkeypatch.setitem(
        registry._SOURCE_CONTEXT_RESOLVERS,
        "fantasy",
        lambda source_code: (source_code, f"{source_code}_JSON"),
    )

    first = registry.load_dataset("language", source_code="ORIO")
    second = registry.load_dataset("languages", source_code="ORIO")

    assert first == ["language"]
    assert second == ["language"]
    assert len(calls) == 1


def test_resolve_dataset_name_normalizes_aliases():
    assert registry.resolve_dataset_name("spell") == "spells"
    assert registry.resolve_dataset_name("magic-items") == "magic_items"
    assert "spells" in registry.list_datasets()


def test_load_dataset_supports_modern_setting(monkeypatch):
    calls = []
    registry.clear_dataset_cache()
    monkeypatch.setitem(
        registry._SETTING_DATASET_SPECS["modern"],
        "spells",
        registry.DatasetSpec(
            name="spells",
            converter_factory=lambda: FakeConverter(["modern-spell"], calls),
            source_filter_mode="source",
        ),
    )
    monkeypatch.setitem(
        registry._SOURCE_CONTEXT_RESOLVERS,
        "modern",
        lambda source_code: (f"{source_code}_SRC", f"{source_code}_JSON"),
    )
    monkeypatch.setitem(registry._SETTING_DEFAULT_SOURCES, "modern", "VSTGCC")

    result = registry.load_dataset("spell", setting="modern")

    assert result == ["modern-spell"]
    assert calls == [
        {
            "source_filter": "VSTGCC_SRC",
            "source": "VSTGCC_SRC",
            "json_source": "VSTGCC_JSON",
        }
    ]


def test_resolve_dataset_name_is_setting_aware():
    assert (
        registry.resolve_dataset_name("background", setting="modern") == "backgrounds"
    )
