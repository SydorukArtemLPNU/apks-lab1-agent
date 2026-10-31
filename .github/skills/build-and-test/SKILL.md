---
name: build-and-test
description: Create the build system (venv + ci.sh/ci.bat + PyInstaller) and pytest unit tests for the hello_app project, producing the executable `hello`. Use when the create-build command runs or the build/tests are missing or broken.
---

# Skill: build-and-test

## When to use

- The `create-build` command is running.
- `ci.sh`, `ci.bat`, `pytest.ini` or `tests/` are missing.

## Prerequisites

`project-scaffold` has been applied (`src/hello_app/core.py` exists).
If not — stop with `build-and-test: run create-project first`.

## Inputs

| Input        | Default     |
|--------------|-------------|
| `package`    | `hello_app` |
| `executable` | `hello`     |

## Outputs

```
requirements-dev.txt   # pytest>=8, pyinstaller>=6.10, pyyaml>=6
pytest.ini             # [pytest] pythonpath = src, testpaths = tests
tests/test_core.py     # test_BasicAddition + greet tests
tests/test_main.py     # main() prints greeting and returns 0
ci.sh                  # Linux/macOS build script
ci.bat                 # Windows build script
```

### Tests (sub-step "tests")

- `tests/test_core.py` must contain **`test_BasicAddition`** that checks
  `add(2, 3) == 5`, `add(-1, 1) == 0`, `add(0, 0) == 0`.
- Also `test_greet_default` (`Hello, World!`) and `test_greet_name`.
- `tests/test_main.py`: `main([])` returns `0` and prints `Hello, World!`
  (use `capsys`); `main(["--name", "CI"])` prints `Hello, CI!`.

### Build scripts (sub-step "build")

`ci.sh` (bash, `set -euo pipefail`, `chmod +x`) and `ci.bat` (`@echo off`,
`setlocal`, exits with `exit /b 1` on any error) perform the same steps,
printing a `==> step` header before each one:

1. `cd` to the script directory.
2. Pick the interpreter: `$PYTHON` env var, else `python3`, else `python`.
3. Create `.venv` if it does not exist.
4. `pip install --upgrade pip` and `pip install -r requirements-dev.txt`
   inside `.venv`.
5. Run tests: `python -m pytest -v --junitxml=reports/junit.xml`.
6. Remove the previous `dist/` (so a stale binary can never pass the
   checks) and build the executable:
   `python -m PyInstaller --onefile --name hello --paths src --distpath dist --workpath build --specpath build src/hello_app/__main__.py`.
7. Smoke test: run `dist/hello` (`dist\hello.exe`) and check the output
   contains `Hello, World!`.
8. Print `==> CI OK`.

Scripts must be re-runnable: an existing `.venv` is reused, PyInstaller
overwrites `dist/hello` (`--noconfirm`).

## Verification

```bash
./ci.sh                                   # ends with "==> CI OK"
test -x dist/hello && ./dist/hello        # -> Hello, World!
grep -q 'test_BasicAddition PASSED' <(.venv/bin/python -m pytest -v)
git check-ignore -q build dist .venv      # exit code 0
```

## Example

Input: `package=hello_app executable=hello`
Expected result: `./ci.sh` prints `5 passed`, builds `dist/hello` and ends
with `==> CI OK`.

## Typical failure

PyInstaller-built binary fails with
`ImportError: attempted relative import with no known parent package` —
`__main__.py` used `from .core import greet`. A PyInstaller entry script runs
as a top-level module, so `__main__.py` must use the absolute import
`from hello_app.core import greet` and PyInstaller must get `--paths src`.
