# Manifest policy

Conftest/Rego v1 teaching policy requiring a truthy top-level `metadata.labels.team` value. This is not a complete ownership/security policy or an admission controller; it does not validate the label's organizational meaning or Pod-template coverage.

The [source-tool runner](../validate-offline.py) checks labeled allowed fixtures and a missing-label denial using Conftest 0.71.1/OPA 1.21.1. Schema checks remain separate. Extend real policy with explicit value/type rules, tested exceptions and a deployment/admission contract.

[Back to examples](../index.md) | [Back to series](../../index.md)
