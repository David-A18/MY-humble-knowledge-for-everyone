---
type: Explanation
title: CDK apps, stacks, constructs, and synthesis
description: Understand the object model before deploying infrastructure.
tags:
- cloud
- cdk
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: stacks
  resource: https://docs.aws.amazon.com/cdk/v2/guide/stacks.html
  title: Stacks
- id: identifiers
  resource: https://docs.aws.amazon.com/cdk/v2/guide/identifiers.html
  title: Identifiers
- id: context
  resource: https://docs.aws.amazon.com/cdk/v2/guide/context.html
  title: Context
---

# CDK apps, stacks, constructs, and synthesis

## Purpose

Understand the object model before deploying infrastructure.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Object model

An App contains Stacks. Each Stack maps to a CloudFormation stack and has an account/region environment. Constructs form a tree of resources and abstractions. L1 constructs closely expose CloudFormation resources; L2 constructs add defaults and conveniences; L3 patterns compose higher-level solutions.[^stacks][^identifiers][^context]

Construct IDs contribute to paths and generated logical IDs. Renaming or moving constructs can cause CloudFormation to see a new resource and replace the old one. Review stateful-resource moves carefully.

## Synthesis and context

`cdk synth` emits a cloud assembly containing templates and metadata/assets. It can be local-only for environment-agnostic examples. Context lookups, bundling, and assets may require credentials, network access, Docker, or cached environment information.

```bash
pnpm exec cdk synth --app 'pnpm exec tsx app.ts'
pnpm exec cdk diff --app 'pnpm exec tsx app.ts'
```

What it does: synthesizes a TypeScript app and compares it with a target stack when access/configuration permit. Run from the TypeScript example directory after installing dependencies. `diff` behavior and credentials differ from purely local assertions.

## Environments and dependencies

Use explicit account/region inputs for real deployments. Keep environment-specific context under review. Avoid placing secrets in context, stack outputs, CLI arguments, or committed synthesized templates. Asset hashes identify built artifacts; asset buckets and deployment roles belong to the bootstrap environment.

Cross-stack references add ordering and coupling. Removing an exported value while another stack imports it can block an update. Favor intentional interfaces and avoid building a single tightly coupled stack graph across unrelated services.

## Safe refactoring

Before reorganizing constructs, compare logical IDs and replacement-sensitive properties. A passing unit test on one property does not prove a refactor preserves resource identity. Inspect the diff, removal policies, and data migration plan.

## Related links

- [Stacks](https://docs.aws.amazon.com/cdk/v2/guide/stacks.html)
- [Identifiers](https://docs.aws.amazon.com/cdk/v2/guide/identifiers.html)
- [Context](https://docs.aws.amazon.com/cdk/v2/guide/context.html)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^stacks]: [Stacks](https://docs.aws.amazon.com/cdk/v2/guide/stacks.html).
[^identifiers]: [Identifiers](https://docs.aws.amazon.com/cdk/v2/guide/identifiers.html).
[^context]: [Context](https://docs.aws.amazon.com/cdk/v2/guide/context.html).
