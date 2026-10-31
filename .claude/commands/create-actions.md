---
description: Create the cross-platform GitHub Actions workflow using the github-actions skill.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash(python3:*), Bash(python:*), Bash(.venv/bin/python:*), Bash(grep:*)
argument-hint: [branches=develop,master] [python_version=3.12]
---

# Command: create-actions

Act as the **build-engineer** agent and follow every rule of its manifest:
@.claude/agents/build-engineer.md

## Preconditions

- `ci.sh` and `ci.bat` exist (run `create-build` first).

## Actions

1. Read `.claude/skills/github-actions/SKILL.md`.
2. Create `.github/workflows/ci.yml` if missing. If it exists, make sure it
   matches the skill (one job, three OSes, only script calls) and fix only the
   differences — never add a second job or duplicate steps.
3. Append an entry to `docs/ai-log.md`.

## Expected files

`.github/workflows/ci.yml`

## Verification

Run the commands from the "Verification" section of the skill. Expected:
the matrix list of three OSes and no build commands inside the workflow.

## Error messages

- `create-actions: run create-build first`
- `create-actions: invalid YAML: <error>`

Do not push. Pushing and checking the Actions tab is done by the user.
