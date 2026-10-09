#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="$ROOT/.venv/bin/python"

cd "$ROOT"

echo "Checking Python syntax..."
"$PYTHON" -m compileall -q backend

echo "Checking Git whitespace errors..."
git diff --check

echo "Running unit tests..."
./scripts/test.sh

echo "All checks passed."
