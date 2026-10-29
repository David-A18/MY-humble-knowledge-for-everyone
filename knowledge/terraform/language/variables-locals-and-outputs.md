---
type: Explanation
title: Variables, locals, and outputs
description: Design typed Terraform module inputs, derived values, and useful outputs
  without confusing redaction with secret protection.
tags:
- terraform
- hcl
- module-contracts
status: draft
maturity: draft
audience: Engineering learners and platform practitioners
maintainer: unassigned
sources:
- id: tf-variables
  title: Input variables
  resource: https://developer.hashicorp.com/terraform/language/values/variables
- id: tf-locals
  title: Local values
  resource: https://developer.hashicorp.com/terraform/language/values/locals
- id: tf-outputs
  title: Output values
  resource: https://developer.hashicorp.com/terraform/language/values/outputs
- id: tf-sensitive
  title: Sensitive and ephemeral data
  resource: https://developer.hashicorp.com/terraform/language/manage-sensitive-data
---

# Variables, locals, and outputs

Variables are a module's input contract, locals name expressions inside that module, and outputs expose selected results to a caller or operator. These are different roles: a local is not a mutable global variable, and a child module cannot read its parent's locals implicitly.[^tf-variables][^tf-locals]

## Make input assumptions explicit

Prefer specific types and validation messages that explain an action the caller can take. A `number` accepts fractional values; if a replica count must be integral, validate that constraint too. Defaults should represent a useful intended choice rather than conceal required environment decisions.

```hcl
variable "replicas" {
  type = number
  validation {
    condition     = var.replicas >= 1 && floor(var.replicas) == var.replicas
    error_message = "replicas must be a positive whole number."
  }
}
```

What it does: rejects zero, negative, and fractional values before they become an invalid release request. It is a focused illustration; the [module lab](../examples/module-workspace-lab/index.md) applies the same rule to each service in a typed map and tests rejection.

| Need | Use | Design question |
| --- | --- | --- |
| Caller chooses a value | Input variable | Is the type precise, and is the value truly optional? |
| Reuse a derived expression | Local value | Does its name explain the calculation? |
| Caller needs a result | Output | Is it a stable contract instead of the entire provider object? |
| Require a valid relationship | Variable validation or suitable precondition | Can the condition be checked with the available values? |

For example, receive `services` as a map of version/replica objects, derive normalized release records in the child, and return a map keyed by service name. Do not require downstream callers to know a private resource name merely to obtain the release result.

## Sensitive output values in state and plan files

Root outputs are available through the CLI; parent configurations access child outputs as `module.<name>.<output>`.[^tf-outputs] Use purpose-specific outputs with descriptions. A root output may remain unknown in a plan until its resource has been applied; that is not automatically a type error.

`sensitive = true` redacts normal output but still permits values to be stored in state/plans. JSON/raw output can reveal them. Ephemeral inputs/child outputs and provider-supported write-only arguments can omit supported runtime values from persistence, but have version and reference-context restrictions.[^tf-sensitive] Do not add real secrets to the teaching lab to test redaction.

## Choose a verification path

Use `terraform validate` for structural consistency and a real plan/test for concrete input values. A test asserting that a deliberately invalid environment or replica count is rejected checks the contract rather than merely repeating an expression. After a contract change, inspect downstream callers and outputs, not only the module's own formatting.

No standalone resource is created by this illustration. For runnable practice use the isolated lab and its cleanup; keep state, saved plans, and sensitive outputs outside Git.

## Evidence and limits

Sources reviewed on 2026-10-29. Local examples were executed with Terraform 1.17.1; the provider lab uses hashicorp/local 2.9.1. These runs cover local state/files, not cloud IAM, remote locking, backend migration, imports, or hosted execution. The guides remain drafts with unassigned ownership. Replace angle-bracket placeholders and confirm the actual root, backend, workspace, and provider identity before adapting commands.

## Related routes

- [Expressions and stable keys](expressions-and-stable-instance-keys.md).
- [Module design](../project-structure/modules-and-composition.md).
- [Back to this section](index.md)
- [Back to Terraform](../index.md)

[^tf-variables]: [Input variables](https://developer.hashicorp.com/terraform/language/values/variables)
[^tf-locals]: [Local values](https://developer.hashicorp.com/terraform/language/values/locals)
[^tf-outputs]: [Output values](https://developer.hashicorp.com/terraform/language/values/outputs)
[^tf-sensitive]: [Sensitive and ephemeral data](https://developer.hashicorp.com/terraform/language/manage-sensitive-data)
