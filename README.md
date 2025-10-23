# blux-doctrine
BLUX Doctrine — enterprise policy and ethics core for the BLUX ecosystem.

## Quick Start

```bash
pip install -e .[dev]
python -m blux_doctrine.cli --help
```

<!-- FILETREE:BEGIN -->
<!-- generated; do not edit manually -->
<details><summary><strong>Repository File Tree</strong> (click to expand)</summary>

```text
.gitignore
.ruff.toml
CHANGELOG.md
CODE_OF_CONDUCT.md
CONTRIBUTING.md
LICENSE
README.md
mkdocs.yml
mypy.ini
pyproject.toml
pytest.ini
    blux_doctrine/
        __init__.py
        cli.py
        config.py
        engine.py
        loader.py
        schema.py
        telemetry.py
        checks/
            __init__.py
            _base.py
            fairness.py
            privacy.py
            provenance.py
            safety.py
            security.py
        dsl/
            parser.py
            syntax.md
        adapters/
            ca.py
            guard.py
            lite.py
            quantum.py
            reg.py
    docs/
        ARCHITECTURE.md
        CONFIGURATION.md
        DSL.md
        EVALUATION.md
        INSTALL.md
        INTEGRATIONS.md
        OPERATIONS.md
        POLICY_MODEL.md
        PRIVACY.md
        ROADMAP.md
        SCHEMA.md
        SECURITY.md
        TROUBLESHOOTING.md
        VISION.md
        index.md
    tests/
        test_adapters_guard.py
        test_checks_security.py
        test_engine.py
        test_schema.py
        fixtures/
            contexts/
                sample_context.json
            policies/
                sample_policy.yaml
    scripts/
        compile_dsl.py
        evaluate_sample.py
        gen_filetree.py
        update_readme_filetree.py
        validate_doctrine.py
    .github/
        workflows/
            ci.yml
            docs.yml
            release.yml
    doctrine/
        rules/
            base.yaml
            privacy.yaml
            redteam.yaml
            security.yaml
        examples/
            example_context.yaml
            example_request.json
        pillars/
            resilience.md
            responsibility.md
            stability.md
            transparency.md
```

</details>
<!-- FILETREE:END -->
