from __future__ import annotations

from blux_doctrine.adapters import guard
from blux_doctrine.schema import Outcome


def test_guard_adapter_returns_decision():
    decision = guard.check({"action": "read", "capabilities": ["security"]}, metadata={})
    assert decision.outcome == Outcome.allow
