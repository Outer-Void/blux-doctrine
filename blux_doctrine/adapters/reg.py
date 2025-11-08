"""Capability registry mappings."""
from __future__ import annotations

from typing import Dict, List

CAPABILITY_MAP: Dict[str, List[str]] = {
    "security": ["shell.exec", "code.deploy"],
    "privacy": ["user.export", "analytics.query"],
    "safety": ["agent.run"],
}


def resolve(action: str) -> List[str]:
    """Return the capabilities required for a given action."""

    return [cap for cap, actions in CAPABILITY_MAP.items() if action in actions]
