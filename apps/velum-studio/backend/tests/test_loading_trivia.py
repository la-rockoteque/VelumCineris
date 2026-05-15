from __future__ import annotations

from pathlib import Path

from app.loading_trivia import load_loading_trivia_items


def test_load_loading_trivia_items_supports_headered_csv(tmp_path: Path) -> None:
    csv_path = tmp_path / "loading_trivia.csv"
    csv_path.write_text(
        "created_at_utc,entity_type,entity_name,source,tidbit,model\n"
        '2026-03-08T20:37:49.466690+00:00,monster,Stoneback Broadcrawler,GuideToOrimond,"Did you know stonebacks brace their shells?",llama3\n',
        encoding="utf-8",
    )

    items = load_loading_trivia_items(csv_path)

    assert len(items) == 1
    assert items[0].entity_type == "monster"
    assert items[0].entity_name == "Stoneback Broadcrawler"
    assert items[0].source == "GuideToOrimond"
    assert items[0].tidbit == "Did you know stonebacks brace their shells?"


def test_load_loading_trivia_items_supports_headerless_csv(tmp_path: Path) -> None:
    csv_path = tmp_path / "loading_trivia.csv"
    csv_path.write_text(
        '2026-03-08T20:37:49.466690+00:00,monster,Stoneback Broadcrawler,GuideToOrimond,"Did you know stonebacks brace their shells?",llama3\n',
        encoding="utf-8",
    )

    items = load_loading_trivia_items(csv_path)

    assert len(items) == 1
    assert items[0].entity_type == "monster"
    assert items[0].entity_name == "Stoneback Broadcrawler"
    assert items[0].source == "GuideToOrimond"
    assert items[0].tidbit == "Did you know stonebacks brace their shells?"
