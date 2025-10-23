"""Generate repository file tree for documentation."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Iterable, List


EXCLUDE = {".git", "__pycache__", "logs", ".pytest_cache"}


def build_tree(root: Path) -> List[str]:
    lines: List[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_path = Path(dirpath).relative_to(root)
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE]
        filenames = [f for f in filenames if not f.endswith(".pyc")]
        indent = "    " * (len(rel_path.parts))
        if rel_path != Path("."):
            lines.append(f"{indent}{rel_path.name}/")
            indent += "    "
        for name in sorted(filenames):
            lines.append(f"{indent}{name}")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?", default=Path.cwd())
    args = parser.parse_args()
    for line in build_tree(args.root):
        print(line)


if __name__ == "__main__":
    main()
