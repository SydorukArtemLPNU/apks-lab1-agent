---
name: github-actions
description: Create .github/workflows/ci.yml with one matrix job for Windows, Linux and macOS that only calls ci.sh / ci.bat and uploads the built executable and test report. Use when the create-actions command runs or the workflow is missing.
---

# Skill: github-actions

## When to use

- The `create-actions` command is running.
- `.github/workflows/ci.yml` is missing or does not cover all three OSes.

## Prerequisites

`ci.sh` and `ci.bat` exist (skill `build-and-test`). If not — stop with
`github-actions: run create-build first`.

## Inputs

| Input            | Default                    |
|------------------|----------------------------|
| `branches`       | `develop`, `master`        |
| `python_version` | `3.12`                     |
| `executable`     | `hello`                    |

## Output

`.github/workflows/ci.yml` with:

- `name: CI`
- triggers: `push` and `pull_request` for the given branches, plus
  `workflow_dispatch`;
- `permissions: contents: read` (least privilege, no secrets used);
- **one** job `build-test` with
  `strategy.fail-fast: false` and
  `matrix.os: [ubuntu-latest, windows-latest, macos-latest]`;
- `runs-on: ${{ matrix.os }}`, `name: build-test (${{ matrix.os }})`;
- steps:
  1. `actions/checkout@v4`;
  2. `actions/setup-python@v5` with `python-version`;
  3. **build and test** — only calls the script:
     - `./ci.sh` with `shell: bash` and `if: runner.os != 'Windows'`;
     - `ci.bat` with `shell: cmd` and `if: runner.os == 'Windows'`;
  4. `actions/upload-artifact@v4` (`if: always()`) named
     `hello-${{ matrix.os }}` with `dist/` and `reports/junit.xml`.

The workflow must **not** contain build or test commands itself
(no `pip install`, `pytest`, `pyinstaller` lines) — all of that lives in
the CI scripts so local and CI runs are identical.

## Verification

```bash
python -c "import yaml,sys; d=yaml.safe_load(open('.github/workflows/ci.yml')); print(d['jobs']['build-test']['strategy']['matrix']['os'])"
# -> ['ubuntu-latest', 'windows-latest', 'macos-latest']
grep -nE 'pytest|pyinstaller|pip install' .github/workflows/ci.yml   # -> nothing
```

After pushing: open the **Actions** tab and confirm three green jobs.

## Example

Input: `branches=develop,master python_version=3.12`
Expected result: the workflow above; on push to `develop` three jobs run,
each uploads `hello-<os>` artifact containing `hello`/`hello.exe`.

## Typical failure

`./ci.sh: Permission denied` on Linux/macOS runners — the executable bit was
lost (e.g. the file was created on Windows). Fix:
`git update-index --chmod=+x ci.sh run.sh` and commit; do **not** add
`chmod` calls or build commands to the workflow.
