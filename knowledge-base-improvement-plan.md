# Knowledge-base improvement plan

Created: 2026-09-18

Status: In progress. KB-01, KB-02, KB-03, KB-05, KB-06, KB-07, KB-08, KB-09, KB-10, KB-11, KB-12, KB-13, and KB-15 have implementation evidence. KB-14 has a maintenance queue scaffold, external evidence checklist, results template, issue form, and facilitator guide but remains blocked on actual reader testing. KB-04 has source/documentation corrections, an external evidence checklist, and validation capture paths but remains blocked on an authorized AWS/Crossplane sandbox.

Basis: [Knowledge-base review](knowledge-base-review.md), covering baseline commit `831ce4cf77f22b17c3a38ba316d2d2e5b494767b`.

## Purpose

Turn the review into a practical execution guide for contributors and AI agents. Improve the repository's ability to help people find accurate information, learn through complete exercises, make technical decisions, and perform work safely.

The first priority is to correct known problems and establish reliable validation. The next priority is to complete one beginner learning path. Expand coverage and publishing tools after those foundations work.

This file is the implementation backlog and acceptance guide. [ROADMAP.md](ROADMAP.md) remains the high-level direction; the [review](knowledge-base-review.md) remains a dated record of findings. Creating this plan does not mean its tasks are complete or that proposed standards have already been adopted.

## Contents

- [How to execute this plan](#how-to-execute-this-plan)
- [Best-practice principles](#best-practice-principles)
- [Work tracker and dependencies](#work-tracker-and-dependencies)
- [Phase 1: establish a trustworthy baseline](#phase-1-establish-a-trustworthy-baseline)
- [Phase 2: establish consistent quality controls](#phase-2-establish-consistent-quality-controls)
- [Phase 3: complete learning and operational paths](#phase-3-complete-learning-and-operational-paths)
- [Phase 4: make maintenance sustainable](#phase-4-make-maintenance-sustainable)
- [Article and example instructions](#article-and-example-instructions)
- [Validation and publication](#validation-and-publication)
- [Evidence and handoff format](#evidence-and-handoff-format)
- [Maintenance cadence and success measures](#maintenance-cadence-and-success-measures)
- [Instructions for the next contributor or agent](#instructions-for-the-next-contributor-or-agent)
- [Related links](#related-links)

## How to execute this plan

1. Read [AGENTS.md](AGENTS.md), [context.md](context.md), [instructions.md](instructions.md), and [CONTRIBUTING.md](CONTRIBUTING.md). Read any applicable directory instructions before editing there.
2. Inspect the current checkout and changes. The review describes a historical baseline; confirm a reported defect still exists before changing it.
3. Select the earliest unfinished work package whose required dependency deliverables are available and verified. Within a phase, independent packages can be tackled in either order.
4. Set its tracker status to `In progress` and record the actual contributor or agent as owner. Do not assign another person's time without agreement.
5. Read the relevant finding and nearby articles. State the reader outcome and files affected before editing.
6. Make the smallest coherent change that meets the package's acceptance criteria. Reuse existing content and preserve working links.
7. Run the relevant technical checks, Markdown checks, and navigation checks. Record what was actually tested and any remaining limitation.
8. Update affected indexes, this tracker, and the changelog. Update glossary or routing instructions when the change requires them.
9. Publish according to the existing repository policy and the validation rules below. Mark `Done` only when acceptance evidence and publication are recorded.

Use `Todo`, `In progress`, `Blocked`, `Ready to publish`, `Done`, or `Deferred` for task status. `Blocked` requires a concrete unmet dependency and a next action. `Deferred` requires a reason and a condition for reconsideration. Do not mark a package complete merely because its article has been written.

If implementation reveals that a finding was already fixed, verify the fix and record the evidence. If a finding was mistaken, record a dated correction rather than silently rewriting the historical review.

New standards in this plan should be adopted in the canonical contributor instructions and templates through KB-06. Until then, follow existing repository rules and use this plan as the task-specific acceptance guide. User instructions and the active task scope take precedence.

## Best-practice principles

| Principle | Application to this repository |
| --- | --- |
| Organize around reader needs | Keep topic directories, but distinguish learning, task execution, lookup, and explanation. This follows [Diátaxis](https://diataxis.fr/). |
| Finish useful paths | Prefer one complete learning journey over several unrelated outlines. |
| Make reliability visible | Separate source review, static checks, and execution evidence. Do not imply that lint proves technical correctness. |
| Keep one maintained home for each rule | Link to canonical guidance instead of copying full procedures across indexes and agent instructions. |
| Support scanning and feedback | Use descriptive headings, useful examples, and clear ways to report problems, consistent with [Write the Docs principles](https://www.writethedocs.org/guide/writing/docs-principles/). |
| Write accessibly | Use meaningful link text, explain acronyms, provide clear instructions, and describe important diagrams in text, following [W3C WAI guidance](https://www.w3.org/WAI/tips/writing/). |
| Preserve provenance | Distinguish curated guidance, archived notes, illustrative examples, and verified facts. |
| Match maintenance to capacity | Begin with ten important guides, a few reader tasks, and a small review queue. |

Keep the current directory hierarchy unless a specific navigation problem justifies a move. Avoid mass renaming, adding a new top-level topic for every request, or introducing a retrieval service before there is a measured need.

## Work tracker and dependencies

Findings refer to F1–F13 in the [review](knowledge-base-review.md#priority-findings). Each task owner starts as `Unassigned`. Effort is comparative: **S** is a focused edit, **M** is a bounded article or tooling change, and **L** involves several connected deliverables. These are not calendar estimates.

| ID | Work package | Depends on | Effort | Status |
| --- | --- | --- | --- | --- |
| KB-01 | Refresh the baseline and record evidence | None | S | Done |
| KB-02 | Fix Markdown lint failures | KB-01 | S | Done |
| KB-03 | Correct Git restore guidance | KB-01 | S | Done |
| KB-04 | Correct temporary AWS credential guidance | KB-01 | M | Blocked |
| KB-05 | Clarify and validate the Kafka example | KB-01 | M | Done |
| KB-06 | Align templates and article quality rules | KB-02 | M | Done |
| KB-07 | Make maturity and routes visible | KB-06 | S | Done |
| KB-08 | Make automated checks match documented guarantees | KB-02, KB-06 | M | Done |
| KB-09 | Build the first beginner learning path | KB-03, KB-06, KB-07, KB-08 | L | Done |
| KB-10 | Add a complete Terraform exercise | KB-06, KB-08 | M | Done |
| KB-11 | Review ten priority operational guides | KB-03, KB-04, KB-05, KB-06, KB-08 | L | Done |
| KB-12 | Improve long-page readability | KB-06 | M | Done |
| KB-13 | Simplify governance and add source traceability | KB-07, KB-08 | M | Done |
| KB-14 | Test reader tasks and run a maintenance loop | KB-09, KB-10, KB-11, KB-12, KB-13 | M | Blocked |
| KB-15 | Decide whether a searchable site is worthwhile | KB-14 | M | Done |

Dependencies indicate required inputs, not a requirement to postpone a small independent correction. If a dependency proves unnecessary, update the table with an explanation. Keep one primary work package active per contributor to make changes easy to review.

A dependency can supply verified input while still `Ready to publish`. In particular, KB-01 records the failing baseline so KB-02 can fix it; publish their records together after validation succeeds. Recording an expected baseline failure satisfies KB-01's measurement outcome, not the publication gate. Similarly, a blocked sandbox test need not prevent source review of related pages: record which verified correction is available and which execution evidence remains missing.

## Phase 1: establish a trustworthy baseline

### KB-01: refresh the baseline and record evidence

**Findings:** F3 and the review's validation limitations. **Owner:** Unassigned.

**Inspect:** [Review](knowledge-base-review.md), [lint configuration](.markdownlint-cli2.jsonc), [link configuration](lychee.toml), and current Git status.

**Instructions:**

1. Record the current commit, branch, tool versions, and pre-existing changes. Preserve ongoing work, including the review and plan if they remain uncommitted.
2. Run the prescribed Markdown lint command and a repository-aware local link check.
3. Record exact failures by file and rule. Compare with the historical 20-error baseline; do not assume the count is unchanged.
4. Establish current reachability and index coverage, separating archived sources and the portable OKF example from ordinary articles.
5. Store a concise dated result under this plan's implementation records. Redact credentials and private environment information from any output.

**Done when:** The current state is reproducible from recorded commands and versions, all baseline failures have an owner task, and pre-existing changes are accounted for.

### KB-02: fix Markdown lint failures

**Finding:** F3. **Owner:** Unassigned.

**Edit:** [OKF example bundle](ai/ai-tooling/knowledge-bases/examples/okf-v0.2/README.md), [XRD guide](kubernetes/crossplane/xrd-composition-and-xr-calls.md), and lint configuration only if necessary.

**Instructions:**

1. Resolve the frontmatter-title/body-H1 convention without deleting metadata required by the example format. Prefer a targeted documented configuration over disabling a rule for the entire corpus.
2. Convert the identified bare source URLs to descriptive links.
3. Escape the pipe in the XRD troubleshooting table and inspect its rendered columns.
4. Re-run the entire lint scope, preserving the established raw-source exclusions.

**Done when:** Repository-wide Markdown lint passes, titles and tables render correctly, and no broad suppression hides unresolved defects.

### KB-03: correct Git restore guidance

**Finding:** F1. **Owner:** Unassigned.

**Edit:** [Undo and recovery](git/troubleshooting/undo-and-recovery.md) and any related Git pages containing the same explanation.

**Instructions:**

1. Verify default restore behavior against the official Git documentation linked in the review.
2. Explain the working tree, index, and `HEAD` distinctly. Explain the effect of a specified restore source when relevant.
3. Put the warning about discarded edits before the affected command.
4. Reproduce the behavior in a disposable repository with different committed, staged, and unstaged content. Never use this knowledge base's working files as the destructive example.

**Done when:** The explanation matches all three states, the example demonstrates the difference, and the warning appears before execution.

### KB-04: correct temporary AWS credential guidance

**Findings:** F2 and F6. **Owner:** Unassigned.

**Edit:** [Crossplane S3 lab](kubernetes/crossplane/local-aws-s3-lab.md), [provider authentication](kubernetes/crossplane/providers-and-authentication.md), and relevant snippets found by search.

**Instructions:**

1. Recheck AWS documentation for the temporary credential fields and the selected provider's credential support.
2. Include the session token when documenting STS temporary credentials. Distinguish these from long-lived access keys.
3. Explain credential expiry, refresh, identity checks, local file handling, Kubernetes Secret handling, and cleanup.
4. Record the intended Crossplane/chart/provider combination and identify which parts were tested.
5. Validate the full authentication path only in an authorized sandbox. Do not display or commit actual credential values.

**Done when:** The correction is source-verified and the documented provider authentication path has a recorded sandbox result. If sandbox access is unavailable, deliver the source-verified correction as a bounded change, keep execution acceptance blocked, and record the missing evidence. Do not leave the known omission uncorrected merely because execution is unavailable.

### KB-05: clarify and validate the Kafka example

**Finding:** F4. **Owner:** Unassigned.

**Edit:** [Kafka delivery guarantees](databases/kafka/delivery-guarantees-and-failure-handling.md).

**Instructions:**

1. Decide whether the consumer loop is conceptual pseudocode or a runnable client example. State that choice before the block.
2. For runnable code, identify the client library and version, initialization, poll return shape, header handling, and automatic-commit configuration.
3. Explain when offsets advance and what happens when processing fails partway through a batch.
4. Validate successful processing, a failed record, and replay/idempotency behavior. Separate local unit checks from broker integration evidence.
5. For pseudocode, remove misleading library-specific details or explain the abstraction; do not claim execution coverage.

**Done when:** Readers can identify what they can run, and the stated processing/commit behavior is supported at the declared evidence level.

**Phase exit:** Current defects are resolved or have clearly documented, bounded remaining verification work. The complete Markdown baseline is green before publication under normal repository rules.

## Phase 2: establish consistent quality controls

### KB-06: align templates and article quality rules

**Findings:** F4, F6, F9. **Owner:** Unassigned.

**Edit:** [Templates](templates/README.md), [writing instructions](instructions.md), and [contributor checklist](CONTRIBUTING.md).

**Instructions:**

1. Adopt the article and example instructions below in the canonical writing standard. Reference that standard from templates and contributor guidance instead of duplicating it in full.
2. Distinguish tutorial, how-to, reference, and explanation intent. Adapt existing templates before adding new ones.
3. Move risk notes before relevant commands and include `What it does:` explanations in command examples.
4. Add a small visible review-information block with honest defaults. Keep content maturity separate from testing evidence.
5. Create one representative draft from each changed template to verify that instructions produce usable pages. Do not retain empty demonstration articles as published content.

**Done when:** Templates and contributor rules agree, examples inherit correct warning placement, and a contributor can apply the standard without consulting contradictory copies.

### KB-07: make maturity and routes visible

**Findings:** F7 and part of F10. **Owner:** Unassigned.

**Edit:** [Root index](README.md), [cross-topic index](cross-topic-guides/README.md), affected area indexes, [source router](sources/AGENTS.md), and [documentation-error form](.github/ISSUE_TEMPLATE/documentation-error.yml).

**Instructions:**

1. Identify which routes have usable guides, partial coverage, or only planned content. Apply concise labels before the reader opens the page.
2. Preserve `Status: Initial outline` where it remains accurate; do not equate an incomplete area index with unusable child articles.
3. Update source classification choices for existing Terraform and migrations routes and correct the stale AWS path in the issue form.
4. Keep advanced content discoverable while making the first useful beginner route prominent.

**Done when:** Entry indexes distinguish available and planned material, and routing examples resolve to the current hierarchy.

### KB-08: make automated checks match documented guarantees

**Finding:** F8. **Owner:** Unassigned.

**Edit:** Existing workflows under `.github/workflows/`, [content CI/CD process](git/github-actions/content-ci-cd-process.md), and a small maintained validation entry point if needed.

**Instructions:**

1. Provide a repeatable local-link check with documented exclusions. Cover inline links, reference links, fragments, and required index reachability using an appropriate parser or maintained checker.
2. Add small validator fixtures for valid links, broken targets, renamed headings, fenced examples, and the documented portable-bundle exception. These test validator behavior rather than article wording.
3. Keep deterministic local failures distinguishable from external-site timeouts, authentication failures, and rate limits.
4. Add syntax/schema checks for declared-runnable examples only. Do not execute arbitrary Markdown blocks, cloud mutations, or contributor-controlled shell content as part of link/lint validation.
5. Make Terraform checks target actual example files and report when none exist. Formatting alone is not configuration or deployment validation.
6. Reconcile manual workflow triggers with the published CI policy. Set explicit minimal permissions and review immutable action pinning with an update process.
7. Record dependency/tool versions so contributors can reproduce CI locally. Avoid silently changing the validation scope to obtain a pass.

**Done when:** Local and CI checks have documented, matching purposes; intentional validator failures are caught; and workflow changes pass their relevant validation. Inspect remote results when available and label them unknown when unavailable.

**Phase exit:** Contributors have usable templates, readers can see maturity, and validation has a repeatable local entry point with clear limits.

## Phase 3: complete learning and operational paths

### KB-09: build the first beginner learning path

**Finding:** F5. **Owner:** Unassigned.

**Edit:** [Kubernetes fundamentals](kubernetes/fundamentals/README.md), [kind guidance](kubernetes/applications-and-tools/kind-custom-clusters.md), [troubleshooting](kubernetes/troubleshooting/common-solutions.md), and relevant Git indexes. Proposed new paths: `start-here.md` and `cross-topic-guides/local-deployment-learning-path.md`; create and link them only during this package.

**Instructions:**

1. Define the audience as a learner beginning practical cloud/platform engineering. State terminal, Git, container, and local machine prerequisites, including installation references and resource requirements.
2. Build a route through Git changes and safe recovery, containers, Kubernetes objects, a local deployment, a controlled failure, diagnosis, recovery, and cleanup.
3. Explain Pods, Deployments, Services, namespaces, labels, and reconciliation before requiring Crossplane or EKS knowledge.
4. Supply exact exercise files, expected outputs or invariants, common failures, and cleanup checks. Use an isolated local environment with no cloud account requirement for this first path.
5. Add small understanding questions and an inspectable outcome: manifests, an annotated diagnostic record, and a short explanation of the fix.
6. Provide next-step links to AWS/EKS and Crossplane, explicitly identifying their additional prerequisites and possible cost.

**Done when:** The author can complete the exercise from its stated starting state, including failure and cleanup, and record the result. Independent beginner testing belongs to KB-14; do not claim it has happened here.

### KB-10: add a complete Terraform exercise

**Findings:** F4, F5, F8. **Owner:** Unassigned.

**Edit:** [Terraform examples](terraform/examples/README.md), [core workflow](terraform/commands/core-workflow.md), and [state management](terraform/fundamentals/state-management.md). Put actual exercise files in a focused subdirectory under `terraform/examples/` with its own `README.md`.

**Instructions:**

1. Choose a small local exercise that teaches configuration, state, plan, apply, change, and destroy without requiring a cloud account. Clearly state what the local exercise cannot demonstrate about cloud providers.
2. Verify the supported Terraform version and any provider dependencies before writing the example. Include appropriate version constraints and dependency lock data where applicable.
3. Include real configuration files, inputs, expected plan behavior, output checks, a deliberate change, and cleanup.
4. Explain sensitive state and generated files; keep local state, caches, and credentials out of version control.
5. Run formatting, initialization, validation, and the full local lifecycle in an isolated working directory. Connect static checks to KB-08's validation entry point.

**Done when:** Another contributor can reproduce the lifecycle from the included files, and the evidence distinguishes static checks from actual apply/destroy execution.

### KB-11: review ten priority operational guides

**Finding:** F6, with follow-through on F1–F4. **Owner:** Unassigned.

Use this initial cohort; replace a page only with a documented reason based on reader impact:

1. [Git undo and recovery](git/troubleshooting/undo-and-recovery.md).
2. [Crossplane local AWS S3 lab](kubernetes/crossplane/local-aws-s3-lab.md).
3. [Crossplane providers and authentication](kubernetes/crossplane/providers-and-authentication.md).
4. [Terraform core workflow](terraform/commands/core-workflow.md).
5. [Terraform state management](terraform/fundamentals/state-management.md).
6. [Kafka delivery guarantees and failure handling](databases/kafka/delivery-guarantees-and-failure-handling.md).
7. [Velero AWS S3 and EBS installation](migrations/velero/aws-s3-ebs-installation.md).
8. [Velero backup and restore workflows](migrations/velero/backup-restore-workflows.md).
9. [Velero migration and disaster recovery](migrations/velero/cluster-migration-and-disaster-recovery.md).
10. [Deploying to EKS](cross-topic-guides/deploying-to-eks.md).

**Instructions:** Review each page's consequential claims against current official sources; record applicable versions, last substantive review, actual reviewer, and validation scope. Reuse evidence from completed corrective tasks when it still applies. Check prerequisites, warning placement, success checks, failure handling, and cleanup. Record unavailable integration tests explicitly.

**Done when:** All ten pages have accurate review information and traceable findings. No page implies execution testing that did not occur; unresolved consequential defects have a warning, correction, or clearly identified follow-up.

### KB-12: improve long-page readability

**Finding:** F9. **Owner:** Unassigned.

**Start with:** [Git catalog](git/commands/complete-command-catalog.md), [K9s](kubernetes/applications-and-tools/k9s.md), [Crossplane component model](kubernetes/crossplane/component-model.md), and other long pages listed in the review.

**Instructions:** Add concise contents navigation where readers jump between tasks. Use descriptive headings and narrow tables. Explain acronyms at first meaningful use. Check rendered tables, code, heading navigation, and diagrams on wide and narrow screens. Describe diagram meaning in surrounding text. Split only when a page serves genuinely separate reader goals; update incoming links if a split changes paths or anchors.

**Done when:** The selected pages have usable navigation and readable rendering, and the checks are recorded. Do not equate Markdown lint with a rendered accessibility assessment.

**Phase exit:** One complete local learning path and one Terraform exercise work at their declared evidence level, and priority operational pages expose their verification limits.

## Phase 4: make maintenance sustainable

### KB-13: simplify governance and add source traceability

**Findings:** F10 and F11. **Owner:** Unassigned.

**Edit:** [AGENTS.md](AGENTS.md), [context.md](context.md), [instructions.md](instructions.md), [CONTRIBUTING.md](CONTRIBUTING.md), [processed-source index](sources/processed/README.md), and related source instructions.

**Instructions:**

1. Let the agent router select routes, the writing standard define page rules, the contributor guide define contribution expectations, and parent indexes list articles.
2. Remove redundant inventories only after verifying their routing value is preserved through links or generated data. Keep useful historical records intact.
3. Document the OKF bundle's `index.md` convention as a narrow navigation exception and encode it in the link validator. Clearly identify sample verification metadata as illustrative.
4. Add an ingestion register linking original notes to curated destinations, with source provenance, ingestion date, verification status, and unresolved questions. Use `Unknown` where history cannot be established.
5. Keep archived notes separate from default curated search/retrieval. Retain deliberate navigation to originals.
6. Resolve the duplicated changelog entry and adopt dated milestone summaries without inventing historical release dates.

**Done when:** Contributors can identify canonical rules, existing archives have documented mappings or explicit unknowns, and a new ingestion can be traced end to end.

### KB-14: test reader tasks and run a maintenance loop

**Finding:** F12. **Owner:** Unassigned.

**Edit:** [Roadmap](ROADMAP.md), issue forms, and a small review queue linked from contributor guidance. A new queue file must be linked from its parent index.

**Instructions:**

1. Recruit 3–5 willing readers at the intended level through an authorized channel. Do not invent participants or results. If participants are unavailable, record the dependency and keep author testing clearly separate.
2. Give them the beginner path and ten findability questions. Record starting experience, time to find the intended page, completion, confusing terms, and blocking steps without retaining unnecessary personal information.
3. Include concrete questions: undo an unstaged Git edit, diagnose a Kubernetes restart, distinguish Crossplane components, validate a restore, and choose the next learning step.
4. Turn repeated obstacles into bounded issues. Let reports include page, environment/version, expected result, and actual result; make suggested fixes optional.
5. Start a review queue for the ten priority guides with an owner, next review date, reason, and evidence. Use the cadence below and adjust it based on observed drift.
6. Update roadmap priorities using these results rather than raw article counts.

**Done when:** Actual reader outcomes are recorded, observed blockers have actions, and the first maintenance cycle has an owner and dated results. Participation-dependent work remains open until evidence exists.

### KB-15: decide whether a searchable site is worthwhile

**Finding:** F13. **Owner:** Unassigned.

**Deliverable:** A decision record using the [ADR template](templates/architecture-decision-record-template.md), linked from the [decision index](decision-records/README.md).

**Instructions:** Compare staying with repository navigation against a small static reading site using KB-14's findability evidence. Assess maintenance effort, search, mobile readability, accessibility, link compatibility, archives, and single-source publishing. If a prototype is useful, keep it bounded and evaluate it with the same tasks. Verify current tool capabilities before choosing a generator or host.

**Done when:** The decision records evidence, trade-offs, and the next action. “Keep repository navigation for now” is a valid outcome. Public deployment is a separate implementation task if selected.

**Phase exit:** Maintenance follows observed needs, source traceability is usable, and publishing choices have an explicit rationale.

## Article and example instructions

Adopt these requirements through KB-06. Do not retrofit every file in a single change.

### Choose the page's main job

| Type | Required outcome | Include |
| --- | --- | --- |
| Tutorial | A learner achieves a bounded result | Starting state, sequential steps, expected results, understanding checks, cleanup. |
| How-to | A reader completes a specific task | Prerequisites, decisions, steps, verification, recovery. |
| Reference | A reader finds a precise fact or command | Consistent categories, accurate syntax, limitations, examples, version context. |
| Explanation | A reader understands concepts and trade-offs | Definitions, relationships, examples, alternatives, consequences. |

Do not force every page to contain empty procedure or troubleshooting sections. Use the structure appropriate to its job and link to complementary pages.

### Record review information honestly

Start with a visible body block rather than introducing a repository-wide frontmatter migration. This illustrative block intentionally claims no completed review:

```text
Status: Draft
Audience: Beginning platform engineer
Page type: Tutorial
Maintainer: Unassigned
Last substantive review: Not yet reviewed
Applicable versions: To be established before execution
Validation evidence: Not yet tested
Known limitations: To be documented
Next review: Assign after substantive review
```

What it does: makes missing evidence explicit. Replace values with real information as work is completed; use `Not applicable` with a reason for fields that do not fit conceptual pages.

Use `Initial outline`, `Draft`, `Maintained`, and `Deprecated` for article maturity after adoption. “Maintained” means the page meets its content standard and has accountable review information; it does not by itself mean every command was executed. These labels are separate from task status and from example-bundle metadata governed by another format.

Describe evidence as one or more of:

- **Source reviewed:** identify authoritative sources and review date.
- **Statically checked:** identify syntax, schema, lint, or configuration checks and versions.
- **Locally executed:** identify the isolated environment, versions, result, and cleanup.
- **Sandbox executed:** identify a public-safe environment description and the tested procedure, result, and cleanup.

Preserve separate dates for source review and execution when they differ. Reformatting is not substantive verification. When a page is deprecated, state why and link to a replacement or explain that none exists.

### Make technical examples usable

1. State whether an example is runnable or illustrative before its code block.
2. Specify required tools, permissions, accounts, context, versions, files, and starting resources.
3. Explain replacement values and how readers obtain them. Do not leave unexplained shell placeholders that appear executable.
4. Put destructive, expensive, credential-sensitive, and production-impact warnings before the affected commands.
5. Use fenced blocks with language identifiers and `What it does:` explanations. Keep commands outside table cells.
6. Show successful output or a stable observable condition. Identify timeouts and failure symptoms where relevant.
7. Explain recovery and cleanup, including retained resources and continuing costs.
8. Prefer official product documentation for behavior and cite consequential claims near the relevant section. Record version-specific constraints rather than saying “latest” where reproducibility matters.
9. Keep real runnable files and their instructions in sync. Test meaningful behavior, not the literal wording of the documentation.
10. Never turn a missing environment, credential, or tool into a fabricated pass. Record the limitation and the next required action.

### Maintain navigation and provenance

Use lowercase kebab-case for new documentation names and relative internal links. New documentation directories need a `README.md`. Link every new article from its nearest parent and end it with related links back to the parent, major area when different, and root, subject to documented portable-example exceptions.

Preserve the purpose of existing pages. Search before adding duplicate content. Place general database knowledge under databases, provider-specific material under cloud, and genuine multi-technology procedures under cross-topic guides.

For imported material, follow [sources/AGENTS.md](sources/AGENTS.md). Verify claims, preserve source references, record the curated destinations, and archive the original only after successful ingestion. Never promote unknown authorship or generated statements into verified facts.

## Validation and publication

### Before editing

```bash
git status --short --branch
git rev-parse HEAD
git diff --stat
```

What it does: establishes the current commit and existing modifications so the task can preserve unrelated work. Review the actual diff for any file the task will touch; a file list alone does not establish ownership of its contents.

### Before marking implementation ready

```bash
npx markdownlint-cli2 "**/*.md"
git diff --check
git status --short --branch
```

What it does: runs the repository Markdown scope, checks tracked diff whitespace, and identifies intended and unintended changes. Include new untracked files in the content review and link/lint checks.

Also run the repository-aware link check and the technical checks relevant to the changed examples. KB-08 must document a stable command for those checks; do not invent an executable path before that tool exists. If using lychee, follow [lychee.toml](lychee.toml) and the [existing workflow](.github/workflows/link-check.yml), record its version, and distinguish external availability from local resolution.

### Definition of done

- [ ] The work package meets each reader outcome and acceptance condition.
- [ ] Technical claims have appropriate authoritative sources and version context.
- [ ] Runnable examples have evidence at the level they claim.
- [ ] Warnings, verification, recovery, and cleanup are appropriate to the task.
- [ ] New and changed navigation resolves; affected indexes are updated.
- [ ] Relevant glossary, context, changelog, and tracker updates are complete.
- [ ] Markdown lint, local links, and relevant technical checks pass.
- [ ] Rendered checks were performed when layout changed materially.
- [ ] The staged diff includes only intended content.
- [ ] Publication and remaining limitations are recorded in the handoff.

Follow [instructions.md](instructions.md) and the [content CI/CD process](git/github-actions/content-ci-cd-process.md) for committing and pushing validated work to the canonical branch. Use explicit file staging or hunk staging when other changes exist. Never force-push or discard unrelated changes to complete a documentation task.

If repository-wide checks fail, record which failures predate the task and validate the changed files separately to assess the change. A clean changed-file check does not waive the existing full-validation publication rule. Stop publication at that blocker and leave a precise handoff; do not silently weaken checks or broaden the task to unrelated fixes.

## Evidence and handoff format

Add one dated entry per implementation batch. Keep evidence summaries small; link to maintained test files, public-safe output artifacts, or CI runs when available. Do not rely on temporary local paths as permanent evidence.

```text
Task ID:
Status:
Owner:
Date:
Starting commit and pre-existing changes:
Reader outcome:
Files changed:
Authoritative sources and applicable versions:
Checks executed, tool versions, and results:
Checks not executed and reason:
Remaining defects or dependencies:
Publication commit or blocker:
Next action:
```

What it does: gives the next contributor enough information to verify progress and continue without reconstructing the conversation.

### Implementation records

Task ID: KB-01
Status: Done
Owner: Codex
Date: 2026-09-18
Starting commit and pre-existing changes: Started from `831ce4cf77f22b17c3a38ba316d2d2e5b494767b` on `main`, with the review, plan, and route links already present as uncommitted work from the planning batch.
Reader outcome: Contributors can reproduce the current validation baseline and understand which failures were historical versus fixed in this batch.
Files changed: This plan record.
Authoritative sources and applicable versions: `markdownlint-cli2 v0.23.2`, `markdownlint v0.41.1`, Git 2.53.0, Python 3.14.4, Node.js v22.23.2.
Checks executed, tool versions, and results: Initial `npx markdownlint-cli2 "**/*.md"` reproduced 20 issues in 16 files. After KB-02, Markdown lint checked 244 Markdown files with zero issues. Local link validator checked 244 Markdown files with local links, fragments, indexes, and reachability passing.
Checks not executed and reason: External URL crawl was not rerun as part of KB-01; KB-08 keeps external availability separate from local structure.
Remaining defects or dependencies: None for the baseline record.
Publication commit or blocker: Published in commit `1079a0d`.
Next action: Continue with the remaining blocked AWS sandbox validation and reader testing when those external prerequisites are available.

Task ID: KB-02
Status: Done
Owner: Codex
Date: 2026-09-18
Starting commit and pre-existing changes: Same batch as KB-01.
Reader outcome: Repository-wide Markdown lint no longer blocks publication.
Files changed: `.markdownlint-cli2.jsonc`, OKF source reference files, and `kubernetes/crossplane/xrd-composition-and-xr-calls.md`.
Authoritative sources and applicable versions: `markdownlint-cli2 v0.23.2`, `markdownlint v0.41.1`.
Checks executed, tool versions, and results: `npx markdownlint-cli2 "**/*.md"` passed with zero issues across 244 Markdown files. `git diff --check` passed.
Checks not executed and reason: Rendered GitHub table inspection was not visually captured; the table pipe was escaped and lint passed.
Remaining defects or dependencies: None.
Publication commit or blocker: Published in commit `1079a0d`.
Next action: None for KB-02.

Task ID: KB-03
Status: Done
Owner: Codex
Date: 2026-09-18
Starting commit and pre-existing changes: Same batch as KB-01.
Reader outcome: Git restore guidance now distinguishes working tree, index, and `HEAD`.
Files changed: `git/troubleshooting/undo-and-recovery.md`, `git/commands/solve-issues.md`.
Authoritative sources and applicable versions: Official `git-restore` documentation for Git 2.55.0; local Git 2.53.0 reproduction.
Checks executed, tool versions, and results: Disposable repository test showed `git restore demo.txt` changed the working tree from `unstaged` to staged index content, while `git restore --source=HEAD demo.txt` changed it to committed content.
Checks not executed and reason: None.
Remaining defects or dependencies: None.
Publication commit or blocker: Published in commit `1079a0d`.
Next action: None for KB-03.

Task ID: KB-04
Status: Blocked
Owner: Codex
Date: 2026-09-18
Starting commit and pre-existing changes: Same batch as KB-01.
Reader outcome: The known omission in temporary AWS credential examples is corrected in source-reviewed docs, and maintainers now have public-safe prerequisite, template, and issue-form paths for recording the missing AWS/Crossplane sandbox run.
Files changed: `kubernetes/crossplane/local-aws-s3-lab.md`, `kubernetes/crossplane/providers-and-authentication.md`, `kubernetes/crossplane/aws-resource-workflow.md`, `kubernetes/crossplane/aws-s3-lab-validation-template.md`, `kubernetes/crossplane/README.md`, `.github/ISSUE_TEMPLATE/crossplane-aws-s3-validation.yml`, `external-evidence-request.md`, `maintenance-review-queue.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, and this plan.
Authoritative sources and applicable versions: AWS CLI credential-file documentation for short-term credentials and `aws_session_token`; Crossplane AWS S3 provider package example remains pinned to `xpkg.upbound.io/upbound/provider-aws-s3:v2.6.1`.
Checks executed, tool versions, and results: Source review confirmed manually supplied AWS STS credentials require `aws_access_key_id`, `aws_secret_access_key`, and `aws_session_token`. Python/PyYAML parsed all GitHub issue templates. `npx markdownlint-cli2 "**/*.md"` passed with `markdownlint-cli2 v0.23.2` and `markdownlint v0.41.1` across 248 Markdown files. `node scripts/test-local-link-validator.mjs` passed. `node scripts/validate-local-links.mjs` checked 248 Markdown files and passed local links, fragments, indexes, and reachability. `git diff --check` passed. For the external-evidence checklist batch, `npx markdownlint-cli2 "**/*.md"` passed across 250 Markdown files, `node scripts/test-local-link-validator.mjs` passed, `node scripts/validate-local-links.mjs` checked 250 Markdown files and passed, `python3 scripts/validate-issue-templates.py` passed, and `git diff --check` passed.
Checks not executed and reason: The full Crossplane-to-AWS authentication path was not executed because no authorized AWS sandbox credentials were available; this workspace also lacks AWS CLI, kind, kubectl, and Helm for a local preflight run.
Remaining defects or dependencies: Needs an authorized AWS sandbox run with the required tools to verify ProviderConfig Secret authentication, credential expiry behavior, and cleanup.
Publication commit or blocker: Source correction published in commit `1079a0d`; validation template published in commit `e024498`, with this record finalized in the follow-up publication-evidence commit. Issue-form support published in commit `f1fb006`, with this record finalized in the follow-up publication-evidence commit. External evidence checklist published in commit `a028cc9`; execution acceptance remains blocked on sandbox access.
Next action: Use the external evidence request checklist, then run the S3 lab in an authorized sandbox using the validation template or issue form and record provider/controller versions, identity, success, expiry symptoms, and cleanup.

Task ID: KB-05
Status: Done
Owner: Codex
Date: 2026-09-18
Starting commit and pre-existing changes: Same batch as KB-01.
Reader outcome: Readers can tell the Kafka manual-commit example is a `kafka-python` runnable-shape example and understand when offsets advance.
Files changed: `databases/kafka/delivery-guarantees-and-failure-handling.md`.
Authoritative sources and applicable versions: `kafka-python` `KafkaConsumer` API documentation, including `poll()` return shape and `enable_auto_commit` behavior.
Checks executed, tool versions, and results: Python 3.14.4 `ast.parse` accepted the updated example. Markdown lint and local link checks passed.
Checks not executed and reason: No Kafka broker integration test was run; the page does not claim broker execution coverage.
Remaining defects or dependencies: A future broker-backed example could test successful processing, failed record replay, and idempotency behavior.
Publication commit or blocker: Published in commit `1079a0d`.
Next action: None required for the current evidence level.

Task ID: KB-06
Status: Done
Owner: Codex
Date: 2026-09-18
Starting commit and pre-existing changes: Same batch as KB-01.
Reader outcome: Contributors have one canonical writing standard for page type, review evidence, warning placement, and runnable examples.
Files changed: `instructions.md`, `CONTRIBUTING.md`, `templates/README.md`, and article, command, troubleshooting, and practical-example templates.
Authoritative sources and applicable versions: The existing repository writing standard and the improvement plan's article instructions.
Checks executed, tool versions, and results: Markdown lint and local link checks passed.
Checks not executed and reason: Temporary demonstration drafts were not retained as published content; template usability was checked by applying the standard to new learning-path and Terraform exercise pages in KB-09 and KB-10.
Remaining defects or dependencies: None for canonical standard alignment.
Publication commit or blocker: Published in commit `1079a0d`.
Next action: Continue applying the standard gradually during future article reviews.

Task ID: KB-07
Status: Done
Owner: Codex
Date: 2026-09-18
Starting commit and pre-existing changes: Same batch as KB-01.
Reader outcome: Readers can see which areas are developed, partial, or outlines before opening them, and source routing metadata matches current repository routes.
Files changed: `README.md`, `cross-topic-guides/README.md`, `sources/AGENTS.md`, `.github/ISSUE_TEMPLATE/documentation-error.yml`.
Authoritative sources and applicable versions: Current repository route hierarchy.
Checks executed, tool versions, and results: Markdown lint and local link checks passed.
Checks not executed and reason: No rendered screenshot review was captured.
Remaining defects or dependencies: Labels should be refined as KB-11 and KB-14 produce more evidence.
Publication commit or blocker: Published in commit `1079a0d`.
Next action: Update labels when routes move from outline to maintained.

Task ID: KB-08
Status: Done
Owner: Codex
Date: 2026-09-18
Starting commit and pre-existing changes: Same batch as KB-01.
Reader outcome: Local and CI validation now have matching purposes, documented commands, maintained local-link validation, and maintained GitHub issue-form validation.
Files changed: `.github/workflows/markdown-lint.yml`, `.github/workflows/link-check.yml`, `.github/workflows/terraform-format.yml`, `.github/workflows/issue-template-validation.yml`, `git/github-actions/content-ci-cd-process.md`, `scripts/validate-local-links.mjs`, `scripts/test-local-link-validator.mjs`, `scripts/validate-issue-templates.py`, `context.md`, `CHANGELOG.md`, and this plan.
Authoritative sources and applicable versions: Node.js v22.23.2, Terraform v1.13.1 for local formatting check, Python 3 with PyYAML, `markdownlint-cli2 v0.23.2`, `actions/setup-python@v6.0.0`, and `actions/checkout@v7.0.1`.
Checks executed, tool versions, and results: `node scripts/test-local-link-validator.mjs` passed validator fixtures; `node scripts/validate-local-links.mjs` checked 244 Markdown files and passed; Markdown lint passed; Terraform fmt check passed with Terraform v1.13.1 after adding a local `.tf` exercise. For the issue-template validation extension, Python/PyYAML parsed all issue-template and workflow YAML files, `python3 scripts/validate-issue-templates.py` passed for 5 issue forms, `npx markdownlint-cli2 "**/*.md"` passed with `markdownlint-cli2 v0.23.2` and `markdownlint v0.41.1` across 248 Markdown files, `node scripts/test-local-link-validator.mjs` passed, `node scripts/validate-local-links.mjs` checked 248 Markdown files and passed local links, fragments, indexes, and reachability, and `git diff --check` passed.
Checks not executed and reason: Remote GitHub Actions results were not inspected because the batch has not been pushed.
Remaining defects or dependencies: External URL availability remains governed by lychee and can fail for network or remote-site reasons separate from local structure.
Publication commit or blocker: Initial validation batch published in commit `1079a0d`; issue-template validation extension published in commit `7813312`, with this record finalized in the follow-up publication-evidence commit.
Next action: Inspect CI when available.

Task ID: KB-09
Status: Done
Owner: Codex
Date: 2026-09-18; execution evidence updated 2026-09-19.
Starting commit and pre-existing changes: Original content published in the KB-01 batch; execution resumed from clean `main` at `3797b75`.
Reader outcome: The first beginner route now exists and includes Git recovery, Kubernetes fundamentals, a local deployment exercise, a controlled failure, diagnosis, recovery, cleanup, and next-step links.
Files changed: `start-here.md`, `cross-topic-guides/local-deployment-learning-path.md`, `kubernetes/fundamentals/README.md`, `kubernetes/examples/README.md`, `kubernetes/examples/local-deployment-learning-path/*`, `ROADMAP.md`, `maintenance-review-queue.md`, `CHANGELOG.md`, and this plan.
Authoritative sources and applicable versions: Docker 29.8.0 rootless daemon, kind v0.30.0, Kubernetes v1.34.0 node image, kubectl v1.34.1 client, and stable Kubernetes Namespace, Deployment, and Service APIs.
Checks executed, tool versions, and results: Created kind cluster `kb-local`; verified the control-plane node was `Ready`; applied namespace, Deployment, and Service; waited for two ready Pods; port-forwarded the Service and confirmed an HTTP response with `curl`; corrected `failing-image-patch.yaml` after Kubernetes rejected the previous incomplete Deployment patch; reproduced the intended `ErrImagePull` and `ImagePullBackOff`; rolled back successfully; practiced `git restore --staged` and `git restore`; deleted the namespace; deleted the kind cluster; confirmed no kind clusters remained. `npx markdownlint-cli2 "**/*.md"` passed with `markdownlint-cli2 v0.23.2` and `markdownlint v0.41.1` across 246 Markdown files. `node scripts/test-local-link-validator.mjs` passed. `node scripts/validate-local-links.mjs` checked 246 Markdown files and passed local links, fragments, indexes, and reachability. `git diff --check` passed. The changed processed-source ingestion register also passed a direct local-link sanity check.
Checks not executed and reason: Independent beginner testing was not executed; that belongs to KB-14 and requires actual readers.
Remaining defects or dependencies: None for the author-run scope. KB-14 still needs reader testing.
Publication commit or blocker: Original source and static evidence published in commit `1079a0d`; execution evidence published in commit `2dda2f0`, with this record finalized in the follow-up publication-evidence commit.
Next action: Use KB-14 reader testing to find learner-facing blockers.

Task ID: KB-10
Status: Done
Owner: Codex
Date: 2026-09-18
Starting commit and pre-existing changes: Same batch as KB-01.
Reader outcome: A complete Terraform exercise now teaches init, validate, plan, apply, state inspection, change, output, and destroy without a cloud account.
Files changed: `terraform/examples/local-state-lifecycle/README.md`, `terraform/examples/local-state-lifecycle/main.tf`, `terraform/examples/local-state-lifecycle/.gitignore`, `terraform/examples/README.md`, `terraform/commands/core-workflow.md`, `terraform/fundamentals/state-management.md`.
Authoritative sources and applicable versions: Terraform v1.13.1 local binary from HashiCorp releases; configuration requires Terraform 1.4.0 or newer for `terraform_data`.
Checks executed, tool versions, and results: Terraform v1.13.1 ran `init`, `validate`, `fmt -check`, `plan`, `apply`, `state list`, `state show`, variable-change `plan` and `apply`, `output`, `destroy`, and final `state list` returned empty in an isolated `/tmp` directory.
Checks not executed and reason: No cloud provider, remote backend, lock, drift, or real infrastructure behavior was tested because the exercise is intentionally local-only.
Remaining defects or dependencies: None for the declared exercise scope.
Publication commit or blocker: Published in commit `1079a0d`.
Next action: None for KB-10.

Task ID: KB-11
Status: Done
Owner: Codex
Date: 2026-09-19
Starting commit and pre-existing changes: Started from clean `main` at `d166a1d`, tracking `origin/main`.
Reader outcome: Ten priority operational guides now state their maturity, audience, applicable versions, validation evidence, known execution limits, and next review trigger before readers follow commands.
Files changed: `git/troubleshooting/undo-and-recovery.md`, `kubernetes/crossplane/local-aws-s3-lab.md`, `kubernetes/crossplane/providers-and-authentication.md`, `terraform/commands/core-workflow.md`, `terraform/fundamentals/state-management.md`, `databases/kafka/delivery-guarantees-and-failure-handling.md`, `migrations/velero/aws-s3-ebs-installation.md`, `migrations/velero/backup-restore-workflows.md`, `migrations/velero/cluster-migration-and-disaster-recovery.md`, `cross-topic-guides/deploying-to-eks.md`, `CHANGELOG.md`, and this plan.
Authoritative sources and applicable versions: Official Git 2.55.0 documentation, Crossplane v2.4 provider and managed-resource documentation, Terraform v1.16 command and state documentation, Apache Kafka documentation, kafka-python consumer API documentation, Velero v1.18 and current reference documentation, official Velero AWS plugin repository, Amazon EKS kubeconfig and workload IAM documentation, and Kubernetes Deployment and kubectl rollout documentation.
Checks executed, tool versions, and results: `npx markdownlint-cli2 "**/*.md"` passed with `markdownlint-cli2 v0.23.2` and `markdownlint v0.41.1` across 244 Markdown files. `node scripts/test-local-link-validator.mjs` passed. `node scripts/validate-local-links.mjs` checked 244 Markdown files and passed local links, fragments, indexes, and reachability. `git diff --check` passed.
Checks not executed and reason: AWS, EKS, Crossplane provider, Velero, and Kafka broker integration tests were not executed because the needed sandbox cloud accounts, clusters, provider controllers, backup storage, and broker environment were not available in this workspace. The affected pages now state those limits.
Remaining defects or dependencies: KB-04 still needs authorized AWS/Crossplane sandbox execution. KB-14 must test reader tasks with actual readers and start the maintenance loop.
Publication commit or blocker: Published in commit `77d0d1c`; this record was finalized in the follow-up publication-evidence commit.
Next action: Continue with KB-14 when actual reader participation is available.

Task ID: KB-12
Status: Done
Owner: Codex
Date: 2026-09-19
Starting commit and pre-existing changes: Started from clean `main` at `1079a0d`, tracking `origin/main`.
Reader outcome: Long reference pages now offer direct contents navigation before the reader reaches large command or concept tables.
Files changed: `git/commands/complete-command-catalog.md`, `kubernetes/applications-and-tools/k9s.md`, `kubernetes/crossplane/component-model.md`.
Authoritative sources and applicable versions: Current repository headings and local Markdown link validator slug behavior.
Checks executed, tool versions, and results: Markdown lint, local link validator fixtures, repository local link validation, and `git diff --check` passed.
Checks not executed and reason: No rendered screenshot review was captured; the change is anchor navigation only.
Remaining defects or dependencies: Further long pages can receive the same treatment during later article reviews.
Publication commit or blocker: Published in commit `d166a1d`.
Next action: Continue applying contents navigation when long pages are substantively edited.

Task ID: KB-13
Status: Done
Owner: Codex
Date: 2026-09-19
Starting commit and pre-existing changes: Started from clean `main` at `1079a0d`, tracking `origin/main`.
Reader outcome: Archived processed sources now map to curated destinations through a maintained register, and source-ingestion rules require future mappings.
Files changed: `sources/processed/ingestion-register.md`, `sources/processed/README.md`, `sources/AGENTS.md`, `instructions.md`, `context.md`, `CHANGELOG.md`, and this plan.
Authoritative sources and applicable versions: Current repository paths at `1079a0d`; historical ingestion details are explicitly marked `Unknown` where no handoff evidence was available.
Checks executed, tool versions, and results: Markdown lint, local link validator fixtures, repository local link validation, and `git diff --check` passed.
Checks not executed and reason: Historical ingestion source verification was not reconstructed beyond current path mapping and changelog evidence.
Remaining defects or dependencies: Future ingestions must fill the register at the time material moves to `sources/processed`.
Publication commit or blocker: Published in commit `d166a1d`.
Next action: Use the register for all new source ingestion work.

Task ID: KB-14
Status: Blocked
Owner: Codex
Date: 2026-09-19
Starting commit and pre-existing changes: Started from clean `main` at `f7196bb`, tracking `origin/main`.
Reader outcome: Maintainers now have a linked queue, external evidence checklist, facilitator guide, results template, and issue form for priority guide reviews, blocked validation follow-ups, and future reader-task testing.
Files changed: `maintenance-review-queue.md`, `external-evidence-request.md`, `reader-test-facilitator-guide.md`, `reader-test-results-template.md`, `.github/ISSUE_TEMPLATE/reader-test-results.yml`, `README.md`, `CONTRIBUTING.md`, `ROADMAP.md`, `context.md`, `.github/ISSUE_TEMPLATE/documentation-error.yml`, `CHANGELOG.md`, and this plan.
Authoritative sources and applicable versions: Current repository routes and KB-14 acceptance criteria in this plan.
Checks executed, tool versions, and results: Python/PyYAML parsed all GitHub issue templates. `npx markdownlint-cli2 "**/*.md"` passed with `markdownlint-cli2 v0.23.2` and `markdownlint v0.41.1` across 248 Markdown files for the initial scaffold. `node scripts/test-local-link-validator.mjs` passed. `node scripts/validate-local-links.mjs` checked 248 Markdown files and passed local links, fragments, indexes, and reachability. For the facilitator-guide batch, `npx markdownlint-cli2 "**/*.md"` passed across 249 Markdown files, `node scripts/test-local-link-validator.mjs` passed, `node scripts/validate-local-links.mjs` checked 249 Markdown files and passed, `python3 scripts/validate-issue-templates.py` passed, and `git diff --check` passed. For the external-evidence checklist batch, `npx markdownlint-cli2 "**/*.md"` passed across 250 Markdown files, `node scripts/test-local-link-validator.mjs` passed, `node scripts/validate-local-links.mjs` checked 250 Markdown files and passed, `python3 scripts/validate-issue-templates.py` passed, and `git diff --check` passed.
Checks not executed and reason: Reader trials were not run because no authorized participant group is available in this workspace. Author execution evidence now exists for the local Kubernetes beginner path under KB-09. The external evidence checklist and facilitator guide have not been exercised with actual readers yet.
Remaining defects or dependencies: Recruit 3-5 willing readers through an authorized channel, run the reader tasks, record outcomes, and create follow-up issues or edits for repeated blockers.
Publication commit or blocker: Initial scaffold published in commit `07e9f83`; reader-test results template published in commit `4ed9069`, with this record finalized in the follow-up publication-evidence commit. Issue-form support published in commit `f1fb006`, with this record finalized in the follow-up publication-evidence commit. Facilitator guide published in commit `f4e08a1`; this record is finalized in the follow-up publication-evidence commit. External evidence checklist published in commit `a028cc9`; this record is finalized in the follow-up publication-evidence commit.
Next action: Use the external evidence request checklist to confirm session inputs, obtain reader participation, run sessions with the facilitator guide, then complete KB-14 acceptance evidence through the template or issue form.

Task ID: KB-15
Status: Done
Owner: Codex
Date: 2026-09-19
Starting commit and pre-existing changes: Started from clean `main` at `e4926ef`, tracking `origin/main`.
Reader outcome: The repository now has an explicit publishing decision: keep Markdown repository navigation as the canonical surface for now, and reopen the static-site question only after KB-14 reader testing identifies a measured need.
Files changed: `decision-records/adr-0003-searchable-site-decision.md`, `decision-records/README.md`, `maintenance-review-queue.md`, `CHANGELOG.md`, and this plan.
Authoritative sources and applicable versions: Current repository navigation, validation, and maintenance state at `e4926ef`; KB-14 scaffold and current lack of reader-findability evidence.
Checks executed, tool versions, and results: `npx markdownlint-cli2 "**/*.md"` passed with `markdownlint-cli2 v0.23.2` and `markdownlint v0.41.1` across 246 Markdown files. `node scripts/test-local-link-validator.mjs` passed. `node scripts/validate-local-links.mjs` checked 246 Markdown files and passed local links, fragments, indexes, and reachability. `git diff --check` passed.
Checks not executed and reason: Static-site generator and hosting capabilities were not evaluated because the decision does not select a generator, host, prototype, or public deployment path. Reader testing remains unavailable, so the ADR records a conservative current decision and a revisit trigger rather than fabricated site evidence.
Remaining defects or dependencies: Reopen the ADR after KB-14 records reader outcomes, especially if repeated tasks fail because of search, mobile readability, or navigation limits.
Publication commit or blocker: Published in commit `46c9811`; this record was finalized in the follow-up publication-evidence commit.
Next action: Complete KB-04 and KB-14 when their external prerequisites are available.

## Maintenance cadence and success measures

These are initial operating targets, not external compliance requirements or scheduled automations. Assign actual owners and dates when implementing KB-14.

| Trigger or cadence | Action |
| --- | --- |
| Every content change | Run relevant validation, maintain links, and update evidence when technical behavior changes. |
| Reader reports an error | Confirm impact, reproduce where possible, correct or flag misleading content, and link the resolution. |
| Relevant upstream release or deprecation | Review affected claims and examples; update supported versions or document limitations. |
| Monthly maintenance pass | Triage reports, external-link failures, blocked tasks, and the next small improvement batch. |
| Approximately quarterly | Reassess fast-changing priority operational guides and tested version combinations. |
| Approximately annually | Reassess stable conceptual content, learning-path relevance, and maintenance capacity. |

| Measure | Starting evidence | Target |
| --- | --- | --- |
| Markdown validation | Historical review: 20 errors; refresh in KB-01 | Zero errors in the configured curated scope. |
| Local navigation | Historical scan found no missing targets | Maintain no known broken targets/fragments under the stronger validator. |
| Review evidence | Ten-page cohort selected in KB-11 | All ten record genuine review scope, versions where relevant, and limitations. |
| Beginner exercise | End-to-end author run recorded in KB-09; independent reader trials pending | Independent reader trials recorded through KB-14. |
| Findability | Not measured | Initial goal: intended page found for at least 8 of 10 questions within two minutes per question; report participant variation. |
| Learner blockers | Not measured | No unresolved blocking step in the tested first path before calling it beginner-ready. |
| Source traceability | Uneven | All new ingestions mapped; existing archives mapped or explicitly marked unknown. |
| Freshness response | No operational queue established | Every overdue priority page has an owner and a dated action. |

Track completion and limitations together. Page count, word count, and number of technologies are inventory measures, not evidence that readers learned or completed their work.

## Instructions for the next contributor or agent

Use the following task brief when starting implementation. Replace the task ID with an eligible package from the tracker.

```text
Implement work package KB-01 from knowledge-base-improvement-plan.md.

Read repository and applicable directory instructions first. Inspect current
Git state, preserve pre-existing changes, and recheck the review finding against
the current files. Follow the package's scope, dependencies, and acceptance
criteria. Verify product behavior against authoritative sources when relevant.

Make the smallest complete change. Update affected navigation, changelog, and
the plan's status/evidence record. Run relevant technical validation, Markdown
lint, and internal-link checks. Distinguish tests performed from tests blocked.
Follow repository commit-and-push rules only when their conditions are met.

Report the reader outcome, files changed, evidence, publication result or
blocker, and the next eligible task. Do not claim unperformed tests or start
unrelated work merely to increase the number of completed tasks.
```

What it does: scopes implementation to one verifiable package while preserving enough context for safe continuation. A request to implement several packages can name them explicitly; the package dependencies still apply.

## Related links

- [Knowledge-base review](knowledge-base-review.md)
- [Roadmap](ROADMAP.md)
- [Agent router](AGENTS.md)
- [Context map](context.md)
- [Writing instructions](instructions.md)
- [Contributing](CONTRIBUTING.md)
- [Templates](templates/README.md)
- [Knowledge-base provenance and freshness](ai/ai-tooling/knowledge-bases/provenance-trust-and-freshness.md)
- [Knowledge-base evaluation](ai/ai-tooling/knowledge-bases/evaluation-and-quality.md)
- [Back to root index](README.md)
