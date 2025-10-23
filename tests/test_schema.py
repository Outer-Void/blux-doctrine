from __future__ import annotations

from blux_doctrine.loader import DoctrineLoader
from blux_doctrine.schema import DoctrineBundle, export_jsonschema


def test_bundle_schema_exports_jsonschema(tmp_path):
    loader = DoctrineLoader(search_locations=[tmp_path])
    tmp_path.joinpath("rules").mkdir()
    tmp_path.joinpath("pillars").mkdir()
    tmp_path.joinpath("pillars", "core.md").write_text("# Core\n", encoding="utf-8")
    tmp_path.joinpath("rules", "base.yaml").write_text(
        "rules:\n  - id: TEST\n    pillar: core\n    match: {}\n    decision:\n      outcome: allow\n      score: 0.1\n      reasons: ['ok']\n",
        encoding="utf-8",
    )
    bundle = loader.load()
    DoctrineBundle.model_validate(bundle.model_dump())
    schema = export_jsonschema()
    assert schema["title"] == "BLUX Doctrine Bundle"
    assert "$ref" in schema


def test_doctrine_loader_uses_project_files():
    loader = DoctrineLoader()
    bundle = loader.load()
    assert bundle.rules
    assert bundle.pillars
