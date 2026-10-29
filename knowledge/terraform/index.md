# Terraform

Practical Terraform notes for infrastructure as code, module design, commands, state, troubleshooting, and examples.

## Suggested learning sequence

Start with [fundamentals](fundamentals/terraform-fundamentals.md) and the [first local state lab](examples/local-state-lifecycle/index.md). Continue with [typed contracts](language/variables-locals-and-outputs.md), [modules](project-structure/modules-and-composition.md), and the [module/workspace lab](examples/module-workspace-lab/index.md). Then study [providers and dependency locks](fundamentals/providers-and-dependency-locking.md), run the [provider alias lab](examples/provider-alias-lab/index.md), and compare [backends](fundamentals/remote-backends-and-locking.md) with [environment boundaries](project-structure/environment-layouts.md).

For operations, use [failure diagnosis](troubleshooting/failures-and-unexpected-plans.md), [plan exit codes](commands/plan-exit-codes-and-ci.md), and the [review checklist](best-practices/review-and-automation-checklist.md). Local checks use Terraform 1.17.1; live cloud/backend acceptance remains explicit follow-up evidence.

## Index

| Section | Focus |
| --- | --- |
| [Fundamentals](fundamentals/index.md) | Core concepts, workflow, providers, resources, and state. |
| [Commands](commands/index.md) | Common CLI workflows and expected outputs. |
| [Language](language/index.md) | HCL syntax, expressions, variables, locals, and outputs. |
| [Project structure](project-structure/index.md) | Repository layouts, modules, environments, and naming. |
| [Troubleshooting](troubleshooting/index.md) | Failed plans, provider issues, state problems, and drift. |
| [Best practices](best-practices/index.md) | Maintainable IaC patterns and review habits. |
| [Examples](examples/index.md) | Practical Terraform examples and walkthroughs. |

## Official documentation

- [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
- [Terraform CLI documentation](https://developer.hashicorp.com/terraform/cli)

[Back to root index](../../README.md)
