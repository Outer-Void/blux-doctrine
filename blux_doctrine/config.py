"""Configuration helpers for BLUX Doctrine."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

import yaml

DEFAULT_CONFIG_LOCATIONS = (
    Path("~/.config/blux-doctrine/config.yaml").expanduser(),
    Path.cwd() / "doctrine" / "config.yaml",
)


def load_config(extra_path: str | None = None) -> Dict[str, Any]:
    """Load configuration from environment, JSON/YAML files."""

    data: Dict[str, Any] = {}
    for location in DEFAULT_CONFIG_LOCATIONS:
        if location.is_file():
            data.update(_load_file(location))

    if extra_path:
        path = Path(extra_path)
        if path.is_file():
            data.update(_load_file(path))

    for key, value in os.environ.items():
        if key.startswith("BLUX_DOCTRINE_CFG_"):
            data[key.removeprefix("BLUX_DOCTRINE_CFG_").lower()] = value
    return data


def _load_file(path: Path) -> Dict[str, Any]:
    if path.suffix in {".json", ".jsonl"}:
        return json.loads(path.read_text(encoding="utf-8"))
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
