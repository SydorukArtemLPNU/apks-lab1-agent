---
description: Read-only verification of structure, agent files, configuration, build, tests and workflow YAML.
allowed-tools: Read, Glob, Grep, Bash(python3 tools/check.py:*), Bash(python tools/check.py:*), Bash(.venv/bin/python tools/check.py:*)
argument-hint: [--static]
---

# Command: check

Act as the **build-engineer** agent and follow every rule of its manifest:
@.claude/agents/build-engineer.md

**This command must not create, modify or delete tracked files.**
(Build outputs in ignored `build/`, `dist/`, `.venv/`, `reports/` are allowed.)

## Preconditions

- Python ≥ 3.10 available.

## Actions

1. Run `python3 tools/check.py` (`python tools\check.py` on Windows). The
   script checks:
   - agent manifest (role, forbidden actions, definition of done);
   - three skills with "When to use", inputs, outputs, verification, failure;
   - six commands, `init-project` calls the others in the right order;
   - project files, `.gitignore`, no tracked build dirs or secrets;
   - workflow YAML: one job, matrix with three OSes, only script calls;
   - runs `ci.sh` / `ci.bat` and requires `==> CI OK`, `dist/hello` and a
     passing `test_BasicAddition`.
2. Show the summary table printed by the script.
3. If any check is `FAIL` — explain the cause and which command/skill should
   fix it. Do **not** fix anything inside `check`.

If `$ARGUMENTS` is `--static`, run `python3 tools/check.py --static` to skip the build (fast mode).

## Verification

Exit code of `tools/check.py`: `0` — all checks passed, `1` — failures.

## Error messages

- `check: N check(s) failed` followed by the list of failed checks.
