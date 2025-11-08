"""Pydantic models for the BLUX Doctrine policy bundle."""
from __future__ import annotations

from enum import Enum
from typing import Dict, Iterable, List, Optional

from pydantic import BaseModel, Field, RootModel, model_validator


class Outcome(str, Enum):
    """Possible decision outcomes."""

    allow = "allow"
    deny = "deny"
    review = "review"


class Pillar(BaseModel):
    """A foundational principle that groups rules."""

    id: str = Field(..., min_length=1)
    title: str
    description: str


class Capability(BaseModel):
    """Represents a capability that rules may reference."""

    id: str = Field(..., min_length=1)
    title: str
    description: Optional[str] = None


class RuleMatch(BaseModel):
    """Criteria required for a rule to trigger."""

    action: Optional[str] = None
    risk: Optional[List[str]] = None
    tags: Optional[List[str]] = None

    def matches(self, payload: Dict[str, object]) -> bool:
        """Return ``True`` if the payload matches the rule constraints."""

        if self.action and payload.get("action") != self.action:
            return False
        if self.risk and not set(self.risk).intersection(payload.get("risk", [])):
            return False
        if self.tags and not set(self.tags).issubset(payload.get("tags", [])):
            return False
        return True


class RuleDecision(BaseModel):
    """Outcome attached to an individual rule."""

    outcome: Outcome
    score: float = Field(..., ge=0.0, le=1.0)
    reasons: List[str]
    remediation: Optional[List[str]] = None


class Rule(BaseModel):
    """Represents a single policy rule."""

    id: str = Field(..., min_length=1)
    pillar: str
    match: RuleMatch
    decision: RuleDecision
    capabilities: Optional[List[str]] = None


class DoctrineBundle(BaseModel):
    """Aggregated doctrine definition."""

    pillars: List[Pillar]
    rules: List[Rule]
    capabilities: Optional[List[Capability]] = None

    @model_validator(mode="after")
    def validate_rule_pillars(self) -> "DoctrineBundle":
        pillar_ids = {pillar.id for pillar in self.pillars}
        for rule in self.rules:
            if rule.pillar not in pillar_ids:
                msg = f"Rule {rule.id} references unknown pillar '{rule.pillar}'"
                raise ValueError(msg)
        return self

    def rule_by_id(self, rule_id: str) -> Optional[Rule]:
        return next((rule for rule in self.rules if rule.id == rule_id), None)

    def pillar_by_id(self, pillar_id: str) -> Optional[Pillar]:
        return next((pillar for pillar in self.pillars if pillar.id == pillar_id), None)


class Decision(BaseModel):
    """Final doctrine evaluation decision."""

    outcome: Outcome
    score: float
    reasons: List[str] = Field(default_factory=list)
    remediations: List[str] = Field(default_factory=list)
    matching_rules: List[str] = Field(default_factory=list)

    @classmethod
    def aggregate(cls, partials: Iterable["Decision"]) -> "Decision":
        """Combine multiple partial decisions into a single outcome."""

        outcome_priority = {Outcome.deny: 2, Outcome.review: 1, Outcome.allow: 0}
        reasons: List[str] = []
        remediations: List[str] = []
        score = 0.0
        matching_rules: List[str] = []
        top_outcome = Outcome.allow

        for partial in partials:
            reasons.extend(partial.reasons)
            remediations.extend(partial.remediations)
            matching_rules.extend(partial.matching_rules)
            score = max(score, partial.score)
            if outcome_priority[partial.outcome] > outcome_priority[top_outcome]:
                top_outcome = partial.outcome

        return cls(
            outcome=top_outcome,
            score=round(score, 4),
            reasons=reasons,
            remediations=remediations,
            matching_rules=matching_rules,
        )


class DoctrineBundleModel(RootModel[DoctrineBundle]):
    """Root model wrapper for JSON schema export."""

    model_config = {"title": "BLUX Doctrine Bundle"}


def export_jsonschema() -> Dict[str, object]:
    """Return the JSON Schema representation of the doctrine bundle."""

    return DoctrineBundleModel.model_json_schema()
