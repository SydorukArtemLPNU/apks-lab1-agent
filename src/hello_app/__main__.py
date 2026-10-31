"""Entry point: ``python -m hello_app [--name NAME]`` and the PyInstaller executable."""
from __future__ import annotations

import argparse
from typing import Sequence

# Absolute import: PyInstaller runs this file as a top-level script.
from hello_app.core import greet


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="hello", description="Print a greeting.")
    parser.add_argument("--name", default="World", help="who to greet (default: World)")
    args = parser.parse_args(argv)
    print(greet(args.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
