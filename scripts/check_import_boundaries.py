#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]

BOUNDARIES: dict[str, tuple[str, ...]] = {
    "models": ("FiveETools", "DNDBeyond", "Homebrewery", "Book"),
    "Spreadsheet": ("FiveETools", "DNDBeyond", "Homebrewery", "Book"),
}

IGNORE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
}


@dataclass(frozen=True)
class Violation:
    file_path: Path
    line: int
    importer_root: str
    imported: str
    forbidden_prefix: str


def iter_python_files(base: Path) -> Iterable[Path]:
    for path in base.rglob("*.py"):
        rel_parts = path.relative_to(base).parts
        if any(part in IGNORE_DIRS for part in rel_parts):
            continue
        yield path


def module_root_from_path(path: Path) -> str | None:
    rel = path.relative_to(ROOT)
    if not rel.parts:
        return None
    return rel.parts[0]


def parse_imported_modules(tree: ast.AST) -> list[tuple[int, str]]:
    imports: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append((node.lineno, alias.name))
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append((node.lineno, node.module))
    return imports


def collect_violations() -> list[Violation]:
    violations: list[Violation] = []

    for file_path in iter_python_files(ROOT):
        importer_root = module_root_from_path(file_path)
        if importer_root not in BOUNDARIES:
            continue

        forbidden = BOUNDARIES[importer_root]

        try:
            tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
        except SyntaxError:
            continue

        for line, imported in parse_imported_modules(tree):
            for prefix in forbidden:
                if imported == prefix or imported.startswith(f"{prefix}."):
                    violations.append(
                        Violation(
                            file_path=file_path,
                            line=line,
                            importer_root=importer_root,
                            imported=imported,
                            forbidden_prefix=prefix,
                        )
                    )
                    break

    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Check import boundaries for shared layers.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return non-zero if any violations are found.",
    )
    args = parser.parse_args()

    violations = collect_violations()

    if violations:
        print(f"Found {len(violations)} import boundary violation(s):")
        for violation in sorted(violations, key=lambda v: (str(v.file_path), v.line)):
            print(
                f"- {violation.file_path}:{violation.line} "
                f"[{violation.importer_root}] imports '{violation.imported}' "
                f"(forbidden prefix: {violation.forbidden_prefix})"
            )
    else:
        print("No import boundary violations found.")

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
