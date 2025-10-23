"""Privacy compliance checks."""
from __future__ import annotations

from ..schema import Decision, Outcome, Rule
from ._base import build_partial


SENSITIVE_FIELDS = {"ssn", "credit_card", "biometric"}


def evaluate(context, rule: Rule) -> Decision:
    data_fields = set(context.request.get("fields", []))
    if data_fields.intersection(SENSITIVE_FIELDS) and "privacy" not in context.capabilities:
        return build_partial(
            outcome=Outcome.deny,
            score=max(rule.decision.score, 0.9),
            reasons=["Sensitive personal data requested without privacy clearance"],
            remediations=["Limit fields to non-sensitive data", "Request privacy capability"],
        )
    return build_partial()
