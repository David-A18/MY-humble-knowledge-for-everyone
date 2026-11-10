# Policy contract lab

- [Learning exercise](policy-contract-lab.md) — Understand fixture assertions, AWS simulation, and the remaining live acceptance.
- [Policy contract checker](check-contracts.py) — Enforce the declared fixture scope; does not evaluate AWS requests.
- [Mutation tests](test-contracts.py) — Catch unintended changes to actions, resources, subjects, audiences, and policy shape.
- [IRSA trust fixture](irsa-trust.json) — One synthetic issuer, audience, namespace, and service account.
- [Read permission fixture](read-policy.json) — Only GetObject under one synthetic S3 prefix.

[Back to examples](../index.md) | [Back to AWS security](../../index.md)
