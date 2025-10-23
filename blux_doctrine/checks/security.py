"""Security rule evaluation."""
from __future__ import annotations

from typing import Sequence

from ..schema import Decision, Outcome, Rule
from ._base import build_partial


SENSITIVE_ACTIONS = {"shell.exec", "code.deploy", "network.open"}


def evaluate(context, rule: Rule) -> Decision:
    request = context.request
    action = request.get("action")
    if action in SENSITIVE_ACTIONS and "security" not in context.capabilities:
        return build_partial(
            outcome=Outcome.review,
            score=max(rule.decision.score, 0.7),
            reasons=[f"Sensitive action '{action}' requires security capability"],
            remediations=["Add 'security' capability token or escalate."],
        )
    return build_partial()
