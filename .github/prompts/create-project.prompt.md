---
agent: build-engineer
description: Create the initial Python Hello World project using the project-scaffold skill.
---

# Command: create-project

Arguments (optional): `${input:project_name:hello}`, `${input:package:hello_app}`.

## Preconditions

- `git-init` has completed (`.gitignore` exists).
- Python ≥ 3.10 is available (`python3 --version` / `python --version`).

## Actions

1. Read `.github/skills/project-scaffold/SKILL.md`.
2. Create every output file of the skill that does not exist yet. For
   existing files: compare with the skill requirements and change only what
   is missing or wrong.
3. Make `run.sh` executable (`chmod +x run.sh`; on Windows
   `git update-index --chmod=+x run.sh` after the file is tracked).
4. Add the "Project" section to `README.md` if it is not there yet.
5. Append an entry to `docs/ai-log.md`.

## Expected files

`src/hello_app/{__init__,core,__main__}.py`, `requirements.txt`, `run.sh`,
`run.bat`, `README.md` (section "Project").

## Verification

Run the commands from the "Verification" section of the skill and show their
output. Expected: `Hello, World!` and `Hello, Lab!`.

## Error messages

- `create-project: python not found` — install Python ≥ 3.10.
- `create-project: verification failed: <command>` — print the output and stop.
