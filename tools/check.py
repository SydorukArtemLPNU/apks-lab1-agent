#!/usr/bin/env python3
"""Read-only verification used by the `check` command of the build-engineer agent.

Usage:
    python3 tools/check.py            # all checks, including build + tests
    python3 tools/check.py --static   # skip running ci.sh / ci.bat

Exit code 0 — every check passed, 1 — at least one check failed.
The script never modifies tracked files; the build step writes only to the
ignored directories .venv/, build/, dist/, reports/.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IS_WINDOWS = os.name == "nt"
OSES = ["ubuntu-latest", "windows-latest", "macos-latest"]
COMMANDS = ["git-init", "create-project", "create-build", "create-actions", "check", "init"]
INIT_ORDER = COMMANDS[:5]
SKILLS = ["project-scaffold", "build-and-test", "github-actions"]
GITIGNORE = [".venv/", "build/", "dist/", "reports/", "__pycache__/", "*.spec"]
PROJECT_FILES = [
    "src/hello_app/__init__.py",
    "src/hello_app/core.py",
    "src/hello_app/__main__.py",
    "tests/test_core.py",
    "tests/test_main.py",
    "requirements.txt",
    "requirements-dev.txt",
    "pytest.ini",
    "ci.sh",
    "ci.bat",
    "run.sh",
    "run.bat",
    "README.md",
    "docs/architecture.md",
    "docs/usage.md",
    "docs/ai-log.md",
]
FORBIDDEN_TRACKED = ("build/", "dist/", ".venv/", "reports/", "__pycache__/")
SECRET_PATTERNS = [
    re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{40,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]
WORKFLOW_FORBIDDEN = re.compile(r"\b(pip install|pytest|pyinstaller|PyInstaller)\b")

results: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> bool:
    results.append((name, ok, detail))
    return ok


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=False
    ).stdout


def has_sections(text: str, sections: list[str]) -> list[str]:
    return [s for s in sections if not re.search(rf"^#+ .*{re.escape(s)}", text, re.M | re.I)]


# --------------------------------------------------------------------------- agent
def check_manifest() -> None:
    rel = ".github/agents/build-engineer.agent.md"
    if not record("agent: manifest exists", (ROOT / rel).is_file(), rel):
        return
    text = read(rel)
    missing = has_sections(text, ["Role", "Area of responsibility", "Forbidden actions", "Definition of done"])
    record("agent: role, limits, done criteria", not missing, ", ".join(missing))


def check_skills() -> None:
    for skill in SKILLS:
        rel = f".github/skills/{skill}/SKILL.md"
        if not record(f"skill: {skill} exists", (ROOT / rel).is_file(), rel):
            continue
        text = read(rel)
        missing = has_sections(text, ["When to use", "Input", "Output", "Verification", "Example", "Typical failure"])
        if not text.startswith("---") or f"name: {skill}" not in text:
            missing.append("frontmatter")
        record(f"skill: {skill} complete", not missing, ", ".join(missing))


def check_commands() -> None:
    for cmd in COMMANDS:
        rel = f".github/prompts/{cmd}.prompt.md"
        ok = (ROOT / rel).is_file() and "description:" in read(rel)
        record(f"command: {cmd}", ok, rel)
    init = ROOT / ".github/prompts/init.prompt.md"
    if init.is_file():
        steps = re.findall(r"^\|\s*\d\s*\|\s*`([a-z-]+)`", init.read_text(encoding="utf-8"), re.M)
        record("command: init order", steps == INIT_ORDER, " -> ".join(steps))


# --------------------------------------------------------------------------- project
def check_project_files() -> None:
    missing = [f for f in PROJECT_FILES if not (ROOT / f).is_file()]
    record("project: required files", not missing, ", ".join(missing))
    test_core = ROOT / "tests/test_core.py"
    record(
        "project: test_BasicAddition defined",
        test_core.is_file() and "def test_BasicAddition" in test_core.read_text(encoding="utf-8"),
    )
    for script in ("ci.sh", "run.sh"):
        mode = git("ls-files", "-s", script).split(" ")[0]
        ok = mode == "100755" if mode else os.access(ROOT / script, os.X_OK)
        record(f"project: {script} executable", ok, mode or "untracked")


def check_git() -> None:
    gi = ROOT / ".gitignore"
    lines = gi.read_text(encoding="utf-8").splitlines() if gi.is_file() else []
    missing = [e for e in GITIGNORE if e not in lines]
    dupes = sorted({line for line in lines if line and lines.count(line) > 1})
    record("git: .gitignore entries", not missing and not dupes,
           ", ".join(missing + [f"duplicate {d}" for d in dupes]))

    tracked = git("ls-files").splitlines()
    bad = [f for f in tracked if any(f.startswith(p) or f"/{p}" in f for p in FORBIDDEN_TRACKED)]
    record("git: no build dirs tracked", not bad, ", ".join(bad[:5]))

    leaks = []
    for f in tracked:
        path = ROOT / f
        if not path.is_file() or path.stat().st_size > 1_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if any(p.search(text) for p in SECRET_PATTERNS):
            leaks.append(f)
    leaks += [f for f in tracked if Path(f).name in (".env", "id_rsa", "id_ed25519")]
    record("git: no secrets tracked", not leaks, ", ".join(leaks))


def check_workflow() -> None:
    rel = ".github/workflows/ci.yml"
    if not record("workflow: ci.yml exists", (ROOT / rel).is_file(), rel):
        return
    text = read(rel)
    try:
        import yaml  # type: ignore
    except ImportError:
        record("workflow: YAML parsed", False, "pyyaml not installed (run ci.sh first or pip install pyyaml)")
        return
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        record("workflow: YAML parsed", False, str(exc).splitlines()[0])
        return
    record("workflow: YAML parsed", True)

    triggers = data.get("on", data.get(True, {})) or {}  # PyYAML parses `on:` as True
    branch_ok = all(
        set((triggers.get(ev) or {}).get("branches", [])) >= {"develop", "master"}
        for ev in ("push", "pull_request")
    )
    record("workflow: push + pull_request to develop/master", branch_ok)

    jobs = data.get("jobs", {})
    record("workflow: exactly one job", len(jobs) == 1, ", ".join(jobs))
    job = next(iter(jobs.values()), {})
    oses = (job.get("strategy", {}).get("matrix", {}) or {}).get("os", [])
    record("workflow: matrix Windows/Linux/macOS", sorted(oses) == sorted(OSES), str(oses))

    runs = [step.get("run", "") for step in job.get("steps", [])]
    record("workflow: calls ci.sh and ci.bat",
           any("ci.sh" in r for r in runs) and any("ci.bat" in r for r in runs))
    inline = [r.strip() for r in runs if WORKFLOW_FORBIDDEN.search(r)]
    record("workflow: no inline build/test commands", not inline, "; ".join(inline))


# --------------------------------------------------------------------------- build
def check_build() -> None:
    script = ["cmd", "/c", "ci.bat"] if IS_WINDOWS else ["bash", "ci.sh"]
    if not (ROOT / script[-1]).is_file():
        record("build: ci script runs", False, f"{script[-1]} missing")
        return
    proc = subprocess.run(script, cwd=ROOT, capture_output=True, text=True, check=False)
    out = proc.stdout + proc.stderr
    tail = " | ".join(out.strip().splitlines()[-3:])
    record("build: ci script exit code 0", proc.returncode == 0, f"exit {proc.returncode}: {tail}")
    record("build: test_BasicAddition passed", re.search(r"test_BasicAddition PASSED", out) is not None)
    exe = ROOT / "dist" / ("hello.exe" if IS_WINDOWS else "hello")
    record("build: executable dist/hello", exe.is_file(), str(exe.relative_to(ROOT)))
    record("build: smoke test", "==> CI OK" in out)
    ignored = git("check-ignore", "build", "dist", ".venv").split()
    record("build: outputs ignored by git", set(ignored) >= {"build", "dist", ".venv"}, " ".join(ignored))


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only verification for the build-engineer agent.")
    parser.add_argument("--static", action="store_true", help="skip running the build")
    args = parser.parse_args()

    before = git("status", "--porcelain")
    check_manifest()
    check_skills()
    check_commands()
    check_project_files()
    check_git()
    check_workflow()
    if not args.static:
        check_build()
    record("check: tracked files unchanged", git("status", "--porcelain") == before)

    width = max(len(name) for name, _, _ in results)
    for name, ok, detail in results:
        line = f"{'PASS' if ok else 'FAIL'}  {name.ljust(width)}"
        print(f"{line}  {detail}".rstrip() if detail and not ok else line)
    failed = [name for name, ok, _ in results if not ok]
    print("-" * (width + 6))
    if failed:
        print(f"check: {len(failed)} check(s) failed")
        return 1
    print(f"check: all {len(results)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
