"""Safety guard checks."""
from __future__ import annotations

from ..schema import Decision, Outcome, Rule
from ._base import build_partial


UNSAFE_TAGS = {"exploit", "malware", "biohazard"}


def evaluate(context, rule: Rule) -> Decision:
    tags = set(context.request.get("tags", []))
    if tags.intersection(UNSAFE_TAGS):
        return build_partial(
            outcome=Outcome.deny,
            score=max(rule.decision.score, 1.0),
            reasons=["Detected unsafe intent tags in request"],
            remediations=["Escalate to human reviewer"],
        )
    return build_partial()
