from __future__ import annotations

import re
from typing import Any

from .spreadsheet_service import RegistryManager


MARKER_ENGLISH = ("english", "source", "base", "common")
MARKER_TRANSLATED = ("translation", "translated", "word", "term")
MARKER_ROMANIZED = ("roman", "romanized", "latin")
MARKER_SCRIPT = ("script", "glyph", "rune", "native", "symbol")
MARKER_PHONETIC = ("phonetic", "phonetics", "pronunciation", "ipa")


class TranslatorService:
    def __init__(self, registry_manager: RegistryManager):
        self.registry_manager = registry_manager

    def available_targets(self, source: str = "auto") -> list[str]:
        names = self.registry_manager.list_sheets(source)
        groups = _language_groups(names)
        if groups:
            return sorted(groups.keys())

        legacy = [name for name in names if "lang" in name.lower()]
        return legacy or ["Languages"]

    def language_context(self, *, source: str, target: str, limit: int = 40) -> dict[str, Any]:
        context = self._resolve_target_context(source=source, target=target)
        if context is None:
            return {
                "source": source,
                "target": target,
                "dictionary_sheet": None,
                "phonetics_sheet": None,
                "script_sheet": None,
                "grammar_sheet": None,
                "sheets": [],
            }

        sheets: list[dict[str, Any]] = []
        for sheet_name in context["ordered_sheets"]:
            try:
                _, records = self.registry_manager.records_for(source, sheet_name, limit=limit)
            except Exception:
                records = []
            sheets.append({"sheet": sheet_name, "rows": records})

        return {
            "source": source,
            "target": context["language"],
            "dictionary_sheet": context["dictionary_sheet"],
            "phonetics_sheet": context["phonetics_sheet"],
            "script_sheet": context["script_sheet"],
            "grammar_sheet": context["grammar_sheet"],
            "sheets": sheets,
        }

    def translate(
        self,
        *,
        source: str,
        target: str,
        text: str,
    ) -> dict[str, Any]:
        if not text.strip():
            raise ValueError("text cannot be empty")

        context = self._resolve_target_context(source=source, target=target)
        if context is None:
            return self._fallback(target=target, text=text, reason="No language sheet found")

        dictionary_sheet = context["dictionary_sheet"] or context["base_sheet"]
        if dictionary_sheet is None:
            return self._fallback(target=target, text=text, reason="No dictionary sheet found")

        _, records = self.registry_manager.records_for(source, dictionary_sheet, limit=12000)
        match = self._find_translation(records, text)
        if match is None:
            return self._fallback(
                target=context["language"],
                text=text,
                reason=f"No exact translation in sheet '{dictionary_sheet}'",
            )

        translated = match.get("translated") or f"[{context['language']}] {text}"
        romanized = match.get("romanized") or translated
        phonetic = match.get("phonetic") or romanized

        symbol_map = self._symbol_map_for_context(source=source, context=context)
        symbolized = self._symbolize_text(phonetic, symbol_map)
        if not symbolized:
            symbolized = match.get("script") or translated

        return {
            "target": context["language"],
            "sheet": dictionary_sheet,
            "input": text,
            "translated": translated,
            "phonetic": phonetic,
            "romanized": romanized,
            "script": symbolized,
            "symbolized": symbolized,
            "audio_text": romanized,
            "status": "ok",
        }

    def _resolve_target_context(self, *, source: str, target: str) -> dict[str, Any] | None:
        names = self.registry_manager.list_sheets(source)
        groups = _language_groups(names)
        wanted = _normalize(target)

        selected_key: str | None = None
        for key in groups:
            if _normalize(key) == wanted:
                selected_key = key
                break
        if selected_key is None:
            for key in groups:
                key_norm = _normalize(key)
                if wanted in key_norm or key_norm in wanted:
                    selected_key = key
                    break

        if selected_key is None and names:
            for name in names:
                if _normalize(name) == wanted:
                    selected_key = name
                    groups[selected_key] = [name]
                    break

        if selected_key is None:
            return None

        group_sheets = groups.get(selected_key, [])
        dictionary_sheet = _pick_sheet(group_sheets, ("dictionary",)) or _pick_sheet(group_sheets, ("lang", "language"))
        phonetics_sheet = _pick_sheet(group_sheets, ("phonetic",))
        script_sheet = _pick_sheet(group_sheets, ("script",))
        grammar_sheet = _pick_sheet(group_sheets, ("grammar",))

        ordered: list[str] = []
        for name in (dictionary_sheet, phonetics_sheet, script_sheet, grammar_sheet):
            if name and name not in ordered:
                ordered.append(name)
        for name in group_sheets:
            if name not in ordered:
                ordered.append(name)

        return {
            "language": selected_key,
            "base_sheet": group_sheets[0] if group_sheets else None,
            "dictionary_sheet": dictionary_sheet,
            "phonetics_sheet": phonetics_sheet,
            "script_sheet": script_sheet,
            "grammar_sheet": grammar_sheet,
            "ordered_sheets": ordered,
        }

    def _find_translation(self, records: list[dict[str, Any]], text: str) -> dict[str, str] | None:
        wanted = text.strip().lower()

        for record in records:
            english_value = _first_by_markers(record, MARKER_ENGLISH)
            if english_value is None:
                continue
            if str(english_value).strip().lower() != wanted:
                continue

            translated = _first_by_markers(record, MARKER_TRANSLATED)
            romanized = _first_by_markers(record, MARKER_ROMANIZED)
            script_text = _first_by_markers(record, MARKER_SCRIPT)
            phonetic = _first_by_markers(record, MARKER_PHONETIC)

            return {
                "translated": str(translated).strip() if translated is not None else "",
                "romanized": str(romanized).strip() if romanized is not None else "",
                "script": str(script_text).strip() if script_text is not None else "",
                "phonetic": str(phonetic).strip() if phonetic is not None else "",
            }
        return None

    def _symbol_map_for_context(self, *, source: str, context: dict[str, Any]) -> dict[str, str]:
        symbol_map: dict[str, str] = {}
        for sheet_name in (context.get("phonetics_sheet"), context.get("script_sheet")):
            if not sheet_name:
                continue
            try:
                _, records = self.registry_manager.records_for(source, sheet_name, limit=8000)
            except Exception:
                continue

            for record in records:
                key = _first_by_markers(record, MARKER_PHONETIC + MARKER_ROMANIZED)
                value = _first_by_markers(record, MARKER_SCRIPT)
                if key is None or value is None:
                    continue

                normalized = _normalize(str(key))
                if normalized:
                    symbol_map[normalized] = str(value).strip()

        return symbol_map

    def _symbolize_text(self, text: str, symbol_map: dict[str, str]) -> str:
        if not text.strip() or not symbol_map:
            return ""

        def _replace(match: re.Match[str]) -> str:
            token = match.group(0)
            normalized = _normalize(token)
            if normalized in symbol_map:
                return symbol_map[normalized]
            return token

        return re.sub(r"[A-Za-z0-9'_-]+", _replace, text)

    def _fallback(self, *, target: str, text: str, reason: str) -> dict[str, Any]:
        synthetic = _synthetic_translate(text)
        return {
            "target": target,
            "sheet": None,
            "input": text,
            "translated": synthetic,
            "phonetic": text,
            "romanized": text,
            "script": synthetic,
            "symbolized": synthetic,
            "audio_text": text,
            "status": "fallback",
            "reason": reason,
        }


def _language_groups(sheet_names: list[str]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}

    for sheet in sheet_names:
        clean = str(sheet).strip()
        lowered = clean.lower()
        normalized = _normalize(clean)

        language_key = ""
        if ":" in clean:
            language_key = clean.split(":", 1)[0].strip()
        elif " - " in clean:
            language_key = clean.split(" - ", 1)[0].strip()
        elif "language" in lowered:
            language_key = clean
        elif "lang" in lowered:
            language_key = clean

        if not language_key:
            continue

        if normalized in {"language", "languages"}:
            language_key = "Languages"

        groups.setdefault(language_key, []).append(clean)

    return groups


def _pick_sheet(sheet_names: list[str], markers: tuple[str, ...]) -> str | None:
    for name in sheet_names:
        normalized = _normalize(name)
        if all(marker in normalized for marker in markers):
            return name
    for name in sheet_names:
        normalized = _normalize(name)
        if any(marker in normalized for marker in markers):
            return name
    return None


def _first_by_markers(record: dict[str, Any], markers: tuple[str, ...]) -> Any:
    for key, value in record.items():
        if value is None:
            continue
        normalized = _normalize(key)
        if any(_normalize(marker) in normalized for marker in markers):
            return value
    return None


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value).lower())


def _synthetic_translate(text: str) -> str:
    letters = []
    for char in text:
        if char.isalpha():
            base = ord("a") if char.islower() else ord("A")
            letters.append(chr(base + ((ord(char) - base + 7) % 26)))
        else:
            letters.append(char)
    return "".join(letters)
