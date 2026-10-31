---
name: project-scaffold
description: Create a minimal Python "Hello World" project skeleton (src package, entry point, README section, .gitignore). Use when the repository has no application source yet or when the create-project command runs.
---

# Skill: project-scaffold

## When to use

- The `create-project` command is running.
- `src/<package>/` does not exist or misses the entry point.

## Inputs

| Input          | Default      | Example        |
|----------------|--------------|----------------|
| `language`     | `python`     | `python`       |
| `project_name` | `hello`      | `hello`        |
| `package`      | `hello_app`  | `hello_app`    |

Only `python` is supported by this skill. For any other language stop and
report: `project-scaffold: unsupported language '<language>'`.

## Outputs

```
src/hello_app/__init__.py     # __version__ = "1.0.0"
src/hello_app/core.py         # pure functions: greet(name="World"), add(a, b)
src/hello_app/__main__.py     # main(argv) -> int; prints greet(); entry point
requirements.txt              # runtime deps (empty, comment only)
run.sh, run.bat               # create .venv if missing and run `python -m hello_app`
.gitignore                    # see list below
README.md                     # section "Project" with run instructions (add, do not duplicate)
```

### Code requirements

- `core.greet(name: str = "World") -> str` returns `"Hello, <name>!"`.
- `core.add(a: int, b: int) -> int` returns `a + b` (used by the unit test).
- `__main__.main(argv=None) -> int`: accepts an optional `--name NAME`
  argument (argparse), prints `greet(name)`, returns `0`.
- `if __name__ == "__main__": raise SystemExit(main())`.
- Only the standard library; type hints; no global side effects on import.

### Run scripts

- `run.sh` (bash, `set -euo pipefail`, executable bit `chmod +x`) and
  `run.bat` (`@echo off`, `setlocal`) must:
  1. `cd` to the script directory;
  2. create `.venv` with `python3 -m venv .venv` (`py -3 -m venv .venv` /
     `python -m venv .venv` on Windows) only if it does not exist;
  3. run `PYTHONPATH=src .venv/bin/python -m hello_app "$@"`
     (`.venv\Scripts\python.exe` on Windows), forwarding all arguments.

### .gitignore entries (each exactly once)

```
.venv/
build/
dist/
reports/
__pycache__/
*.py[cod]
*.spec
.pytest_cache/
.DS_Store
.vscode/
.env
```

## Verification

```bash
test -f src/hello_app/__main__.py && test -f src/hello_app/core.py
PYTHONPATH=src python3 -m hello_app            # -> Hello, World!
PYTHONPATH=src python3 -m hello_app --name Lab # -> Hello, Lab!
./run.sh                                        # -> Hello, World!
grep -c '^build/$' .gitignore                   # -> 1
```

## Example

Input: `language=python project_name=hello package=hello_app`
Expected result: the files above; `./run.sh` prints `Hello, World!`.

## Typical failure

`ModuleNotFoundError: No module named 'hello_app'` when running
`python -m hello_app` — `src` is not on `PYTHONPATH`. Fix: run through
`run.sh`/`run.bat` or set `PYTHONPATH=src`; do **not** move the package out of
`src/`.
