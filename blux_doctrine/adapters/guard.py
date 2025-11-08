"""Pre-execution policy hook for BLUX Guard."""
from __future__ import annotations

from typing import Dict

from ..engine import DoctrineEngine, EvaluationContext
from ..loader import DoctrineLoader
from ..schema import Decision


def check(request: Dict[str, object], metadata: Dict[str, object] | None = None) -> Decision:
    bundle = DoctrineLoader().load()
    engine = DoctrineEngine(bundle)
    context = EvaluationContext(
        request=request,
        metadata=metadata or {},
        capabilities=request.get("capabilities", []),
    )
    return engine.evaluate(context)
