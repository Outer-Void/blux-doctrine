"""Update the README file tree section."""
from __future__ import annotations

import re
from pathlib import Path

from gen_filetree import build_tree


MARKER_BEGIN = "<!-- FILETREE:BEGIN -->"
MARKER_END = "<!-- FILETREE:END -->"


def update_readme(readme_path: Path) -> None:
    content = readme_path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"{MARKER_BEGIN}.*?{MARKER_END}", re.DOTALL,
    )
    tree_lines = ["```text", *build_tree(Path.cwd()), "```"]
    replacement = (
        f"{MARKER_BEGIN}\n<!-- generated; do not edit manually -->\n"
        "<details><summary><strong>Repository File Tree</strong> (click to expand)</summary>\n\n"
        + "\n".join(tree_lines)
        + "\n\n</details>\n"
        + MARKER_END
    )
    updated = pattern.sub(replacement, content)
    readme_path.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    update_readme(Path("README.md"))
