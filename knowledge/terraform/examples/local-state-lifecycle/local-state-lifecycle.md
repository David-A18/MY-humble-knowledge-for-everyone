---
type: Tutorial
title: Terraform local state lifecycle
description: Create, update, inspect, and remove one local Terraform resource while learning what plans and state record.
tags: [terraform, tutorial, state, beginner]
status: draft
maturity: draft
audience: Beginning platform engineer
maintainer: unassigned
sources:
  - id: terraform-data
    resource: https://developer.hashicorp.com/terraform/language/resources/terraform-data
    title: Terraform - terraform_data resource
  - id: terraform-plan
    resource: https://developer.hashicorp.com/terraform/cli/commands/plan
    title: Terraform - terraform plan
  - id: terraform-show
    resource: https://developer.hashicorp.com/terraform/cli/commands/show
    title: Terraform - terraform show
  - id: terraform-apply
    resource: https://developer.hashicorp.com/terraform/cli/commands/apply
    title: Terraform - terraform apply
  - id: terraform-state
    resource: https://developer.hashicorp.com/terraform/language/state
    title: Terraform - State
  - id: terraform-sensitive
    resource: https://developer.hashicorp.com/terraform/language/manage-sensitive-data
    title: Terraform - Manage sensitive data
  - id: terraform-init
    resource: https://developer.hashicorp.com/terraform/cli/commands/init
    title: Terraform - terraform init
  - id: terraform-fmt
    resource: https://developer.hashicorp.com/terraform/cli/commands/fmt
    title: Terraform - terraform fmt
  - id: terraform-validate
    resource: https://developer.hashicorp.com/terraform/cli/commands/validate
    title: Terraform - terraform validate
  - id: terraform-state-list
    resource: https://developer.hashicorp.com/terraform/cli/commands/state/list
    title: Terraform - terraform state list
  - id: terraform-state-show
    resource: https://developer.hashicorp.com/terraform/cli/commands/state/show
    title: Terraform - terraform state show
  - id: terraform-output
    resource: https://developer.hashicorp.com/terraform/cli/commands/output
    title: Terraform - terraform output
  - id: terraform-local-backend
    resource: https://developer.hashicorp.com/terraform/language/backend/local
    title: Terraform - Local backend
  - id: terraform-dependency-lock
    resource: https://developer.hashicorp.com/terraform/language/files/dependency-lock
    title: Terraform - Dependency lock file
stale_after: 2026-12-19
---

# Terraform local state lifecycle

## What you will learn

Create one `terraform_data` resource, inspect its state, change
an input, and remove it. This resource follows Terraform's
managed-resource lifecycle but **does not create cloud
infrastructure**. It lets you see what plan, apply, and state
mean without an AWS account or bill.[^terraform-data]

Read [Terraform fundamentals](../../fundamentals/terraform-fundamentals.md)
first if configuration, resource, state, plan, and apply are new
terms. This page is a hands-on path, not an explanation of all
Terraform providers or backends.

The local path was first run on 2026-10-06. On 2026-10-11,
the copied-file and Git setup and the Terraform commands in steps
2–5 were run again in a disposable directory with Terraform v1.13.1.
Captured Terraform output used `-no-color`; the downloaded official
archive passed its published SHA-256 check. The run observed one
addition, one in-place update, one destruction, an ignored state and
plan file, a plain plan back toward the default, a stale saved-plan
error, and no final resource entries. The online clone was not run.
The guarded cleanup later refused `/tmp` and removed a disposable
six-character lab path; it was not tested in every shell or platform.
Claude Opus 5.5 reviewed the tutorial and linked explanation read-only
on 2026-10-11. This is local command and source-review evidence, not a
human reader test or a cloud deployment. The page remains `draft`.

| Stage | What should change | What should stay the same |
| --- | --- | --- |
| Initialize and validate | Terraform prepares the directory and checks configuration. | No managed resource exists yet. |
| Plan creation | A saved plan proposes one resource. | State is not yet created by this plan. |
| Apply creation | State records `terraform_data.release`. | No external service is created. |
| Plan and apply an update | The stored version changes from `1.0.0` to `1.1.0`. | The resource address stays the same. |
| Plan and apply destruction | State no longer lists the resource. | There was no cloud resource to delete. |

```mermaid
flowchart TB
  config["main.tf<br/>default version 1.0.0"] --> create["Plan +<br/>review only"]
  create --> applyCreate["Apply saved plan"]
  applyCreate --> stateOne["Local state<br/>version 1.0.0"]
  stateOne --> change["Plan ~ with -var 1.1.0<br/>review only"]
  change --> applyChange["Apply saved plan"]
  applyChange --> stateTwo["Local state<br/>version 1.1.0"]
  stateTwo --> destroy["Plan -<br/>review only"]
  stateTwo -.->|plain plan| reverse["~ back to default 1.0.0<br/>not applied"]
  destroy --> applyDestroy["Apply saved plan"]
  applyDestroy --> empty["Local state<br/>no managed resources"]
```

Text alternative: the configuration starts with version `1.0.0`. A create
plan proposes one addition, but only applying it records that version in
local state. A second plan uses a one-command `-var` override to propose
version `1.1.0`; applying it updates state. A destroy plan proposes one
resource deletion, and applying it leaves no managed resources in state.
From version `1.1.0`, a separate plain plan would propose returning to
the unchanged `1.0.0` default; the tutorial does not apply that side path.
Each plan is a review step, while each apply changes the recorded state.

## Before you start

You need Terraform 1.4.0 or newer, Git, permission to create a temporary
local directory, and a Bash shell on Linux, macOS, WSL, or Git Bash.
You also need a local
clone of this repository for the supporting files. If you are reading
online and do not already have one, run this in a directory where
`knowledge-source` does not exist:

```bash
git clone https://github.com/David-A18/MY-humble-knowledge-for-everyone.git knowledge-source
cd knowledge-source
```

The [supporting `main.tf`](main.tf) defines two input variables
(`environment` and `release_version`), a local value `app_name`,
a `terraform_data.release` resource, and a root output
`release_summary`. The resource's `input` object
stores illustrative application release details in local
state.[^terraform-data] If these block names are unfamiliar, read
[How values move through Terraform configuration](../../language/how-values-move-through-terraform.md)
before starting the commands.

The exercise uses the default local backend. Terraform stores
its state as a local file here; in a shared infrastructure
project, state needs different storage and access controls.
[^terraform-state][^terraform-local-backend]

## 1. Make a disposable copy

From the knowledge-base repository root:

```bash
terraform_lab_dir=$(mktemp -d /tmp/kb-terraform-local.XXXXXX)
cp knowledge/terraform/examples/local-state-lifecycle/main.tf "$terraform_lab_dir/"
cp knowledge/terraform/examples/local-state-lifecycle/.gitignore "$terraform_lab_dir/"
cd "$terraform_lab_dir"
git init
git add -- main.tf .gitignore
git -c user.name="Local Lab" -c user.email="lab@example.invalid" commit -m "add local Terraform exercise"
pwd
```

The temporary Git commit gives you a known starting point.
The example identity applies only to this local commit. All
Terraform commands below run **inside this temporary
directory**, never in the knowledge-base checkout. The
copied [`.gitignore`](.gitignore) excludes local state,
saved plans, and Terraform's working directory. Keep using
this terminal and note the path printed by `pwd`; the
`terraform_lab_dir` shell variable is lost when that shell closes.
Your global Git signing or hook settings may still affect this
temporary commit; if it fails, inspect that error before continuing.
Confirm that both files were copied and the commit succeeded before
starting step 2; a failed `cp` does not stop the later commands by itself.

## 2. Initialize and check the configuration

```bash
terraform version
terraform init
terraform fmt -check
terraform validate
```

Expected result: `terraform init` succeeds,
`terraform fmt -check` exits successfully (it may print
nothing; a listed filename means formatting needs attention), and
`terraform validate` reports that the
configuration is valid. Formatting and validation inspect
the configuration; they do not create the managed resource. Stop and fix any
reported error before planning. Check that `terraform version` reports
at least 1.4.0.[^terraform-init][^terraform-fmt][^terraform-validate]

## 3. Plan and create the first state entry

```bash
terraform plan -out=create.tfplan
terraform show create.tfplan
```

Look for **one resource addition**: `terraform_data.release`,
with a plan summary of `1 to add, 0 to change, 0 to destroy`.
The root output `release_summary` also appears under
`Changes to Outputs`; it is a result, not a second resource.
The `+` symbol means create. Planning proposes a change;
it does not yet save the new resource in state. The saved
`create.tfplan` records the plan you are about to apply.
The three values in `input` are already known; `id`, `output`, and
the root `release_summary` show `(known after apply)` until Terraform
applies the plan.
Read it before the next command.[^terraform-plan]
[^terraform-show]

```bash
terraform apply create.tfplan
terraform state list
terraform state show terraform_data.release
terraform output release_summary
git status --short --ignored
```

Expected result: state lists `terraform_data.release`.
Its input and output have a `version`
entry with value `"1.0.0"`; spacing and key quoting differ between
`state show` and `output`. In Git status, `!! create.tfplan` and
`!! terraform.tfstate` mean those files are ignored, not absent.
The `id` shown in state identifies this Terraform-managed entry;
it is not the ID of a cloud object, because this example created none.
Applying a saved plan does **not** prompt for another approval; passing
the plan file is the approval. Here the resource's data
exists only in local Terraform state.[^terraform-apply]
[^terraform-data][^terraform-state-list][^terraform-state-show][^terraform-output]

## 4. Change a value without replacing the resource

The `release_version` variable defaults to `1.0.0`.
Override it for this run, save the proposed update, and
inspect it:

```bash
terraform plan -var='release_version=1.1.0' -out=change.tfplan
terraform show change.tfplan
```

Expected result: Terraform proposes an **in-place update**
of `terraform_data.release`, shown by `~` and the summary
`0 to add, 1 to change, 0 to destroy`. The
`release_summary` output also changes. This is an update rather
than a replacement. The address remains
`terraform_data.release`; its stored `input.version`
will change. `terraform_data` uses `input` for an
update; `triggers_replace` would request replacement
instead.[^terraform-data][^terraform-plan]
The plan shows `input.version` moving from `"1.0.0"` to `"1.1.0"`;
the resource's `output` and root `release_summary` change to
`(known after apply)` until the saved plan is applied.

Apply **that same reviewed plan**, then inspect the new
record:

```bash
terraform apply change.tfplan
terraform state show terraform_data.release
terraform output release_summary
```

Expected result: the state and output now have a `version` entry
with value `"1.1.0"`. A plain apply with the same `-var` option
would calculate a fresh plan; using `change.tfplan` applies the
one you just reviewed.[^terraform-apply]

The `-var` override belonged to the saved update plan only;
`main.tf` still defaults to `1.0.0`. If you run a plain
plan now, it proposes changing the stored value back to `1.0.0`:

```bash
terraform plan
```

This is a read-only comparison. Do not apply that extra plan in this
tutorial; its `~` is a consequence of the unchanged default, not a
failed update.
Terraform's note that this plain plan was not saved with `-out` is
expected; this side plan is only for inspection.[^terraform-plan]
The following destroy-mode plan removes the resource regardless
of that default; it does not first update the resource.

## 5. Review cleanup before removing state

> [!WARNING]
> The following destroy-mode plan is for this disposable
> `terraform_data` exercise only. In a real Terraform
> project, applying a destroy plan can delete external
> infrastructure and data.

```bash
terraform plan -destroy -out=destroy.tfplan
terraform show destroy.tfplan
```

Expected result: one proposed resource destruction,
`terraform_data.release`, shown by `-` and the summary
`0 to add, 0 to change, 1 to destroy`. The
`release_summary` output is also removed. If the plan
proposes any other resource action, **stop**. Check the current
directory and state before applying.[^terraform-plan]

```bash
terraform apply destroy.tfplan
terraform state list
```

Expected result: `terraform state list` prints no
managed resources. Destroying this `terraform_data`
resource removes its state entry; it has no corresponding
cloud object to delete.[^terraform-data][^terraform-apply]
The local `terraform.tfstate` file, its backup, and saved
plans can still exist even though the state lists no managed
resources; `destroy` does not securely erase those files.

## If a step fails or you stop early

Do not apply a different saved plan just to make progress.
If Terraform reports `Saved plan is stale`, its state has
changed since that plan was made. Inspect the current state,
rerun the `terraform plan` command for the intended next step,
review the new plan, and apply that new file only if it matches
your intent. Reapplying `create.tfplan` after the resource was
created produced this expected error in the disposable run.
[^terraform-plan][^terraform-apply]

If your terminal closes, find the directory using the path
printed by `pwd` in step 1. Multiple `/tmp/kb-terraform-local.*`
directories may exist, so inspect its `main.tf` and `.gitignore`
before running commands or removing it. In a new Bash shell, set
`terraform_lab_dir` to that exact inspected path, then run
`cd "$terraform_lab_dir"` before resuming the state check or cleanup.

Once the final state has no resources and you no longer need the
exercise, check the exact directory that would be removed:

```bash
printf 'Lab directory: %s\n' "$terraform_lab_dir"
```

Only if state lists no resources and you no longer need the files,
run this guarded cleanup in the **same Bash shell**. It checks the
temporary path shape and expected lab files before removing anything:

```bash
if [[ "${terraform_lab_dir:-}" =~ ^/tmp/kb-terraform-local\.[[:alnum:]]{6}$ ]] &&
   [[ -f "$terraform_lab_dir/main.tf" && -f "$terraform_lab_dir/.gitignore" && -d "$terraform_lab_dir/.git" ]]; then
  cd /tmp
  rm -rf -- "$terraform_lab_dir"
else
  printf 'Cleanup skipped: inspect the saved lab path first.\n'
fi
```

This removes the local state, backup, saved plans, and temporary
Git repository. The guard rejects a missing or unexpected path;
`-f` suppresses prompts for read-only Git object files. This cleanup
does not apply to any cloud resource. If the shell variable is missing
or the path is uncertain, locate and inspect the directory first.

## What the files teach

| Path | Why it exists | Git handling |
| --- | --- | --- |
| `main.tf` | The requested resource, inputs, and output. | Commit the configuration. |
| `.terraform/`, if present | Terraform working data for installed providers and modules. This built-in-provider example did not create it in the recorded run. | Ignore it if present. |
| `terraform.tfstate` and backup files | Local record of managed objects and prior snapshots; a backup can retain earlier values after destroy. | Ignore and protect them. |
| `create.tfplan`, `change.tfplan`, `destroy.tfplan` | Opaque saved plans for the exact steps above. | Ignore and protect them. |
| `.terraform.lock.hcl` | Not created by this built-in-provider lab; a real project with external provider selections may have one. | Review and commit it with the configuration.[^terraform-dependency-lock] |

In this lab the values are harmless examples, but real
state and saved plans can contain sensitive values.
`.gitignore` prevents accidental normal staging; it is
not encryption or access control. Treat real plan and
state files accordingly.[^terraform-state]
[^terraform-sensitive]

## Check your understanding

1. Which command first caused
   `terraform_data.release` to appear in state?
2. Why did `terraform show change.tfplan` show
   an update instead of a replacement?
3. Why did the tutorial apply a saved plan after
   inspecting it instead of running a fresh apply?
4. What would be different if the same destroy
   workflow targeted a real cloud provider resource?

## Deeper study

- [`terraform_data` resource](https://developer.hashicorp.com/terraform/language/resources/terraform-data)
  for its `input`, `output`, and replacement behavior.
- [Terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan),
  [show](https://developer.hashicorp.com/terraform/cli/commands/show),
  and [apply](https://developer.hashicorp.com/terraform/cli/commands/apply)
  for the saved-plan workflow.
- [Terraform state](https://developer.hashicorp.com/terraform/language/state)
  for the local record and team storage choices.
- [Initialize](https://developer.hashicorp.com/terraform/cli/commands/init),
  [format](https://developer.hashicorp.com/terraform/cli/commands/fmt), and
  [validate](https://developer.hashicorp.com/terraform/cli/commands/validate)
  a local configuration before planning.
- [State list](https://developer.hashicorp.com/terraform/cli/commands/state/list),
  [state show](https://developer.hashicorp.com/terraform/cli/commands/state/show),
  and [output](https://developer.hashicorp.com/terraform/cli/commands/output)
  for inspecting the result.
- [Review and apply a Terraform change](../../commands/core-workflow.md)
  for applying this sequence to real infrastructure.

[Back to Terraform local state lifecycle](index.md)

[^terraform-data]: [Terraform - terraform_data resource](https://developer.hashicorp.com/terraform/language/resources/terraform-data), source record `terraform-data`.
[^terraform-plan]: [Terraform - terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan), source record `terraform-plan`.
[^terraform-show]: [Terraform - terraform show](https://developer.hashicorp.com/terraform/cli/commands/show), source record `terraform-show`.
[^terraform-apply]: [Terraform - terraform apply](https://developer.hashicorp.com/terraform/cli/commands/apply), source record `terraform-apply`.
[^terraform-state]: [Terraform - State](https://developer.hashicorp.com/terraform/language/state), source record `terraform-state`.
[^terraform-sensitive]: [Terraform - Manage sensitive data](https://developer.hashicorp.com/terraform/language/manage-sensitive-data), source record `terraform-sensitive`.
[^terraform-init]: [Terraform - terraform init](https://developer.hashicorp.com/terraform/cli/commands/init), source record `terraform-init`.
[^terraform-fmt]: [Terraform - terraform fmt](https://developer.hashicorp.com/terraform/cli/commands/fmt), source record `terraform-fmt`.
[^terraform-validate]: [Terraform - terraform validate](https://developer.hashicorp.com/terraform/cli/commands/validate), source record `terraform-validate`.
[^terraform-state-list]: [Terraform - terraform state list](https://developer.hashicorp.com/terraform/cli/commands/state/list), source record `terraform-state-list`.
[^terraform-state-show]: [Terraform - terraform state show](https://developer.hashicorp.com/terraform/cli/commands/state/show), source record `terraform-state-show`.
[^terraform-output]: [Terraform - terraform output](https://developer.hashicorp.com/terraform/cli/commands/output), source record `terraform-output`.
[^terraform-local-backend]: [Terraform - Local backend](https://developer.hashicorp.com/terraform/language/backend/local), source record `terraform-local-backend`.
[^terraform-dependency-lock]: [Terraform - Dependency lock file](https://developer.hashicorp.com/terraform/language/files/dependency-lock), source record `terraform-dependency-lock`.
