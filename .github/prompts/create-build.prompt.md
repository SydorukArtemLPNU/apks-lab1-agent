---
agent: build-engineer
description: Create the build system (venv + ci scripts + PyInstaller) and pytest tests using the build-and-test skill.
---

# Command: create-build

## Preconditions

- `src/hello_app/core.py` exists (run `create-project` first).

## Actions

1. Read `.github/skills/build-and-test/SKILL.md`.
2. Sub-step **tests**: create `pytest.ini`, `tests/test_core.py`
   (with `test_BasicAddition`), `tests/test_main.py` if missing.
3. Sub-step **build**: create `requirements-dev.txt`, `ci.sh`, `ci.bat` if
   missing; make `ci.sh` executable.
4. Run `./ci.sh` (Linux/macOS) or `ci.bat` (Windows) and show the tail of the
   output.
5. Append an entry to `docs/ai-log.md`.

## Expected files

`requirements-dev.txt`, `pytest.ini`, `tests/test_core.py`,
`tests/test_main.py`, `ci.sh`, `ci.bat`; after the run (ignored by Git):
`.venv/`, `build/`, `dist/hello`, `reports/junit.xml`.

## Verification

```bash
./ci.sh | tail -n 5                 # -> "==> CI OK"
./dist/hello                        # -> Hello, World!
git check-ignore build dist .venv   # -> all three printed
```

## Error messages

- `create-build: run create-project first`
- `create-build: tests failed` — show the pytest output, do not change tests
  to make them pass; fix the code or ask the user.
- `create-build: executable not produced` — show PyInstaller output.
