"""Minimal DSL compiler that proxies to YAML."""
from __future__ import annotations

import yaml


def compile_text(text: str) -> str:
    """Return YAML string compiled from DSL text.

    The enterprise DSL is a superset of YAML, so we validate and re-emit the
    structure to guarantee consistent formatting.
    """

    data = yaml.safe_load(text)
    return yaml.safe_dump(data, sort_keys=False)


def compile_file(path: str, destination: str | None = None) -> str:
    with open(path, "r", encoding="utf-8") as handle:
        result = compile_text(handle.read())
    if destination:
        with open(destination, "w", encoding="utf-8") as handle:
            handle.write(result)
    return result
