---
type: "Explanation"
title: "State management"
description: "Explain how Terraform state maps configuration to real infrastructure and why state handling is operationally sensitive."
tags: [terraform, state-management]
status: stable
maturity: maintained
audience: "Beginning platform engineer"
maintainer: unassigned
sources:
  - id: terraform-state
    resource: https://developer.hashicorp.com/terraform/language/state
    title: Terraform state documentation
  - id: terraform-backends
    resource: https://developer.hashicorp.com/terraform/language/backend
    title: Terraform backend documentation
  - id: terraform-state-locking
    resource: https://developer.hashicorp.com/terraform/language/state/locking
    title: Terraform state locking documentation
  - id: terraform-remote-state
    resource: https://developer.hashicorp.com/terraform/language/state/remote
    title: Terraform remote state documentation
  - id: terraform-sensitive-data
    resource: https://developer.hashicorp.com/terraform/language/manage-sensitive-data
    title: Terraform sensitive data documentation
  - id: terraform-state-cli
    resource: https://developer.hashicorp.com/terraform/cli/commands/state
    title: terraform state command reference
  - id: terraform-state-list
    resource: https://developer.hashicorp.com/terraform/cli/commands/state/list
    title: terraform state list command reference
  - id: terraform-state-show
    resource: https://developer.hashicorp.com/terraform/cli/commands/state/show
    title: terraform state show command reference
  - id: terraform-state-mv
    resource: https://developer.hashicorp.com/terraform/cli/commands/state/mv
    title: terraform state mv command reference
  - id: terraform-state-rm
    resource: https://developer.hashicorp.com/terraform/cli/commands/state/rm
    title: terraform state rm command reference
  - id: terraform-plan
    resource: https://developer.hashicorp.com/terraform/cli/commands/plan
    title: terraform plan command reference
  - id: terraform-moved-blocks
    resource: https://developer.hashicorp.com/terraform/language/modules/develop/refactoring
    title: Terraform moved blocks and refactoring documentation
stale_after: 2026-12-21
---

# State management

## Purpose

Explain how Terraform state maps configuration to real infrastructure and why state handling is operationally sensitive.

Status: Maintained
Audience: Beginning platform engineer
Page type: Explanation
Maintainer: Unassigned
Last substantive review: 2026-09-21
Applicable versions: Terraform CLI v1.16 state, backend, locking, sensitive-data, plan, and state-command documentation; linked local exercise previously executed with Terraform v1.13.1
Validation evidence: Source reviewed against official HashiCorp Terraform documentation on 2026-09-21. Terraform CLI is not installed in this workspace, so this pass did not re-execute the local exercise.
Known limitations: This page explains state concepts and safe decision points. It does not replace backend-specific runbooks, cloud IAM guidance, incident-specific recovery procedures, or live drift and locking drills.
Next review: 2026-12-21 or after a relevant Terraform state, backend, locking, sensitive-data, or state-command behavior change

## Mental model

Terraform state is the record Terraform uses to connect configuration addresses
to real infrastructure objects. A resource block such as
`aws_instance.web` is an address in configuration. The state records which real
remote object currently belongs to that address, plus metadata Terraform needs
for future plans.[^terraform-state]

```text
configuration address
  -> state binding
  -> remote object identity
  -> next plan decision
```

What it means: when Terraform plans, it compares configuration, prior state,
and provider refresh results to decide whether to create, update, replace, or
destroy objects. If the state binding is wrong, Terraform may propose changes
that surprise the operator even when the configuration looks reasonable.

## Key Ideas

| Concept | Why it matters |
| --- | --- |
| State snapshot | Records resource bindings and metadata used by Terraform operations. |
| Backend | Defines where state is stored and, for some backends, how teams share and lock it. |
| Locking | Prevents concurrent write operations when the backend supports locking. |
| Resource address | The configuration path Terraform uses to identify a resource instance. |
| Drift | A remote object differs from the configuration or from the state Terraform last recorded. |
| State command | A CLI command for inspecting or carefully changing state without editing the JSON file directly. |

> [!CAUTION]
> Treat state and saved plan files as sensitive. Terraform can store secret
> values in state and plans when secret values appear directly in configuration,
> even if terminal output redacts sensitive variables or outputs.[^terraform-sensitive-data][^terraform-plan]

## Storage and collaboration

By default, Terraform stores local state in `terraform.tfstate` and may create
`terraform.tfstate.backup`. Local state is simple for a single-user exercise,
but it is a poor collaboration mechanism because each operator must have the
latest state and must avoid concurrent runs manually.[^terraform-state][^terraform-remote-state]

For team work, use HCP Terraform or a remote backend that fits the platform.
Remote state lets multiple people share the same state data, and fully featured
remote backends can support locking. Some backends are remote storage only, so
check the backend documentation before assuming that locking is available.[^terraform-backends][^terraform-remote-state]

Backend configuration has important limits:

- A root module can define only one backend block.
- Backend blocks cannot use normal named values such as input variables,
  locals, or data source attributes.
- Do not put access credentials directly in backend configuration. Use the
  credential mechanism expected by the backend or platform.[^terraform-backends]

## Locking

Terraform locks state automatically for operations that could write state when
the backend supports locking. If locking fails, Terraform does not continue. Do
not set `-lock=false` as a routine fix for blocked work.[^terraform-state-locking]

Use `terraform force-unlock` only when automatic unlocking failed for your own
stale lock. Force-unlocking a lock another run still owns can allow multiple
writers to modify the same state, which can corrupt the record Terraform relies
on.[^terraform-state-locking]

## Safe operating checklist

- [ ] Confirm the working directory, workspace, backend, and target account or
  project before running `plan` or `apply`.
- [ ] Confirm the state storage location and whether the backend supports
  locking.
- [ ] Run `terraform plan` and read the proposed resource actions before
  applying.
- [ ] Treat saved plan files as sensitive artifacts and store or delete them
  according to the repository and platform policy.
- [ ] Avoid direct JSON edits to `terraform.tfstate`; use Terraform CLI
  commands or configuration-based refactoring features.
- [ ] Back up state before state mutation commands, even though Terraform state
  subcommands that modify state also write backup files.
- [ ] Use peer review for `state mv`, `state rm`, imports, backend migration,
  or any recovery operation that changes ownership of real infrastructure.

## Inspection Commands

```bash
terraform state list
terraform state show <resource-address>
terraform plan
```

What it does: lists tracked resource addresses, shows the attributes Terraform
has recorded for one address, and compares configuration and state to produce a
proposed action plan.[^terraform-state-list][^terraform-state-show][^terraform-plan]

Expected result: `terraform state list` gives you exact addresses to use in
inspection or state operations. `terraform state show` should target one exact
address. `terraform plan` should show whether Terraform intends to create,
update, replace, or destroy anything.

## State Mutation Commands

State mutation commands are for narrow recovery or refactoring cases. Use the
`terraform state` subcommands instead of editing the JSON state file directly;
Terraform keeps the CLI stable even if the underlying state format changes.[^terraform-state-cli]
They do not replace normal `plan` and `apply` review.

| Goal | Prefer | Use with care |
| --- | --- | --- |
| Rename or move a resource in configuration | A `moved` block, because the move is reviewed in configuration and plan output. | `terraform state mv` for older workflows or urgent repair. |
| Remove Terraform management without destroying the real object | A `removed` block or a reviewed removal workflow when available for the case. | `terraform state rm` when you intentionally want Terraform to forget the object. |
| Inspect state content | `terraform state list`, `terraform state show`, `terraform show -json`. | Direct JSON parsing only for maintained tooling that handles format changes. |
| Correct drift | Normal configuration change plus `plan` and `apply`, or `plan -refresh-only` when the goal is only to update records and outputs. | Manual state edits only for documented incident recovery. |

### Move a binding after a refactor

```bash
terraform state mv aws_instance.web module.compute.aws_instance.web
```

What it does: changes the binding in state so the existing remote object is
tracked by the new address. HashiCorp documents `state mv` for cases such as
renaming a resource block or moving a resource into a child module.[^terraform-state-mv]

Expected result: the next `terraform plan` should not propose destroying the
old object only because the address changed.

Safer alternative: for Terraform v1.1 and later, record many refactors with a
`moved` block so the address change is versioned in configuration and visible
in plan review.[^terraform-moved-blocks]

### Remove a binding without destroying the object

> [!WARNING]
> `terraform state rm` makes Terraform forget the selected object. The remote
> object still exists, but Terraform no longer manages it. A later plan may try
> to create a replacement if the configuration still declares the resource.

```bash
terraform state rm 'module.legacy.aws_s3_bucket.logs'
```

What it does: removes the state binding for the selected address without first
destroying the remote object.[^terraform-state-rm]

Expected result: `terraform state list` no longer shows the selected address.
Before applying future changes, confirm whether the configuration was also
removed, replaced by an import, or intentionally left unmanaged.

## Drift and Refresh

Terraform refreshes state during normal planning so the plan can account for
remote objects that changed outside Terraform. When the only intended action is
to update Terraform's records and root outputs to match remote changes, use
refresh-only planning:

```bash
terraform plan -refresh-only
```

What it does: creates a plan whose goal is to update state and root outputs to
match remote objects, without proposing normal infrastructure changes.[^terraform-plan]

Expected result: the plan explains the record changes Terraform would make.
Review it with the same care as a normal plan, because it still changes what
Terraform records as true.

## Recovery Decision Points

| Situation | First check | Safer next step |
| --- | --- | --- |
| Plan wants to destroy and recreate a renamed object | Did only the resource address change? | Add a `moved` block or use `state mv`, then plan again. |
| Remote object was changed during an incident | Is the new remote setting intended to stay? | Encode the setting in configuration, or use refresh-only review when only state and outputs need reconciliation. |
| State lock is stuck | Is another Terraform run still active? | Wait or stop the owning run. Use force-unlock only for your own stale lock. |
| State contains sensitive material | Which backend stores it and who can read it? | Restrict backend access, avoid committing state or plans, and remove direct secret values from configuration. |
| Terraform must stop managing an object | Should the object continue to exist? | Remove management intentionally with a reviewed `removed` or `state rm` workflow. |

## Local practice exercise

Use [Terraform local state lifecycle](../examples/local-state-lifecycle/index.md) to create, inspect, change, and destroy a local state entry without a cloud account.

## Related links

- [Terraform state documentation](https://developer.hashicorp.com/terraform/language/state)
- [Terraform backends documentation](https://developer.hashicorp.com/terraform/language/backend)
- [Terraform state locking documentation](https://developer.hashicorp.com/terraform/language/state/locking)
- [Terraform remote state documentation](https://developer.hashicorp.com/terraform/language/state/remote)
- [Terraform sensitive data documentation](https://developer.hashicorp.com/terraform/language/manage-sensitive-data)
- [terraform state command reference](https://developer.hashicorp.com/terraform/cli/commands/state)
- [terraform plan command reference](https://developer.hashicorp.com/terraform/cli/commands/plan)
- [Terraform moved blocks and refactoring documentation](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring)
- [Terraform local state lifecycle](../examples/local-state-lifecycle/index.md)
- [Back to Terraform fundamentals](index.md)
- [Back to Terraform index](../index.md)
- [Back to root index](../../../README.md)

[^terraform-state]: Official Terraform state documentation, source record `terraform-state`.
[^terraform-backends]: Official Terraform backend documentation, source record `terraform-backends`.
[^terraform-state-locking]: Official Terraform state locking documentation, source record `terraform-state-locking`.
[^terraform-remote-state]: Official Terraform remote state documentation, source record `terraform-remote-state`.
[^terraform-sensitive-data]: Official Terraform sensitive data documentation, source record `terraform-sensitive-data`.
[^terraform-state-cli]: Official Terraform state command reference, source record `terraform-state-cli`.
[^terraform-state-list]: Official Terraform state list command reference, source record `terraform-state-list`.
[^terraform-state-show]: Official Terraform state show command reference, source record `terraform-state-show`.
[^terraform-state-mv]: Official Terraform state mv command reference, source record `terraform-state-mv`.
[^terraform-state-rm]: Official Terraform state rm command reference, source record `terraform-state-rm`.
[^terraform-plan]: Official Terraform plan command reference, source record `terraform-plan`.
[^terraform-moved-blocks]: Official Terraform moved blocks and refactoring documentation, source record `terraform-moved-blocks`.
