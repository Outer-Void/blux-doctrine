"""Adapter exposing a Typer sub-application for bluxq."""
from __future__ import annotations

from typer import Typer

from ..cli import get_app


def get_quantum_app() -> Typer:
    """Return the Typer app to be mounted under bluxq."""

    return get_app()
