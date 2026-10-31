---
agent: build-engineer
description: Check the Git repository, create or update .gitignore, show Git state.
---

# Command: git-init

## Preconditions

- Current directory is the repository root (contains `.github/agents/`).
- `git` is installed (`git --version`).

## Actions

1. Run `git rev-parse --is-inside-work-tree`. If it fails, run
   `git init -b master` (never re-initialise an existing repository).
2. Ensure `.gitignore` contains every entry from the list in
   `.github/skills/project-scaffold/SKILL.md` (section ".gitignore entries").
   Add only missing lines; never duplicate existing ones.
3. Show `git status --short --branch` and `git branch --list`.

## Expected files

- `.gitignore` (created or updated).

## Verification

```bash
git rev-parse --is-inside-work-tree            # -> true
for e in .venv/ build/ dist/ reports/; do grep -qx "$e" .gitignore || echo "missing $e"; done   # -> nothing
```

## Error messages

- `git-init: git is not installed` — install Git and retry.
- `git-init: not in repository root` — `.github/agents/` not found.

Do not commit, push, delete branches or change remotes.
