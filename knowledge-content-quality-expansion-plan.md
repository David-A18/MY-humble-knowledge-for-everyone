# Knowledge content quality and expansion plan

Created: 2026-09-21

Status: Active planning guide

## Purpose

This plan turns the structurally sound OKF knowledge bundle into a more useful,
precise, and teachable resource. It governs what to improve next and how to
review it. It does not replace the [knowledge-base improvement
plan](knowledge-base-improvement-plan.md), which records the completed
structural improvement cycle, the [maintenance review
queue](maintenance-review-queue.md), which schedules known guide reviews, or
the [roadmap](ROADMAP.md), which names broad subject areas.

The intended result is a knowledge base where a reader can understand a topic,
choose an appropriate action, carry it out safely, and check the result. An AI
agent should be able to find the same evidence, distinguish a draft from a
reviewed guide, and cite the relevant source without treating illustrative
content as a verified fact.

## Current baseline

The generated catalog records 161 concepts in `knowledge/`: 151 `draft` and
10 `stable`. Twenty-six concepts have a freshness deadline, and no concept has
an assigned maintainer. This is a strong structural starting point, but it
means that breadth must not be presented as uniform technical authority.

Update 2026-09-30: after the first teaching-hub wave added Git fundamentals,
the catalog records 163 concepts: 153 `draft` and 10 `stable`. The number of
concepts with a freshness deadline is unchanged at 26.

Later on 2026-09-30, the programming terminology split added two focused
concepts, bringing the catalog to 165 concepts: 155 `draft` and 10 `stable`.

The repository already provides the foundations this plan will use:

- OKF metadata, directory indexes, local-link validation, and a generated
  catalog make content addressable.
- Diátaxis-oriented templates distinguish tutorials, how-to guides,
  references, explanations, and troubleshooting guides.
- The maintenance queue identifies ten safety- or operations-sensitive guides
  whose evidence needs regular review.
- Golden retrieval cases and reader-test materials allow human and AI
  discoverability to be measured instead of assumed.

## Quality standard for every new or revised concept

Before expanding a page, decide its single primary reader outcome. Split a page
when it asks the reader to learn a concept, execute a task, and troubleshoot a
failure without clear separation. Use links to connect the complementary
Diátaxis pages.

Every substantive concept must provide the following information at a depth
appropriate to its type:

| Quality need | What the reader should receive |
| --- | --- |
| Purpose | What problem the page solves and when it is the right route. |
| Audience | Assumed knowledge, intended role, and prerequisites. |
| Vocabulary | Definitions for domain terms and acronyms before they are relied on. |
| Causal model | The components, flow, or state change that explains why the guidance works. |
| Decision support | Preconditions, trade-offs, limits, and signals for choosing an option. |
| Action | Ordered, scoped steps; commands only where they help complete the task. |
| Evidence | Official primary sources for material claims, linked in the page and metadata when reviewed. |
| Verification | The expected signal, output, or observation that shows the reader is on track. |
| Recovery | Safe first checks, likely failure modes, rollback, and cleanup when an action can change state. |
| Navigation | Parent index, related concepts, and the next sensible learning or operational step. |

Do not manufacture `verified`, `sources`, `stale_after`, or a maintainer. Add
them only after the relevant review has occurred. Keep a page `draft` when its
coverage, technical evidence, or review ownership is incomplete.

### Type-specific expectations

| Type | Minimum reader outcome |
| --- | --- |
| Tutorial | A newcomer can complete one bounded learning journey and explain what changed. |
| How-to Guide | A practitioner can safely achieve one known goal under stated conditions. |
| Reference | A reader can look up syntax, fields, limits, or behavior without narrative ambiguity. |
| Explanation | A reader understands the model, relationships, and trade-offs behind a subject. |
| Troubleshooting Guide | A reader can narrow symptoms through safe checks and choose a recovery path. |
| Decision Record | A maintainer can understand the context, choice, consequences, and reconsideration trigger. |
| Learning Path | A learner can choose a starting point, sequence, completion signal, and next route. |
| Template | A contributor can create a conforming page without guessing its structure or evidence needs. |
| Glossary | A reader can resolve a term quickly and follow it to deeper guidance. |
| Asset Guide | A contributor can find, license, describe, and maintain a visual asset safely. |

## Precision protocol

Use this protocol for new technical claims and for every priority-guide review.

1. Start with the reader question and the exact scope: product, component,
   version or release family when relevant, environment, permission boundary,
   and intended outcome.
2. Read current primary documentation before writing product behavior,
   command syntax, security guidance, service limits, or compatibility claims.
   Use a vendor's official documentation, standard, or upstream project
   documentation in preference to a secondary summary.
3. State conditions instead of universal wording. Replace claims such as
   "always" or "works automatically" with the prerequisite, default, or
   configuration that makes the behavior true.
4. Separate facts, recommendations, and examples. Label illustrative names,
   values, manifests, and output. Explain the risk and suitability of a
   recommended choice.
5. Bind every command to a context: working directory, selected cluster or
   account, required identity, target resource, and whether it reads or
   changes state. Put warnings before destructive or billable actions.
6. Add an expected result and a safe first diagnostic after each important
   action. For a state-changing procedure, add rollback and cleanup.
7. Use keyed source footnotes for important claims and add structured OKF
   source records, a genuine review record, and a freshness deadline when the
   page is ready to become `stable`.
8. Check internal links, metadata, command paths, and Markdown after editing.
   Static checks prove repository integrity; they do not prove runtime product
   behavior.

## Explanation protocol

Write explanations so that readers first understand the situation and then the
action. A useful default sequence is:

1. Define the subject in plain language and identify the problem it addresses.
2. Explain why it matters and when a reader should use it.
3. Show the smallest accurate model: components, data flow, control flow, or
   lifecycle states.
4. Describe the main trade-off or decision boundary.
5. Walk through one realistic, bounded example, including what it does and
   what the reader should observe.
6. Link to the specific how-to, reference, or troubleshooting route needed for
   the reader's next action.

The detailed learner-facing standard, including analogies with stated limits
and how to tailor it by Diátaxis type, is in [Teach for
understanding](instructions.md#teach-for-understanding). Progress against it is
tracked in the [teaching-hub coverage tracker](#teaching-hub-coverage-tracker).

Use a Mermaid diagram when a relationship or lifecycle is difficult to infer
from prose. Each diagram needs nearby text that names the actors, direction of
flow, and the decision it helps the reader make. Do not add decorative diagrams
or screenshots that do not answer a reader question.

Keep paragraphs focused on one idea. Define an acronym at first use, prefer
concrete nouns over vague references, and explain why an example's value was
chosen. For command examples, include `What it does`, `Expected result`, and,
when appropriate, `If it fails`.

## Prioritization model

Select work from a small, visible backlog rather than adding pages because a
topic sounds broad or popular. Score candidate work during planning against
these five questions:

| Factor | Question |
| --- | --- |
| Reader demand | Does a learning path, reader result, issue, or repeated search need show that people need it? |
| Risk and consequence | Could imprecision cause data loss, a security problem, unexpected cost, downtime, or harmful advice? |
| Learning leverage | Does the concept unblock several other tasks or provide a needed mental model? |
| Evidence quality | Are current authoritative sources available and can the claim be reviewed honestly? |
| Maintenance capacity | Is there a realistic reviewer, freshness cadence, and scope small enough to keep accurate? |

Prioritize high-demand and high-risk material with strong primary evidence.
Defer pages that cannot yet be sourced, bounded, or maintained. Record the
chosen reader outcome, evidence plan, and intended index route before drafting.

## Master section quality checklist

This is the complete current checklist of indexed sections in `knowledge/`.
Each checkbox represents a section-level review, not an automatic assertion
that every page is correct or `stable`. Tick a box only after the section's
index, direct concepts, navigation, terminology, evidence gaps, and expansion
needs have been reviewed and recorded in the relevant change, review queue, or
issue.

For every checked section, confirm all of the following:

- Its index accurately describes the current content and links to every direct
  concept and child section.
- Every direct concept has a clear Diátaxis outcome, accurate scope, and an
  appropriate lifecycle status.
- Important technical claims have an evidence plan; high-risk or operational
  pages have source, validation, and freshness needs recorded honestly.
- Missing prerequisites, terminology, examples, troubleshooting paths, and
  related links are captured as focused follow-up work.
- The section is represented in reader tasks or retrieval cases when people or
  AI agents need to find it for a core task.

### Bundle entry points and shared material

- [ ] [Knowledge bundle entry](knowledge/index.md) — top-level navigation,
  trust signals, and goal-based routes.
- [ ] [Start here](knowledge/start-here.md) — local beginner route, completion
  signals, and links to the next learning route.
- [ ] [Glossary](knowledge/glossary.md) — shared terms, definitions, and links
  to canonical explanations.
- [ ] [Decision records](knowledge/decision-records/index.md) — repository and
  architecture decision history, consequences, and review triggers.
- [ ] [Templates](knowledge/templates/index.md) — current Diátaxis templates,
  evidence instructions, and contributor usability.
- [ ] [Assets](knowledge/assets/index.md) — asset discovery, licensing, and
  accessibility guidance.
  - [ ] [Diagrams](knowledge/assets/diagrams/index.md) — accuracy, source
    attribution, text alternatives, and where a diagram improves understanding.
  - [ ] [Icons](knowledge/assets/icons/index.md) — licensing, purpose, and
    accessible use.
  - [ ] [Images](knowledge/assets/images/index.md) — licensing, captions,
    alternative text, and maintenance.

### Cloud

- [ ] [Cloud](knowledge/cloud/index.md) — provider-neutral scope, provider
  selection, and links to practical routes.
  - [ ] [AWS](knowledge/cloud/aws/index.md) — service selection, account and
    identity boundaries, and cross-links to Kubernetes and Terraform.
    - [ ] [AWS architecture](knowledge/cloud/aws/architecture/index.md) —
      reliability, trade-offs, and reference patterns.
    - [ ] [AWS compute](knowledge/cloud/aws/compute/index.md) — workload
      selection, operations, limits, and cost implications.
    - [ ] [AWS databases](knowledge/cloud/aws/databases/index.md) — workload
      fit, resilience, performance, and operational boundaries.
    - [ ] [AWS FinOps](knowledge/cloud/aws/finops/index.md) — allocation,
      cost controls, ownership, and optimization evidence.
    - [ ] [AWS fundamentals](knowledge/cloud/aws/fundamentals/index.md) —
      account model, regions, identity, and foundational vocabulary.
    - [ ] [AWS governance and access](knowledge/cloud/aws/governance-and-access/index.md)
      — IAM, organization boundaries, least privilege, and audit trails.
    - [ ] [AWS networking](knowledge/cloud/aws/networking/index.md) — VPC,
      routing, connectivity, DNS, and security boundaries.
    - [ ] [AWS security](knowledge/cloud/aws/security/index.md) — threat model,
      identity, data protection, and incident-response links.
    - [ ] [AWS solutions architect](knowledge/cloud/aws/solutions-architect/index.md)
      — design criteria, trade-offs, and review examples.
    - [ ] [AWS storage](knowledge/cloud/aws/storage/index.md) — storage choice,
      durability, lifecycle, recovery, and cost implications.
    - [ ] [AWS troubleshooting](knowledge/cloud/aws/troubleshooting/index.md)
      — symptom-led diagnostics, safe checks, and recovery paths.
  - [ ] [Azure](knowledge/cloud/azure/index.md) — scope, authoritative sources,
    first useful learning routes, and maintenance capacity.
  - [ ] [Edge and CDN](knowledge/cloud/edge/index.md) — caching model, routing,
    invalidation, observability, and provider-specific limits.
  - [ ] [Google Cloud](knowledge/cloud/gcloud/index.md) — scope, authoritative
    sources, first useful learning routes, and maintenance capacity.
  - [ ] [Cloud solutions](knowledge/cloud/solutions/index.md) — reusable
    deployment, reliability, migration, scaling, and operations patterns.

### Kubernetes

- [ ] [Kubernetes](knowledge/kubernetes/index.md) — core model, learning
  progression, safe operations, and navigation across subtopics.
  - [ ] [Applications and tools](knowledge/kubernetes/applications-and-tools/index.md)
    — tool purpose, access boundaries, operational workflows, and currency.
  - [ ] [Best practices](knowledge/kubernetes/best-practices/index.md) —
    context, exceptions, security, reliability, and source-backed guidance.
  - [ ] [Commands](knowledge/kubernetes/commands/index.md) — context safety,
    command scope, expected output, and read-versus-write boundaries.
  - [ ] [Core objects](knowledge/kubernetes/core-objects/index.md) — object
    relationships, lifecycle, ownership, and practical examples.
  - [ ] [Crossplane](knowledge/kubernetes/crossplane/index.md) — provider
    lifecycle, credentials, managed-resource safety, compositions, and runtime
    evidence limits.
  - [ ] [Examples](knowledge/kubernetes/examples/index.md) — prerequisites,
    runnable scope, verification, cleanup, and learning value.
    - [ ] [Local deployment learning path](knowledge/kubernetes/examples/local-deployment-learning-path/index.md)
      — beginner instructions, expected local results, failure recovery, and
      completion evidence.
  - [ ] [Fundamentals](knowledge/kubernetes/fundamentals/index.md) — vocabulary,
    control-plane model, workload lifecycle, and links to applied routes.
  - [ ] [Tricks](knowledge/kubernetes/tricks/index.md) — correctness, scope,
    security implications, and when not to use a shortcut.
  - [ ] [Troubleshooting](knowledge/kubernetes/troubleshooting/index.md) —
    symptom-to-diagnosis paths for pods, services, DNS, storage, scheduling,
    ingress, and safe recovery.

### Git and delivery automation

- [ ] [Git](knowledge/git/index.md) — state model, learning route, collaboration
  practices, and recovery boundaries.
  - [ ] [Git best practices](knowledge/git/best-practices/index.md) — branch,
    commit, review, and shared-history guidance with trade-offs.
  - [ ] [Git commands](knowledge/git/commands/index.md) — intent, preconditions,
    state changes, expected output, and recovery for commands.
  - [ ] [GitHub Actions](knowledge/git/github-actions/index.md) — workflow
    syntax, permissions, supply-chain safety, secrets, and troubleshooting.
  - [ ] [Git tricks](knowledge/git/tricks/index.md) — accurate use cases,
    limitations, and safer alternatives where needed.
  - [x] [Git troubleshooting](knowledge/git/troubleshooting/index.md) — safe
    decision trees for undo, conflicts, recovery, and escalation.

### Terraform

- [ ] [Terraform](knowledge/terraform/index.md) — core workflow, state safety,
  learning progression, and links to provider-specific material.
  - [ ] [Terraform best practices](knowledge/terraform/best-practices/index.md)
    — scope, exceptions, policy, security, and collaboration practices.
  - [ ] [Terraform commands](knowledge/terraform/commands/index.md) — command
    state changes, plan review, permissions, expected results, and recovery.
  - [ ] [Terraform examples](knowledge/terraform/examples/index.md) — runnable
    assumptions, local safety, validation, and cleanup.
    - [ ] [Local state lifecycle](knowledge/terraform/examples/local-state-lifecycle/index.md)
      — tutorial precision, state inspection, failure modes, and destroy proof.
  - [ ] [Terraform fundamentals](knowledge/terraform/fundamentals/index.md) —
    providers, resources, state, modules, variables, and lifecycle model.
  - [ ] [Terraform language](knowledge/terraform/language/index.md) — syntax,
    type behavior, expressions, and version-sensitive references.
  - [ ] [Terraform project structure](knowledge/terraform/project-structure/index.md)
    — repository layout, module boundaries, environments, and ownership.
  - [ ] [Terraform troubleshooting](knowledge/terraform/troubleshooting/index.md)
    — diagnostics, state safety, drift, locking, and escalation paths.

### Data, migration, security, and operations

- [ ] [Databases](knowledge/databases/index.md) — data-model and platform-choice
  criteria, operational risk, and cross-topic routes.
  - [ ] [Kafka](knowledge/databases/kafka/index.md) — delivery semantics,
    consumer and producer behavior, observability, replay, and runtime limits.
  - [ ] [MongoDB](knowledge/databases/mongodb/index.md) — modeling, validation,
    scaling, consistency, backup, and operational guidance.
- [ ] [Migrations](knowledge/migrations/index.md) — migration planning,
  prerequisites, cutover, verification, rollback, and disaster recovery.
  - [ ] [Velero](knowledge/migrations/velero/index.md) — backup, restore,
    storage, snapshots, migration, validation drills, and cleanup evidence.
- [ ] [Security](knowledge/security/index.md) — cross-topic threat model,
  security boundaries, and routes to authoritative guidance.
  - [ ] [Identity federation](knowledge/security/identity-federation/index.md)
    — trust relationships, credential lifecycle, permissions, and auditability.
- [ ] [FinOps](knowledge/finops/index.md) — allocation, accountability, budgets,
  anomalies, optimization, and decision criteria.
- [ ] [DevOps](knowledge/devops/index.md) — delivery, reliability, automation,
  observability, and operational feedback loops.
  - [ ] [Code quality](knowledge/devops/code-quality/index.md) — quality signals,
    tool configuration, false positives, and remediation decisions.
- [ ] [Programming languages](knowledge/programming-languages/index.md) — clear
  curriculum boundaries, language-specific evidence, and practical examples.

### AI, machine learning, and knowledge engineering

- [ ] [AI](knowledge/ai/index.md) — safe engineering use, system boundaries,
  current coverage, and links to specialized material.
  - [ ] [AI tooling](knowledge/ai/ai-tooling/index.md) — tool selection,
    authentication and access limits, workflow safety, and current product
    documentation.
    - [ ] [Knowledge bases](knowledge/ai/ai-tooling/knowledge-bases/index.md)
      — knowledge architecture, authoring, provenance, freshness, retrieval,
      and agent behavior.
      - [ ] [OKF v0.2 example bundle](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/index.md)
        — conformance to the upstream format, clear separation from the
        canonical bundle, and safe illustrative data.
        - [ ] [Example concepts](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/concepts/index.md)
          — example metadata and reader purpose.
        - [ ] [Example references](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/references/index.md)
          — fixture navigation and source/attestation semantics.
          - [ ] [Example attesters](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/references/attesters/index.md)
            — illustrative attester records and non-production boundaries.
          - [ ] [Example executors](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/references/executors/index.md)
            — illustrative execution records and non-production boundaries.
          - [ ] [Example sources](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/references/sources/index.md)
            — illustrative source records and provenance semantics.
- [ ] [AI agents](knowledge/ai-agents/index.md) — agent workflows, tools,
  evaluation, safety, retrieval, and operational ownership.
- [ ] [LLM](knowledge/llm/index.md) — prompting, retrieval, evaluation,
  deployment, limits, and responsible-use guidance.
- [ ] [ML](knowledge/ml/index.md) — data, training, evaluation, model risk, and
  practical learning routes.
- [ ] [MLOps](knowledge/mlops/index.md) — lifecycle, deployment, monitoring,
  governance, reproducibility, and incident response.

### Architecture and combined workflows

- [ ] [Solutions architect](knowledge/solutions-architect/index.md) —
  requirement discovery, trade-offs, architecture review, proof of concept,
  reliability, security, and cost.
- [ ] [Cross-topic guides](knowledge/cross-topic-guides/index.md) — end-to-end
  routes across GitHub Actions, Terraform, cloud, Kubernetes, deployment, and
  observability; verify each route's handoffs and prerequisites.

### How to use the checklist

1. Start with one top-level section and its direct child routes. Do not tick a
   parent merely because a single child was reviewed.
2. Create a short review record: scope inspected, evidence reviewed, reader
   outcome, gaps found, follow-up links, and the next review decision.
3. Turn broad gaps into small, separately reviewable changes. For example,
   create one Kubernetes DNS troubleshooting guide instead of extending a
   general Kubernetes page with a partial answer.
4. Update the checkbox in the same pull request that records the section
   review. Reopen it when upstream changes, reader feedback, or a major new
   child route changes the section's quality assessment.
5. Use the completed checklist to choose the next highest-value backlog item;
   a checked section can still gain new content, but it must pass the same
   quality standard.

## Teaching-hub coverage tracker

This tracker records which concepts have been written or rewritten against the
[Teach for understanding](instructions.md#teach-for-understanding) standard. It
is separate from the section checklist above: a page can meet the teaching
standard while its section review is still open.

Run `python3 scripts/validate-teaching-coverage.py` after each wave. It
compares the wave entries and area totals with the generated catalog, catches
duplicate or missing paths, and reports the current count. It checks the
accounting only; it cannot establish that an explanation is clear or correct.

"Authored to the standard" means only that the page was drafted with the
standard's elements and passed the repository's static checks. It does not
mean the page has been independently reviewed, reader-tested, or verified
against a running system, and it does not change the page's lifecycle status.

### Wave 1 (2026-09-30)

| Concept | Type | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- | --- |
| [Git fundamentals](knowledge/git/git-fundamentals.md) | Explanation | New page, authored to the standard. | Keyed citations to Pro Git chapters; the walk-through is labelled illustrative. No execution or review record. | Independent technical review; reader test; freshness decision. |
| [Kubernetes fundamentals](knowledge/kubernetes/fundamentals/kubernetes-fundamentals.md) | Explanation | Rewritten to the standard. | Keyed citations to Kubernetes concept pages; the trace is labelled conceptual. No cluster run for this rewrite. | Independent technical review; reader test; a freshness decision for the rewritten text. |
| [Terraform fundamentals](knowledge/terraform/fundamentals/terraform-fundamentals.md) | Explanation | Rewritten to the standard. | Keyed citations to HashiCorp documentation; the `terraform_data` example is labelled illustrative and not executed for this page. | Independent technical review; reader test; a freshness decision for the rewritten text. |
| [Start here](knowledge/start-here.md) | Learning Path | Route order only: Git fundamentals now precedes Git undo and recovery. | Existing validation evidence left unchanged; a known limitation records that the new and rewritten explanations are unreviewed. | Route re-review after reader testing. |

The `stale_after` dates on Kubernetes fundamentals (2026-12-19) and Terraform
fundamentals (2026-12-20) were set on the earlier versions of those pages and
were carried over unchanged. They are not evidence that the rewritten text was
re-reviewed. Git fundamentals has no freshness date because no review has
happened.

Supporting changes in the same wave, none of which is a reviewed concept:

- The [knowledge article template](knowledge/templates/knowledge-article-template.md)
  now offers separate Explanation and How-to Guide skeletons that follow the
  standard. It is an authoring aid, remains a draft, has not been independently
  reviewed or tried by a contributor, and is still counted as not yet reviewed
  in the table below.
- A golden retrieval case, `git-edit-stage-commit-push`, points to Git
  fundamentals. It checks that the path and source ID exist; it does not
  measure retrieval ranking or answer quality.

### Wave 2 (2026-09-30)

Six existing Explanation concepts were rewritten. None was reviewed by anyone
other than the author, none was reader-tested, and none of the examples was
run against a real system. All six remain `draft`, and none has a
`stale_after`, `verified`, or maintainer value, because no review or ownership
decision has happened.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Relational vs. document databases](knowledge/databases/relational-vs-document-databases.md) | Rewritten to the standard. | Keyed citations to PostgreSQL and MongoDB documentation; the order example is labelled illustrative. | Independent technical review; reader test; freshness decision. |
| [MongoDB fundamentals](knowledge/databases/mongodb/fundamentals.md) | Rewritten to the standard. | Keyed citations to the MongoDB manual and, for the backup point, MongoDB's Atlas architecture guidance; the ticket document is labelled illustrative JSON, not database output. | Independent technical review; reader test; freshness decision. |
| [Kafka topic and event design](knowledge/databases/kafka/topic-and-event-design.md) | Rewritten to the standard. | Keyed citations to Apache Kafka 4.1 documentation and the Apache Avro specification; partitions and offsets in the example are invented. The cross-partition ordering and event-format statements are labelled in the page as inferences, because the cited Kafka pages do not state them. | Independent technical review, including the version-pinned Kafka links; reader test; freshness decision. |
| [Custom resources and CRDs](knowledge/kubernetes/core-objects/custom-resources-and-crds.md) | Rewritten to the standard. | Keyed citations to Kubernetes and Crossplane documentation; the platform API walk-through is conceptual, with no manifest and no cluster run. | Independent technical review; reader test; freshness decision. |
| [OIDC fundamentals](knowledge/security/identity-federation/oidc-fundamentals.md) | Rewritten to the standard. | Keyed citations to OpenID Connect Core and Discovery, GitHub, and AWS STS documentation; both examples use placeholder claims and show no token. | Independent security review before anyone relies on it; reader test; freshness decision. |
| [CDN and edge fundamentals](knowledge/cloud/edge/cdn-and-edge-fundamentals.md) | Rewritten to the standard. | Keyed citations to RFC 9111 and the CloudFront Developer Guide; the cache-key example is reasoned from the model, not a recorded test. Only CloudFront's provider behaviour was checked. | Independent technical review; a second provider's documentation for the provider-neutral claims; reader test; freshness decision. |

Supporting changes in the same wave: parent index descriptions for the six
pages were updated, and two golden retrieval cases were added
(`cdn-cache-key-personalized-leak` and `oidc-signin-versus-workload-federation`).
The cases check that paths and source IDs exist. They do not measure retrieval
ranking or answer quality.

### Wave 3 (2026-09-30)

Five cross-topic Explanation concepts were rewritten from initial outlines.
Their `maturity` moved from `initial-outline` to `draft` because each now has
full content; that is a statement about completeness of the draft, not about
review. `status` stays `draft`. No `verified`, `stale_after`, `generated`, or
maintainer value was added, and no example was run.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [End-to-end deployment](knowledge/cross-topic-guides/end-to-end-deployment.md) | Rewritten to the standard. | Keyed citations to GitHub, Terraform, and Kubernetes documentation; the service walk-through is labelled illustrative. | Independent technical review; reader test; freshness decision. |
| [GitHub Actions with Kubernetes](knowledge/cross-topic-guides/github-actions-with-kubernetes.md) | Rewritten to the standard. | Keyed citations to GitHub and Kubernetes documentation; no workflow file and no cluster run. | Independent technical review; reader test; freshness decision. |
| [GitHub Actions with Terraform](knowledge/cross-topic-guides/github-actions-with-terraform.md) | Rewritten to the standard. | Keyed citations to Terraform CLI documentation, HashiCorp's automation tutorial, and GitHub documentation; the pipeline walk-through is invented. The partial-apply statement is labelled as not quoted from the cited pages. | Independent technical and security review; reader test; freshness decision. |
| [Terraform on AWS](knowledge/cross-topic-guides/terraform-on-aws.md) | Rewritten to the standard. | Keyed citations to the S3 backend, backend, locking, AWS provider, and AWS IAM documentation; the wrong-account example is reasoned, with placeholder account numbers and no AWS call. The AWS provider registry page is rendered by script, so its content was checked against the provider's documentation source. | Independent technical and security review; reader test; freshness decision. |
| [Observability stack](knowledge/cross-topic-guides/observability-stack.md) | Rewritten to the standard. | Keyed citations to OpenTelemetry documentation and the Google SRE Book; the incident story is invented. | Independent technical review; a check against one concrete stack; reader test; freshness decision. |

The two Terraform pages have no analogy of their own. They rely on the
analogy in Terraform fundamentals and use a diagram and a worked example
instead, which the type-tailoring guidance allows when an analogy would not
add understanding.

Supporting changes in the same wave: the cross-topic index now describes the
five pages and lists them as drafts, and three golden retrieval cases were
added (`green-pipeline-is-not-working-deployment`,
`terraform-saved-plan-artifact-sensitivity`, and
`terraform-s3-backend-locking-default`). Retrieval cases are static: they
check that the expected paths and source IDs exist. They do not test
retrieval ranking or answer quality.

### Wave 4 (2026-09-30)

Three existing Explanation concepts under Kubernetes applications and tools
were rewritten. None was reviewed by anyone other than the author, none was
reader-tested, and no example was run against a cluster, Flux, or Argo CD.
All three remain `status: draft` and `maturity: draft`. No `verified`,
`stale_after`, `generated`, or maintainer value was added.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [GitOps](knowledge/kubernetes/applications-and-tools/gitops.md) | Rewritten to the standard. | Keyed citations to the OpenGitOps principles and glossary and to Flux and Argo CD documentation; the service walk-through is labelled illustrative. The statement that an unreconciled hand edit can later be overwritten is reasoning, not a quoted claim. | Independent technical review; reader test; freshness decision. |
| [Flux](knowledge/kubernetes/applications-and-tools/flux.md) | Rewritten to the standard. | Keyed citations to Flux component, source, Kustomization, HelmRelease, and installation documentation; the commit walk-through is conceptual, with invented revisions, no YAML, and no cluster run. The statement that a failed fetch leaves the previous revision applied is reasoning from the documented chain. | Independent technical review; a check against a running Flux installation; reader test; freshness decision. |
| [Argo CD vs. Flux](knowledge/kubernetes/applications-and-tools/argo-cd-vs-flux.md) | Rewritten to the standard. | Keyed citations to Argo CD and Flux documentation for each comparison row; the team decision is invented. The explanation of why overlapping ownership conflicts is labelled in the page as reasoned, because neither project documents the two tools managing one resource. Operational overhead is described only as what each installation runs. | Independent technical review by someone who has operated both tools; reader test; freshness decision. |

The cited pages were read on 2026-09-30 from the Argo CD `stable`
documentation and the current Flux documentation. The links are not pinned to
a version, so defaults described in the three pages can change when either
project releases; that is a reason for a freshness decision, which has not
been made.

Supporting changes in the same wave: the applications-and-tools index and the
Kubernetes index fast path now describe the three pages, and one golden
retrieval case was added (`gitops-prune-and-self-heal-defaults`). The case is
static: it checks that the expected paths and source IDs exist. It does not
test retrieval ranking or answer quality.

### Wave 5 (2026-09-30)

Two existing Kubernetes explanations were rewritten around a single reader
decision each. Both stay `draft` and have no independent review, reader test,
running-cluster result, assigned maintainer, or new freshness record.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Gateway API and Ingress](knowledge/kubernetes/applications-and-tools/gateway-api-and-ingress.md) | Rewritten to explain the external request path, object roles, route ownership, and choice of API. | Keyed citations to Kubernetes and Gateway API documentation; the two-team request path is illustrative. Acceptance of a route is explicitly separated from external reachability. | Independent technical review; implementation-specific feature check; reader test; freshness decision. |
| [Stateful workloads](knowledge/kubernetes/core-objects/stateful-workloads.md) | Rewritten to explain Pod identity, separate storage claims, placement, and two deletion policies. | Keyed citations to Kubernetes storage and controller documentation; the three-Pod failure is illustrative, with no cluster run or restore test. | Independent technical review; storage-driver behavior check; reader test; freshness decision. |

The current Kubernetes documentation was consulted on 2026-09-30. These
pages contain no manifests to apply. The diagrams illustrate relationships,
not observed infrastructure.

### Wave 6 (2026-09-30)

The FinOps allocation how-to and its AWS tag explanation were rewritten as a
connected reader route. Both remain drafts. The previously recorded
`stale_after` on cost allocation basics was carried over; it is not evidence
that this rewrite was independently reviewed.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Cost allocation basics](knowledge/finops/cost-allocation-basics.md) | Added a direct, shared, and unallocated cost model, an illustrative reconciled report, expected outcome, and checks. | Keyed FinOps Framework citation and existing structured source records; the 100-unit report is invented and no provider report was run. | Independent FinOps and finance review; a real provider report check; reader test; freshness decision for the rewrite. |
| [AWS cost allocation tags](knowledge/cloud/aws/finops/cost-allocation-tags.md) | Rewritten to separate resource tagging from billing activation, explain reporting delays and historical backfill, and bound tag coverage. | Keyed citations to AWS Billing and FinOps documentation; the EC2 scenario is illustrative, with no account access or billing action. | Independent AWS billing review; a real report check; reader test; freshness decision. |

The AWS and FinOps pages were consulted on 2026-09-30. In particular, AWS
backfill can apply activation to earlier billing periods, but only dates when
a resource was actually tagged can have that historical tag value.

### Wave 7 (2026-09-30)

The programming section's long page mixed the Bootstrap web toolkit with the
general first-time setup meaning. It is now a short disambiguation route, and
two focused explanations carry the detail. All three pages remain drafts.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Bootstrap and bootstrapping](knowledge/programming-languages/bootstrap-and-bootstrapping.md) | Rewritten as a term disambiguation with a bounded example and next routes. | Keyed citations to Bootstrap and Terraform documentation; the team sentence is illustrative. | Independent editorial review; reader test. |
| [Bootstrap frontend toolkit](knowledge/programming-languages/bootstrap-frontend-toolkit.md) | New explanation of CSS classes, optional JavaScript, and a responsive grid with a text sketch. | Keyed Bootstrap 5.3 citations; HTML and visual expectation are illustrative and were not browser-tested. | Browser check of the sample; accessibility review; reader test; freshness decision. |
| [Bootstrapping a system](knowledge/programming-languages/bootstrapping-a-system.md) | New explanation of dependency order with project and Terraform backend examples and a diagram. | Keyed npm and HashiCorp citations; no npm install, Terraform run, or AWS change was performed. | Technical review; a safe first-run check; reader test; freshness decision. |

The Bootstrap 5.3, npm CLI v11, and current Terraform documentation were
consulted on 2026-09-30. The text diagram and Mermaid relationships are
teaching aids, not observed results.

### Wave 8 (2026-09-30)

The AI retrieval explanation was rewritten to distinguish searching from
fetching, give a small result example with honest lifecycle status, and show
how a budget can be evaluated. It remains a draft.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Retrieval and context efficiency](knowledge/ai/ai-tooling/knowledge-bases/retrieval-and-context-efficiency.md) | Rewritten with a plain model, library analogy, search-to-fetch diagram, illustrative result, method choices, and measurement questions. | Keyed SQLite and Elasticsearch documentation for full-text matching and BM25. The example is explicitly invented and uses the real target page's `draft` status; no retrieval service or ranking evaluation ran. | Independent technical review; a measured search evaluation; reader test; freshness decision. |

The SQLite and Elasticsearch documentation was consulted on 2026-09-30.
The example no longer implies that the draft provenance page was stable or
human-reviewed.

### Wave 9 (2026-09-30)

The bundle entry now puts the reader's question before the OKF format, and
Start here now offers honest first-topic choices while preserving the
previously tested local platform exercise route.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Start here](knowledge/start-here.md) | Expanded from a platform-only route into a topic chooser with a reusable read-example-check-sources sequence and a distinct local exercise path. | The previously recorded local Kubernetes and Terraform exercise evidence remains scoped to that local path. The new topic choices and route have no independent reader test or execution evidence. | First-time reader test across several interests; revise confusing handoffs; review planned-area labels and route choices. |

The `knowledge/index.md` introduction and goal table now lead with a
reader question. This is a navigation and teaching change, not a claim that
all listed subjects are complete.

### Wave 10 (2026-09-30)

The two DevOps code-quality explanations were rewritten to distinguish the
scanner, quality profile, new-code definition, and gate; and to show how
GitHub Actions analysis, project binding, pull request decoration, required
checks, and code scanning alerts fit together. Both remain drafts.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [SonarQube](knowledge/devops/code-quality/sonarqube.md) | Rewritten with an editor analogy, a four-part model, an illustrative change flow, and gate-versus-test limits. | Keyed current SonarQube Server 2026.1 documentation for analysis, new code, and quality gates. The change is invented; no scanner or server was run. | Independent technical review; example against a real project; reader test; freshness decision. |
| [SonarQube GitHub integration](knowledge/devops/code-quality/sonarqube-github-integration.md) | Rewritten with three distinct connections, an illustrative pull request path, and diagnosis by missing step. | Keyed current SonarQube Server 2026.1 documentation for Actions, App setup, binding, pull request analysis, and security alerts. No GitHub App or check was configured. | Edition-specific integration review; real pull request check; reader test; freshness decision. |

The official SonarQube Server 2026.1 pages were consulted on 2026-09-30.
Several old `devops-platform-integration` URLs had moved and were replaced.
These pages explain behavior; they do not record a deployed integration.

After this wave, the glossary was reorganized into browsable letter ranges,
six beginner terms were added, and 22 terms received routes to deeper pages.
It remains outside the authored count: many specialized definitions still
lack a canonical explanation link and need an editorial pass.

### Wave 11 (2026-09-30)

The first two GitHub Actions learning pages were rewritten as a connected
route: learn the event-to-result model, then read the YAML nesting and
permissions in one bounded example.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [GitHub Actions components and concepts](knowledge/git/github-actions/components-and-concepts.md) | Rewritten with a workshop analogy, an illustrative parallel-job diagram, a small manual workflow, data boundaries, and understanding checks. | Keyed current GitHub documentation for the core model, workflow syntax, secrets, artifacts, and caching. The YAML has not been run. | Independent technical review; run the tiny workflow in a safe repository; reader test; freshness decision. |
| [GitHub Actions workflow structure](knowledge/git/github-actions/workflow-structure.md) | Rewritten around one complete Node test workflow, a nesting map, change decisions, and the job file-sharing boundary. | Keyed GitHub workflow syntax and token documentation plus official checkout and setup-node action repositories. The example assumes a compatible Node project and has not been run. | Independent technical review; run in a matching sample repository; reader test; freshness decision. |

The current GitHub documentation was consulted on 2026-09-30. The page is a
draft explanation, not evidence of an operating pipeline.

### Wave 12 (2026-09-30)

The Daily Git commands page was narrowed to the one task a beginner needs
most often: turn one intended file change into a reviewed local commit.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Daily Git commands](knowledge/git/commands/daily-commands.md) | Rewritten as a four-step how-to with read/write labels, expected status and diff signals, safe unstaging, scope limits, and next routes. | Keyed official Git manual pages. The inspect-stage-review-unstage-restage-commit sequence passed in a disposable local repository on 2026-09-30; no push or shared history operation was run. | Independent technical review; reader test; freshness decision. |

The Git command documentation was consulted on 2026-09-30. The disposable
check confirms the command sequence under one local setup; it does not
validate every Git version, repository state, or team policy.

### Wave 13 (2026-09-30)

Two connected AWS architecture explanations were rewritten around the
question a learner can test mentally: what happens if one compute replica
disappears, and where does its replacement find required information?

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Stateful vs. stateless on AWS](knowledge/cloud/aws/architecture/stateful-vs-stateless.md) | Rewritten with a bounded cart example, replica and store diagram, state inventory, and limits of the stateless label. | Keyed AWS Well-Architected and Lambda application-design documentation. The cart example is invented; no AWS application or failure test ran. | Independent AWS architecture review; real failure and data-recovery check; reader test; freshness decision. |
| [Stateless application patterns on AWS](knowledge/cloud/aws/architecture/stateless-application-patterns.md) | Rewritten with shared-state and queue model, a bounded photo-upload sequence, partial-failure cases, and retry limits. | Keyed AWS Well-Architected, S3, SQS standard-queue, and Lambda documentation. The scenario is invented; no AWS resource or failure test ran. | Independent architecture and security review; real upload and retry test; reader test; freshness decision. |

The AWS documentation was consulted on 2026-09-30. This page gives a
classification model and does not claim a particular service or workload
meets its recovery goals.

### Wave 14 (2026-09-30)

The blue-green deployment explanation was narrowed from a broad cloud
service catalog to the release path and its rollback boundary.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Blue-green deployment](knowledge/cloud/solutions/blue-green-deployment.md) | Rewritten with a two-stage analogy, illustrative checkout release, traffic diagram, stage questions, and shared-data rollback limit. | Keyed AWS CodeDeploy and ECS, Azure Container Apps, and Cloud Run documentation. No deployment, traffic migration, or rollback was executed. | Independent release engineering review; a real cutover and rollback exercise; reader test; freshness decision. |

The provider documentation was consulted on 2026-09-30. The diagrams and
release path are illustrative, not evidence of a production cutover.

A separate accuracy correction in the OKF v0.2 guide now identifies
`knowledge/` as this repository's declared bundle and marks its sample
verification metadata as invented. That guide remains outside the authored
count until it receives a full teaching and source review.

### Wave 15 (2026-09-30)

The Velero introduction now explains the separate Kubernetes-object and
volume-data paths before directing readers to the operational pages.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Velero fundamentals](knowledge/migrations/velero/fundamentals.md) | Rewritten with a two-part recovery model, limited workshop analogy, illustrative notes-app restore, and questions that expose the object/data distinction. | Keyed official Velero v1.18 how-it-works, CSI, File System Backup, and restore documentation plus Kubernetes storage documentation. No cluster backup or restore ran. | Independent Velero review; a real backup and restore exercise with application check; reader test; freshness decision. |

The Velero v1.18 documentation was consulted on 2026-09-30. This first
explanation does not certify the detailed Velero runbooks or a workload's
recovery design.

### Wave 16 (2026-09-30)

The Velero architecture page now follows a request from the Kubernetes API
through its controller to backup storage and a separate restore cluster.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Velero components and architecture](knowledge/migrations/velero/components-and-architecture.md) | Rewritten with a bounded request-and-controller model, limited order-slip analogy, storage diagram, second-cluster example, and diagnosis questions. | Keyed official Velero v1.18 how-it-works, locations, and File System Backup documentation. No cluster, backup, or restore ran. | Independent Velero review; real backup discovery and restore exercise; reader test; freshness decision. |

The Velero v1.18 documentation was consulted on 2026-09-30. This page
explains component responsibility; it does not certify the operating
runbooks or the durability of a particular backup location.

### Wave 17 (2026-09-30)

The AWS stateful design checklist now asks readers to identify the state,
failure scope, recovery targets, and evidence before choosing a mechanism.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Stateful design decision checklist](knowledge/cloud/aws/architecture/stateful-design-decision-checklist.md) | Rewritten with a bounded order-store example, a limited shop analogy, separate replica and backup paths, RTO/RPO explanations, and application-level verification questions. | Keyed AWS Well-Architected recovery-objective and restore-test guidance, plus the Kubernetes StatefulSet documentation. The scenario is invented; no AWS resource or recovery test ran. | Independent resilience and database review; a real failure and restore exercise; reader test; freshness decision. |

The AWS and Kubernetes documentation was consulted on 2026-09-30. The page
does not assert that any deployed workload meets its recovery targets.

### Wave 18 (2026-09-30)

The AWS networking explanation now distinguishes connection-tracking state
from application data and follows the request and reply separately.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Stateful networking](knowledge/cloud/aws/networking/stateful-networking.md) | Rewritten with a request-and-reply model, bounded HTTPS scenario, limited door-attendant analogy, packet-path diagram, and diagnosis questions. | Keyed Amazon VPC security-group, network ACL, custom ACL, and VPC security documentation. No AWS network or traffic test ran. | Independent VPC and network-security review; a real packet-path test; reader test; freshness decision. |

The Amazon VPC documentation was consulted on 2026-09-30. The example is not
an authorization to open any particular public port or ephemeral range.

### Wave 19 (2026-09-30)

The security-groups explanation now follows a new request to a database
resource and explains what a source-group reference does and does not do.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Security groups](knowledge/cloud/aws/networking/security-groups.md) | Rewritten with a web-to-database model, bounded group-reference example, limited guest-list analogy, direction and association questions, and a separate return-path route. | Keyed Amazon VPC security-group, rule, and VPC security documentation. The scenario is invented; no AWS rule or packet test ran. | Independent AWS network-security review; a real path and rule test; reader test; freshness decision. |

The Amazon VPC documentation was consulted on 2026-09-30. This page does
not certify a specific security-group configuration or application access.

### Wave 20 (2026-09-30)

Kafka fundamentals now follows one event into a partition and out to two
independent consumer groups, leaving topic design and delivery guarantees to
their own pages.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Kafka fundamentals](knowledge/databases/kafka/fundamentals.md) | Rewritten with a bounded order event, limited notice-board analogy, producer-to-group diagram, partition-local ordering, independent offsets, and retention limits. | Keyed Apache Kafka introduction, 4.1 design, and topic-configuration documentation. The scenario is invented; no Kafka cluster ran. | Independent Kafka review; an actual producer/consumer exercise; reader test; freshness decision. |

The Apache Kafka documentation was consulted on 2026-09-30. This page does
not claim that an unconfigured cluster has any particular delivery or
durability guarantee.

### Wave 21 (2026-09-30)

The Kafka consumer-group explanation now separates partition assignment,
position lag, and replay consequences from the operational offset command.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Kafka consumer groups, lag, and replay](knowledge/databases/kafka/consumer-groups-lag-and-replay.md) | Rewritten with an illustrative two-partition assignment, limited bookmark analogy, offset-gap example, and replay side-effect boundary. | Keyed Apache Kafka 4.1 design, operations, and topic-configuration documentation. No consumer group or reset ran. | Independent Kafka and payment-flow review; a real consumer/replay exercise; reader test; freshness decision. |

The Apache Kafka documentation was consulted on 2026-09-30. The example
does not establish a measured consumer lag or authorize an offset reset.

### Wave 22 (2026-09-30)

The Kafka operations page now maps producer, partition, consumer, and
application signals to the first investigation question for a missing
outcome.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Kafka operations](knowledge/databases/kafka/operations.md) | Rewritten with a signal-path diagram, limited delivery-line analogy, bounded one-partition lag incident, and separate application checks. | Keyed Apache Kafka 4.1 monitoring, operations, and design documentation. No Kafka cluster, incident, or recovery action ran. | Independent Kafka SRE review; an actual failure investigation; reader test; freshness decision. |

The Apache Kafka documentation was consulted on 2026-09-30. The incident
scenario and metrics are illustrative rather than operational evidence.

### Wave 23 (2026-09-30)

The MongoDB data-modeling page now teaches one decision: which related data
belongs inside a ticket document, and which data should be stored separately.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [MongoDB data modeling](knowledge/databases/mongodb/data-modeling.md) | Rewritten with an access-pattern table, limited folder analogy, ticket-to-user-and-comment diagram, and bounded illustrative JSON documents. | Keyed official MongoDB workload, relationships, embedding, references, and unbounded-array guidance. No MongoDB workload ran. | Independent MongoDB review; representative query and write measurements; reader test; freshness decision. |

The MongoDB documentation was consulted on 2026-09-30. The example's
requirements and data are invented; they do not establish a production model.

### Wave 24 (2026-09-30)

The MongoDB schema-validation and indexing page now follows the ticket model
through separate write-shape and read-access decisions.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [MongoDB schema validation and indexing](knowledge/databases/mongodb/schema-validation-and-indexing.md) | Rewritten with a bounded library analogy, write/read diagram, illustrative validator and compound index, and an explain-plan check. | Keyed official MongoDB validation, invalid-document, query optimization, compound-index, and explain documentation. No MongoDB deployment or query ran. | Independent MongoDB review; validation and query exercise on representative data; reader test; freshness decision. |

The MongoDB documentation was consulted on 2026-09-30. No performance claim
is based on a measured workload.

### Wave 25 (2026-09-30)

The MongoDB replication, sharding, and consistency page now distinguishes
copies, partitions, and operation-visibility settings instead of treating
them as one kind of scaling or safety feature.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [MongoDB replication, sharding, and consistency](knowledge/databases/mongodb/replication-sharding-and-consistency.md) | Rewritten with a limited ledger/cabinet analogy, replica-versus-shard diagram, and an invented ticket write/read sequence. | Keyed official MongoDB replication, sharding, routing, concern, read-preference, and Atlas recovery documentation. No deployment or failover ran. | Independent MongoDB review; deployment-specific read/write and recovery exercise; reader test; freshness decision. |

The MongoDB documentation was consulted on 2026-09-30. The ticket sequence
illustrates a possible timing boundary, not an observed result.

### Wave 26 (2026-09-30)

The MongoDB operations page now begins with a reader-visible symptom and
traces the application, query, member, and shard boundaries before proposing
a change.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [MongoDB operations](knowledge/databases/mongodb/operations.md) | Rewritten with a request-path diagram, limited restaurant analogy, invented slow-ticket timings, explain-plan interpretation, and symptom-to-check routing. | Official MongoDB slow-query, index-use, profiler, replica-set, routing, and Atlas recovery documentation is cited or linked. No MongoDB deployment or query ran. | Independent MongoDB operations review; representative slow-query investigation; backup/restore exercise; reader test; freshness decision. |

The MongoDB documentation was consulted on 2026-09-30. The numeric
observations are invented and do not demonstrate a performance result.

### Wave 27 (2026-09-30)

The Kafka delivery-guarantees page now makes the external side-effect and
offset-commit boundary the main lesson, with producer retries and Kafka
transactions explained as distinct boundaries.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Kafka delivery guarantees and failure handling](knowledge/databases/kafka/delivery-guarantees-and-failure-handling.md) | Rewritten with an invented shipment sequence, limited bookmark analogy, crash-window diagram, repeat-safe effect decision, and precise transaction scope. | Keyed official Kafka 4.1 design, producer and topic configuration, producer/consumer APIs, and Debezium outbox documentation; the targeted retrieval case now requires the specific Kafka design source. The earlier 2026-09-19 review and syntax-check note remain historical; the code example was removed. No broker ran. | Independent Kafka and application-transaction review; broker and external database failure exercise; reader test; freshness decision. |

The Kafka documentation was consulted on 2026-09-30. No external side
effect or offset commit was observed in a running system.

### Wave 28 (2026-09-30)

The Content CI/CD process page now follows the repository's actual
`develop`-to-`main` path and explains why source publication and website
deployment are separate decisions.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Content CI/CD process](knowledge/git/github-actions/content-ci-cd-process.md) | Rewritten with a bounded editing-table analogy, branch-flow diagram, illustrative Kafka page edit, and an evidence table. Removed outdated direct-`main` and review-skipping policy. | Current `AGENTS.md`, `CONTRIBUTING.md`, workflow files, ADR-0005, website rollout plan, and keyed official GitHub workflow-event and branch-protection documentation. No merge or site dispatch ran. | Independent repository-governance review; verify live protection settings before claiming enforcement; reader test; freshness decision. |

The local workflow and governance files were inspected on 2026-09-30. The
diagram explains the intended flow, not an observed deployment.

### Wave 29 (2026-09-30)

The GitHub and AWS OIDC explanations now form a beginner route through
identity, trust, STS exchange, and role permissions. The current GitHub
subject formats are called out because a copied older-format example could
lead to a failed or overly broad trust policy.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [AWS OIDC federation](knowledge/git/github-actions/aws-oidc-federation.md) | Rewritten around one GitHub job, a token-to-credential diagram, bounded badge analogy, invented deployment, and failure-boundary checks. | Current GitHub OIDC reference, AWS configuration guide, AWS IAM role guide, and upstream credentials-action documentation. No deployment or token exchange ran. | Independent GitHub/AWS security review; controlled role-assumption exercise; reader test; freshness decision. |
| [IAM OIDC provider and STS web identity](knowledge/cloud/aws/security/iam-oidc-provider-and-sts-web-identity.md) | Rewritten around provider registration, role trust, STS exchange, and effective permissions, with a bounded example and diagram. | Current AWS IAM provider and role guides and STS API reference. No AWS role, provider, or workload ran. | Independent IAM review; controlled federation exercise; reader test; freshness decision. |

The OIDC fundamentals page received a targeted correction to label its
older-format GitHub subject example; it was already counted in wave 2 and
is not counted again here.

### Wave 30 (2026-09-30)

OIDC token validation now teaches the receiver's trust boundary instead of
offering a single pseudocode recipe for ID and access tokens.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [OIDC token validation](knowledge/security/identity-federation/oidc-token-validation.md) | Rewritten with a trust-boundary diagram, limited signed-letter analogy, invented two-token rejection example, and separate ID-token, JWT access-token, and opaque-token paths. | OpenID Connect Core and Discovery, RFC 8725, RFC 9068, and RFC 7662 are cited. No application or token was tested. | Independent identity-security review; test with the selected provider and library; reader test; freshness decision. |

### Wave 31 (2026-10-01)

Two AI knowledge-base explanations now teach the evidence behind an answer:
where a claim came from and whether it is current, and how to test that a
knowledge base leads to an accurate, attributable answer. Both remain
`draft` with an unassigned maintainer and no `verified`, `generated`, or
`stale_after` value.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Provenance, trust, and freshness](knowledge/ai/ai-tooling/knowledge-bases/provenance-trust-and-freshness.md) | Rewritten around three separate questions, producer versus corpus versus index revisions, a limited timetable analogy, a claim-dependent authority table, and an invented Orders API schema change from detection to merge with a surfaced conflict. The old reconciliation YAML, which used realistic-looking dates and hashes, was replaced by a labelled placeholder record. | Keyed citations to the OKF v0.2 specification, W3C PROV-DM, and W3C PROV-O. The page states that PROV is optional in this bundle. No reconciler, renderer, or review workflow ran. | Independent review by a knowledge-systems maintainer; a real reconciliation exercise; reader test; freshness decision. The OKF specification link follows the upstream `main` branch and is not pinned. |
| [Evaluation and quality](knowledge/ai/ai-tooling/knowledge-bases/evaluation-and-quality.md) | Rewritten around five separately scored layers, a limited mystery-shopper analogy, an evaluation-loop diagram, an invented question with ranked results, hit@k, precision at k, reciprocal rank, MRR, and a pass/fail answer check. Authorization-before-disclosure and deterministic generated-region rules are kept at conceptual depth; the long observability and cache lists were trimmed. | Keyed citations to the Stanford IR book's ranked-evaluation section, the Azure Architecture Center RAG retrieval guide (for the MRR definition and negative questions), and the BEIR paper. The page states that `tests/retrieval-cases.yaml` is a static path and source-ID check. No search, ranking, answer scoring, or reader test ran. | Independent review; a measured retrieval run over the golden cases; reader test; freshness decision. |

The external sources were consulted on 2026-10-01. The ranked results, MRR
arithmetic, answers, API, revisions, and conflict are invented teaching
material, not observations.

### Wave 32 (2026-10-01)

The EKS human-access and workload-identity explanations now form one route
that keeps three questions apart: a person's AWS permissions, a person's
Kubernetes API permissions, and a Pod's AWS permissions. The human-access
page corrects an earlier claim that Kubernetes RBAC is always the second
gate. Both pages remain `draft` with an unassigned maintainer and no
`verified`, `generated`, or `stale_after` value.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [EKS human identity and Kubernetes RBAC](knowledge/security/identity-federation/eks-human-identity-and-rbac.md) | Rewritten around IAM authentication, the access entry, and two additive authorization methods: scoped EKS access policies and group names used by RBAC bindings. Adds a limited workshop analogy, an authorization-flow diagram, an invented developer who has console access but no Pod read access until either method grants it, the documented `kubectl auth can-i --list` and impersonation limits, and scoped external OIDC sign-in. Standalone state-changing AWS CLI commands and the unexecuted RoleBinding manifest were replaced by a field table and official how-to links. | Keyed citations to the current Amazon EKS access entry, access policy, access policy permissions, create access entry, Kubernetes API access, and external OIDC pages, plus Kubernetes RBAC and authorization documentation. No cluster, access entry, or `kubectl` check ran. | Independent EKS security review; controlled access-entry exercise that confirms the documented `kubectl auth can-i` behaviour; reader test; freshness decision. |
| [EKS workload identity](knowledge/cross-topic-guides/eks-workload-identity.md) | Rewritten around the service account as the shared starting point and two credential paths: IRSA token to STS `AssumeRoleWithWebIdentity`, and Pod Identity association to agent to EKS Auth. Adds a limited hotel-and-gym analogy, a two-path diagram, a condition-based choice table covering environment, agent, SDK, trust reuse, session tags, and cross-account roles, narrow-boundary habits including the IMDS caveat, and an invented two-workload example. Kubernetes RBAC is kept separate. | Keyed citations to the current Amazon EKS service-account comparison, Pod Identity overview, how-it-works, association, and target-role pages, IRSA overview, Pod configuration, SDK and cross-account pages, the EKS Best Practices IAM chapter, and Kubernetes RBAC good practices. No cluster, association, role, or credential exchange ran. | Independent EKS/IAM security review; controlled exercise of both paths; reader test; freshness decision. |

The official AWS and Kubernetes pages were consulted on 2026-10-01. The
cluster, roles, namespaces, workloads, and people in both examples are
invented teaching material, not observations. The statement that Pod
creation rights also expose a service account's mapped AWS role is the workload identity
page's inference from two cited sources, and is labelled as such there.

### Wave 33 (2026-10-01)

The GitHub Actions security page now teaches one decision: what code a job
runs, what credential it receives, and what that credential can change.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [GitHub Actions security, secrets, and permissions](knowledge/git/github-actions/security-secrets-and-permissions.md) | Rewritten with a limited workshop analogy, trust-boundary diagram, invented documentation PR/deployment sequence, distinct token/secret/environment/OIDC controls, and an event-risk table. Removed a movable action-version example and an implied automatic environment approval gate. | Keyed current GitHub documentation for workflow syntax, secure use, secrets, deployment environments, OIDC, and `pull_request_target`. No workflow ran. | Independent Actions security review; controlled PR and deployment workflow exercise; reader test; freshness decision. |

### Wave 34 (2026-10-01)

The CDN caching and origin-protection page now teaches the separate decisions
about who may share a cached response and who may reach the origin directly.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [CDN caching and origin protection](knowledge/cloud/edge/cdn-caching-and-origin-protection.md) | Rewritten with a limited shelf-and-door analogy, two-boundary diagram, invented public catalog and private account example, origin-pattern table, and understanding checks. Corrected the reversed cache-key trade-off and explained CloudFront's positive minimum TTL override of private response headers. | Keyed RFC 9111 and current CloudFront cache-key, cache-policy, origin-request, S3 OAC, VPC-origin, custom-origin, and invalidation documentation. No CDN configuration or request was tested. | Independent CDN/security review; controlled cache and direct-origin checks; second provider review before generalising; reader test; freshness decision. |

### Wave 35 (2026-10-01)

The CloudFront page now applies the edge model to AWS distribution routing,
viewer and origin connections, and origin protection without repeating the
general caching lesson.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [CloudFront](knowledge/cloud/aws/networking/cloudfront.md) | Rewritten with a limited reception-desk analogy, ordered path-rule example, routing diagram, separate viewer and origin TLS, S3 OAC, WAF, logging limits, and understanding checks. | Keyed current Amazon CloudFront documentation for delivery, behaviours, policies, domains, origin protocol, OAC, WAF, and logging. The site and requests are invented; no distribution was configured or queried. | Independent CloudFront/security review; controlled routing, TLS, cache, and direct-origin checks; reader test; freshness decision. |

### Wave 36 (2026-10-01)

The CDN-in-front-of-EKS explanation now connects a cache decision to the
application target path without treating the Kubernetes Service as a universal
packet hop.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [CDN in front of EKS](knowledge/cross-topic-guides/cdn-in-front-of-eks.md) | Rewritten with a limited two-route-sheet analogy, an invented asset and signed-in API example, a diagram of cache hits and ALB instance/IP target paths, three boundary checks, and understanding questions. | Keyed current CloudFront delivery, cache, VPC-origin, and origin-HTTPS documentation; EKS ALB Ingress and Kubernetes Ingress/Service documentation. No CDN, ALB, or cluster was configured or queried. | Independent AWS/Kubernetes security review; controlled cache, direct-origin, TLS, and target-path checks; reader test; freshness decision. |

### Wave 37 (2026-10-01)

The multi-CDN page now teaches how two independent caches, one shared
origin, and DNS steering affect a migration or failover.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Multi-CDN operations](knowledge/cloud/edge/multi-cdn-operations.md) | Rewritten with a limited two-shopfront analogy, independent-cache diagram, invented documentation-site traffic shift, outcome contract, purge comparison, DNS-cache limit, incident signals, and understanding checks. | Keyed current Akamai caching, rules, Fast Purge, and DataStream documentation plus CloudFront cache, invalidation, and logging and Route 53 weighted routing, DNS, and health-check documentation. No DNS, CDN, purge, or failover action ran. | Independent edge/SRE review; controlled parity, purge, and failover exercise; reader test; freshness decision. |

### Wave 38 (2026-10-01)

The Akamai-versus-CloudFront page now compares a site's required outcomes
with the documented provider controls instead of giving a categorical winner.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Akamai vs. CloudFront](knowledge/cloud/edge/akamai-vs-cloudfront.md) | Rewritten with a limited delivery-service analogy, parallel-path diagram, invented AWS-hosted site, provider-control mapping, selection questions, and understanding checks. Removed unsupported blanket recommendations and separated similarly named capabilities from measured equivalence. | Keyed current Akamai Property Manager, origin, security, EdgeWorkers, and activation documentation and CloudFront behaviour, origin, WAF, edge-function, and distribution-status documentation. No configuration, contract, performance, or cost evidence was tested. | Independent Akamai/CloudFront review; side-by-side workload test and current contract/entitlement check before choosing; reader test; freshness decision. |

### Wave 39 (2026-10-01)

The ECS and ECS-versus-EKS pages now form a beginner route from ECS objects
to the platform API decision, with no categorical winner for a normal API.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Amazon ECS](knowledge/cloud/aws/compute/amazon-ecs.md) | Rewritten around task definition, running task, desired service count, and capacity provider. Uses a limited help-desk analogy, invented photo API, relationship diagram, and identity, network, storage, and health boundaries. Removed unexecuted live-change commands and the broad feature inventory. | Keyed current Amazon ECS task-definition, service, capacity, role, networking, load-balancing, and storage documentation. No AWS task or request ran. | Independent ECS review; controlled replacement and data-lifetime check; reader test; freshness decision. |
| [ECS vs. EKS](knowledge/cloud/aws/compute/ecs-vs-eks.md) | Rewritten as a conditional choice about orchestration APIs and operating work, with a two-path diagram and invented photo API whose custom-resource requirement changes the fit. Corrects unconditional ECS recommendations and includes EKS Auto Mode. | Keyed current ECS, EKS, and Kubernetes primary docs; no platform, portability, price, or performance comparison ran. | Independent AWS/Kubernetes review; representative workload and cost comparison; reader test; freshness decision. |

### Wave 40 (2026-10-01)

The ECR page now connects the image build to its storage and ECS pull, while
keeping registry operations in the official procedures.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Amazon ECR](knowledge/cloud/aws/compute/amazon-ecr.md) | Rewritten around registry, repository, image, tag, digest, access, retention, and scanning, with a bounded warehouse analogy, invented photo API release, and build-to-ECR-to-ECS diagram. Distinguishes Helm chart artifacts from application images and removes unexecuted live commands. | Keyed current ECR registry, image, policy, tag, lifecycle, scan, and Helm documentation plus the ECS execution-role guide. No image, task, scan, or registry operation ran. | Independent ECR/ECS review; controlled pull, retention, and rollback check; reader test; freshness decision. |

### Wave 41 (2026-10-01)

The EKS-to-ECS migration page now follows the application contract and
cutover evidence instead of assuming each Kubernetes object has a direct
replacement.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [EKS to ECS migration](knowledge/cloud/aws/compute/eks-to-ecs-migration.md) | Rewritten with a bounded restaurant-move analogy, invented photo API, parallel-runtime diagram, responsibility map, traffic/data/rollback boundaries, workload exceptions, and understanding checks. Removed untested commands and categorical fit claims. | Keyed current Kubernetes and AWS ECS, EKS Auto Mode, and ALB docs; no cluster, task, route, data migration, or workload test ran. | Independent AWS/Kubernetes and data-recovery review; controlled migration and rollback exercise; reader test; freshness decision. |

### Wave 42 (2026-10-01)

The MSK page now connects AWS cluster management to the Kafka application
responsibilities already taught in the database section.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Amazon MSK](knowledge/cloud/aws/databases/amazon-msk.md) | Expanded from an outline into a managed-boundary explanation with a limited sorting-center analogy, invented order event, diagram, Provisioned/Serverless choice, network and IAM gates, lag limits, and understanding checks. | Keyed current AWS MSK overview, cluster-type, client-access, IAM, monitoring, lag, and quota docs. No cluster, client, metric, or event was tested. | Independent Kafka/AWS review; representative client and failure check; reader test; freshness decision. |

### Wave 43 (2026-10-01)

The MongoDB-on-AWS pages now form a broad hosting-choice guide and a
focused comparison of the two managed options.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [MongoDB on AWS](knowledge/cloud/aws/databases/mongodb-on-aws.md) | Rewritten with a limited workshop analogy, three ownership paths, invented ticket application, candidate diagram, and decision sequence covering behavior, access, recovery, and observed cost. | Keyed current MongoDB Atlas, self-managed MongoDB, and AWS DocumentDB primary docs; no cluster, query, restore, or cost test ran. | Independent database architecture review; representative workload and restore exercise; reader test; freshness decision. |
| [DocumentDB vs. MongoDB Atlas](knowledge/cloud/aws/databases/documentdb-vs-mongodb-atlas.md) | Rewritten as a version-aware comparison with an invented ticket workload, parallel-candidate test diagram, compatibility and network boundaries, restore criteria, and understanding checks. | Keyed current AWS DocumentDB 8.0 compatibility, API, differences, VPC, and backup docs plus MongoDB Atlas cluster, endpoint, and restore docs. No database, query, failover, or cost test ran. | Independent DocumentDB/Atlas review; side-by-side behavior, performance, and restore test; reader test; freshness decision. |

### Wave 44 (2026-10-01)

The Apigee page now teaches the request path and the separate app-access
path, including the policies that must actually run.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Apigee API management](knowledge/cloud/gcloud/apigee.md) | Rewritten with a limited museum analogy, invented learning API, request and product-access diagram, proxy and environment vocabulary, app-key and quota policy boundaries, hybrid ownership, and understanding checks. | Keyed current Google Cloud Apigee proxy, environment, product, app, policy, analytics, and hybrid docs. No proxy, policy, request, runtime, or analytics result was tested. | Independent Apigee/security review; controlled access and quota checks; reader test; freshness decision. |

### Wave 45 (2026-10-02)

The EKS-to-MSK guide now joins the AWS service and Kafka application
explanations through the Pod's three separate gates.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [EKS to MSK applications](knowledge/cross-topic-guides/eks-to-msk-applications.md) | Rewritten with a bounded delivery-driver analogy, invented order-to-shipment flow, diagram, network/identity/application gates, IAM authorization scope, lag limitations, and understanding checks. | Keyed current AWS MSK client, bootstrap, IAM, EKS workload identity, and consumer-lag docs plus Apache Kafka documentation. No Pod, cluster, role, event, or shipment was tested. | Independent EKS/Kafka security review; controlled connection and failure checks; reader test; freshness decision. |

### Wave 46 (2026-10-02)

The GitOps-on-EKS guide now follows one change through distinct Kubernetes
and AWS reconciliation and verification boundaries.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [GitOps on EKS](knowledge/cross-topic-guides/gitops-on-eks.md) | Rewritten with a bounded building-plan analogy, invented photo API, diagram, three permission boundaries, controller-placement conditions, and understanding checks. | Keyed current Argo CD, Flux, and Amazon EKS documentation. No GitOps run, cluster, ALB, Pod, user request, or reader test occurred. | Independent GitOps/EKS security review; controlled rollout and user-path checks; reader test; freshness decision. |

### Wave 47 (2026-10-02)

The EKS deployment explanation now separates access, image delivery,
Kubernetes rollout, and user verification.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Deploying to EKS](knowledge/cross-topic-guides/deploying-to-eks.md) | Rewritten with a limited delivery analogy, invented photo API, diagram, failure-owner table, and understanding checks. Removed unexecuted live commands and unsupported review and freshness claims. | Keyed current Amazon EKS, Amazon ECR, and Kubernetes documentation. No AWS account, image, cluster, Deployment, or user request was tested. | Independent EKS/security review; controlled release and recovery exercise; reader test; freshness decision. |

### Wave 48 (2026-10-02)

The APISIX-on-EKS page now follows both the client request and the
Kubernetes-to-gateway configuration change.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [APISIX on EKS](knowledge/cross-topic-guides/apisix-on-eks.md) | Rewritten with a limited venue analogy, invented lesson API, two-path diagram, ownership and failure tables, TLS placement, plugin boundaries, and understanding checks. | Keyed current Apache APISIX and Amazon EKS/NLB documentation. No cluster, gateway, route, plugin, load balancer, client request, or reader test ran. Claude Code was unavailable at its weekly subscription limit, so this pass did not receive Opus review. | Independent APISIX/EKS security and Opus review; controlled route, policy, TLS, and failure checks; reader test; freshness decision. |

### Wave 49 (2026-10-02)

The EKS operations guide now starts from a symptom and traces distinct AWS,
Kubernetes, Pod-identity, and user-path evidence.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [EKS operations](knowledge/cross-topic-guides/eks-operations.md) | Rewritten with a limited library analogy, invented lesson-API incident, boundary diagram, evidence table, and understanding checks. Corrected the Pod Identity annotation claim. | Keyed current Amazon EKS and Kubernetes documentation. No account, cluster, Pod, credential, service, user request, or reader test ran. Claude Code was at its weekly subscription limit, so no Opus review occurred. | Independent EKS security and Opus review; controlled incident checks; reader test; freshness decision. |

### Wave 50 (2026-10-02)

The Kubernetes-on-AWS page now teaches how Kubernetes objects meet AWS
resources, with ownership varying by the EKS mode and chosen integrations.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Kubernetes on AWS](knowledge/cross-topic-guides/kubernetes-on-aws.md) | Rewritten with a limited theatre analogy, invented photo API, Kubernetes-to-AWS mapping, ownership diagram, standard/Auto Mode differences, and understanding checks. | Keyed current Amazon EKS, Amazon ECR, and Kubernetes documentation. No cluster, ALB, Pod, S3 object, EBS volume, request, or reader test ran. Claude Code remained at its weekly limit, so no Opus review occurred. | Independent EKS/security and Opus review; controlled network, IAM, and storage checks; reader test; freshness decision. |

### Wave 51 (2026-10-02)

The EKS tooling-cluster guide now shows the choice between local and
central controllers, the target-cluster authority required, and the
limits of a central outage.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [EKS tooling cluster architecture](knowledge/cross-topic-guides/eks-tooling-cluster-architecture.md) | Rewritten with a bounded school-district analogy, invented two-workload-cluster example, management/user-path diagram, local-versus-central comparison, failure table, and recovery questions. | Keyed current Amazon EKS, Argo CD, and Flux documentation. No cluster, controller, credentials, outage, recovery, application request, or reader test ran. Claude Code remained at its weekly limit, so no Opus review occurred. | Independent EKS/GitOps security and Opus review; controlled cross-cluster access, outage, and recovery exercise; reader test; freshness decision. |

### Wave 52 (2026-10-02)

The local deployment learning path now makes each stage's learner outcome
and evidence boundary explicit. The image-failure command uses a narrow
strategic merge patch, and every `kubectl` command names the intended context.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Local deployment learning path](knowledge/cross-topic-guides/local-deployment-learning-path.md) | Reworked with a sequence/outcome map, clearer Deployment/Service/port-forward model, two-replica rolling-update arithmetic, bounded failure interpretation, explicit context, recovery, and official next steps. | Current kind, Kubernetes, and Git references were checked. The earlier revision recorded a 2026-09-19 local run. This revised patch and command sequence were **not** run: no active Docker daemon, kind, or kubectl is available in the current environment. Claude Code remained at its weekly limit, so no Opus review occurred. | Run the revised path end to end in a disposable local cluster; independent Kubernetes and Opus review; KB-14 reader test; freshness decision. |

### Wave 53 (2026-10-02)

The Crossplane-on-AWS explanation now follows a request through its
Kubernetes and AWS objects, then teaches the four decisions that
control bootstrap, identity, API exposure, and external ownership.
This completes an initial teaching pass for all sixteen cross-topic
guides, not their independent review or reader testing.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Crossplane on AWS](knowledge/cross-topic-guides/crossplane-on-aws.md) | Rewritten with a bounded library-desk analogy, invented payments bucket request, XR-to-MR-to-AWS diagram, four-boundary table, Pod Identity/IRSA conditions, ownership and deletion cautions, and failure handoffs. | Keyed current Crossplane and Amazon EKS documentation. No provider, bucket, IAM role, controller, account, application, deletion, or reader test ran. Claude Code remained at its weekly limit, so no Opus review occurred. | Independent Crossplane/AWS security and Opus review; controlled provider-identity, account, lifecycle, and deletion exercises; reader test; freshness decision. |

### Wave 54 (2026-10-02)

The Common Git use cases guide now teaches one small change from an
updated `develop` branch to a reviewable remote topic branch, with
clear boundaries between local edits, staged content, commits, and
published work.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Common Git use cases](knowledge/git/commands/common-use-cases.md) | Rewritten as an outcome-led branch workflow with context checks, staged review, three-dot branch comparison, first push, stop signals, and short routes to other tasks. | Current official Git documentation was checked. The core fetch/switch/pull/edit/add/diff/commit/push sequence succeeded in a disposable clone with a bare remote; no real GitHub pull request or reader test was run. Claude Code remained at its weekly limit, so no Opus review occurred. | Independent Git/Opus review; reader task for branch selection, staged-versus-working-tree reasoning, and remote publishing; freshness decision. |

### Wave 55 (2026-10-02)

Solve Git issues now routes a reader by symptom and change location
instead of repeating a broad list of destructive commands. The
detailed recovery procedures remain in Undo and recovery.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Solve Git issues](knowledge/git/commands/solve-issues.md) | Rewritten as a Troubleshooting Guide with read-only first checks, a symptom-to-route table, an index-versus-working-tree example, and stop signals for destructive or shared-history changes. | Current official Git references were checked. The staged-file example was reproduced in a disposable repository; no shared-branch revert, lost-commit recovery, or reader test was run. Claude Code remained at its weekly limit, so no Opus review occurred. | Independent Git/Opus review; reader tasks for staged, shared-history, and lost-commit scenarios; freshness decision. |

### Wave 56 (2026-10-02)

Git troubleshooting commands now begins with read-only context
checks and routes four distinct symptoms to focused evidence.
The guide no longer interleaves diagnostic commands with actions
that change tracked files, credentials, or repository maintenance state.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Git troubleshooting commands](knowledge/git/commands/troubleshooting-commands.md) | Rewritten with branch/upstream, ignored-file, conflict, and object-integrity paths; each explains what the check can and cannot establish. | Current official Git documentation was checked. A disposable repository reproduced a tracked `build/output.txt` still appearing in status despite a matching ignore rule. No remote rejection, conflict, corruption, or reader test was run. Claude Code remained at its weekly limit, so no Opus review occurred. | Independent Git/Opus review; reader tasks for rejected push and tracked-file confusion; freshness decision. |

### Wave 57 (2026-10-02)

GitHub Actions common solutions now traces the first missing
handoff from event to run, job, step, credentials, and outcome.
It distinguishes GitHub token scope, secret availability, and
cloud OIDC trust before suggesting a configuration change.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [GitHub Actions common solutions](knowledge/git/github-actions/common-solutions.md) | Rewritten as a Troubleshooting Guide with an event-to-outcome diagram, text alternative, bounded branch/path trigger example, symptom table, repository versus cloud authority map, and environment/concurrency limits. | Keyed current official GitHub documentation. No workflow, runner, secret, OIDC exchange, deployment, or reader test ran. Claude Code remained at its weekly limit, so no Opus review occurred. | Independent GitHub Actions/security and Opus review; controlled trigger, fork, permission, OIDC, and queue cases; reader test; freshness decision. |

### Wave 58 (2026-10-02)

The Terraform local state tutorial now explains each change in
state before showing the command. It uses a disposable copy and
reviewed saved plans for create, in-place update, and destroy.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Terraform local state lifecycle](knowledge/terraform/examples/local-state-lifecycle/local-state-lifecycle.md) | Rewritten as a Tutorial with a stage table, expected outcomes, stop conditions, state-file boundaries, and understanding checks. | The full revised sequence ran in a disposable local directory with Terraform v1.13.1 from an official archive verified against its published SHA-256 sum. Observed one addition, one in-place update, one destruction, and empty final state. No cloud resource or human reader test was involved. Claude Code remained at its weekly limit, so no Opus review occurred. | Independent Terraform and Opus review; novice reader exercise; freshness decision. |

### Wave 59 (2026-10-02)

The two older stable Terraform pages have been substantially rewritten
for beginners. Their previous 2026-09-21 source review no longer covers
the new text, so both now show `draft` status and need fresh review.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Terraform state management](knowledge/terraform/fundamentals/state-management.md) | Explains address-to-object binding, backend and lock boundaries, drift, and reviewed moves/removals through an invented server, bounded register analogy, diagram and text alternative, and understanding checks. | Current official HashiCorp state, backend, locking, plan, sensitive-data, moved, and removed documentation checked. Mermaid diagram rendered and visually inspected. The example was not run. Claude Code remained at its weekly limit. | Independent Terraform and Opus review; novice reader test; freshness decision. |
| [Review and apply a Terraform change](knowledge/terraform/commands/core-workflow.md) | Turns a command reference into a target-to-verification How-to Guide with expected evidence at each stage, saved-plan approval boundary, partial-apply caution, and service check. | Current official HashiCorp CLI and lock-file documentation checked. The `fmt -recursive -check` and `workspace show` commands passed in the separate disposable local lab; no cloud plan or apply ran for the illustrative staging service. Claude Code remained at its weekly limit. | Independent Terraform and Opus review; project-specific approval, backend, and service checks; novice reader test; freshness decision. |

### Wave 60 (2026-10-02)

Git undo and recovery now starts with the location of the mistake
and uses narrow changes before considering history edits. The prior
2026-09-21 review does not cover the rewritten text, so the page is
`draft` pending fresh review.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Git undo and recovery](knowledge/git/troubleshooting/undo-and-recovery.md) | Symptom-to-location table and decision diagram; a staged-versus-working-tree file example; scoped restore, revert, private soft reset, reflog branch, and untracked cleanup paths with explicit stop conditions. | Current official Git documentation checked. A Git 2.53.0 disposable repository reproduced the file example and confirmed restore, branch-backed soft reset, scoped clean, and revert. `git clean -n -- build/` summarized the directory, prompting an added individual-file inspection step. Mermaid diagram rendered and visually inspected. Claude Code remained at its weekly limit. | Independent Git and Opus review; novice reader tasks including shared commit and lost tip; complex conflict and sparse-checkout cases; freshness decision. |

### Wave 61 (2026-10-02)

The GitHub Actions examples page now teaches how to choose a workflow
shape before copying YAML. Its previous broad recipes included stale
action versions and an invalid Terraform example, so the replacement is
`draft` pending review.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [GitHub Actions workflow shapes](knowledge/git/github-actions/examples-and-use-cases.md) | Event, job, permission, and inspectable-result model; PR, matrix, publishing, deployment, maintenance, and Terraform choices; one bounded PR test example; merge-gate and user-outcome boundaries; diagram and understanding checks. | Current official GitHub workflow, token, branch, environment, registry, and action documentation checked. The illustrative YAML parsed and the Mermaid diagram rendered and was visually inspected. No workflow executed in a repository; Claude Code remained at its weekly limit. | Independent Actions and Opus review; actual repository workflow run; novice reader tasks; freshness decision. |

### Wave 62 (2026-10-02)

The GitHub Actions command page now has a single reader task: inspect a
run, locate the first failure, and choose an appropriate next action.
The earlier broad command inventory mixed terminal and in-job controls.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Inspect a GitHub Actions run](knowledge/git/github-actions/commands.md) | One failed-run path through list, view, failed-step logs, and fix-versus-rerun choice; a boundary table distinguishes terminal CLI commands from job environment files and marks privileged controls. | Current official GitHub CLI and Actions documentation checked. Read-only `gh run list` and `gh run view` succeeded on this repository; `gh run rerun --help` confirmed flags. No workflow was triggered or rerun. Claude Code remained at its weekly limit. | Independent Actions and Opus review; novice reader task on a failed run; controlled rerun exercise; freshness decision. |

### Wave 63 (2026-10-02)

The Actions `uses` catalog now teaches how to choose a dependency from
its source and authority instead of offering broad, copyable recipes
whose versions and permissions can drift.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Choose a GitHub Actions action](knowledge/git/github-actions/actions-and-uses-catalog.md) | Explains step actions versus job-level reusable workflows; groups common official and vendor-maintained source repositories by need; gives a reviewed-ref, metadata, permission, and outcome checklist with a bounded checkout example. | Current official GitHub workflow syntax, secure-use, reusable-workflow, token, checkout, and setup-node documentation checked. The older unverified deployment, third-party, and obsolete-version snippets were removed. No sample workflow executed; Claude Code remained at its weekly limit. | Independent Actions/security and Opus review; novice action-selection task; workflow execution and freshness decision. |

### Wave 64 (2026-10-02)

The advanced Git page now shows one safe, useful operation in depth:
inspect a previous commit beside unfinished work. The prior command
inventory mixed routine read tasks, history rewrites, server commands,
and a fictitious review note in a copyable example.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Inspect an older Git revision in a second worktree](knowledge/git/commands/advanced-commands.md) | Explains shared repository data versus separate files, indexes, and `HEAD`; a clean temporary checkout, checks before removal, diagram, and task-to-command boundaries for rebase, range-diff, cherry-pick, bisect, sparse checkout, fsck, and leased force push. | Current official Git documentation checked. The full worktree add, inspect, status, remove sequence passed in a disposable Git 2.53.0 repository while an edit in the original directory remained intact. Mermaid rendered and was visually inspected. Claude Code remained at its weekly limit. | Independent Git and Opus review; novice reader task; version and platform variation; freshness decision. |

### Wave 65 (2026-10-02)

The version-sensitive “complete” Git inventory is now a task-based
command map. Readers can find the exact manual for a command and see
whether it reads files, changes the index, moves local history, contacts
a remote, or touches repository maintenance data.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Find the right Git command](knowledge/git/commands/complete-command-catalog.md) | Task-to-command map with official manual links; state and effect boundaries; installed-command discovery; a bounded unstaged-versus-staged file example; links to focused Git teaching routes. | Official Git command, everyday, CLI, and revision documentation checked. `git help -a` and the status/diff example were checked on Git 2.53.0, with the file example reproduced in a disposable repository. No Opus review occurred. | Independent Git and Opus review; novice command-selection task; version and platform variation; freshness decision. |

### Wave 66 (2026-10-02)

The MCP entry now teaches one relationship: how an AI host uses a
client to request a server capability. A bounded knowledge-search
example shows what the protocol carries and where source quality,
permissions, and answer evaluation remain separate responsibilities.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Model Context Protocol](knowledge/ai/ai-tooling/model-context-protocol.md) | Host, client, and server roles; tools, resources, and prompts; illustrative Terraform-state lookup; transport and permission boundaries; current official learning links. Removed obsolete, unrun SDK recipes. | Official MCP architecture, base protocol, tools, resources, transport, and TypeScript SDK v2 documentation checked. Mermaid rendered and visually inspected. No live MCP server or Opus review occurred. | Independent MCP and Opus review; novice concept task; current SDK example in a separate how-to if needed; freshness decision. |

### Wave 67 (2026-10-02)

The knowledge-base overview now starts with the reader's goal:
understand a topic simply, then follow the official documentation for
precise details. It shows how one curated Markdown article becomes
discoverable without treating the website or search index as another
source of truth.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Knowledge-base creation, management, and optimization](knowledge/ai/ai-tooling/knowledge-bases-creation-management-and-optimization.md) | Plain-language source-to-reader model; bounded Terraform-state example; diagram and text alternative; roles for topic indexes, static website, search, and optional AI access; new-topic path. | Official Git, OKF, Astro, Pagefind, MCP, and HashiCorp documentation checked. Mermaid rendered and visually inspected. No Opus review occurred. | Independent content/architecture and Opus review; novice reader task; website integration check; freshness decision. |

### Wave 68 (2026-10-02)

The proof-of-concept page now shows why a team runs a small experiment:
to reduce one important uncertainty before committing to a larger
project. The knowledge-search example separates a reproducible test
from claims about future readers or production readiness.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Proof of concept](knowledge/solutions-architect/proof-of-concept.md) | One-unknown model, decision-flow diagram and text alternative, bounded invented search example, evidence and production boundaries, official next-step links. | Official Google Cloud migration, Azure Well-Architected, and AWS Redshift PoC guidance checked. Mermaid rendered and visually inspected. No experiment or Opus review occurred. | Independent architecture and Opus review; novice reader task; a real PoC record if this repository later runs one; freshness decision. |

### Wave 69 (2026-10-02)

The reference architecture now gives readers a small, accurate
source-to-article-to-reader model and a separate change path. It
labels reconciliation and optional AI access as design choices rather
than implying that those services already run.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Reference architecture](knowledge/ai/ai-tooling/knowledge-bases/reference-architecture.md) | Distinguishes upstream product authority, curated Markdown authority, and rebuildable outputs; shows the reading and change paths; provides a Terraform-state example and new-topic rule. | Official OKF, Git, Astro, Pagefind, MCP, and HashiCorp documentation checked. Two Mermaid diagrams rendered and visually inspected. No Opus review occurred. | Independent architecture and Opus review; novice reader task; actual website and reconciliation behavior check; freshness decision. |

### Wave 70 (2026-10-02)

The AI knowledge-security page now starts with a trust boundary a
beginner can remember: retrieved text is evidence, not permission or
instruction. The invented example ties that boundary to document
access at search and fetch time and to a separate review path for edits.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Security and governance](knowledge/ai/ai-tooling/knowledge-bases/security-and-governance.md) | Three trust boundaries, bounded public/private retrieval example, diagram and text alternative, risk-to-evidence table, official deeper study. | Current OWASP prompt-injection, Azure AI Search document access, MCP tools, and NIST AI RMF guidance checked. Mermaid rendered and visually inspected. No attack test or Opus review occurred. | Independent security and Opus review; novice reader task; adversarial retrieval test if a private corpus is introduced; freshness decision. |

### Wave 71 (2026-10-02)

The standards page now answers a reader's first question: which job
needs a format or tool? An invented Orders API shows why an API schema,
a beginner article, search, MCP, and an optional relationship graph do
different work.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Knowledge standards landscape](knowledge/ai/ai-tooling/knowledge-bases/knowledge-standards-landscape.md) | Task-based layer map, bounded Orders API example, optional graph roles, diagram and text alternative, official specification links, RDF maturity distinction. | Current primary OKF, OpenAPI, AsyncAPI, JSON Schema, W3C, MCP, AGENTS.md, and llms.txt documents checked. Mermaid rendered and visually inspected. No Opus review occurred. | Independent standards and Opus review; novice choice task; freshness check for evolving specifications. |

### Wave 72 (2026-10-02)

The CrashLoopBackOff page now treats the status as a restart delay,
not a root cause. Its read-only diagnostic path leads from the last
terminated container and prior logs to a specific next investigation.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Diagnose CrashLoopBackOff](knowledge/kubernetes/troubleshooting/crashloopbackoff.md) | Context check, last-state and previous-log inspection, decision diagram and text alternative, cause table, invented missing-setting example, verification after a fix. | Current official Kubernetes Pod lifecycle, debug, logs, probe, and resource documentation checked. Mermaid rendered and visually inspected. No cluster or Opus review occurred. | Independent Kubernetes and Opus review; novice symptom task; disposable cluster reproduction; freshness decision. |

### Wave 73 (2026-10-02)

The kubectl entry now follows one beginner task from cluster context
to Deployment, Pods, events, and logs. It avoids assuming that a
Deployment name is also its Pod label and treats workload readiness
as different from a user-path test.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Inspect a Kubernetes Deployment with kubectl](knowledge/kubernetes/commands/kubectl-basics.md) | Read-only context-to-Pod task, selector check, evidence interpretation, invented two-replica case, decision table, diagram and text alternative. Removed an unsupported freshness date. | Current official Kubernetes kubectl context/get/logs, Deployment, and Pod debugging documentation checked. Mermaid rendered and visually inspected. No cluster or Opus review occurred. | Independent Kubernetes and Opus review; beginner task in disposable cluster; permission and platform variation; freshness decision. |

### Wave 74 (2026-10-02)

The kind page now uses local image pull failure as its primary
troubleshooting outcome. It checks the selected cluster and the Pod's
recorded image and pull policy before giving a scoped image-load action.
Other local symptoms lead to their own evidence and official guidance.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Diagnose a local image pull in kind](knowledge/kubernetes/troubleshooting/kind.md) | Read-first local image path, computer-versus-node image model, conditional `kind load` fix, post-fix check, and routes for context, runtime, scheduling, and host-port symptoms. | Current official kind and Kubernetes documentation checked. No cluster or Opus review occurred. | Independent Kubernetes and Opus review; disposable kind reproduction for matching and mismatched tags and pull policies; beginner symptom task; freshness decision. |

### Wave 75 (2026-10-02)

The two kind explanations now form a route from cluster shape to image
distribution and finally to symptom diagnosis. Their examples separate
configuration at cluster creation, a NodePort Service inside the cluster,
and the image path from a host or registry to a node.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [How kind custom clusters fit together](knowledge/kubernetes/applications-and-tools/kind-custom-clusters.md) | Host/container-node model, limited multi-node analogy, illustrative two-node configuration, complete host-to-Pod port path, node-versus-app-image distinction, and understanding checks. | Current official kind Configuration, Quick Start, Node Image, and Kubernetes Service documentation checked. Example YAML parsed; both Mermaid diagrams rendered and inspected. No kind cluster or Opus review occurred. | Independent Kubernetes and Opus review; disposable cluster with matching and mismatched NodePort; beginner model task; freshness decision. |
| [How images reach a kind Pod](knowledge/kubernetes/applications-and-tools/kind-images-and-local-registries.md) | Side-load-versus-registry decision, host/node network boundary, pull-policy behavior, private-registry scope, image-flow diagram, and evidence-based failure routes. Removed bare registry push commands that omitted setup. | Current official kind Quick Start, Local Registry, Private Registries, and Kubernetes Images documentation checked. Mermaid rendered and inspected. No image build, registry, cluster, or Opus review occurred. | Independent Kubernetes and Opus review; disposable side-load and configured-registry exercises; beginner image-path task; freshness decision. |

### Wave 76 (2026-10-02)

The Kubernetes command pages now separate a read-only opening inspection
from a reviewed live change. The first leads readers to the right
diagnostic path; the second makes diff, apply, rollout, and user
verification distinct checks.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Begin a safe kubectl inspection session](knowledge/kubernetes/commands/daily-usage.md) | Context-and-namespace check, Deployment and Pod scan, one-Pod evidence path, bounded address analogy, diagram and text alternative, symptom routes. | Current official Kubernetes context, get, describe, logs, and Pod-debug documentation checked. Mermaid rendered and inspected. No cluster or Opus review occurred. | Independent Kubernetes and Opus review; beginner inspection in a disposable cluster; access-variation check; freshness decision. |
| [Review and apply a Kubernetes manifest change](knowledge/kubernetes/commands/common-commands.md) | Scoped target-to-user path, `kubectl diff` exit-code interpretation, manifest review, apply, rollout and user verification, source-of-truth recovery boundary, diagram and text alternative. | Current official Kubernetes diff, apply, rollout-status, Deployment, and context documentation checked. Mermaid rendered and inspected. No cluster or Opus review occurred. | Independent Kubernetes and Opus review; disposable rollout and failed-rollout exercise; beginner change task; freshness decision. |

### Wave 77 (2026-10-03)

The Kubernetes troubleshooting overview now helps a reader find the first
failed handoff from Pod state to Service and user request. The former
multi-workflow command page now answers a different, focused question:
is a CPU or memory symptom caused by a scheduling request, a container
limit, or node pressure?

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Find the first failing Kubernetes boundary](knowledge/kubernetes/troubleshooting/common-solutions.md) | Read-first symptom map, staged request diagram, invented Service example, selector/readiness/EndpointSlice distinction, `publishNotReadyAddresses` caveat, and focused next routes. Removed unreviewed test-Pod creation and rollback recipes. | Current official Kubernetes Pod lifecycle, Debug Pods, Debug Services, Service, and EndpointSlices documentation checked. Mermaid rendered and inspected. No cluster or Opus review occurred. | Independent Kubernetes and Opus review; novice symptom-to-check task; disposable Service-selector and readiness reproductions; freshness decision. |
| [Investigate Kubernetes resource pressure](knowledge/kubernetes/commands/workflows.md) | Requests-versus-limits-versus-node-pressure model, read-only diagnostic path, optional metrics with delay and scope limits, invented insufficient-memory scheduling case, diagram and text alternative. | Current official Kubernetes resource management, node-pressure, kubectl top, metrics pipeline, and Pod-debug documentation checked. Mermaid rendered and inspected. No cluster or Opus review occurred. | Independent Kubernetes and Opus review; disposable scheduling/OOM/eviction cases; novice resource-symptom task; freshness decision. |

### Wave 78 (2026-10-03)

The former advanced command catalog now focuses on one reader task:
distinguish what an API field permits, what a Deployment currently stores,
and what the API server would accept from a proposed manifest. The tricks
index now routes readers to focused tasks and retains only read-oriented
examples.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Inspect a Kubernetes API field before changing a manifest](knowledge/kubernetes/commands/advanced-commands.md) | Schema/live/proposed model, invented Deployment, scoped inspection and server dry-run steps, permissions and dry-run limits, diagram and text alternative. Moved debugging, node maintenance, and field ownership to their official procedures. | Current official Kubernetes api-resources, explain, get, apply, and API dry-run documentation checked. Mermaid rendered and inspected. No cluster or Opus review occurred. | Independent Kubernetes and Opus review; disposable dry-run success, authorization failure, and webhook case; novice field-inspection task; freshness decision. |

### Wave 79 (2026-10-03)

The former eksctl command catalog now helps a reader choose the owner of
an EKS change before choosing a tool or procedure. Its invented Pending-Pod
case separates Deployment replicas, scheduling evidence, and the cluster's
compute path. It also corrects the earlier implication that eksctl's cluster
dry run is a complete AWS change preview.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Choose the right control path for an EKS change](knowledge/kubernetes/commands/eksctl-commands.md) | Workload/compute/access ownership model, bounded class-and-building analogy, invented lesson-API case, read-only target checks, diagram and text alternative, focused AWS and Kubernetes references. Removed live infrastructure mutation recipes. | Current official eksctl overview, cluster, node-group, access-entry, Pod Identity, Auto Mode, and dry-run documentation checked, along with Kubernetes Deployment documentation. Mermaid rendered and inspected. No AWS or cluster command or Opus review occurred. | Independent EKS and Opus review; disposable target-and-scheduling scenario; novice owner-selection task; freshness decision. |

### Wave 80 (2026-10-03)

The Helm page now teaches the chart, values, rendered manifest, and
release-revision relationship before pointing to deeper procedures. An
invented two-environment example separates a chart package from two
installations. Crossplane installation remains an example of where Helm's
release boundary ends and another controller's package lifecycle begins.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [How Helm turns a chart into a release](knowledge/kubernetes/applications-and-tools/helm.md) | Blueprint analogy with limits, chart/values/release diagram and text alternative, invented dev/prod release comparison, preview-versus-server-versus-user checks, rollback and CRD boundaries, Crossplane controller handoff. Replaced unrun install and provider mutation recipes with official procedures. | Current official Helm usage, template, upgrade, status, and CRD documentation plus Crossplane install and provider documentation checked. Mermaid rendered and inspected. No Helm binary, cluster exercise, or Opus review occurred. | Independent Helm/Crossplane and Opus review; disposable chart rendering and cluster release exercise; novice chart-versus-release task; freshness decision. |

### Wave 81 (2026-10-03)

The K9s page now follows one inspection task from context and namespace
to a selected Pod, its description, logs, and the next evidence route.
It replaces a large, version-sensitive shortcut inventory with the small
set of keys documented for that task and distinguishes read-only UI
controls from actual Kubernetes authorization.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Inspect a failing Pod with K9s](knowledge/kubernetes/applications-and-tools/k9s.md) | Context-to-Pod evidence path, invented image-pull row, status-versus-cause distinction, symptom table, diagram and text alternative, read-only-mode limit, focused official sources. Removed unverified shortcuts, config recipes, and live modification routes. | Current official K9s overview, commands, and configuration plus Kubernetes Pod lifecycle and Pod-debug documentation checked. Mermaid rendered and inspected. No K9s binary, cluster session, or Opus review occurred. | Independent K9s/Kubernetes and Opus review; versioned K9s walkthrough in a disposable cluster; novice Pod-inspection task; freshness decision. |

### Not yet reviewed against the teaching standard

Counts come from the generated catalog on 2026-10-03, which records 165
concepts. The "authored to the standard" column covers waves 1 to 81
together: one hundred ten concepts, none of them independently reviewed after
their teaching passes. The remaining 55 have not yet been authored or
assessed against the teaching standard.

The embedded OKF example under AI tooling uses reserved types for format
demonstration, so most teaching elements do not apply there.

| Area | Concepts in catalog | Authored to the standard | Not yet reviewed |
| --- | --- | --- | --- |
| Bundle root (Start here, glossary) | 2 | 1 | 1 |
| AI, including the embedded OKF example | 20 | 8 | 12 |
| Cloud | 21 | 21 | 0 |
| Cross-topic guides | 16 | 16 | 0 |
| Databases | 11 | 11 | 0 |
| Decision records | 5 | 0 | 5 |
| DevOps | 2 | 2 | 0 |
| FinOps | 1 | 1 | 0 |
| Git | 17 | 17 | 0 |
| Kubernetes | 45 | 20 | 25 |
| Migrations | 9 | 2 | 7 |
| Programming languages | 3 | 3 | 0 |
| Security | 3 | 3 | 0 |
| Solutions architect | 1 | 1 | 0 |
| Templates | 5 | 0 | 5 |
| Terraform | 4 | 4 | 0 |
| **Total** | **165** | **110** | **55** |

All four Terraform and all 17 Git concepts have now received an initial
teaching pass. Their drafts still need independent review and reader tasks
before stronger trust claims.

### Candidates for the next wave

- Try the revised knowledge article template on the next new Explanation and
  How-to Guide, and record what a contributor found unclear.
- Align the practical example, troubleshooting, and command reference
  templates with the type-specific expectations.
- Link glossary entries for working tree, index, reconciliation, and state to
  the new explanations.
- The sibling pages the wave 2 rewrites now link to and partly overlap:
  Kafka fundamentals, MongoDB data modeling, OIDC token validation, CDN
  caching and origin protection, and stateful workloads.
- The sibling pages the wave 4 rewrites now link to and partly overlap: Flux
  reconciliation and Helm releases, GitOps security and multi-tenancy, and
  tooling clusters.
- The network and storage procedures adjacent to wave 5: APISIX architecture,
  Velero storage and volume backups, and the missing beginner Service concept.
- The cross-topic guides now need independent technical review and
  reader-task testing after their initial teaching passes.
- A dedicated observability section, if reader demand supports it; the
  observability explanation currently links to troubleshooting pages because
  no such section exists.
- The local deployment learning path's "Concepts before commands" section.
- Terraform language basics, variables, and outputs as focused explanations.

## Expansion phases

### Phase 1: make priority operational guidance dependable

Review the ten guides in the [maintenance review
queue](maintenance-review-queue.md#priority-operational-guide-queue): Git
recovery; Crossplane provider authentication and the AWS S3 lab; Terraform
workflow and state; Kafka delivery; Velero installation, restore, and disaster
recovery; and EKS deployment.

For each guide, confirm the scope against official sources, correct ambiguous
or stale claims, add prerequisites and verification signals, and preserve the
honest evidence limitation. Promote a guide to `stable` only when its sources,
review record, freshness deadline, and maintainer meet the repository profile.
Where an authorized sandbox run is useful, record the actual version,
environment, result, and cleanup proof; do not require a live environment to
write or correct source-reviewed documentation.

**Exit criterion:** each selected guide has a documented evidence level, a
clear next review decision, no known high-risk unsupported claim, and a
maintainer or an explicitly recorded unassigned status in the review queue.

### Phase 2: complete the core reader journeys

Strengthen the routes people are most likely to use first:

- Git: state model, safe undo decision tree, conflicts, and recovery limits.
- Kubernetes: workload diagnosis from symptom through logs, events, resource
  inspection, ownership, and safe recovery.
- Terraform: provider, resource, variable, module, state, backend, plan, and
  apply as one connected workflow, with local and remote-state boundaries.
- Cloud and FinOps: IAM and networking prerequisites, cost allocation,
  budgets, anomalies, and the choices that affect cost responsibility.

Use the reader-test tasks to identify the exact broken handoff between pages.
Favour a complete sequence with verification over a large standalone overview.

**Exit criterion:** a reader can start from `knowledge/start-here.md`, finish
the local route, find a next route for a stated task, and complete the selected
task without an unexplained prerequisite or navigation dead end.

### Phase 3: add focused coverage by evidence and dependency

Add new concepts in small, linked slices. Start with missing pages that enable
existing routes: Kubernetes services, DNS, storage, scheduling, ingress, and
common workload failures; Terraform modules, providers, backends, variables,
and workspaces; AWS IAM and networking; and cross-topic deployment examples.

Treat AI agents, LLM, ML, MLOps, programming languages, Azure, and Google
Cloud as planned coverage until a focused brief establishes a reader need,
scope, official-source set, and maintainer path. Do not fill an index with
thin summaries merely to make a category look complete.

**Exit criterion:** each new page has a primary outcome, the correct Diátaxis
type, a parent-index link, related links, and an evidence plan before its first
substantive draft is merged.

### Phase 4: improve AI retrieval and answer grounding

Expand `tests/retrieval-cases.yaml` with questions from reader research,
support issues, and high-risk tasks. Each case should identify the expected
concept, the metadata or source evidence an agent should inspect, and the
condition that makes an answer unsafe or incomplete.

Measure whether an agent can find the right page within the retrieval budget,
distinguish draft from stable material, and cite source-backed claims when a
source record exists. Add a serving or search layer only after those measures
show a navigation or retrieval gap that repository Markdown and the generated
catalog cannot address.

**Exit criterion:** the golden cases cover core learning, troubleshooting,
decision, and safety questions; failures create small content, metadata, or
navigation changes with a recorded reason.

### Phase 5: run a sustainable feedback and review loop

Recruit three to five willing readers through the existing privacy-aware
protocol. Ask them to perform the documented tasks, record only the approved
anonymous results, and convert recurring confusion into focused improvements.

Review `stable` technical concepts at their freshness deadline or when an
upstream release, deprecation, or security change affects them. Review `draft`
concepts when a contributor is ready to supply the missing evidence. Update
the log, catalog, indexes, and changelog whenever a change affects navigation,
trust, or lifecycle status.

**Exit criterion:** reader results identify repeated blockers, at least one
improvement is linked to observed feedback, and overdue stable pages are
reviewed, deprecated, or returned to draft rather than silently left stale.

## Contributor workflow

For each content change, follow this sequence:

1. Write a brief: reader question, outcome, Diátaxis type, target route,
   prerequisite pages, evidence sources, and success signal.
2. Inspect existing pages and indexes to avoid duplicate concepts and select
   the smallest coherent change.
3. Draft using the relevant template. Build the explanation before adding
   detail or commands.
4. Check the precision protocol with a source reviewer or the contributor who
   verified the claim. Record only evidence that actually exists.
5. Validate the page and the whole repository using the checks in
   [AGENTS.md](AGENTS.md#validation-and-publication).
6. Update indexes, related links, glossary terms, `knowledge/log.md`, and
   `CHANGELOG.md` when the change requires them.
7. Add or refine a retrieval case when the change addresses a task an AI agent
   should be able to discover reliably.

## Measures and review cadence

Use these measures to guide improvement. They are targets for evidence and
learning, not grounds to label content complete prematurely.

| Measure | Initial target | Evidence |
| --- | --- | --- |
| Priority-guide review | All ten queue entries have a current scope and evidence decision. | Maintenance queue and page review records. |
| Trust coverage | Every `stable` technical concept has genuine sources, a review record, freshness deadline, and owner. | OKF validation and metadata review. |
| Explanation quality | Every selected core concept answers purpose, model, trade-off, example, and next action. | Editorial review checklist. |
| Reader navigation | Most reader-test tasks are completed without hints or a reported route blocker. | Anonymous reader-test results. |
| AI discoverability | Every core task has a passing golden retrieval case with the intended guide in scope. | Retrieval-case validation and measured runner, when available. |
| Freshness | No stable concept remains past its review deadline without a recorded decision. | Maintenance queue and OKF metadata. |

Run page-level checks in every content change. Review the maintenance queue at
least monthly, review coverage and reader feedback quarterly, and re-prioritize
after upstream product changes or repeated reader failures. Adjust the cadence
when the number of stable pages or contributor capacity makes a shorter cycle
necessary.

## Definition of success

The knowledge base is progressing well when its expansion is selective,
traceable, and useful. A newcomer can follow a complete route without guessing
what to do next. A practitioner can identify the scope and risk of a procedure
before acting. A maintainer can tell who reviewed a stable claim and when it is
due again. An AI agent can find the right concept, respect its lifecycle status,
and ground an answer in the material rather than inventing certainty.

## Related links

- [Knowledge bundle](knowledge/index.md)
- [Roadmap](ROADMAP.md)
- [Knowledge-base improvement plan](knowledge-base-improvement-plan.md)
- [Knowledge-base review](knowledge-base-review.md)
- [Maintenance review queue](maintenance-review-queue.md)
- [Reader test facilitator guide](reader-test-facilitator-guide.md)
- [Writing instructions](instructions.md)
- [Contributor guide](CONTRIBUTING.md)
- [AI agent guide](AGENTS.md)
- [Back to repository index](README.md)
