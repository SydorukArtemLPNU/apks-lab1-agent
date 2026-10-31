---
description: Orchestrator — runs git-init, create-project, create-build, create-actions and check in order, stopping on the first error.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash(git rev-parse:*), Bash(git init:*), Bash(git status:*), Bash(git branch:*), Bash(git --version), Bash(grep:*), Bash(for e in:*), Bash(python3:*), Bash(python:*), Bash(PYTHONPATH=src python3:*), Bash(chmod +x:*), Bash(./run.sh:*), Bash(test:*), Bash(./ci.sh:*), Bash(./dist/hello:*), Bash(git check-ignore:*), Bash(.venv/bin/python:*), Bash(python3 tools/check.py:*), Bash(python tools/check.py:*), Bash(.venv/bin/python tools/check.py:*)
---

# Command: init-project (orchestrator)

Act as the **build-engineer** agent and follow every rule of its manifest:
@.claude/agents/build-engineer.md

Runs the full scenario. Safe to run again on an existing project: every
command is idempotent and only adds what is missing.

## Preconditions

- Repository root with `.claude/agents/build-engineer.md`.
- `git` and Python ≥ 3.10 installed. If not — stop with
  `init-project: missing prerequisite <tool>`.

## Steps

Execute the commands **in this exact order**. For each step: read its command
file, perform it, run its verification, and print
`[init-project] step N/5 <command>: OK` or `[init-project] step N/5 <command>: FAILED`.

| # | Command          | Command file                                 | Passes to next step |
|---|------------------|----------------------------------------------|---------------------|
| 1 | `git-init`       | `.claude/commands/git-init.md`         | repo + `.gitignore` |
| 2 | `create-project` | `.claude/commands/create-project.md`   | `src/hello_app`, run scripts |
| 3 | `create-build`   | `.claude/commands/create-build.md`     | `ci.sh`/`ci.bat`, tests, `dist/hello` |
| 4 | `create-actions` | `.claude/commands/create-actions.md`   | `.github/workflows/ci.yml` |
| 5 | `check`          | `.claude/commands/check.md`            | final report |

## Error handling

- If a step fails, **stop immediately**, do not run the following steps,
  print the failing step, the command output and a suggested fix.
- Never mark the run successful unless step 5 (`check`) exits with code 0.

## Final report

Print a table: step, status, created/changed files. Then list the next manual
actions for the user: review the diff, commit (agent / project / CI as
separate commits), push the `feature/...` branch, open a PR to `develop`.
Append a summary entry to `docs/ai-log.md`.
