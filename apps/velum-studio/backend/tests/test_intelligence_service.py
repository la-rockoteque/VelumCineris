from __future__ import annotations

from app.services.intelligence_service import DEFAULT_OPENAI_MODEL, IntelligenceService


def test_suggest_field_parses_json_and_normalizes_validation_options(monkeypatch) -> None:
    service = IntelligenceService()
    monkeypatch.setattr(
        service,
        "_run_openai",
        lambda **_: {
            "ok": True,
            "text": '```json\n{"suggested_value":"evocation","rationale":"Best fit for the spell context."}\n```',
        },
    )

    payload = service.suggest_field(
        sheet="Spells",
        field_name="School",
        row_data={"Name": "Arc Flash", "School": ""},
        validation_options=["Abjuration", "Evocation"],
        model="gpt-5-mini",
    )

    assert payload["provider"] == "chatgpt"
    assert payload["status"] == "ok"
    assert payload["field_name"] == "School"
    assert payload["suggested_value"] == "Evocation"
    assert payload["rationale"] == "Best fit for the spell context."


def test_suggest_field_falls_back_when_openai_is_unavailable(monkeypatch) -> None:
    service = IntelligenceService()
    monkeypatch.setattr(service, "_run_openai", lambda **_: {"ok": False, "error": "Missing OPENAI_API_KEY"})

    payload = service.suggest_field(
        sheet="Spells",
        field_name="Description",
        row_data={"Name": "Arc Flash", "Description": ""},
        validation_options=[],
        model="llama3.1:8b",
    )

    assert payload["provider"] == "heuristic"
    assert payload["status"] == "fallback"
    assert payload["model"] == DEFAULT_OPENAI_MODEL
    assert payload["reason"] == "Missing OPENAI_API_KEY"
    assert "Arc Flash" in payload["suggested_value"]
