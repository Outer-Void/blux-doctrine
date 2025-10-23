"""Explanatory reasoning bridge for BLUX cA."""
from __future__ import annotations

from typing import Dict

from ..engine import DoctrineEngine, EvaluationContext
from ..loader import DoctrineLoader
from ..schema import Decision


def explain(request: Dict[str, object]) -> str:
    bundle = DoctrineLoader().load()
    engine = DoctrineEngine(bundle)
    context = EvaluationContext(
        request=request,
        metadata=request.get("metadata", {}),
        capabilities=request.get("capabilities", []),
    )
    decision = engine.evaluate(context)
    return _render(decision)


def _render(decision: Decision) -> str:
    lines = [f"Outcome: {decision.outcome.value}", f"Score: {decision.score:.2f}"]
    if decision.reasons:
        lines.append("Reasons:")
        lines.extend(f"- {reason}" for reason in decision.reasons)
    if decision.remediations:
        lines.append("Remediations:")
        lines.extend(f"- {item}" for item in decision.remediations)
    return "\n".join(lines)
