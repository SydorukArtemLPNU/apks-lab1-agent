#!/usr/bin/env bash
# Run hello_app from sources inside the project virtual environment.
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -d .venv ]; then
    python3 -m venv .venv
fi

PYTHONPATH=src exec .venv/bin/python -m hello_app "$@"
