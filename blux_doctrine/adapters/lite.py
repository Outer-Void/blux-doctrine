"""Orchestration gate for BLUX Lite."""
from __future__ import annotations

from typing import Dict

from ..engine import DoctrineEngine, EvaluationContext
from ..loader import DoctrineLoader
from ..schema import Decision


def admit(job: Dict[str, object]) -> Decision:
    bundle = DoctrineLoader().load()
    engine = DoctrineEngine(bundle)
    context = EvaluationContext(
        request=job,
        metadata=job.get("metadata", {}),
        capabilities=job.get("capabilities", []),
    )
    return engine.evaluate(context)
