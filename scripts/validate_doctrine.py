"""Validate the doctrine bundle using the schema."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from blux_doctrine.loader import DoctrineLoader
from blux_doctrine.schema import DoctrineBundle, export_jsonschema


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, nargs="?", default=Path("doctrine"))
    args = parser.parse_args()

    loader = DoctrineLoader(search_locations=[args.path])
    bundle = loader.load()
    DoctrineBundle.model_validate(bundle.model_dump())
    print(json.dumps(export_jsonschema(), indent=2))
    print(f"Validated {len(bundle.rules)} rules")


if __name__ == "__main__":
    main()
