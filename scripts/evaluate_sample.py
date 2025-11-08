"""Quick doctrine evaluation demo."""
from __future__ import annotations

import json
from pathlib import Path

from blux_doctrine.engine import DoctrineEngine, EvaluationContext
from blux_doctrine.loader import DoctrineLoader


def main() -> None:
    request = json.loads(Path("doctrine/examples/example_request.json").read_text(encoding="utf-8"))
    context_data = json.loads(
        json.dumps(
            yaml.safe_load(
                Path("doctrine/examples/example_context.yaml").read_text(encoding="utf-8")
            )
        )
    )
    bundle = DoctrineLoader().load()
    engine = DoctrineEngine(bundle)
    context = EvaluationContext(
        request=request,
        metadata=context_data.get("metadata", {}),
        capabilities=context_data.get("capabilities", []),
    )
    decision = engine.evaluate(context)
    print(json.dumps(decision.model_dump(mode="json"), indent=2))


if __name__ == "__main__":
    import yaml  # imported lazily to keep CLI light

    main()
