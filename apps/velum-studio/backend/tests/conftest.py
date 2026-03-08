from __future__ import annotations

import sys
from pathlib import Path


def _ensure_path(path: Path) -> None:
    text = str(path)
    if text not in sys.path:
        sys.path.insert(0, text)


REPO_ROOT = Path(__file__).resolve().parents[4]
BACKEND_ROOT = Path(__file__).resolve().parents[1]

_ensure_path(REPO_ROOT)
_ensure_path(BACKEND_ROOT)
