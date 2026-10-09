#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="$ROOT/.venv/bin/python"

if [[ ! -x "$PYTHON" ]]; then
    echo "ERROR: Virtual environment not found at $ROOT/.venv"
    echo "Create it with: python3 -m venv .venv"
    exit 1
fi

cd "$ROOT"
export PYTHONPATH="$ROOT/backend${PYTHONPATH:+:$PYTHONPATH}"

echo "Python interpreter: $("$PYTHON" -c 'import sys; print(sys.executable)')"
echo "Running unit tests..."

"$PYTHON" -m unittest discover -s backend/tests -v

echo "All tests passed."
