"""Loader utilities for BLUX Doctrine bundles."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

import yaml

from .schema import DoctrineBundle, Pillar, Rule

DEFAULT_LOCATIONS = (
    Path(os.getenv("BLUX_DOCTRINE_HOME", "~/.config/blux-doctrine")).expanduser(),
    Path.cwd() / "doctrine",
)


class DoctrineLoader:
    """Load doctrine bundles from multiple sources."""

    def __init__(self, search_locations: Sequence[Path] | None = None):
        env_override = os.getenv("BLUX_DOCTRINE_PATH")
        if env_override:
            search_locations = [Path(env_override)]
        self.search_locations = list(search_locations or DEFAULT_LOCATIONS)

    def discover_files(self) -> List[Path]:
        """Return doctrine rule files found across search locations."""

        files: List[Path] = []
        for base in self.search_locations:
            rules_dir = base / "rules"
            if rules_dir.is_dir():
                for candidate in sorted(rules_dir.glob("*.yaml")):
                    files.append(candidate)
        return files

    def load(self) -> DoctrineBundle:
        """Load, merge, and validate doctrine files."""

        pillars: Dict[str, Pillar] = {}
        rules: Dict[str, Rule] = {}

        for location in self.search_locations:
            pillar_dir = location / "pillars"
            if pillar_dir.is_dir():
                for md_file in pillar_dir.glob("*.md"):
                    pillar_id = md_file.stem
                    content = md_file.read_text(encoding="utf-8")
                    lines = content.strip().splitlines()
                    title = lines[0].lstrip("# ") if lines else pillar_id.title()
                    description = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""
                    pillars[pillar_id] = Pillar(
                        id=pillar_id,
                        title=title,
                        description=description or "Pillar description unavailable.",
                    )

        for file in self.discover_files():
            with file.open("r", encoding="utf-8") as handle:
                data = yaml.safe_load(handle) or {}
            if isinstance(data, dict):
                for rule_data in data.get("rules", []):
                    rule = Rule.model_validate(rule_data)
                    rules[rule.id] = rule
            elif isinstance(data, list):
                for rule_data in data:
                    rule = Rule.model_validate(rule_data)
                    rules[rule.id] = rule

        bundle = DoctrineBundle(pillars=list(pillars.values()), rules=list(rules.values()))
        return bundle

    def export(self, destination: Path) -> None:
        """Export the merged doctrine bundle to JSON."""

        bundle = self.load()
        destination.write_text(
            json.dumps(bundle.model_dump(mode="json"), indent=2),
            encoding="utf-8",
        )


def load_default_bundle() -> DoctrineBundle:
    """Convenience helper for loading the default doctrine bundle."""

    loader = DoctrineLoader()
    return loader.load()
