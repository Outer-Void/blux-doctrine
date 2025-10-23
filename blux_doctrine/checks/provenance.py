"""Provenance checks for data lineage."""
from __future__ import annotations

from ..schema import Decision, Outcome, Rule
from ._base import build_partial


def evaluate(context, rule: Rule) -> Decision:
    source = context.metadata.get("source", "")
    if source == "unknown":
        return build_partial(
            outcome=Outcome.review,
            score=max(rule.decision.score, 0.5),
            reasons=["Data source unknown; require provenance verification"],
            remediations=["Attach provenance manifest or cite data registry"],
        )
    return build_partial()
