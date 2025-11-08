"""Fairness checks ensure balanced treatment."""
from __future__ import annotations

from ..schema import Decision, Outcome, Rule
from ._base import build_partial


BIAS_ATTRIBUTES = {"gender", "ethnicity", "religion"}


def evaluate(context, rule: Rule) -> Decision:
    filters = set(context.request.get("filters", []))
    if filters.intersection(BIAS_ATTRIBUTES):
        return build_partial(
            outcome=Outcome.review,
            score=max(rule.decision.score, 0.6),
            reasons=["Potential bias attribute detected in filters"],
            remediations=["Remove bias attributes or document justification"],
        )
    return build_partial()
