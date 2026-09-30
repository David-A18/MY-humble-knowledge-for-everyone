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

### Not yet reviewed against the teaching standard

Counts come from the generated catalog on 2026-09-30, which records 165
concepts. The "authored to the standard" column covers waves 1 to 21
together: forty-one concepts, none of them independently reviewed after
their teaching passes. The remaining 124 have not yet been authored or
assessed against the teaching standard.

The embedded OKF example under AI tooling uses reserved types for format
demonstration, so most teaching elements do not apply there.

| Area | Concepts in catalog | Authored to the standard | Not yet reviewed |
| --- | --- | --- | --- |
| Bundle root (Start here, glossary) | 2 | 1 | 1 |
| AI, including the embedded OKF example | 20 | 1 | 19 |
| Cloud | 21 | 8 | 13 |
| Cross-topic guides | 16 | 5 | 11 |
| Databases | 11 | 5 | 6 |
| Decision records | 5 | 0 | 5 |
| DevOps | 2 | 2 | 0 |
| FinOps | 1 | 1 | 0 |
| Git | 17 | 4 | 13 |
| Kubernetes | 45 | 7 | 38 |
| Migrations | 9 | 2 | 7 |
| Programming languages | 3 | 3 | 0 |
| Security | 3 | 1 | 2 |
| Solutions architect | 1 | 0 | 1 |
| Templates | 5 | 0 | 5 |
| Terraform | 4 | 1 | 3 |
| **Total** | **165** | **41** | **124** |

The 2026-09-21 quality passes on Git undo and recovery, the core Terraform
workflow, and Terraform state management applied the precision protocol. They
have not yet been assessed against the teaching standard, so they are counted
as not yet reviewed above.

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
- The remaining cross-topic guides, which are marked as developed but have
  not been assessed against the standard, starting with deploying to EKS and
  GitOps on EKS.
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
