"""Doctrine evaluation engine."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence

from .checks import fairness, privacy, provenance, safety, security
from .schema import Decision, DoctrineBundle, Outcome, Rule
from .telemetry import TelemetryLogger


@dataclass
class EvaluationContext:
    request: Dict[str, object]
    metadata: Dict[str, object]
    capabilities: Sequence[str]


class DoctrineEngine:
    """Evaluate requests against the doctrine bundle."""

    def __init__(self, bundle: DoctrineBundle, telemetry: TelemetryLogger | None = None):
        self.bundle = bundle
        self.telemetry = telemetry or TelemetryLogger()
        self.check_modules = [
            security,
            privacy,
            safety,
            fairness,
            provenance,
        ]

    def evaluate(self, context: EvaluationContext) -> Decision:
        """Evaluate the context and return a final decision."""

        partials: List[Decision] = []
        for rule in self._matching_rules(context.request):
            partial = self._apply_rule(rule, context)
            partials.append(partial)

        if not partials:
            decision = Decision(outcome=Outcome.allow, score=0.0, reasons=[])
        else:
            decision = Decision.aggregate(partials)

        self.telemetry.record(event="decision", payload=decision.model_dump())
        return decision

    def _matching_rules(self, request: Dict[str, object]) -> Iterable[Rule]:
        for rule in self.bundle.rules:
            if rule.match.matches(request):
                yield rule

    def _apply_rule(self, rule: Rule, context: EvaluationContext) -> Decision:
        reasons = list(rule.decision.reasons)
        remediations = list(rule.decision.remediation or [])
        score = rule.decision.score
        outcome = rule.decision.outcome

        for module in self.check_modules:
            result = module.evaluate(context, rule)
            outcome = self._max_outcome(outcome, result.outcome)
            reasons.extend(result.reasons)
            remediations.extend(result.remediations)
            score = max(score, result.score)

        decision = Decision(
            outcome=outcome,
            score=round(score, 4),
            reasons=reasons,
            remediations=remediations,
            matching_rules=[rule.id],
        )
        self.telemetry.record(
            event="rule_evaluated",
            payload={"rule_id": rule.id, "outcome": decision.outcome.value, "score": score},
        )
        return decision

    @staticmethod
    def _max_outcome(first: Outcome, second: Outcome) -> Outcome:
        priority = {Outcome.deny: 2, Outcome.review: 1, Outcome.allow: 0}
        return first if priority[first] >= priority[second] else second
