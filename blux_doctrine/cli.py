"""Typer CLI for BLUX Doctrine."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer
import yaml

from .engine import DoctrineEngine, EvaluationContext
from .loader import DoctrineLoader
from .schema import Decision, export_jsonschema

app = typer.Typer(help="BLUX Doctrine command line interface")


def get_app() -> typer.Typer:
    return app


@app.command()
def check(path: Path = typer.Argument(..., help="Path to doctrine bundle YAML/DSL")) -> None:
    """Validate doctrine file(s) and print summary."""

    loader = DoctrineLoader(search_locations=[path.parent])
    bundle = loader.load()
    typer.echo(f"Loaded {len(bundle.rules)} rules across {len(bundle.pillars)} pillars")


@app.command()
def eval(
    request: Path = typer.Option(..., exists=True, help="JSON request file"),
    context: Path = typer.Option(..., exists=True, help="YAML context file"),
) -> None:
    """Evaluate a request against the doctrine."""

    loader = DoctrineLoader()
    bundle = loader.load()
    engine = DoctrineEngine(bundle)
    request_payload = json.loads(request.read_text(encoding="utf-8"))
    context_payload = yaml.safe_load(context.read_text(encoding="utf-8")) or {}
    evaluation = EvaluationContext(
        request=request_payload,
        metadata=context_payload.get("metadata", {}),
        capabilities=context_payload.get("capabilities", []),
    )
    decision = engine.evaluate(evaluation)
    typer.echo(json.dumps(decision.model_dump(mode="json"), indent=2))


@app.command()
def explain(last: bool = typer.Option(False, help="Reserved for future use")) -> None:
    """Display a placeholder explanation."""

    if last:
        typer.echo("No cached decision available in this standalone build.")
    else:
        typer.echo("Provide --last to retrieve stored decisions when supported.")


@app.command()
def bundle(destination: Optional[Path] = typer.Option(None, help="Path to write bundle JSON")) -> None:
    """Export the merged doctrine bundle to stdout or a file."""

    loader = DoctrineLoader()
    merged = loader.load()
    data = merged.model_dump(mode="json")
    if destination:
        destination.write_text(json.dumps(data, indent=2), encoding="utf-8")
        typer.echo(f"Bundle written to {destination}")
    else:
        typer.echo(json.dumps(data, indent=2))


@app.command("schema")
def schema_cmd() -> None:
    """Print the JSON schema for doctrine bundles."""

    typer.echo(json.dumps(export_jsonschema(), indent=2))


if __name__ == "__main__":
    app()
