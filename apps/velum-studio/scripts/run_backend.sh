#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT_DIR"

poetry run uvicorn app.main:app --host "${VELUM_HOST:-127.0.0.1}" --port "${VELUM_PORT:-8765}" --app-dir apps/velum-studio/backend
