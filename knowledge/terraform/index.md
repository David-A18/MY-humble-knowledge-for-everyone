# Terraform

The [beginner local lifecycle](local-state-lifecycle.md) follows the [local Kubernetes route](../cross-topic-guides/local-deployment-learning-path.md) but owns separate local state. Its runner checks that CLI input overrides do not rewrite configuration.

Practical Terraform notes for infrastructure as code, module design, commands, state, troubleshooting, and examples.

## Suggested learning sequence

Start with [fundamentals](fundamentals/terraform-fundamentals.md) and the [first local state lab](local-state-lifecycle.md). Continue with [typed contracts](language/variables-locals-and-outputs.md), [modules](project-structure/modules-and-composition.md), and the [module/workspace lab](module-workspace-lab.md). Then study [providers and dependency locks](fundamentals/providers-and-dependency-locking.md), run the [provider alias lab](provider-alias-lab.md), and compare [backends](fundamentals/remote-backends-and-locking.md) with [environment boundaries](project-structure/environment-layouts.md).

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
| [Local state lifecycle](local-state-lifecycle.md) | Practice init, plan, state inspection, change review, and cleanup without a cloud account. |
| [Module and workspace lab](module-workspace-lab.md) | Run a provider-free module contract and reject invalid inputs. |
| [Provider alias lab](provider-alias-lab.md) | Pass a declared provider alias into a child module with a pinned provider. |
| [Lab files](../../examples/terraform/README.md) | Runnable Terraform files for the labs, kept outside the knowledge bundle. |

## Official documentation

- [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
- [Terraform CLI documentation](https://developer.hashicorp.com/terraform/cli)

[Back to root index](../../README.md)
