"""Compile DSL doctrine files into YAML."""
from __future__ import annotations

import argparse
from pathlib import Path

from blux_doctrine.dsl.parser import compile_file


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path, nargs="?")
    args = parser.parse_args()
    compile_file(str(args.source), str(args.destination) if args.destination else None)


if __name__ == "__main__":
    main()
