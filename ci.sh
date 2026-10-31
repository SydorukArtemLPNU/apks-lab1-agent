#!/usr/bin/env bash
# Build + test script for Linux/macOS (used locally and in GitHub Actions).
set -euo pipefail

echo "==> step: cd to project root"
cd "$(dirname "$0")"

echo "==> step: select interpreter"
if [ -n "${PYTHON:-}" ]; then
    PY="$PYTHON"
elif command -v python3 >/dev/null 2>&1; then
    PY=python3
else
    PY=python
fi
"$PY" --version

echo "==> step: create virtual environment"
if [ ! -x .venv/bin/python ]; then
    "$PY" -m venv .venv
fi
VPY=.venv/bin/python

echo "==> step: install dependencies"
"$VPY" -m pip install --upgrade pip
"$VPY" -m pip install -r requirements-dev.txt

echo "==> step: run tests"
mkdir -p reports
"$VPY" -m pytest -v --junitxml=reports/junit.xml

echo "==> step: build executable"
rm -rf dist
"$VPY" -m PyInstaller --noconfirm --onefile --name hello --paths src \
    --distpath dist --workpath build --specpath build src/hello_app/__main__.py

echo "==> step: smoke test"
OUT="$(./dist/hello)"
echo "$OUT"
case "$OUT" in
    *"Hello, World!"*) ;;
    *) echo "smoke test failed: unexpected output" >&2; exit 1 ;;
esac

echo "==> CI OK"
