# Synthetic access-review lab

- [Tutorial](access-review-lab.md) — Understand identity joins, overlapping paths, review expiry and evidence boundaries.
- [Synthetic snapshot](snapshot.json) — Teaching identities/accounts/assignments; not an AWS API response or customer export.
- [Inventory reconciler](reconcile.py) — Read local input and emit a scoped report; no IAM evaluation or account access.
- [Regression tests](test-reconcile.py) — Check group expansion, deduplication, invalid inputs, expiry and uncertainty handling.

[Back to examples](../index.md) | [Back to governance and access](../../index.md)
