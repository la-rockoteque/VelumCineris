from __future__ import annotations

import json
import os
import re
from typing import Any
from urllib import request
from urllib.error import HTTPError, URLError


DEFAULT_OPENAI_MODEL = "gpt-5-mini"
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


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

        openai_model = self._resolve_openai_model(model)
        result = self._run_openai(prompt=prompt, model=openai_model)
        if result["ok"]:
            return {
                "mode": normalized_mode,
                "provider": "chatgpt",
                "model": openai_model,
                "status": "ok",
                "suggestions": result["text"],
            }

        return {
            "mode": normalized_mode,
            "provider": "heuristic",
            "model": openai_model,
            "status": "fallback",
            "reason": result["error"],
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

    def suggest_field(
        self,
        *,
        sheet: str,
        field_name: str,
        row_data: dict[str, Any] | None,
        validation_options: list[str] | None = None,
        model: str = DEFAULT_OPENAI_MODEL,
    ) -> dict[str, Any]:
        normalized_field_name = field_name.strip()
        if not normalized_field_name:
            raise ValueError("field_name cannot be empty")

        current_value = _stringify((row_data or {}).get(normalized_field_name))
        openai_model = self._resolve_openai_model(model)
        result = self._run_openai(
            prompt=self._field_prompt(
                sheet=sheet,
                field_name=normalized_field_name,
                current_value=current_value,
                row_data=row_data,
                validation_options=validation_options or [],
            ),
            model=openai_model,
        )

        if result["ok"]:
            suggestion = self._parse_field_suggestion(
                result["text"],
                current_value=current_value,
                validation_options=validation_options or [],
            )
            return {
                "provider": "chatgpt",
                "model": openai_model,
                "status": "ok",
                "field_name": normalized_field_name,
                "current_value": current_value,
                "suggested_value": suggestion["suggested_value"],
                "rationale": suggestion["rationale"],
                "reason": None,
            }

        fallback = self._fallback_field_suggestion(
            sheet=sheet,
            field_name=normalized_field_name,
            current_value=current_value,
            row_data=row_data,
            validation_options=validation_options or [],
        )
        return {
            "provider": "heuristic",
            "model": openai_model,
            "status": "fallback",
            "field_name": normalized_field_name,
            "current_value": current_value,
            "suggested_value": fallback["suggested_value"],
            "rationale": fallback["rationale"],
            "reason": result["error"],
        }

    def _field_prompt(
        self,
        *,
        sheet: str,
        field_name: str,
        current_value: str,
        row_data: dict[str, Any] | None,
        validation_options: list[str],
    ) -> str:
        context = json.dumps(row_data or {}, ensure_ascii=True)
        constraints = (
            f"Allowed validation options: {json.dumps(validation_options, ensure_ascii=True)}.\n"
            if validation_options
            else ""
        )
        return (
            "You are a DnD 5e balancing editor helping fill one spreadsheet field.\n"
            f"Sheet: {sheet or 'Unknown'}\n"
            f"Target field: {field_name}\n"
            f"Current field value: {current_value or '(empty)'}\n"
            f"{constraints}"
            f"Full item context JSON: {context}\n"
            "Return only valid JSON with this shape:\n"
            '{"suggested_value":"spreadsheet-ready text","rationale":"one or two concise sentences"}\n'
            "Rules:\n"
            "- Suggest a value only for the target field.\n"
            "- Preserve the item's tone and intended role.\n"
            "- Optimize for balanced, official-adjacent D&D 5e wording.\n"
            "- Keep the value compact enough to paste directly into the spreadsheet.\n"
            "- If validation options are provided, use those exact values only.\n"
            "- If the current value is already strong, you may keep it and explain why.\n"
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

    def _fallback_field_suggestion(
        self,
        *,
        sheet: str,
        field_name: str,
        current_value: str,
        row_data: dict[str, Any] | None,
        validation_options: list[str],
    ) -> dict[str, str]:
        name = _pick_name(row_data or {})
        normalized_field = _normalize(field_name)

        if current_value.strip():
            return {
                "suggested_value": current_value,
                "rationale": "OpenAI was unavailable, so the safest fallback is to preserve the current field value.",
            }

        if validation_options:
            return {
                "suggested_value": validation_options[0],
                "rationale": "OpenAI was unavailable, so the fallback uses the first allowed validation option.",
            }

        if "description" in normalized_field or "effect" in normalized_field or "text" in normalized_field:
            return {
                "suggested_value": (
                    f"{name} channels controlled power in a way that stays readable at the table and balanced for its intended role."
                ),
                "rationale": f"Fallback wording for {sheet or 'this sheet'} keeps the field immediately usable until ChatGPT is available.",
            }

        if "range" in normalized_field:
            return {
                "suggested_value": "60 feet",
                "rationale": "Fallback range uses a common 5e baseline that is broadly serviceable.",
            }

        if "duration" in normalized_field:
            return {
                "suggested_value": "Instantaneous",
                "rationale": "Fallback duration uses the least assumption-heavy 5e wording.",
            }

        return {
            "suggested_value": "",
            "rationale": f"No reliable fallback suggestion was available for {field_name}.",
        }

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

    def _run_openai(self, *, prompt: str, model: str) -> dict[str, Any]:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {"ok": False, "error": "Missing OPENAI_API_KEY"}

        payload = {
            "model": model,
            "input": prompt,
        }
        req = request.Request(
            OPENAI_RESPONSES_URL,
            method="POST",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )

        try:
            with request.urlopen(req, timeout=20) as response:
                raw = response.read().decode("utf-8")
            parsed = json.loads(raw)
            text = self._extract_openai_text(parsed)
            if not text:
                return {"ok": False, "error": "OpenAI returned an empty response."}
            return {"ok": True, "text": text}
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            return {"ok": False, "error": f"OpenAI request failed ({exc.code}): {detail}"}
        except (TimeoutError, URLError, OSError, ValueError) as exc:
            return {"ok": False, "error": f"OpenAI unavailable: {exc}"}

    def _extract_openai_text(self, payload: dict[str, Any]) -> str:
        output_text = payload.get("output_text")
        if isinstance(output_text, str) and output_text.strip():
            return output_text.strip()

        parts: list[str] = []
        for item in payload.get("output", []):
            if not isinstance(item, dict):
                continue
            for content in item.get("content", []):
                if not isinstance(content, dict):
                    continue
                text_value = content.get("text")
                if isinstance(text_value, str) and text_value.strip():
                    parts.append(text_value.strip())
                    continue
                if isinstance(text_value, dict):
                    nested_value = text_value.get("value")
                    if isinstance(nested_value, str) and nested_value.strip():
                        parts.append(nested_value.strip())
        return "\n".join(parts).strip()

    def _parse_field_suggestion(
        self,
        text: str,
        *,
        current_value: str,
        validation_options: list[str],
    ) -> dict[str, str]:
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned, flags=re.IGNORECASE | re.DOTALL)

        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
            if not match:
                raise ValueError("OpenAI did not return valid JSON for the field suggestion.")
            parsed = json.loads(match.group(0))

        suggested_value = _stringify(parsed.get("suggested_value"))
        rationale = _stringify(parsed.get("rationale"))
        if validation_options:
            suggested_value = _normalize_to_validation_options(suggested_value, validation_options)

        return {
            "suggested_value": suggested_value if suggested_value or not current_value else current_value,
            "rationale": rationale or "Balanced field suggestion generated from the current item context.",
        }

    def _resolve_openai_model(self, model: str) -> str:
        candidate = model.strip()
        if not candidate:
            return os.getenv("VELUM_OPENAI_MODEL", DEFAULT_OPENAI_MODEL)

        lowered = candidate.lower()
        if ":" in candidate or lowered.startswith(("llama", "mistral", "qwen", "gemma")):
            return os.getenv("VELUM_OPENAI_MODEL", DEFAULT_OPENAI_MODEL)
        return candidate


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


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _normalize_to_validation_options(value: str, validation_options: list[str]) -> str:
    if not value.strip() or not validation_options:
        return value.strip()

    exact = {option: option for option in validation_options}
    if value in exact:
        return exact[value]

    normalized_map = {_normalize(option): option for option in validation_options}
    normalized_value = _normalize(value)
    if normalized_value in normalized_map:
        return normalized_map[normalized_value]

    parts = [part.strip() for part in re.split(r"[;,]", value) if part.strip()]
    if parts and all(_normalize(part) in normalized_map for part in parts):
        return ", ".join(normalized_map[_normalize(part)] for part in parts)

    return value.strip()
