---
type: Explanation
title: Expressions and stable instance keys
description: Choose Terraform collection expressions and resource keys that preserve
  identity across ordinary configuration changes.
tags:
- terraform
- for-each
- hcl
status: draft
maturity: draft
audience: Engineering learners and platform practitioners
maintainer: unassigned
sources:
- id: tf-for-each
  title: for_each reference
  resource: https://developer.hashicorp.com/terraform/language/meta-arguments/for_each
- id: tf-dynamic
  title: Dynamic nested blocks
  resource: https://developer.hashicorp.com/terraform/language/expressions/dynamic-blocks
- id: tf-moved
  title: Refactoring with moved blocks
  resource: https://developer.hashicorp.com/terraform/language/modules/develop/refactoring
- id: tf-validation
  title: Custom validation and checks
  resource: https://developer.hashicorp.com/terraform/language/validate
---

# Expressions and stable instance keys

Terraform expressions compute desired values and relationships; they are not an imperative script executed top to bottom. A reference tells Terraform about a dependency. Splitting blocks into several `.tf` files in one module does not create an execution sequence.

## Separate collection shaping from object identity

| Construct | Primary job | Common mistake |
| --- | --- | --- |
| `for` expression | Transform/filter a collection | Assuming it creates resources by itself. |
| Resource/module `for_each` | Create instances keyed by a map or set | Choosing an unstable or sensitive identifier. |
| `count` | Create numerically indexed instances | Removing a list entry and unintentionally shifting address meanings. |
| Conditional expression | Select a value of compatible type | Hiding a missing prerequisite behind an unsafe default. |
| `dynamic` block | Generate repeatable nested blocks in a supported schema | Trying to generate whole resource instances or lifecycle meta-arguments. |

`for_each` accepts a map or set of strings and needs instance keys known before resource operations. Sensitive keys and impure values such as `timestamp()` are unsuitable because keys become visible resource identities.[^tf-for-each]

For the lab's services map, `api` and `worker` become addresses such as `module.release["api"].terraform_data.release`. Adding `batch` should create its own instance without replacing the two existing services. Numeric indexing can be appropriate for interchangeable instances, but stable business names are easier to review when individual identity matters.

## Use expressions to expose intent

```hcl
output "releases" {
  value = { for name, release in module.release : name => release.record }
}
```

What it does: returns each module's public record under its stable service key. It belongs in the runnable [module lab](../examples/module-workspace-lab/index.md), where the provider-independent resource stores a teaching record in local state.

Unknown values are not automatically failures: a resource output can legitimately become known after apply. Distinguish an unknown attribute value from an unknown set of instance keys. Avoid routine `-target` or artificial `depends_on` blocks as a substitute for a clear graph.

## Keep nested generation readable

Use explicit nested blocks when there are only a few fixed items. A `dynamic` block generates schema-supported nested arguments, and cannot generate `lifecycle` or `provisioner` meta-argument blocks.[^tf-dynamic] Excessive nesting makes plans and review harder; extract a small typed input or module only when it clarifies ownership and outcome.

Renaming a resource or changing keys can change addresses even when the remote intent is the same. A suitable `moved` block records the refactor for plan review; removing historical moves can break older consumers' upgrade paths.[^tf-moved]

For safety constraints, use the mechanism that actually blocks the intended failure. A failing `check` assertion normally emits a warning and continues, unlike suitable input validation or lifecycle conditions.[^tf-validation] Verify the failure outcome explicitly in tests. The lab exercises an added key and two moved addresses without replacement; no cloud resource behavior is implied.

## Evidence and limits

Sources reviewed on 2026-10-29. Local examples were executed with Terraform 1.17.1; the provider lab uses hashicorp/local 2.9.1. These runs cover local state/files, not cloud IAM, remote locking, backend migration, imports, or hosted execution. The guides remain drafts with unassigned ownership. Replace angle-bracket placeholders and confirm the actual root, backend, workspace, and provider identity before adapting commands.

## Related routes

- [Module and workspace lab](../examples/module-workspace-lab/index.md).
- [Unexpected plan diagnosis](../troubleshooting/failures-and-unexpected-plans.md).
- [Back to this section](index.md)
- [Back to Terraform](../index.md)

[^tf-for-each]: [for_each reference](https://developer.hashicorp.com/terraform/language/meta-arguments/for_each)
[^tf-dynamic]: [Dynamic nested blocks](https://developer.hashicorp.com/terraform/language/expressions/dynamic-blocks)
[^tf-moved]: [Refactoring with moved blocks](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring)
[^tf-validation]: [Custom validation and checks](https://developer.hashicorp.com/terraform/language/validate)
