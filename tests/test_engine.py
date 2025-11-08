from __future__ import annotations

from blux_doctrine.engine import DoctrineEngine, EvaluationContext
from blux_doctrine.loader import DoctrineLoader
from blux_doctrine.schema import Outcome


def test_engine_returns_decision_with_reasons():
    bundle = DoctrineLoader().load()
    engine = DoctrineEngine(bundle)
    context = EvaluationContext(
        request={"action": "shell.exec", "risk": ["high"], "tags": ["maintenance"]},
        metadata={"source": "operations"},
        capabilities=[],
    )
    decision = engine.evaluate(context)
    assert decision.outcome in {Outcome.review, Outcome.deny}
    assert decision.reasons
    assert "SEC-001" in decision.matching_rules


def test_engine_allows_safe_action():
    bundle = DoctrineLoader().load()
    engine = DoctrineEngine(bundle)
    context = EvaluationContext(
        request={"action": "read"},
        metadata={"source": "operations"},
        capabilities=["security"],
    )
    decision = engine.evaluate(context)
    assert decision.outcome == Outcome.allow
