#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LINT_TARGETS = [
    "scripts/check_import_boundaries.py",
    "scripts/run_quality_matrix.py",
    "FiveETools/cli.py",
    "FiveETools/datasets",
    "FiveETools/services",
    "FiveETools/exports",
    "Book/cli.py",
    "Book/datasets",
    "Book/services",
    "Book/exports",
    "Book/mappers",
]

TYPE_TARGETS = [
    "scripts/check_import_boundaries.py",
    "scripts/run_quality_matrix.py",
    "FiveETools/cli.py",
    "FiveETools/datasets",
    "FiveETools/services",
    "FiveETools/exports",
    "Book/cli.py",
    "Book/datasets",
    "Book/services",
    "Book/exports",
    "Book/mappers",
]

TEST_COMMANDS = [
    [sys.executable, "scripts/check_import_boundaries.py", "--strict"],
    [sys.executable, "-m", "pytest", "-q", "scripts/tests/test_check_import_boundaries.py"],
    [sys.executable, "-m", "pytest", "-q", "Book/tests/test_formatters.py"],
]

STAGE_COMMANDS = {
    "lint": [
        [
            sys.executable,
            "-m",
            "ruff",
            "check",
            *LINT_TARGETS,
            "--config",
            "Book/ruff.toml",
        ]
    ],
    "type": [
        [
            sys.executable,
            "-m",
            "pyright",
            *TYPE_TARGETS,
        ]
    ],
    "test": TEST_COMMANDS,
}


def _run(command: list[str]) -> int:
    print(f"$ {' '.join(command)}")
    completed = subprocess.run(command, cwd=ROOT)
    return int(completed.returncode)


def run_stage(stage: str) -> int:
    for command in STAGE_COMMANDS[stage]:
        code = _run(command)
        if code != 0:
            return code
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run root quality matrix checks.")
    parser.add_argument(
        "--stage",
        choices=["lint", "type", "test", "all"],
        required=True,
        help="Quality stage to run.",
    )
    args = parser.parse_args()

    if args.stage == "all":
        for stage in ("lint", "type", "test"):
            code = run_stage(stage)
            if code != 0:
                return code
        return 0

    return run_stage(args.stage)


if __name__ == "__main__":
    raise SystemExit(main())
