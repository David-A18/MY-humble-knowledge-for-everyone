# Knowledge-base review

Review date: 2026-09-18

Baseline: `831ce4cf77f22b17c3a38ba316d2d2e5b494767b` on `main`, before adding this report.

## Purpose

Assess how well this repository helps people learn engineering, understand technical decisions, and perform practical work. Identify what to preserve, what needs correction, and where limited maintenance time will produce the greatest benefit.

This is a repository-wide documentation review: structural checks cover the tracked Markdown corpus; editorial and technical assessment uses representative articles and targeted source verification. It is not a claim that every command, product statement, or cloud deployment has been independently tested.

## Contents

- [Overall assessment](#overall-assessment)
- [Scope and method](#scope-and-method)
- [Repository inventory](#repository-inventory)
- [What is working well](#what-is-working-well)
- [Coverage by knowledge area](#coverage-by-knowledge-area)
- [Priority findings](#priority-findings)
- [Recommended reader experience](#recommended-reader-experience)
- [Recommended article contract](#recommended-article-contract)
- [Maintenance and contribution model](#maintenance-and-contribution-model)
- [Implementation sequence](#implementation-sequence)
- [Success measures](#success-measures)
- [Validation results and limitations](#validation-results-and-limitations)
- [Related links](#related-links)

## Overall assessment

The repository already provides useful engineering knowledge. Its strongest feature is its operational perspective: many pages explain decisions, failure modes, identity boundaries, diagnostics, and recovery instead of merely listing definitions. The topic hierarchy, relative links, templates, glossary, source intake process, and contributor instructions give it a sound foundation.

Its current shape is closer to an expanding engineering reference library than a guided learning resource. Someone who already knows to search for Crossplane, Velero, EKS, Kafka, or Git recovery can find substantial material. Someone who needs to learn the prerequisites, choose a first exercise, or know whether a procedure was tested faces more uncertainty.

The next investment should be in completing reader journeys and making reliability visible. Adding more top-level topics would increase the maintenance burden before addressing those needs.

| Dimension | Assessment | Main reason |
| --- | --- | --- |
| Topic organization | Strong foundation | Predictable directories and extensive index coverage. |
| Practical reference value | Strong in selected areas | Detailed Kubernetes, Crossplane, Velero, and Git material. |
| Beginner learning experience | Developing | Several foundations are outlines; no root-level guided curriculum. |
| Technical trust | Needs improvement | Useful references coexist with specific errors and uneven verification evidence. |
| Reproducible exercises | Developing | Some good labs, but no general contract for tested versions and executable examples. |
| Automated quality controls | Partial, with a failing baseline | Lint and link workflows exist; local lint currently fails. |
| Freshness and ownership | Developing | Maintenance is described, but article-level review evidence is not consistently implemented. |
| Public participation | Good foundation | License, contribution guide, and issue forms are present. |

These judgments are qualitative. They are not certification scores or measured learner outcomes.

## Scope and method

The review followed the repository's [agent router](AGENTS.md), [context map](context.md), [writing instructions](instructions.md), and [contribution guide](CONTRIBUTING.md). It also inspected the roadmap, glossary, changelog, templates, source ingestion rules, repository workflows, lint configuration, and link-check configuration.

The assessment combined:

1. A tracked-file inventory and automated scans of Markdown structure, outline markers, navigation links, frontmatter, page lengths, and example assets.
2. A fence-aware local link scan over the curated validation scope, plus a heading-fragment check.
3. Reading of repository policy and representative content across the main routes, with deeper inspection of Git recovery, Terraform workflows, Crossplane installation, Kafka delivery guarantees, Velero migration, and knowledge-base governance.
4. A real Markdown lint run, a disposable Git reproduction, and selected checks against official or project-maintained documentation.
5. Comparison with established documentation practices, adapted to a small public project.

### Best-practice basis

| Source | Principle used in this review |
| --- | --- |
| [Diátaxis](https://diataxis.fr/) | Distinguish tutorials, how-to guides, reference, and explanation according to reader needs. |
| [Write the Docs: documentation principles](https://www.writethedocs.org/guide/writing/docs-principles/) | Make information discoverable, current, skimmable, and open to reader participation. |
| [Google Technical Writing: audience](https://developers.google.com/tech-writing/one/audience) | Explain the knowledge readers need beyond what they already know. |
| [KCS: content health](https://library.serviceinnovation.org/KCS/Knowledge-Centered_Success_Practices_Guide/301-Evolve_Loop/Practice_5_Content_Health) | Improve whether a defined audience can find and use knowledge. |
| [W3C WAI: writing for accessibility](https://www.w3.org/WAI/tips/writing/) | Use meaningful headings, descriptive links, clear instructions, and text alternatives. |
| [GitHub Actions: secure use](https://docs.github.com/en/actions/reference/security/secure-use) | Limit workflow permissions and use immutable action references where appropriate. |

These sources inform the assessment. The priorities, proposed targets, and implementation sequence below are recommendations for this repository, not requirements imposed by those frameworks.

## Repository inventory

All counts refer to the baseline commit. The new report and its navigation links are excluded.

| Measure | Observed result |
| --- | --- |
| Tracked files | 261 |
| Markdown files | 249 |
| Markdown files in the configured curated validation scope | 238 |
| Markdown files excluded under source intake/archive paths | 11, including two directory indexes and nine archived source documents |
| `README.md` files | 77 |
| Markdown files across the 17 reader-facing knowledge areas | 212 |
| Non-`README.md` files in those areas | 145, including example-bundle documents |
| Knowledge-area pages explicitly marked `Status: Initial outline` | 41 |
| Local inline-link occurrences checked in curated Markdown | 1,908 |
| Missing local targets found by that scan | 0 |
| Local heading-fragment links checked | 94; no mismatches found |
| Unique HTTP(S) destinations extracted from inline links | 310; not a complete external availability audit |
| Documentation directories missing a `README.md` | 0 |
| Tracked Terraform `.tf` files | 0 |
| Non-Markdown files under `assets/` | 0 |
| Knowledge-area pages containing Mermaid fences | 6 |

The outline count is based on actual standalone status lines, not mentions of the status convention. Many marked files are indexes that already link to useful articles; 41 does not mean 41 empty pages. Conversely, an absent outline marker does not establish completeness.

Approximate whitespace-delimited counts are 137,732 words across the knowledge areas and 108,144 words in the excluded source paths. These counts include code and tables. Archived notes are therefore a substantial portion of the material a repository-wide search could encounter; their separation from curated guidance matters.

## What is working well

### The information architecture is coherent

The [root index](README.md) exposes major areas and fast paths, and the [context map](context.md) makes placement decisions explicit. Provider-specific cloud material, general database topics, Kubernetes tooling, and cross-topic workflows have reasonably distinct homes.

The navigation scan found nearly complete reachability from the root. The one curated Markdown exception was the historical [GitHub Actions pipeline report](github-actions-pipeline-report.md). This is a small discoverability gap, not widespread structural disorder.

### Several articles teach operational judgment

The [Velero migration guide](knowledge/migrations/velero/cluster-migration-and-disaster-recovery.md) distinguishes Kubernetes objects, provider snapshots, portable file data, application validation, and rollback boundaries. That helps readers avoid equating a successful restore command with a successful migration.

The [Kafka delivery guide](knowledge/databases/kafka/delivery-guarantees-and-failure-handling.md) discusses duplicate processing, idempotency, external side effects, and outbox patterns. Its conceptual scope is useful even though one code example needs clarification, described below.

The [Crossplane S3 lab](knowledge/kubernetes/crossplane/local-aws-s3-lab.md) includes a sandbox requirement, identity checks, reconciliation observation, and external-resource cleanup. Those are good elements to retain when correcting its credential example.

### There is already a maintainable contribution foundation

The [templates](knowledge/templates/index.md), [contributor guide](CONTRIBUTING.md), [issue forms](.github/ISSUE_TEMPLATE/documentation-error.yml), [CODEOWNERS](.github/CODEOWNERS), and [MIT license](LICENSE) reduce the work needed to welcome contributors. The [source ingestion instructions](sources/AGENTS.md) explicitly require classification, verification, and curation rather than blind copying.

### The repository already explains many of its own next steps

The [provenance and freshness guide](knowledge/ai/ai-tooling/knowledge-bases/provenance-trust-and-freshness.md) and [evaluation guide](knowledge/ai/ai-tooling/knowledge-bases/evaluation-and-quality.md) describe source authority, verification, lifecycle, and measurable retrieval quality. A lightweight application of those ideas to the main corpus would be more useful than introducing another elaborate knowledge-management architecture.

## Coverage by knowledge area

Counts include indexes and examples. The assessment concerns documentation coverage, not a certification of product accuracy.

| Area | Markdown files | Assessment and next useful addition |
| --- | --- | --- |
| [Git](knowledge/git/index.md) | 22 | Broad command and recovery coverage. Correct restore semantics; add a beginner exercise covering working tree, index, commit, and safe undo. |
| [Terraform](knowledge/terraform/index.md) | 10 | Seven pages are marked outlines; only two non-index articles exist. Add one complete configuration with plan, apply, validation, state explanation, and cleanup. |
| [Kubernetes](knowledge/kubernetes/index.md) | 53 | Strong advanced tooling and command coverage. Complete the fundamentals route before expanding specialist tooling further. |
| [Cloud](knowledge/cloud/index.md) | 38 | Useful AWS compute, edge, and architecture material. Azure remains a starting outline; Google Cloud has Apigee coverage. Show those differences clearly. |
| [Databases](knowledge/databases/index.md) | 14 | Useful Kafka and MongoDB explanations. Add a reproducible local exercise and stronger operational diagnostic examples. |
| [Migrations](knowledge/migrations/index.md) | 11 | Velero provides a comparatively developed reading sequence. Add a tested compatibility matrix and a small recovery rehearsal with evidence. |
| [Security](knowledge/security/index.md) | 5 | Focused identity-federation coverage. Add a beginner identity/permissions path and connect it to practical AWS and Kubernetes exercises. |
| [FinOps](knowledge/finops/index.md) | 1 | Top-level outline; some AWS tagging guidance exists elsewhere. Start with one cost-allocation or cleanup exercise linked to existing cloud material. |
| [DevOps](knowledge/devops/index.md) | 4 | SonarQube and GitHub integration provide a concrete starting point. Connect them to a complete delivery exercise. |
| [Programming languages](knowledge/programming-languages/index.md) | 2 | Bootstrap/bootstrapping is currently the only focused article. Clarify that this is selective coverage, not a general language curriculum. |
| [MLOps](knowledge/mlops/index.md) | 1 | Outline. Keep visibly planned until there is a bounded, useful learning outcome. |
| [AI](knowledge/ai/index.md) | 30 | Substantial tooling and knowledge-base guidance, including a structured example bundle. Distinguish example metadata from real repository verification. |
| [AI agents](knowledge/ai-agents/index.md) | 1 | Outline with related tooling links. Clarify its boundary with AI tooling before creating overlapping articles. |
| [LLM](knowledge/llm/index.md) | 1 | Outline with related links. Define a distinct audience and first practical outcome. |
| [ML](knowledge/ml/index.md) | 1 | Outline. Reserve expansion for demonstrated reader demand. |
| [Solutions architect](knowledge/solutions-architect/index.md) | 2 | The PoC guide is useful. Add an applied decision exercise with constraints and evidence. |
| [Cross-topic guides](knowledge/cross-topic-guides/index.md) | 16 | Valuable integration routes, but five are marked outlines, including end-to-end deployment and observability. Complete one full journey first. |

The concentration in AWS and Kubernetes is a reasonable strength for a small project. The improvement is to describe that strength honestly and help readers follow it, rather than trying to make all 17 areas equally deep immediately.

## Priority findings

Priority definitions: **P1** means correct soon because it affects reliability or a central reader goal; **P2** means address in the next improvement cycle; **P3** means useful polish after higher-impact work. These priorities are relative to this repository.

### F1 — P1: Correct the Git restore explanation

**Evidence:** [Undo and recovery](knowledge/git/troubleshooting/undo-and-recovery.md), under “Discard one file's local edits,” says that `git restore path/to/file` replaces the file with the committed version.

**Finding:** By default, this command restores the working tree from the index. The committed version and index can differ. The [official Git reference](https://git-scm.com/docs/git-restore) confirms the default source. A disposable local repository reproduced the difference: `HEAD` contained `committed`, the index contained `staged`, and running restore changed the working file to `staged`.

**Reader impact:** A learner can misunderstand which changes survive an undo operation.

**Recommendation:** Explain working tree, index, and `HEAD` explicitly. Put the loss-of-unstaged-edits warning before the example. If teaching restoration from `HEAD`, identify that source explicitly and describe its effect on staged versus unstaged content. Search related Git pages for the same wording.

**Acceptance:** A small demonstration with different committed, staged, and unstaged content matches every explanation.

### F2 — P1: Complete the temporary AWS credentials example

**Evidence:** The [Crossplane S3 lab](knowledge/kubernetes/crossplane/local-aws-s3-lab.md), under “Create temporary AWS credentials,” includes an access key and secret key but omits a session token.

**Finding:** For AWS STS temporary credentials, the session token is part of the credential set. The [AWS shared credentials documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) shows `aws_session_token` alongside the key and secret. A long-lived IAM access key that is later deleted is a different credential model.

**Reader impact:** A reader following the temporary-credential guidance can create an incomplete provider credential file and encounter authentication failures.

**Recommendation:** Include the token for STS credentials, explain expiration and refresh, and verify the exact secret-backed configuration with the chosen provider version. Check related credential snippets for consistency. This finding is source-verified; the cloud lab was not executed during this review.

**Acceptance:** The documented temporary credential path authenticates in a sandbox, and the guide explains how expiry appears and how to clean up.

### F3 — P1: Restore the Markdown validation baseline

**Evidence:** Running the prescribed command at the baseline produced **20 issues in 16 files** using `markdownlint-cli2 v0.23.2` and `markdownlint v0.41.1`.

| Rule | Count | Observed cause |
| --- | --- | --- |
| MD025 | 15 | OKF example documents contain both a frontmatter `title` and a body H1; the current rule treats the frontmatter title as a heading. |
| MD034 | 4 | Bare source URLs in the OKF example's source-reference documents. |
| MD056 | 1 | An unescaped pipe inside an inline command in the Crossplane XRD guide's troubleshooting table. |

The table error is in [XRDs, Compositions, and XR calls](knowledge/kubernetes/crossplane/xrd-composition-and-xr-calls.md), baseline line 498. The other failures are under the [OKF example bundle](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/readme-concept.md).

**Recommendation:** Resolve the title/frontmatter convention deliberately, preserve required example metadata, format source links, and escape the table pipe. Keep the scope of any lint exception narrow. The MD025 results do not mean those files necessarily contain two visible H1 lines.

**Acceptance:** The complete prescribed lint command succeeds with a recorded tool version, and rendering preserves the intended document titles and table cells.

### F4 — P1: Make runnable examples distinguishable from conceptual sketches

**Evidence:** The [Kafka delivery guide](knowledge/databases/kafka/delivery-guarantees-and-failure-handling.md) contains a Python “Manual commit consumer pattern” with `consumer.poll(timeout_ms=1000)` iterated as records, but it names no client library or setup.

**Finding:** For `kafka-python`, the matching `poll` API returns a mapping from topic-partitions to lists of records, as documented by the [project's KafkaConsumer reference](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html). Iterating that mapping directly yields keys, not the records used by the snippet. Because the article does not identify a library, this is an ambiguous example contract rather than proof of a failure in every possible client implementation.

**Recommendation:** Either label the block explicitly as pseudocode or select a library/version and show compatible polling, headers, consumer configuration, and commit handling. For manual-commit examples, make the automatic-commit setting explicit. Explain what happens when processing fails partway through a batch.

**Acceptance:** Runnable examples identify their dependencies and pass a bounded test; conceptual examples say that they are illustrative before the code.

### F5 — P1: Complete a beginner path through existing content

**Evidence:** [Kubernetes fundamentals](knowledge/kubernetes/fundamentals/index.md), [Terraform examples](knowledge/terraform/examples/index.md), and [end-to-end deployment](knowledge/cross-topic-guides/end-to-end-deployment.md) are outlines, while advanced Crossplane and platform material is extensive. The root primarily asks readers to choose a technology.

**Reader impact:** The reader who needs the most guidance must already know the vocabulary and prerequisites to navigate effectively.

**Recommendation:** Add a short “Start here” route for the intended first audience: people learning practical cloud and platform engineering. Separate learning, solving a problem, and comparing designs. Link existing pages in a deliberate order and fill only the missing prerequisites needed for the first complete exercise.

**Acceptance:** A new reader can select a starting point, understand prerequisites, complete one exercise, verify success, and identify the next lesson without the maintainer's help.

### F6 — P1: Add visible verification and version information to operational guides

**Evidence:** The templates do not require a review date, tested environment, or validation method. Frontmatter appears in 16 knowledge-area files, all within the OKF example bundle. Outside that bundle, structured review metadata is not consistently present. Version details do appear in prose and commands, so this is not a claim that versioning is entirely absent.

The [Helm guide](knowledge/kubernetes/applications-and-tools/helm.md) recommends reviewed chart versions, while the [Crossplane S3 lab](knowledge/kubernetes/crossplane/local-aws-s3-lab.md) installs the core chart without a version and pins a provider separately. Readers cannot identify a single documented, tested combination from that lab.

**Recommendation:** Start with the most consequential operational pages. Record audience, content status, last substantive review, source verification versus execution testing, and the relevant tool/provider versions. Pin versions in reproducible labs; explain version-dependent choices in general references.

**Acceptance:** A reader can tell whether a procedure was source-reviewed, statically checked, or actually run, and for which environment. Never populate a “verified” field merely because text was generated or reformatted.

### F7 — P2: Expose content maturity before readers open a page

**Evidence:** The [root area table](README.md) presents established material and early outlines together. Some area indexes retain an outline marker even after acquiring substantive child articles. The [cross-topic index](knowledge/cross-topic-guides/index.md) does not identify its five outline guides in the listing.

**Recommendation:** Add concise maturity labels to entry points, such as “available guides,” “partial coverage,” and “planned.” Distinguish an index's scope from each child article's readiness. Review labels when content changes.

**Acceptance:** Readers do not mistake a planned topic or workflow outline for a finished tutorial. Empty breadth does not dominate the first screen of navigation.

### F8 — P2: Make checks match the promises in the documentation

**Evidence:** The [Terraform format workflow](.github/workflows/terraform-format.yml) runs `terraform fmt -recursive -check`, but the baseline contains no `.tf` files. It does not validate Terraform embedded in Markdown. The three workflows lack `workflow_dispatch`, although the [content CI/CD process](knowledge/git/github-actions/content-ci-cd-process.md) lists it as an expected trigger. The workflows also use action tags and have no explicit `permissions` block.

The [link workflow](.github/workflows/link-check.yml) uses `fail: false` on the action but then explicitly exits on a nonzero result. It should not be described as silently ignoring failures.

**Recommendation:** Keep fast Markdown and deterministic local-link checks. Add syntax/schema checks only for examples declared runnable. Store selected examples as actual files when this makes testing easier. Add manual workflow dispatch or amend the documented policy. Set explicit minimal permissions; consider verified full commit SHA action pins with an update process, following [GitHub's guidance](https://docs.github.com/en/actions/reference/security/secure-use).

Separate local link failures from temporary external-site failures so maintainers can triage them accurately. A formatting check should never be presented as deployment or behavioral validation.

**Acceptance:** Each required CI result describes what it actually checked. A broken declared-runnable example is detectable, and a no-input formatting job does not imply example coverage.

### F9 — P2: Apply the writing rules consistently, starting with templates

**Evidence:** [CONTRIBUTING.md](CONTRIBUTING.md) asks for tables of contents on long pages. Using 1,500 whitespace-delimited words as a review heuristic, 23 knowledge-area pages are long; 16 of those have no internal heading-fragment navigation links. This is a discoverability signal, not a mandatory length limit. GitHub also provides its own heading outline.

Examples worth reviewing include the [Git command catalog](knowledge/git/commands/complete-command-catalog.md), [K9s guide](knowledge/kubernetes/applications-and-tools/k9s.md), and [Crossplane component model](knowledge/kubernetes/crossplane/component-model.md).

The [command template](knowledge/templates/command-reference-template.md) tells authors to explain risk before a command but places its warning after the example. It also omits the `What it does:` pattern requested by [instructions.md](instructions.md). The Terraform apply warning similarly follows the command.

**Recommendation:** Fix the templates first. Add a compact contents list where readers need to jump among independent tasks. Put safety context before relevant mutations. Keep diagrams accompanied by prose; preserve useful text flows already present. Check wide tables on narrow screens before expanding them.

**Acceptance:** A copied template produces the intended structure without requiring contributors to reconcile contradictory examples. Long reference pages have usable entry points.

### F10 — P2: Reduce navigation and policy maintenance duplication

**Evidence:** [AGENTS.md](AGENTS.md), [context.md](context.md), [instructions.md](instructions.md), and [CONTRIBUTING.md](CONTRIBUTING.md) overlap in navigation, style, validation, and publication rules. The 408-line baseline context map enumerates many individual articles already listed in parent indexes.

Concrete drift is visible: [sources/AGENTS.md](sources/AGENTS.md) omits Terraform and migrations from its `principal_topic` accepted-values list and dedicated classification rows; the [documentation-error form](.github/ISSUE_TEMPLATE/documentation-error.yml) still suggests `aws/networking/security-groups.md` instead of the current cloud-prefixed route. The changelog repeats the GitHub Actions `uses:` expansion entry.

**Recommendation:** Give each guide one clear responsibility and link to canonical rules. Keep the agent router concise, let parent indexes own article lists, and generate any necessary expanded inventory. Update the stale route examples and classification choices.

**Acceptance:** A normal article addition has a small, predictable update set; routing, templates, and contributor instructions agree.

### F11 — P2: Preserve archive provenance without making raw notes authoritative

**Evidence:** [Processed sources](sources/processed/README.md) correctly says archived files are not curated documentation, but the index does not list source-to-destination mappings. The [changelog](CHANGELOG.md) records broad ingestion batches without a per-source mapping table. Some curated articles link back to source notes, but traceability is uneven.

**Recommendation:** Add a small ingestion register with original source path, curated destination links, ingestion date, and remaining uncertainties. When known, record original author/source and reuse permission context; do not assume repository licensing establishes rights for every imported note. Exclude raw archives from any future default public search or retrieval index, while preserving deliberate access to them.

The OKF bundle also needs an explicit navigation exception: its [README](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/readme-concept.md) delegates to `index.md`. Four example files omit direct parent-README links, and ten omit direct repository-root links. They are reachable through the bundle. Forcing repository navigation into a portable example may be less appropriate than documenting the exception.

**Acceptance:** A maintainer can trace an ingested document to its curated destinations, and a reader or retrieval tool can distinguish archive, example, and authoritative guidance.

### F12 — P2: Turn feedback into a learning and maintenance loop

**Evidence:** Issue forms provide a good reporting mechanism, but [ROADMAP.md](ROADMAP.md) contains broad, undated expansion goals without completion criteria. The changelog is entirely under `Unreleased`. The checkout does not provide evidence of learner success measurements, reader tests, or an operational review queue.

**Recommendation:** Choose a few reader tasks, test them with people at the intended level, and record where they get stuck. Ask issue reporters for page, environment/version, expected result, and actual result without requiring them to know the fix. Prioritize recurring failures over requests to add unrelated breadth. Periodically summarize completed milestones by date.

**Acceptance:** Roadmap items name an outcome and a definition of done, and observed reader problems influence the next batch of work.

### F13 — P3: Consider a searchable reading site after the content improvements

**Evidence:** The tracked repository provides Markdown navigation but no dedicated documentation-site configuration or publishing workflow. GitHub and local search remain useful access mechanisms. This review did not inspect remote hosting settings, so it does not establish that no external site exists.

**Recommendation:** First measure whether readers struggle to find answers. If a site would help, publish from the existing Markdown source with search, breadcrumbs, responsive tables, code copy controls, and visible maturity/review information. Keep raw archives out of default search. Check link rendering and Mermaid accessibility in the selected renderer.

**Acceptance:** The same canonical content serves both repository and site readers without a second manually maintained copy. Use reader search tasks to justify the extra tooling and maintenance.

## Recommended reader experience

Keep the existing topic hierarchy. Add a short goal-based entry layer rather than moving every file.

| Reader goal | Suggested route | Evidence of success |
| --- | --- | --- |
| “I am learning practical engineering” | Git basics → local Kubernetes foundations → a small deployment → controlled failure and recovery. | Reader explains the components, deploys a workload, diagnoses a failure, and cleans up. |
| “I need to solve a problem now” | Symptom → first checks → diagnostic evidence → safe action → verification and escalation. | Reader selects a fix from observed evidence and verifies recovery. |
| “I need to choose an approach” | Requirements → comparison → constraints → small PoC → recorded decision. | Reader explains a choice and its trade-offs using evidence. |

### First learning path to complete

1. Teach working tree, index, commits, branches, and recovery through one disposable Git repository.
2. Explain Pods, Deployments, Services, namespaces, labels, and reconciliation before introducing platform abstractions.
3. Run a local workload using the existing [kind guidance](knowledge/kubernetes/applications-and-tools/kind-custom-clusters.md).
4. Introduce one deliberate failure and use the [troubleshooting sequence](knowledge/kubernetes/troubleshooting/common-solutions.md) to diagnose it.
5. Verify recovery and remove the lab resources.
6. Offer AWS/EKS and Crossplane as subsequent paths with explicit account, cost, identity, and prerequisite requirements.

This sequence is a proposal, not an existing complete course. Prefer local exercises where they can teach the intended concept without cloud access.

### Demonstrate work skills through artifacts

For readers building confidence for engineering work, end exercises with something inspectable: a small repository, an annotated command transcript, a diagram, a recovery checklist, or a decision record. Add a few questions that require explanation, such as why a Deployment can have ready Pods while a Service has no usable endpoints.

Assessment should test understanding and diagnosis, not just successful command copying. These exercises can support learning and portfolios; they do not establish employment outcomes.

### Use documentation types lightly

The [existing templates](knowledge/templates/index.md) already support much of the needed structure. Label the main intent of a page without introducing four new directory trees everywhere:

- **Tutorial:** a bounded learning exercise with a known starting state and successful ending.
- **How-to:** steps for a specific task, assuming relevant prior knowledge.
- **Reference:** precise lookup material, organized for scanning.
- **Explanation:** concepts, trade-offs, and relationships.

This application of [Diátaxis](https://diataxis.fr/) can start with a few high-value pages. Split a mixed page only when the reader goals genuinely diverge; modest repetition can be useful when it preserves context.

## Recommended article contract

The following is a proposed minimum, not a new repository policy enacted by this report.

### Shared information

For maintained technical articles, provide:

- Purpose and intended reader.
- Prerequisites or a link to them.
- Content state: outline, draft, maintained, or deprecated.
- Last substantive review date and accountable maintainer or area.
- Relevant official references, linked near consequential claims where practical.
- Applicable versions and validation evidence when behavior depends on them.
- Parent navigation and a useful next step.

Metadata can be readable text or frontmatter. A small consistent vocabulary is more valuable than requiring a complex schema everywhere. General concepts do not need a fabricated “tested with” field.

### Additional requirements for procedures

| Element | What the reader needs |
| --- | --- |
| Starting state | Required tools, files, versions, permissions, account, context, and existing resources. |
| Intended result | A concrete outcome, not just “understand the tool.” |
| Inputs | Which values to replace and how to obtain valid values. |
| Safety | Cost, mutation, data-loss, or credential implications before the affected step. |
| Steps | Commands or actions in dependency order with explanations. |
| Verification | Expected output or invariant, including how failure differs. |
| Recovery | A safe response to common failures and a clear stop condition. |
| Cleanup | Resources to remove and checks for leftovers or continuing cost. |
| Evidence | Source review, static validation, local execution, or sandbox execution; date and scope. |

For a conceptual sketch, explicitly say what it omits. For a runnable lab, provide actual example files when readers would otherwise assemble several large snippets. Keep article and example changes together.

Do not require exhaustive testing of every command catalog. Prioritize runnable tutorials, destructive operations, authentication, backup/restore, and infrastructure lifecycle instructions.

## Maintenance and contribution model

### Assign responsibility without creating unnecessary ceremony

The existing single default [CODEOWNERS](.github/CODEOWNERS) entry is reasonable for a small project. Add area ownership when contributors are available, and allow the maintainer to remain responsible for multiple areas.

Retain the lightweight publication approach for ordinary content. Use the additional technical scrutiny already contemplated by the [content CI/CD guide](knowledge/git/github-actions/content-ci-cd-process.md) for sensitive security guidance, destructive operations, and consequential product claims. This review does not recommend mandatory human approval for every typo or navigation fix.

### Start with a small review queue

Review on relevant upstream changes and reader-reported failures. As an initial planning assumption, check fast-changing operational examples roughly quarterly and more stable conceptual pages annually. Adjust those intervals to actual drift and available capacity; elapsed time alone does not prove a page is wrong.

Review the first ten highest-impact guides before attempting metadata backfill across the whole corpus. Keep a queue that records page, reason for review, owner, evidence, and disposition.

### Treat AI assistance as a contribution method

Preserve the existing requirement to verify claims. Agent-written material should enter the same evidence and validation process as any other contribution. Example `generated` and `verified` values in the OKF bundle must remain clearly illustrative; they are not evidence that the main knowledge base was reviewed by those actors.

For this repository's size, the immediate needs are good files, useful indexes, and reliable review signals. A vector database, knowledge graph, MCP service, or automated source-reconciliation system should follow a demonstrated use case and evaluation results.

## Implementation sequence

Suggested phases are for planning, not delivery estimates. Effort is relative: **small** is a focused edit or configuration change; **medium** is a complete article or bounded automation change; **large** requires several connected articles or user testing.

### First phase: restore confidence

| Order | Work | Effort | Completion condition |
| --- | --- | --- | --- |
| 1 | Resolve baseline lint findings (F3). | Small | Full Markdown lint passes without broad suppressions. |
| 2 | Correct Git restore and temporary credential guidance (F1–F2). | Small–medium | Explanations match the stated environment and supporting evidence. |
| 3 | Classify and repair the Kafka example (F4). | Small–medium | It is clearly illustrative or works with its named client. |
| 4 | Fix template warning placement and example explanations (F9). | Small | New articles inherit the intended standard. |
| 5 | Mark outline routes in entry indexes (F7). | Small | Readers can identify incomplete paths before following them. |
| 6 | Correct stale route examples and ingestion taxonomy (F10). | Small | Contribution entry points agree with current directories. |

### Second phase: complete one learning journey

| Order | Work | Effort | Completion condition |
| --- | --- | --- | --- |
| 7 | Add a goal-based starting page and a local beginner path (F5). | Large | A new reader completes a deployment and recovery exercise. |
| 8 | Add review/version evidence to ten priority guides (F6). | Medium | Each states what was verified and how. |
| 9 | Add one complete Terraform example (F4, F8). | Medium | Real files, useful checks, expected results, and cleanup exist. |
| 10 | Align CI behavior and policy (F8). | Medium | Checks and documented guarantees match. |

### Third phase: sustain and improve

| Order | Work | Effort | Completion condition |
| --- | --- | --- | --- |
| 11 | Simplify overlapping maintenance maps and document bundle exceptions (F10–F11). | Medium | Normal changes require fewer redundant edits. |
| 12 | Add ingestion traceability and a review queue (F11–F12). | Medium | Sources and overdue review work are discoverable. |
| 13 | Run reader trials and update the roadmap (F12). | Medium | Observed difficulties determine the next improvements. |
| 14 | Evaluate whether a searchable site is worth maintaining (F13). | Medium–large | Navigation/search evidence supports the decision. |

Avoid a mass rename, an all-at-once taxonomy rewrite, or a blanket conversion to OKF as the first project. Existing links and familiar routes are assets; preserve them while improving the experience.

## Success measures

Track a small set of useful signals. Targets below are proposed starting points and should be adjusted after collecting a baseline.

| Signal | Baseline from this review | Initial target |
| --- | --- | --- |
| Markdown lint errors | 20 | Zero in the configured curated scope. |
| Missing local inline-link targets | Zero found | Maintain zero; put a repeatable check in CI. |
| Priority guides with review evidence | Not yet a defined cohort | Select ten guides and document evidence for all ten. |
| Beginner path completion | Not measured | Try the first path with 3–5 intended readers; record every blocking step. |
| Findability | No task-based measurement in the checkout | Test ten common questions; start with a goal of finding the intended page for eight within two minutes. |
| Runnable tutorial completion | Not comprehensively tested | Every tutorial in the first path has a recorded successful run and cleanup check. |
| Stale-content resolution | No operational queue found | Track unresolved high-impact reports and time to correction. |
| Source traceability | Inconsistent | Every newly ingested source has a destination mapping. |

Do not use article count, total words, or number of technologies as the primary success measure. Measure whether people can find, understand, apply, and verify the knowledge they need.

## Validation results and limitations

### Checks performed

| Check | Result and interpretation |
| --- | --- |
| Starting Git status | Clean `main`, tracking `origin/main`, at the recorded baseline. |
| File inventory | All 261 tracked paths inventoried; Markdown structure scanned across the corpus. |
| Markdown lint | Failed at baseline: 20 issues in 16 files. These were pre-existing. |
| Local target scan | No missing targets among 1,908 inline-link occurrences in 238 files. |
| Heading fragments | No mismatches among 94 local fragment links, using a fence-aware heading-slug check. |
| Index presence | Every documentation directory had a `README.md`; `.github` metadata directories were exempt. |
| Root reachability | One curated Markdown page lacked a route from the root: the historical pipeline report. |
| Parent article indexing | All knowledge-area non-README files were directly linked by their parent README except the OKF bundle log, reachable through its canonical `index.md`. |
| Git restore behavior | Reproduced in a temporary repository without changing this repository's working files. |
| Selected external verification | Best-practice sources and the Git, AWS credential, and Kafka API findings were checked online. |

### Reproducing the baseline checks

```bash
git status --short --branch
git rev-parse HEAD
git ls-tree -r --name-only 831ce4cf77f22b17c3a38ba316d2d2e5b494767b
npx markdownlint-cli2 "**/*.md"
```

What it does: shows the current working state, identifies the current commit, lists the reviewed baseline's tracked paths, and runs lint against the current checkout. For a historical lint comparison, use a separate checkout at the baseline; do not discard current work to recreate it.

Inventory counts classify the 17 knowledge-area directories separately from governance, assets, templates, and sources. The local link scan resolves relative inline Markdown destinations after excluding fenced examples and checks heading fragments separately. It excludes `sources/incoming/` and `sources/processed/` to match the configured curated scope. The temporary audit script was a review aid, not a new repository validator.

The scan is not a full Markdown-renderer implementation: it does not establish correctness of every possible HTML, generated, image, or reference-style link. A maintained parser-aware checker should be used for permanent enforcement.

### What this review does not establish

- It does not certify every technical claim across approximately 138,000 words of knowledge-area content.
- It does not report the availability of all 310 extracted external destinations; selected reference checks are not a full external link crawl.
- It does not show that cloud resources, Kubernetes examples, Terraform, Kafka, or Velero procedures were successfully deployed.
- It does not assert the current result of remote GitHub Actions, branch protection, repository visibility, or hosting settings; those were not queried.
- It does not establish accessibility conformance or usability from real reader testing. Those require rendered-page and participant checks.
- It does not perform a complete secret scan, source-rights review, or content plagiarism analysis.

The report records findings and recommendations. Adding it does not fix the baseline defects, implement a learning path, or change repository governance. Publication remains subject to the repository's validation rules; the existing lint failures need resolution before the normal commit-and-push workflow can complete.

## Related links

- [Root index](README.md)
- [Roadmap](ROADMAP.md)
- [Contributing](CONTRIBUTING.md)
- [Writing instructions](instructions.md)
- [Templates](knowledge/templates/index.md)
- [Source ingestion instructions](sources/AGENTS.md)
- [Knowledge-base provenance, trust, and freshness](knowledge/ai/ai-tooling/knowledge-bases/provenance-trust-and-freshness.md)
- [Knowledge-base evaluation and quality](knowledge/ai/ai-tooling/knowledge-bases/evaluation-and-quality.md)
- [Historical GitHub Actions pipeline report](github-actions-pipeline-report.md)
