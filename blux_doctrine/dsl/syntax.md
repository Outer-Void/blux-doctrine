# BLUX Doctrine DSL Syntax

The enterprise DSL is intentionally conservative. It mirrors YAML semantics
while allowing authors to omit boilerplate such as a top-level `rules:` key.

Example:

```yaml
- id: SEC-001
  pillar: stability
  match:
    action: "shell.exec"
    risk: ["high"]
  decision:
    outcome: "review"
    score: 0.35
    reasons:
      - "High-risk shell execution; operator approval required."
    remediation:
      - "Run within sandbox profile 'dev-secure'."
```

Files authored with this DSL are validated and normalized through
`blux_doctrine.dsl.parser.compile_file`, producing deterministic YAML output
ready for the loader and engine.
