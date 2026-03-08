from __future__ import annotations

import json
from typing import Any
from urllib import request
from urllib.error import URLError


class IntelligenceService:
    MODES = ("level_spell", "adjust_species", "balance_stats", "custom")

    def suggest(
        self,
        *,
        mode: str,
        instruction: str,
        row_data: dict[str, Any] | None,
        use_local_llm: bool,
        model: str,
    ) -> dict[str, Any]:
        normalized_mode = mode.strip().lower()
        if normalized_mode not in self.MODES:
            raise ValueError(f"mode must be one of: {', '.join(self.MODES)}")

        prompt = self._prompt(normalized_mode, instruction, row_data)

        if use_local_llm:
            result = self._run_ollama(prompt=prompt, model=model)
            if result["ok"]:
                return {
                    "mode": normalized_mode,
                    "provider": "ollama",
                    "model": model,
                    "status": "ok",
                    "suggestions": result["text"],
                }

            fallback = self._fallback(normalized_mode, instruction, row_data)
            return {
                "mode": normalized_mode,
                "provider": "heuristic",
                "model": model,
                "status": "fallback",
                "reason": result["error"],
                "suggestions": fallback,
            }

        return {
            "mode": normalized_mode,
            "provider": "heuristic",
            "model": model,
            "status": "ok",
            "suggestions": self._fallback(normalized_mode, instruction, row_data),
        }

    def _prompt(self, mode: str, instruction: str, row_data: dict[str, Any] | None) -> str:
        context = json.dumps(row_data or {}, ensure_ascii=True)
        return (
            "You are a DnD 5e content balancing assistant. "
            f"Task mode: {mode}. "
            f"User instruction: {instruction or 'No extra instruction provided.'}\n"
            f"Item context JSON: {context}\n"
            "Return concise bullet points with rationale."
        )

    def _fallback(self, mode: str, instruction: str, row_data: dict[str, Any] | None) -> str:
        name = _pick_name(row_data or {})
        base = [
            f"Target item: {name}",
            f"Mode: {mode}",
            "Review action economy, DPR, and saving throw pressure compared to same-tier official content.",
            "Prefer additive tweaks over full rewrites to preserve lore identity.",
        ]
        if instruction:
            base.append(f"User directive applied: {instruction.strip()}")
        return "\n".join(f"- {line}" for line in base)

    def _run_ollama(self, *, prompt: str, model: str) -> dict[str, Any]:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
        }
        req = request.Request(
            "http://127.0.0.1:11434/api/generate",
            method="POST",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )

        try:
            with request.urlopen(req, timeout=8) as response:
                raw = response.read().decode("utf-8")
            parsed = json.loads(raw)
            text = str(parsed.get("response", "")).strip()
            if not text:
                return {"ok": False, "error": "Local model returned empty response."}
            return {"ok": True, "text": text}
        except (TimeoutError, URLError, OSError, ValueError) as exc:
            return {"ok": False, "error": f"Ollama unavailable: {exc}"}


def _pick_name(row_data: dict[str, Any]) -> str:
    for key in ("Name", "Spell Name", "Condition Name", "Feature Name"):
        for row_key, value in row_data.items():
            if _normalize(row_key) == _normalize(key) and _has_value(value):
                return str(value).strip()
    for value in row_data.values():
        if _has_value(value):
            return str(value).strip()
    return "Unnamed item"


def _normalize(value: str) -> str:
    return "".join(ch for ch in str(value).lower() if ch.isalnum())


def _has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    return True
