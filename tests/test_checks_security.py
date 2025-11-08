from __future__ import annotations

from blux_doctrine.checks import security
from blux_doctrine.engine import EvaluationContext
from blux_doctrine.schema import Decision, Outcome, Rule, RuleDecision, RuleMatch


class DummyContext:
    def __init__(self, request, capabilities):
        self.request = request
        self.metadata = {}
        self.capabilities = capabilities


def make_rule(action: str) -> Rule:
    return Rule(
        id="TEST",
        pillar="stability",
        match=RuleMatch(action=action),
        decision=RuleDecision(outcome=Outcome.allow, score=0.1, reasons=["base"]),
    )


def test_security_review_for_sensitive_action():
    context = DummyContext({"action": "shell.exec"}, [])
    rule = make_rule("shell.exec")
    partial = security.evaluate(context, rule)
    assert partial.outcome == Outcome.review
    assert partial.score >= 0.7


def test_security_allow_with_capability():
    context = DummyContext({"action": "shell.exec"}, ["security"])
    rule = make_rule("shell.exec")
    partial = security.evaluate(context, rule)
    assert partial.outcome == Outcome.allow
