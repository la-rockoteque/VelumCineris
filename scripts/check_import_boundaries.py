#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]

BOUNDARIES: dict[str, tuple[str, ...]] = {
    "models": ("FiveETools", "DNDBeyond", "Homebrewery", "Book"),
    "Spreadsheet": ("FiveETools", "DNDBeyond", "Homebrewery", "Book"),
}

PATH_SPECIFIC_BOUNDARIES: dict[str, tuple[str, ...]] = {
    "DNDBeyond/datasets": ("FiveETools.core",),
    "Homebrewery/datasets": ("FiveETools.core",),
    "Homebrewery/core/Helpers": ("FiveETools.core",),
    "Book/services": ("Book.book_api", "Book.google_docs_client"),
}

IGNORE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
}

ARCH_GUARDRAIL_TEST = "FiveETools/tests/test_architecture_guardrails.py"
NOTEBOOK_BANNED_IMPORT_PATTERNS: tuple[tuple[str, str], ...] = (
    ("src.sources", r"\b(?:from|import)\s+src\.sources\b"),
    (
        "FiveETools.core.Helpers.gsheets_client",
        r"\b(?:from|import)\s+FiveETools\.core\.Helpers\.gsheets_client\b",
    ),
)
TOP_LEVEL_SHEET_SCAN_DIRS: tuple[str, ...] = (
    "FiveETools/core/fantasy",
    "FiveETools/core/modern",
    "models/datasets",
)


@dataclass(frozen=True)
class Violation:
    file_path: Path
    line: int
    importer_root: str
    imported: str
    forbidden_prefix: str


@dataclass(frozen=True)
class NotebookViolation:
    file_path: Path
    cell_index: int
    line: int
    forbidden_pattern: str


@dataclass(frozen=True)
class TopLevelSheetCallViolation:
    file_path: Path
    line: int
    call_name: str


def iter_python_files(base: Path) -> Iterable[Path]:
    for path in base.rglob("*.py"):
        rel_parts = path.relative_to(base).parts
        if any(part in IGNORE_DIRS for part in rel_parts):
            continue
        yield path


def iter_notebook_files(base: Path) -> Iterable[Path]:
    for path in base.rglob("*.ipynb"):
        rel_parts = path.relative_to(base).parts
        if any(part in IGNORE_DIRS for part in rel_parts):
            continue
        yield path


def iter_top_level_scan_files(base: Path) -> Iterable[Path]:
    for rel_dir in TOP_LEVEL_SHEET_SCAN_DIRS:
        scan_dir = base / rel_dir
        if not scan_dir.exists():
            continue
        for path in scan_dir.rglob("*.py"):
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


def _iter_notebook_source_lines(source: object) -> Iterable[tuple[int, str]]:
    if isinstance(source, str):
        lines = source.splitlines()
    elif isinstance(source, list):
        lines = [str(line).rstrip("\n") for line in source]
    else:
        return

    for line_number, line_text in enumerate(lines, start=1):
        yield line_number, line_text


def collect_notebook_violations() -> list[NotebookViolation]:
    violations: list[NotebookViolation] = []
    pattern_objects = [
        (label, re.compile(pattern))
        for label, pattern in NOTEBOOK_BANNED_IMPORT_PATTERNS
    ]

    for file_path in iter_notebook_files(ROOT):
        try:
            notebook = json.loads(file_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue

        cells = notebook.get("cells")
        if not isinstance(cells, list):
            continue

        for cell_index, cell in enumerate(cells, start=1):
            if not isinstance(cell, dict) or cell.get("cell_type") != "code":
                continue

            for line, text in _iter_notebook_source_lines(cell.get("source")):
                for forbidden_pattern, pattern in pattern_objects:
                    if pattern.search(text):
                        violations.append(
                            NotebookViolation(
                                file_path=file_path,
                                cell_index=cell_index,
                                line=line,
                                forbidden_pattern=forbidden_pattern,
                            )
                        )
                        break

    return violations


def _is_sheet_call(func: ast.AST) -> str | None:
    if isinstance(func, ast.Attribute):
        if func.attr.startswith("get_sheet"):
            return func.attr
    elif isinstance(func, ast.Name):
        if func.id.startswith("get_sheet"):
            return func.id
    return None


class _TopLevelSheetCallVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.violations: list[tuple[int, str]] = []

    def visit_Call(self, node: ast.Call) -> None:  # noqa: N802
        call_name = _is_sheet_call(node.func)
        if call_name:
            self.violations.append((node.lineno, call_name))
        self.generic_visit(node)

    def _visit_function_signature(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef | ast.Lambda
    ) -> None:
        # Only inspect decorators/defaults; function body is not import-time execution.
        decorator_list = getattr(node, "decorator_list", [])
        for decorator in decorator_list:
            self.visit(decorator)
        for default in node.args.defaults:
            self.visit(default)
        for default in node.args.kw_defaults:
            if default is not None:
                self.visit(default)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
        self._visit_function_signature(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:  # noqa: N802
        self._visit_function_signature(node)

    def visit_Lambda(self, node: ast.Lambda) -> None:  # noqa: N802
        # Lambda body executes when invoked, not at import time.
        self._visit_function_signature(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802
        for decorator in node.decorator_list:
            self.visit(decorator)
        for base in node.bases:
            self.visit(base)
        for keyword in node.keywords:
            self.visit(keyword.value)
        for stmt in node.body:
            self.visit(stmt)


def collect_top_level_sheet_call_violations() -> list[TopLevelSheetCallViolation]:
    violations: list[TopLevelSheetCallViolation] = []

    for file_path in iter_top_level_scan_files(ROOT):
        try:
            tree = ast.parse(
                file_path.read_text(encoding="utf-8"), filename=str(file_path)
            )
        except SyntaxError:
            continue

        visitor = _TopLevelSheetCallVisitor()
        for stmt in tree.body:
            visitor.visit(stmt)

        for line, call_name in visitor.violations:
            violations.append(
                TopLevelSheetCallViolation(
                    file_path=file_path,
                    line=line,
                    call_name=call_name,
                )
            )

    return violations


def collect_python_violations() -> list[Violation]:
    violations: list[Violation] = []

    for file_path in iter_python_files(ROOT):
        importer_root = module_root_from_path(file_path)
        rel_path = file_path.relative_to(ROOT).as_posix()
        forbidden: tuple[str, ...] = ()
        if importer_root in BOUNDARIES:
            forbidden = (*forbidden, *BOUNDARIES[importer_root])
        for path_prefix, path_forbidden in PATH_SPECIFIC_BOUNDARIES.items():
            if rel_path.startswith(path_prefix):
                forbidden = (*forbidden, *path_forbidden)
        if not forbidden:
            continue

        try:
            tree = ast.parse(
                file_path.read_text(encoding="utf-8"), filename=str(file_path)
            )
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


def run_architecture_guardrails() -> int:
    command = [sys.executable, "-m", "pytest", "-q", ARCH_GUARDRAIL_TEST]
    print(f"Running architecture guardrails: {' '.join(command)}")
    result = subprocess.run(command, cwd=ROOT)
    return int(result.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check Python import boundaries and notebook import guardrails."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return non-zero if any violations are found.",
    )
    parser.add_argument(
        "--skip-guardrails",
        action="store_true",
        help=f"Skip pytest guardrails ({ARCH_GUARDRAIL_TEST}).",
    )
    args = parser.parse_args()

    if not args.skip_guardrails:
        guardrail_code = run_architecture_guardrails()
        if guardrail_code != 0:
            return guardrail_code

    python_violations = collect_python_violations()
    top_level_sheet_call_violations = collect_top_level_sheet_call_violations()
    notebook_violations = collect_notebook_violations()

    if python_violations:
        print(f"Found {len(python_violations)} import boundary violation(s):")
        for violation in sorted(
            python_violations, key=lambda v: (str(v.file_path), v.line)
        ):
            print(
                f"- {violation.file_path}:{violation.line} "
                f"[{violation.importer_root}] imports '{violation.imported}' "
                f"(forbidden prefix: {violation.forbidden_prefix})"
            )
    if notebook_violations:
        print(f"Found {len(notebook_violations)} notebook legacy import violation(s):")
        for violation in sorted(
            notebook_violations, key=lambda v: (str(v.file_path), v.cell_index, v.line)
        ):
            print(
                f"- {violation.file_path}:cell {violation.cell_index}:line {violation.line} "
                f"(forbidden import: {violation.forbidden_pattern})"
            )
    if top_level_sheet_call_violations:
        print(
            "Found "
            f"{len(top_level_sheet_call_violations)} import-time sheet-call violation(s):"
        )
        for violation in sorted(
            top_level_sheet_call_violations,
            key=lambda v: (str(v.file_path), v.line, v.call_name),
        ):
            print(
                f"- {violation.file_path}:{violation.line} "
                f"(top-level call: {violation.call_name})"
            )

    if (
        not python_violations
        and not notebook_violations
        and not top_level_sheet_call_violations
    ):
        print("No import boundary violations found.")

    if args.strict and (
        python_violations or notebook_violations or top_level_sheet_call_violations
    ):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
