# Generated knowledge artifacts

This directory contains deterministic artifacts derived from the canonical
[knowledge bundle](../knowledge/index.md). Do not edit generated files by hand.

- [Knowledge catalog](knowledge-catalog.json) - Flattened OKF concept metadata
  for AI retrieval, filtering, and maintenance tooling.

Rebuild and verify it with:

```bash
python3 scripts/build-knowledge-catalog.py
python3 scripts/build-knowledge-catalog.py --check
```

[Back to repository index](../README.md)
