"""Utilities for check modules."""
from __future__ import annotations

from typing import Iterable, List

from ..schema import Decision, Outcome


def build_partial(
    outcome: Outcome = Outcome.allow,
    score: float = 0.0,
    reasons: Iterable[str] | None = None,
    remediations: Iterable[str] | None = None,
) -> Decision:
    return Decision(
        outcome=outcome,
        score=score,
        reasons=list(reasons or []),
        remediations=list(remediations or []),
    )
