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

Update 2026-10-05: after correcting unsupported trust claims in the
embedded OKF example, the catalog still has 165 concepts, now all `draft`.
The initial pass covers every concept; draft status remains until review
evidence justifies a change.

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
decision each. Both stay `draft` and have no reader test, running-cluster
result, assigned maintainer, or new freshness record. The Gateway API page
received a later Opus review in [focused review round 11](#focused-review-round-11-2026-10-06).

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Gateway API and Ingress](knowledge/kubernetes/applications-and-tools/gateway-api-and-ingress.md) | Explains the external request path, listener attachment, backend references, TLS boundary, and choice of API. | Opus 5.5 read-only review and current Kubernetes/Gateway API documentation check; the two-team example is illustrative. The diagram rendered and was inspected. | Implementation-specific feature and public-request check; reader test; freshness decision. |
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
| [Cost allocation basics](knowledge/finops/cost-allocation-basics.md) | Teaches a first allocation policy with precedence, five nonoverlapping report buckets, calculated coverage measures, and a decision-tree diagram. | Opus 5.5 read-only review; current FinOps Framework, FOCUS, and AWS primary sources checked. The 100-unit report is invented; the diagram rendered and was inspected. | Independent finance review; a real provider report check; reader test; freshness decision. |
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
| [Retrieval and context efficiency](knowledge/ai/ai-tooling/knowledge-bases/retrieval-and-context-efficiency.md) | Rewritten with a plain model, library analogy, search-to-fetch diagram, illustrative result, method choices, and measurement questions. Later review clarified candidate retrieval versus reranking, permission filtering, corpus revision, and evidence budgets. | Keyed SQLite, Elasticsearch, and Azure documentation; the invented example uses the real target page's `draft` status, excerpt, and page source IDs. Claude Opus 5.5 reviewed the page read-only; the revised diagram rendered and was inspected. No retrieval service or ranking evaluation ran. | A measured search evaluation; reader test; freshness decision. |

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
| [APISIX on EKS](knowledge/cross-topic-guides/apisix-on-eks.md) | Rewritten with a limited venue analogy, invented lesson API, two-path diagram, ownership and failure tables, TLS placement, plugin boundaries, and understanding checks. A later focused review corrected the backend request path and added NLB target and client-IP decisions. | Keyed Apache APISIX and Amazon EKS/NLB documentation; Claude Opus 5.5 reviewed the focused revision read-only. No cluster, gateway, route, plugin, load balancer, client request, or reader test ran. | Independent APISIX/EKS security review; controlled route, policy, TLS, and failure checks; reader test; freshness decision. |

### Wave 49 (2026-10-02)

The EKS operations guide now starts from a symptom and traces distinct AWS,
Kubernetes, Pod-identity, and user-path evidence.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [EKS operations](knowledge/cross-topic-guides/eks-operations.md) | Rewritten with a limited library analogy, invented lesson-API incident, boundary diagram, evidence table, and understanding checks. A later focused review added an explicit Service-selector mismatch, access-error decisions, image-pull ownership, and Auto Mode caveats. | Current Amazon EKS, Amazon ECR, and Kubernetes documentation checked; Claude Opus 5.5 reviewed the focused revision read-only. No account, cluster, Pod, credential, service, user request, or reader test ran. | Independent EKS security review; controlled incident checks; reader test; freshness decision. |

### Wave 50 (2026-10-02)

The Kubernetes-on-AWS page now teaches how Kubernetes objects meet AWS
resources, with ownership varying by the EKS mode and chosen integrations.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Kubernetes on AWS](knowledge/cross-topic-guides/kubernetes-on-aws.md) | Rewritten with a limited theatre analogy, invented photo API, Kubernetes-to-AWS mapping, ownership diagram, standard/Auto Mode differences, and understanding checks. A later focused review corrected ALB target modes, integration ownership, workload identity, and storage limits. | Keyed current Amazon EKS, Amazon ECR, Amazon EBS, and Kubernetes documentation. Claude Opus 5.5 reviewed the focused revision read-only; the revised diagram was rendered and inspected. No cluster, ALB, Pod, S3 object, EBS volume, request, or reader test ran. | Independent EKS/security review; controlled network, IAM, and storage checks; reader test; freshness decision. |

### Wave 51 (2026-10-02)

The EKS tooling-cluster guide now shows the choice between local and
central controllers, the target-cluster authority required, and the
limits of a central outage.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [EKS tooling cluster architecture](knowledge/cross-topic-guides/eks-tooling-cluster-architecture.md) | Rewritten with a bounded school-district analogy, invented two-workload-cluster example, management/user-path diagram, local-versus-central comparison, failure table, and recovery questions. A later focused review added the EKS-managed Argo CD option, three target-access gates, broad-credential risk, and an outage and recovery path. | Keyed current Amazon EKS, Argo CD, Flux, and Kubernetes documentation checked; Claude Opus 5.5 reviewed the focused changes read-only, and the diagram was rendered and inspected. No cluster, controller, credentials, outage, recovery, application request, or reader test ran. | Independent EKS/GitOps security review; controlled cross-cluster access, outage, and recovery exercise; reader test; freshness decision. |

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
| [Find the right Git command](knowledge/git/commands/complete-command-catalog.md) | Task-to-command map with official manual links; state and effect boundaries; installed-command discovery; a bounded unstaged-versus-staged file example; links to focused Git teaching routes. | Official Git command, everyday, CLI, revision, switch, merge, rebase, and bisect documentation checked. In focused round 21, Claude Opus 5.5 reviewed the page twice read-only. The state example ran in a disposable Git 2.53.0 repository and a separate bisect check confirmed detached `HEAD` and reset. | Independent Git domain review; novice command-selection task; version and platform variation; freshness decision. |

### Wave 66 (2026-10-02)

The MCP entry now teaches one relationship: how an AI host uses a
client to request a server capability. A bounded knowledge-search
example shows what the protocol carries and where source quality,
permissions, and answer evaluation remain separate responsibilities.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Model Context Protocol](knowledge/ai/ai-tooling/model-context-protocol.md) | Host, client, and server roles; tools, resources, and prompts; illustrative Terraform-state lookup; transport and permission boundaries; current official learning links. Removed obsolete, unrun SDK recipes. | Official MCP architecture, base protocol, tools, resources, transport, and TypeScript SDK v2 documentation checked. In focused round 20, Claude Opus 5.5 reviewed the page twice read-only, the host/model/approval path was corrected, and the revised diagram rendered and was inspected. No live MCP server ran. | Independent MCP domain review; novice concept task; current SDK example in a separate how-to if needed; freshness decision. |

### Wave 67 (2026-10-02)

The knowledge-base overview now starts with the reader's goal:
understand a topic simply, then follow the official documentation for
precise details. It shows how one curated Markdown article becomes
discoverable without treating the website or search index as another
source of truth.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Knowledge-base creation, management, and optimization](knowledge/ai/ai-tooling/knowledge-bases-creation-management-and-optimization.md) | Plain-language source-to-reader model; bounded Terraform-state example; diagram and text alternative; roles for topic indexes, static website, search, and optional AI access; new-topic path. | Official Git, OKF, Astro, Pagefind, MCP, and HashiCorp documentation checked. In focused round 20, Claude Opus 5.5 reviewed the page twice read-only and the revised source-to-site diagram rendered and was inspected. The separate site was checked as a local scaffold. | Independent content/architecture review; novice reader task; website integration check; freshness decision. |

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
| [Reference architecture](knowledge/ai/ai-tooling/knowledge-bases/reference-architecture.md) | Distinguishes upstream product authority, curated Markdown authority, and rebuildable outputs; shows the reading and change paths; provides a Terraform-state reader journey and new-topic rule. Later review made the separate website pin, Pagefind-from-HTML order, and two review gates explicit. | Official OKF, Git, Astro, Pagefind, MCP, and HashiCorp documentation checked. Claude Opus 5.5 reviewed the page twice read-only; Codex inspected the sibling website project's lock, scripts, and deployment status directly. Both revised diagrams rendered and were inspected. | Novice reader task; actual website and reconciliation behavior check; public deployment check; freshness decision. |

### Wave 70 (2026-10-02)

The AI knowledge-security page now starts with a trust boundary a
beginner can remember: retrieved text is evidence, not permission or
instruction. The invented example ties that boundary to document
access at search and fetch time and to a separate review path for edits.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Security and governance](knowledge/ai/ai-tooling/knowledge-bases/security-and-governance.md) | Three trust boundaries, bounded public/private retrieval example, diagram and text alternative, risk-to-evidence table, official deeper study. Later review made the end reader's access, service credential, output leak path, and separate edit authority explicit. | OWASP, Azure AI Search, MCP tools and security guidance, and NIST AI RMF checked. Claude Opus 5.5 reviewed the page twice read-only; the revised diagram rendered and was inspected. No attack or private-corpus test ran. | Independent implementation-level security review; novice reader task; adversarial retrieval test if a private corpus is introduced; freshness decision. |

### Wave 71 (2026-10-02)

The standards page now answers a reader's first question: which job
needs a format or tool? An invented Orders API shows why an API schema,
a beginner article, search, MCP, and an optional relationship graph do
different work.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Knowledge standards landscape](knowledge/ai/ai-tooling/knowledge-bases/knowledge-standards-landscape.md) | Task-based layer map, bounded Orders API example, optional graph roles, diagram and text alternative, official specification links, RDF maturity distinction. | Current primary OKF, OpenAPI, AsyncAPI, JSON Schema, W3C, MCP, AGENTS.md, and llms.txt documents checked. In focused round 20, Claude Opus 5.5 reviewed the page twice read-only, OpenAPI/JSON Schema and MCP wording was corrected, W3C RDF status was checked on 2026-10-07, and the revised diagram rendered and was inspected. | Independent standards review; novice choice task; freshness check for evolving specifications. |

### Wave 72 (2026-10-02)

The CrashLoopBackOff page now treats the status as a restart delay,
not a root cause. Its read-only diagnostic path leads from the last
terminated container and prior logs to a specific next investigation.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Diagnose CrashLoopBackOff](knowledge/kubernetes/troubleshooting/crashloopbackoff.md) | Context check, per-container last-state and previous-log inspection, decision diagram and text alternative, clean-exit and init-container branches, cause table, invented missing-setting example, and verification over the prior failure interval. | Current official Kubernetes Pod lifecycle, debug, init-container, logs, probe, resource, and node-pressure documentation checked. Claude Opus 5.5 reviewed the guide read-only; revised Mermaid rendered and was visually inspected. No cluster or reader task ran. | Independent Kubernetes review; novice symptom task; disposable cluster reproduction; freshness decision. |

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

### Wave 82 (2026-10-03)

The APISIX troubleshooting page now answers one symptom question:
which component returned a 404 for a specific request? It separates
the request path from the controller configuration path, uses an
invented Gateway API route, and treats accepted route status as
evidence about configuration rather than a guarantee of matching
the real request.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Trace an APISIX 404 to its first failed handoff](knowledge/kubernetes/troubleshooting/apisix.md) | Exact-request capture, entry/gateway/route/backend boundaries, controller handoff diagram and text alternative, read-only HTTPRoute inspection, conditional listener-port mismatch, evidence-to-next-step table, official source routes. | Current official APISIX deployment, Gateway API support, configuration troubleshooting, Gateway API HTTPRoute, and Kubernetes Service-debug documentation checked. Mermaid rendered and inspected. No gateway, cluster, request, or Opus review occurred. | Independent APISIX/Gateway API and Opus review; disposable route-match and listener-port reproductions; novice 404 task; freshness decision. |

### Wave 83 (2026-10-03)

The Flux reconciliation page now follows a `HelmRelease` declaration in Git
through two different controllers. The example deliberately uses an unusable
chart address and invented versions. An explicit `healthChecks` entry shows
when a ready `Kustomization` also waits for the Helm release, while the
separate chart-source path explains where the package comes from.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [How Flux applies a HelmRelease from Git](knowledge/kubernetes/applications-and-tools/flux-reconciliation-and-helm.md) | Request-and-installer analogy with limits, two-path diagram and text alternative, invented Git/chart example, minimal manifests, source-to-reconciler status table, explicit health-check and pruning implications, focused official source routes. | Current official Flux Kustomization, HelmRelease, Helm-repository, Helm guide, and troubleshooting documentation checked. Mermaid rendered and inspected. No Flux or Helm binary, chart fetch, cluster run, or Opus review occurred. | Independent Flux/Helm and Opus review; disposable chart/release exercise including fetch and health-check failures; novice controller-handoff task; freshness decision. |

### Wave 84 (2026-10-03)

The GitOps security page now explains which human and machine identities
matter at each boundary. It removes an incomplete Flux manifest that could
have implied `targetNamespace` and `serviceAccountName` alone created a
tested tenant boundary. The invented two-team example distinguishes Argo CD
project policy, Flux impersonation in both controller stages, Kubernetes
workload access, and secret delivery.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [GitOps security and multi-tenancy](knowledge/kubernetes/applications-and-tools/gitops-security-and-multitenancy.md) | Delivery-desk analogy with limits, four-gate diagram and text alternative, invented payments/catalog boundary, Argo CD and Flux control explanations, secret and workload-access boundaries, understanding checks, official routes. Removed incomplete security YAML and untested incident mutations. | Current official GitHub branch protection, Argo CD Projects and declarative setup, Flux tenancy/Kustomization/HelmRelease/secrets, and Kubernetes RBAC documentation checked. Mermaid rendered and inspected. No cluster, denied request, or Opus review occurred. | Independent GitOps/Kubernetes security and Opus review; disposable allowed/denied tenant exercise including a HelmRelease; novice identity-boundary task; freshness decision. |

### Wave 85 (2026-10-03)

The APISIX introduction now follows a single invented lesson request
through route matching, an optional configured API-key plugin, an upstream,
and application logic. A second diagram separates live request traffic
from the Kubernetes controller's configuration updates and corrects the
assumption that every request must pass through kube-proxy.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [What Apache APISIX does for an API](knowledge/kubernetes/applications-and-tools/apache-apisix.md) | Lobby analogy with limits, invented lesson request, request and configuration diagrams with text alternatives, route/plugin/upstream/application ownership table, Kubernetes Service versus APISIX Service distinction, version-aware Gateway API link, understanding checks. | Current official APISIX route, plugin, controller, Kubernetes resource, and Gateway API documentation checked. Both Mermaid diagrams rendered and inspected. No gateway, route, backend, request, or Opus review occurred. | Independent APISIX and Opus review; disposable gateway and controller request exercise; novice route-versus-backend task; freshness decision. |

### Wave 86 (2026-10-03)

The APISIX architecture page now separates Kubernetes route declarations,
the controller-to-gateway configuration path, the live request path, and
the gateway's configuration-storage mode. It removes an untested EKS
Service manifest and port-forward recipe, keeping AWS implementation
details on the existing EKS guide. Gateway API status and listener-port
limits are explained as evidence rather than proof of user success.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [How the APISIX gateway and controller fit together](knowledge/kubernetes/applications-and-tools/apisix-architecture-and-deployment.md) | Two-path diagram and text alternative, invented lesson route, Gateway API object responsibilities and condition limits, documented traditional/decoupled/standalone mode comparison, failure-boundary table, understanding checks. | Current official APISIX deployment-mode, controller architecture, install, Gateway API, and resource documentation plus Gateway API implementer guidance checked. Mermaid rendered and inspected. No cluster, APISIX mode, listener, backend, request, or Opus review occurred. | Independent APISIX/Gateway API and Opus review; disposable route/status and mode-restart exercise; novice controller-versus-gateway task; freshness decision. |

### Wave 87 (2026-10-03)

The APISIX policy page now follows one invented lesson request through
optional authentication, a quota, a release split, and gateway signals.
It separates client authentication from lesson-level authorization,
explains where a rate counter lives, and replaces an untested rate-limit
snippet with the documented default behavior. Its diagram describes
possible outcomes rather than claiming a fixed plugin execution order.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [How APISIX policies shape one request](knowledge/kubernetes/applications-and-tools/apisix-security-traffic-and-observability.md) | Invented lesson request, branch diagram and text alternative, four policy questions, local-versus-shared quota scope, canary and telemetry limits, failure table, understanding checks. | Current official APISIX plugin, key-auth, openid-connect, limit-count, traffic-split, request-id, prometheus, and opentelemetry documentation checked. Mermaid rendered and inspected. No gateway, backend, quota, identity provider, canary, telemetry collector, reader task, or Opus review occurred. | Independent APISIX/security and Opus review; disposable request exercise across multiple gateway replicas and telemetry paths; novice policy-scope task; freshness decision. |

### Wave 88 (2026-10-03)

The Crossplane component page now follows one invented bucket request
instead of beginning with a catalogue of manifests and advanced objects.
It separates the platform API definition, individual request,
composition pipeline, managed resource, and external provider call.
It then places package revisions, activation, provider identity,
composition revision, and operations around that main path. The older
unexecuted manifests were removed; version-specific procedures remain
available through the focused guides and official documentation.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [How Crossplane's components turn a request into a resource](knowledge/kubernetes/crossplane/component-model.md) | Bounded request-desk analogy, invented TeamBucket request, diagram and text alternative, role table, four failure boundaries, advanced-component map, next-question routes, understanding checks. | Current official Crossplane overview, XRD, XR, Composition, Provider, Function, Managed Resource, activation-policy, and Configuration documentation checked. Mermaid rendered and inspected. No cluster, provider, bucket, account, request, reader task, or Opus review occurred. | Independent Crossplane and Opus review; disposable XR-to-MR-to-provider exercise; beginner component-boundary task; freshness decision. |

### Wave 89 (2026-10-03)

The managed-resource page now follows one invented bucket from a stored
request through provider observation and later reconciliation. It
separates desired fields, observed fields, and application use;
explains why immutable fields are not silently replaced; and treats
observe-only import, pause, and deletion as distinct lifecycle choices.
The older unexecuted manifests and mutations were removed in favor of
the official version-specific procedures.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [How a Crossplane managed resource changes over time](knowledge/kubernetes/crossplane/managed-resources-and-lifecycle.md) | Bounded thermostat analogy, invented reports-bucket sequence, reconciliation diagram and text alternative, desired-versus-observed field map, status limits, import and deletion choices, failure-boundary table, understanding checks. | Current official Crossplane managed-resource, import, and Usage guidance plus Kubernetes finalizer documentation checked. Mermaid rendered and inspected. No cluster, provider, bucket, import, deletion, reader task, or Opus review occurred. | Independent Crossplane/provider and Opus review; disposable drift/import/pause/delete exercise with provider-specific policies; novice desired-versus-observed task; freshness decision. |

### Wave 90 (2026-10-03)

The Crossplane provider page now follows one invented bucket API call
through package health, provider configuration, the controller Pod's
credential source, and external authorization. It separates the
provider's identity from the application's identity and makes EKS Pod
Identity and IRSA conditional on the actual provider runtime. It
removes the static credential recipe, a pinned package example, and
unsupported review and freshness claims.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [How a Crossplane provider reaches an external API](knowledge/kubernetes/crossplane/providers-and-authentication.md) | Bounded courier analogy, invented reports-bucket call, four-gate diagram and text alternative, package-versus-authorization table, conditional EKS identity comparison, first-missing-boundary table, understanding checks. | Current official Crossplane Provider, managed-resource, and activation guidance plus Amazon EKS Pod Identity and IRSA documentation checked. Mermaid rendered and inspected. No provider, EKS cluster, Pod identity, credential, bucket, AWS call, reader task, or Opus review occurred. | Independent Crossplane/AWS security and Opus review; disposable provider identity and allow/deny exercise; novice package-versus-credential task; freshness decision. |

### Wave 91 (2026-10-03)

The direct-MR versus platform-API page now answers one design
question instead of repeating the component glossary. An invented
image repository follows both routes to the same provider controller.
It separates what the resource author chooses from what a platform
team can standardize, then explains the cost of versioning and
reviewing the abstraction. Unexecuted provider installation and MR
manifests were removed; focused pages retain the operational paths.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [When to use a managed resource or a Crossplane platform API](knowledge/kubernetes/crossplane/providers-compositions-and-managed-resources.md) | Bounded ingredients-versus-meal analogy, invented image-repository request, converging-route diagram and text alternative, choice table, change scenario, bypass boundary, next-page routes, understanding checks. | Current official Crossplane overview, managed-resource, XRD, Composition, and Configuration documentation checked. Mermaid rendered and inspected. No provider, repository, Composition, request, reader task, or Opus review occurred. | Independent Crossplane/platform security and Opus review; disposable direct-MR-versus-XR exercise with provider access controls; novice choice task; freshness decision. |

### Wave 92 (2026-10-03)

The Composition page now follows an invented WebApplication request
from XRD schema to selected function pipeline, composed Deployment
and Service, and a separate user-path check. It distinguishes a
schema-valid XR, locally rendered desired objects, live controller
conditions, and application behavior. The long unrun manifest was
removed, while official procedure and revision references remain.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [How a Crossplane Composition fulfills one application request](knowledge/kubernetes/crossplane/compositions.md) | Bounded form-and-recipe analogy, invented WebApplication input/output table, XR-to-resource diagram and text alternative, pipeline questions, revision scenario, layered validation table, understanding checks. | Current official Crossplane XRD, Composition, CompositionRevision, and CLI documentation plus Kubernetes Deployment and Service documentation checked. Mermaid rendered and inspected. No Crossplane CLI render, cluster, Deployment, Service, user request, reader task, or Opus review occurred. | Independent Crossplane/Kubernetes and Opus review; disposable local render and cluster exercise; novice schema-versus-implementation task; freshness decision. |

### Wave 93 (2026-10-03)

The XRD/XR page now answers the caller's question first: create an XR.
One invented network request shows the API definition, implementation,
request, composed resources, provider, and external API. The old long,
unrun configuration examples were replaced by a small illustrative XR
and selection fragment. The page separates admission, reconciliation,
readiness, and an application-level outcome.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [How to request a Crossplane platform API](knowledge/kubernetes/crossplane/xrd-composition-and-xr-calls.md) | Bounded order-form analogy, invented PlatformNetwork request, diagram and text alternative, selection explanation, Terraform comparison with limits, layered evidence table, understanding checks. | Current official Crossplane XRD, XR, and Composition documentation plus HashiCorp module overview checked. Mermaid rendered and inspected. No XRD, Composition, function, provider, network, cloud account, application check, reader task, or Opus review occurred. | Independent Crossplane and Opus review; disposable XR-to-provider exercise; novice request-object task; freshness decision. |

### Wave 94 (2026-10-03)

The Terraform/Crossplane comparison now follows one invented
payments-network need through two operating paths. It keeps the
decision near the top, shows what each workflow previews or
observes, and gives a clear example of using both with
separate resource ownership. Repeated feature lists and
unrun network manifests were removed.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [When to use Terraform or Crossplane](knowledge/kubernetes/crossplane/terraform-vs-crossplane.md) | Bounded inspection-versus-caretaker analogy, two-path diagram and text alternative, invented network decision table, ownership boundary, post-change observations, understanding checks. | Current official HashiCorp plan, state, and modules guidance plus Crossplane XRD, XR, Composition, and managed-resource documentation checked. Mermaid rendered and inspected. No Terraform run, cluster, cloud network, application check, reader task, or Opus review occurred. | Independent Terraform/Crossplane and Opus review; disposable comparison of plan/apply and XR reconciliation; novice operating-model choice task; freshness decision. |

### Wave 95 (2026-10-03)

The Crossplane operating-model page now follows one invented
SecureBucket request and distinguishes application, platform,
GitOps, controller, and provider responsibilities. It separates
request changes from implementation changes, and connects
pre-rollout review with live and application-level checks.
It presents this as a possible team pattern rather than
a universal professional rule.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [How a team operates a Crossplane platform API](knowledge/kubernetes/crossplane/professional-operating-model.md) | Bounded service-counter analogy, role map, request path diagram and text alternative, change-type comparison, access boundary, delivery layers, understanding checks. | Current official Crossplane XRD, XR, Composition, CompositionRevision, Provider, CLI, and Argo CD guidance plus Kubernetes RBAC documentation checked. Opus 5.5 read-only review on 2026-10-04 identified status-flow and scope issues; corrections were checked against official docs and diagrams rerendered. No cluster, bucket, provider identity, GitOps sync, cloud API call, application check, or reader task occurred. | Independent platform-security review; disposable request and implementation-change exercise; novice ownership task; freshness decision. |

### Wave 96 (2026-10-03)

The GitOps/operations page now follows an invented SecureBucket
retention change through the GitOps and Crossplane loops. It
distinguishes sync, XR and managed-resource readiness, and an
application outcome. It also maps implementation promotion,
operating signals, and external identity needed for recovery.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [How GitOps and Crossplane keep a platform request running](knowledge/kubernetes/crossplane/production-gitops-and-operations.md) | Bounded two-delivery-round analogy, change-path diagram and text alternative, layered signal table, failure handoff, promotion and recovery explanations, understanding checks. | Current official Crossplane Argo CD, XR, Composition, CompositionRevision, managed-resource, provider, metrics, and upgrade documentation checked. Opus 5.5 read-only review on 2026-10-04 identified status and diagram errors; corrections were checked against official docs and diagrams rerendered. No GitOps sync, cluster, provider upgrade, bucket, backup restore, application operation, or reader task occurred. | Independent GitOps/Crossplane review; disposable sync-to-cloud and recovery exercises; novice two-loop diagnosis task; freshness decision. |

### Wave 97 (2026-10-04)

The Crossplane troubleshooting guide now starts with an invented
paused Bucket deletion and follows the first missing handoff.
It distinguishes API rejection, XR and managed-resource
conditions, pause and deletion state, provider identity,
ambiguous creation, and application outcomes. Unrun
mutating pause and finalizer recipes were removed.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Find the first failing Crossplane handoff](knowledge/kubernetes/crossplane/troubleshooting.md) | Bounded parcel-tracking analogy, invented paused Bucket example, decision diagram and text alternative, condition table, controller-log routing, deletion and ambiguous-create boundaries, understanding checks. | Opus 5.5 read-only review of the prior page and neighboring guides. Current official Crossplane troubleshooting, XRD, XR, managed-resource, activation, provider, Usage, and CLI documentation checked. Mermaid rendered and inspected. No cluster, bucket, provider, deletion, application check, or reader task occurred. | Independent Crossplane/provider security review; disposable paused-deletion, missing-kind, and provider-denial exercises; novice first-failure task; freshness decision. |

### Wave 98 (2026-10-04)

The application-delivery example now follows an invented request from
an empty ECR repository through CI image publication, a digest-based
release, Kubernetes rollout, and a user-path check. The previous
unrun XRD and Composition examples implied that an image already
existed in the repository they created. The new page separates the
three identities, readiness signals, and deletion decisions.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [How one platform request reaches a running application](knowledge/kubernetes/crossplane/application-delivery-platform-api.md) | Bounded shelf analogy, staged request table, handoff diagram and text alternative, identity and readiness maps, lifecycle decisions, understanding checks. | Opus 5.5 read-only review of the prior page identified image-order, readiness, identity, and deletion issues. Current official Crossplane Composition, function, XR, managed-resource, AWS ECR, EKS, and Kubernetes documentation checked. Mermaid rendered and inspected. No provider, ECR repository, image push, cluster, rollout, user request, or reader task occurred. | Independent Crossplane, Kubernetes, AWS, and platform-security review; disposable repository-to-image-to-rollout and deletion exercises; novice handoff task; freshness decision. |

### Wave 99 (2026-10-04)

The Crossplane deployment-patterns reference now uses one invented VPC
and two subnets to answer how to repeat resources and connect dependencies.
It separates a multi-document YAML file, fixed Composition, and function
loop, and explains provider references, temporary unresolved states,
stable identity, and the risk of removing desired resources. Long unrun
manifests and duplicate Terraform comparisons were removed.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Choose how Crossplane repeats and connects resources](knowledge/kubernetes/crossplane/deployment-patterns-and-references.md) | Bounded form-folder analogy, one network request, repetition choice table, dependency diagram and text alternative, reference method and observation tables, understanding checks. | Opus 5.5 read-only review of the prior page found invalid standalone controller selector, ambiguous loops, and unrun examples; corrections checked against current official Crossplane managed-resource, Composition, XRD, function, and CLI documentation. Mermaid rendered and inspected. No Composition render, provider, AWS network, cluster, or reader task occurred. | Independent Crossplane/AWS review; disposable fixed-versus-loop and reference-resolution exercises; novice choice task; freshness decision. |

### Wave 100 (2026-10-04)

The AWS VPC platform API page now explains a proposed network request as
an asynchronous path through VPC, subnets, routing, and optional endpoints.
It removes a large untested Composition and a false consumer-facing
`deletionPolicy: Orphan` guarantee for v2 namespaced managed resources.
The page separates API acceptance, provider reconciliation, and actual
connectivity, and names the decisions that require a disposable AWS test.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [How one Crossplane request becomes an AWS network](knowledge/kubernetes/crossplane/aws-vpc-platform-api.md) | Bounded order/work-order analogy, illustrative PlatformNetwork request, resource-purpose table, dependency diagram and text alternative, delivery signals, deletion decision, understanding checks. | Opus 5.5 read-only review of a neighboring page flagged the old deletion-policy field and likely provider-schema issues. Current official Crossplane XRD, XR, Composition, managed-resource and AWS subnet routing, network ACL, S3 and DynamoDB gateway-endpoint documentation checked. Mermaid rendered and inspected. No XRD, provider, cluster, AWS network, connectivity check, deletion, or reader task occurred. | Independent AWS networking and Crossplane/provider review; disposable network and retention exercise; novice request-to-connectivity task; freshness decision. |

### Wave 101 (2026-10-04)

The AWS resource workflow now follows one invented S3 request through
Kubernetes acceptance, Composition, managed-resource reconciliation,
AWS observation, application use, change, and deletion. The prior page
repeated an unrun lab and included cloud-creating, drift-writing,
pausing, and cleanup commands. The revised explanation routes execution
to the dedicated lab and clarifies that a `SecureBucket` name alone
cannot enforce access controls.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [How an AWS resource request moves through Crossplane](knowledge/kubernetes/crossplane/aws-resource-workflow.md) | Bounded work-order analogy, invented SecureBucket request, direct-versus-XR convergence diagram and text alternative, setup and evidence tables, lifecycle boundaries, understanding checks. | Opus 5.5 read-only review of the prior workflow found inactive-policy, unsafe adoption, incomplete Composition, and lab-duplication problems. Current official Crossplane installation, provider, managed-resource, XRD, XR, Composition, activation, and AWS S3 naming documentation checked. Mermaid rendered and inspected. No cluster, provider, AWS bucket, application check, deletion, or reader task occurred. | Independent Crossplane/AWS review; disposable direct-versus-XR and lifecycle exercise; novice handoff task; freshness decision. |

### Wave 102 (2026-10-04)

The Crossplane reference page now routes a reader's concrete question
to an official Crossplane, provider, or AWS source. It distinguishes
current documentation from the installed CRD and package version,
explains the provider identity boundary, and separates local rendering
from live AWS evidence. A long undifferentiated list of secondary
and tangential links was removed.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Find the right Crossplane source for your question](knowledge/kubernetes/crossplane/references.md) | Question-to-source tables for first-failure, design, provider, identity, and AWS boundaries; concise example of an accepted XR with no bucket; local teaching routes. | Current official Crossplane installation, v2, XRD, XR, Composition, managed-resource, activation, CLI, and troubleshooting documentation plus Upbound provider and AWS EKS sources checked. Local and external links validated by repository checks. No installed provider schema, cluster, AWS call, or novice source-finding task occurred. | Independent Crossplane reference audit; novice find-the-source task; freshness decision. |

### Wave 103 (2026-10-04)

The local AWS S3 lab now teaches one bounded bucket lifecycle: check the
provider credential identity, install the control plane and a pinned
provider, use a random candidate name, observe both Kubernetes and AWS,
and confirm a valid-identity 404 before removing the cluster. It no
longer treats AWS's default public-access blocks as proof of a
Crossplane-managed block or asks readers to mutate live tags for drift.
The lab remains draft because no Docker daemon, kind, kubectl, Helm,
AWS CLI, or authorized AWS sandbox run was available in this review.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Create and remove one S3 bucket with Crossplane](knowledge/kubernetes/crossplane/local-aws-s3-lab.md) | One-bucket work-order model and diagram with text alternative, prerequisites, identity precheck, explicit success and cleanup gates, source-linked commands, understanding checks. | Opus 5.5 read-only review found identity mismatch, default public-access false proof, name/adoption, wait, and cleanup risks. Current Crossplane install, provider, managed-resource, activation, Upbound v2.6.1 schema, AWS STS, S3 naming, HeadBucket, deletion, and public-access docs checked. Chart 2.4.2 confirmed in the stable index; twelve shell blocks parsed with `bash -n`. Diagram rendered and inspected. No live cluster, provider, AWS bucket, deletion, or reader task occurred. | Authorized sandbox execution with evidence record; independent Crossplane/AWS review; novice lab task; freshness decision. |

### Wave 104 (2026-10-04)

The companion validation guide now records actual pass criteria for the
same-file AWS identity, installed versions, CRD, Bucket conditions,
external result, and deletion. It removes old public-access and drift
checkpoints that no longer belong to the lab and requires `partial`
or `inconclusive` where evidence is missing.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Record evidence from a Crossplane S3 sandbox lab](knowledge/kubernetes/crossplane/aws-s3-lab-validation-template.md) | One bounded evidence-recording task, pass criteria per handoff, failure fields, explicit outcome choices, and source-linked status limits. | Opus 5.5 read-only review of the old template identified blank pass labels, credential-identity confusion, and default-public-access false proof. Current Crossplane managed-resource and AWS HeadBucket docs checked. No authorized run or real record exists. | Complete with a real authorized sandbox run; independent evidence review; first maintainer usability task. |

### Wave 105 (2026-10-04)

The tooling-cluster decision page now starts from one shared GitOps
service and compares local, central, hybrid, and externally managed
placements. It separates local admission and secret reconciliation
from services that can be shared, and asks what a third cluster changes
for ownership, access, and recovery.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [When a tooling cluster helps](knowledge/kubernetes/applications-and-tools/tooling-clusters.md) | Shared-workshop analogy, invented two-cluster choice, placement table, per-function boundaries, three decision questions, understanding checks. | Opus 5.5 read-only review of the prior two pages identified push-only assumptions, duplicated outcomes, unsafe default CI co-location, and false outage certainty. Current Argo CD, Flux, Kubernetes RBAC/policy, and External Secrets Operator docs checked. No cluster layout, access, outage, or reader task was tested. | Independent platform-security review; novice placement choice; access and outage exercise; freshness decision. |

### Wave 106 (2026-10-04)

The tooling-cluster architecture page now traces central-push
management separately from user and optional telemetry paths. It
names local-pull reconciliation as an alternative and makes target
identity, network, RBAC, outage, and independent recovery evidence
explicit. Cloud-specific access remains in the EKS guide.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [How a tooling cluster connects to workload clusters](knowledge/kubernetes/applications-and-tools/tooling-cluster-architecture.md) | Dispatch-desk analogy, invented two-target diagram and text alternative, five-boundary table, central-push versus local-pull choice, conditional failure matrix, recovery questions. | Opus 5.5 read-only review of the prior pages guided the split; current Argo CD, Flux, and Kubernetes RBAC documentation checked. Diagram rendered and inspected. No GitOps controller, target API, telemetry, outage, recovery, or reader task was tested. | Independent GitOps/platform-security review; access and outage exercise; novice path tracing; freshness decision. |

### Wave 107 (2026-10-04)

The glossary now opens core words that its more advanced entries use:
cluster, container, controller, desired state, node, namespace, Pod,
repository, and more. It links existing deeper routes, separates
Crossplane terms from ordinary meanings, and corrects a few definitions
whose wording was specific to this repository's policy rather than the
general term. Its one-sentence definition format follows the Glossary
contract; the linked pages carry examples and diagrams.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Glossary](knowledge/glossary.md) | Added prerequisite terms and direct links, scoped overloaded words, corrected prompt, Crossplane config, CI/CD, and retrieval definitions, and made the starting links land on explanations. | Opus 5.5 reviewed the previous glossary read-only. Crossplane v2 ProviderConfig and EnvironmentConfig details checked against official docs; linked local concepts and OKF Glossary contract checked. No novice term-finding test or independent technical review occurred. | Novice find-a-term task; independent glossary and Crossplane version review; freshness decision. |

### Wave 108 (2026-10-04)

The Velero volume page now explains where each copy actually lives.
It follows one invented notes app through object archive, native or
CSI snapshot, CSI snapshot data movement, and File System Backup, and
asks readers to choose from the intended restore destination. Untested
creation commands and manifests moved out of this Explanation; the
page names exact evidence needed before trusting an off-backend copy.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Where a Velero backup keeps objects and volume data](knowledge/migrations/velero/storage-and-volume-backups.md) | Workshop analogy, invented notes app, volume-path diagram and text alternative, four-method comparison, destination-first choice, FSB and data-mover prerequisites, understanding checks. | Opus 5.5 read-only review of the previous page found misleading data-mover, FSB, and snapshot assumptions. Current Velero v1.18 how-it-works, CSI, data movement, FSB, and volume-policy docs plus Kubernetes snapshot docs checked. Diagram rendered and inspected. No cluster, volume, backup, snapshot, upload, restore, or reader test occurred. | Independent storage/Velero review; test each chosen method with a disposable workload and destination; novice method-choice task; freshness decision. |

### Wave 109 (2026-10-04)

The Velero workflow page now has one safe learning outcome: copy a
disposable ConfigMap through object backup into a second empty
namespace and read the result. It removes production-named, unrun
backup and restore examples, broad cluster filters, hooks, schedules,
resource modifiers, and PVC implications from a beginner How-to.
Those are separate, more advanced tasks with their own official docs.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Back up and restore one ConfigMap with Velero](knowledge/migrations/velero/backup-restore-workflows.md) | One-note archive analogy, object path diagram and text alternative, guarded preflight, narrow object backup, mapped restore, value check, and conditional cleanup. | Opus 5.5 read-only review of the prior command catalog identified live-production and PVC-data risks; Velero v1.18 backup, restore, and how-it-works docs checked. Shell blocks parsed with `bash -n`; diagram rendered and inspected. No live Velero server, backup location, Kubernetes cluster, backup, restore, or reader task was available. | Run in disposable cluster with real backup storage and record output; independent Velero review; novice task; freshness decision. |

### Wave 110 (2026-10-05)

The Velero cross-cluster explanation now separates the Kubernetes
object archive, volume-data path, destination prerequisites, and
application cutover. An invented notes app shows what Velero can
carry and what must be rebuilt or checked. It removes unrun
source/destination commands, production namespace restores, and the
unsafe suggestion to make a shared source backup prefix writable from
the destination.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [How a Velero backup reaches another cluster](knowledge/migrations/velero/cluster-migration-and-disaster-recovery.md) | Library-move analogy, invented notes-app diagram and text alternative, item-location and target-prerequisite tables, planned-versus-disaster comparison, evidence sequence and cutover questions. | Opus 5.5 read-only review of the prior page identified two-writer, shared-prefix, CRD, volume-portability, and rollback risks. Current Velero v1.18 migration, disaster, how-it-works, restore, and location docs checked. Diagram rendered and inspected. No source/destination cluster, volume backup, restore, outage, cutover, or reader task was tested. | Independent Velero/security review; authorized two-cluster drill with data checksum and side-effect isolation; novice handoff task; freshness decision. |

### Wave 111 (2026-10-05)

The EKS Velero page now teaches the S3 archive and two different EBS
snapshot control paths before an operator chooses an install method.
It separates Velero's AWS identity from the EBS CSI driver's identity,
names the extra work needed to copy volume bytes into S3, and lists
evidence for both object and volume recovery. Unrun bucket, IAM,
add-on, and Helm creation examples were removed from this Explanation.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [How Velero on EKS uses S3 and EBS](knowledge/migrations/velero/aws-s3-ebs-installation.md) | Two-worker analogy, invented photo-app diagram and text alternative, component/identity tables, native-versus-CSI comparison, and evidence ladder. | Opus 5.5 read-only review of the prior page identified misleading IAM, CSI/native, version, and untested command paths. Current Velero v1.18 install, CSI, data mover, FSB, and locations docs; canonical AWS plugin compatibility table; EKS EBS driver, snapshot-controller, and Pod Identity docs checked. Diagram rendered and inspected. No EKS cluster, S3 bucket, IAM binding, Velero installation, EBS snapshot, restore, or reader task occurred. | Independent AWS/Velero review; authorized disposable EKS install with both object and selected EBS restore evidence; novice identity-path task; freshness decision. |

### Wave 112 (2026-10-05)

The Velero troubleshooting page now follows one concrete symptom: a restore
finishes, but the application cannot read its old data. It separates absent
objects, missing volume bytes, a Pending or Bound PVC, and an application
failure, with read-only checks before any repair is considered.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Find why a Velero restore has no application data](knowledge/migrations/velero/troubleshooting-and-operations.md) | Parcel analogy with its limit, backup-to-application diagram and text alternative, method-specific evidence table, read-only command sequence, and questions that distinguish object and data recovery. | Opus 5.5 read-only reviews of the prior and revised page identified PVC-state conflation, unsafe blind repairs, Pending and Bound nuances, and mover/FSB evidence gaps; the revised page addresses them. Current Velero v1.18 troubleshooting, restore, FSB, CSI, and data-movement docs checked. Diagram rendered and inspected. No Velero cluster, incident, restore, or reader task was tested. | Independent Velero/storage review; disposable restore cases for missing object, missing data, Pending and Bound PVC; novice diagnosis task; freshness decision. |

### Wave 113 (2026-10-05)

The Velero use-case page now helps a beginner choose a recovery pattern
instead of inviting them to run untested production cutover commands.
It identifies what Velero carries, what GitOps and other service owners
must provide, and the evidence needed before traffic moves.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Choose where Velero fits in a recovery plan](knowledge/migrations/velero/real-use-cases-and-runbooks.md) | Moving-plan analogy and its limit, invented notes-app scenario, layer diagram and text alternative, six use-case choices, RPO/RTO terms, and plan-readiness questions. | Opus 5.5 read-only reviews of the prior and revised page found unsafe unscoped restores, stopped-Pod FSB, source-bucket, GitOps ownership, data-before-workload ordering, and cross-cloud storage mapping assumptions; the revised page addresses them. Current Velero v1.18 migration, FSB, restore, data-movement, and how-it-works docs and Argo CD automated-sync docs checked. Diagram rendered and inspected. No cluster, cutover, restore, or reader task was tested. | Independent Velero/GitOps review; controlled scenario and novice route-choice task; freshness decision. |

### Wave 114 (2026-10-05)

The Velero automation page now teaches the request path and its trust
boundaries instead of offering an untested production workflow and IAM
policy. It separates the runner's AWS and Kubernetes access from the
Velero server's storage permissions, and makes plan approval and
application recovery evidence explicit.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [How automation asks Velero to back up or restore](knowledge/migrations/velero/possible-integrations.md) | Library-request analogy with its limit, GitHub-to-Velero diagram and text alternative, identity and request tables, invented rehearsal path, and boundary-first failure routing. | Opus 5.5 read-only reviews of the prior and revised page identified shell and output injection, untrusted role/cluster selection, excessive RBAC, broad restore scope, mismatched approval and execution, missing OIDC environment binding, and false green-job confidence; the revised page addresses them. Current Velero v1.18 how-it-works, restore, migration, and troubleshooting docs, GitHub OIDC and environment docs, and EKS access-entry and authentication-mode docs checked. Diagram rendered and inspected. No workflow, IAM role, EKS cluster, backup, restore, or reader task was tested. | Independent GitHub/AWS/Velero security review; authorized disposable workflow with fixed cluster identity and scoped permissions; novice request-path task; freshness decision. |

### Wave 115 (2026-10-05)

The five decision records now distinguish their historical choices from
the current OKF and website rules. Each gives a beginner the reason for
the choice, what still applies, and a condition for reconsideration.
The earlier website deferral remains visible as history without being
presented as current policy.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [ADR-0001: Knowledge base structure](knowledge/decision-records/ADR-0001-knowledge-base-structure.md) | Explains why focused pages and topic indexes help, then dates the `README.md` to `index.md` OKF change and names a reader-task reconsideration trigger. | Current authoring rules, root index, and 2026-09-20 bundle log checked; Opus 5.5 reviewed the prior records. No reader task was run. | Independent governance review and reader navigation task. |
| [ADR-0002: Source ingestion and topic taxonomy](knowledge/decision-records/ADR-0002-source-ingestion-and-topic-taxonomy.md) | Separates raw notes from curated knowledge, clarifies today's route names and ingestion register, and names when taxonomy needs review. | Source ingestion instructions, register route, and current knowledge index checked; Opus 5.5 reviewed the prior records. No ingestion was run. | Independent source-ingestion review and contributor route-choice task. |
| [ADR-0003: Earlier searchable-site deferral](knowledge/decision-records/adr-0003-searchable-site-decision.md) | Explains why the site was once deferred and makes clear that ADR-0005 superseded the timing decision before reader-session evidence existed. | ADR-0005 and the repository improvement-plan history checked; Opus 5.5 reviewed the prior records. No reader session was claimed. | Independent historical review; no new action under this superseded choice. |
| [ADR-0004: Canonical Markdown and discovery](knowledge/decision-records/adr-0004-machine-readable-discovery.md) | Keeps catalog and validation rules active, marks the site-deferral clause historical, and shows how metadata, indexes, catalog, and search relate. | Current OKF instructions, website plan, catalog generator, and listed official documentation checked; Opus 5.5 reviewed the prior records. No retrieval-service measurement was run. | Independent catalog/website contract review and retrieval task; freshness decision by recorded deadline. |
| [ADR-0005: Git-backed reading site](knowledge/decision-records/adr-0005-git-backed-reading-site.md) | Uses one concept-update example to explain pinned source revisions, derived catalog/search, and post-launch reconsideration through reader tasks. | Website source-side plan and current repository contract checked; Opus 5.5 reviewed the prior records. No public reader task or host validation was claimed. | Independent website-contract review and observed post-launch reader tasks. |

Opus 5.5 also reviewed the revised records. Its findings led to explicit
decision-state labels, a correction to the ingestion-register wording,
historical wording for the superseded site clause, and alignment of the
maintenance queue with ADR-0005's post-launch reader-testing decision.

### Wave 116 (2026-10-05)

The contributor templates now separate instructions from the text to
copy. Each copyable skeleton starts with the intended concept type and
unclaimed draft metadata. The template index gives a short path for
placing a new topic, updating its parent index, and validating the
bundle. The authoring instructions name accepted maturity values. The
OKF validator now rejects template markers in concept frontmatter;
contributors still search the body for unfilled examples before publication.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Knowledge article template](knowledge/templates/knowledge-article-template.md) | Removed the fake default source, aligned Explanation example and visual order, clarified type choice and source-ID use. | Opus 5.5 read-only review of prior templates identified placeholder-source risk; current authoring rules and validator values checked. No contributor copy trial occurred. | New-contributor trial for both skeletons and review of source-footnote placement. |
| [Tutorial template](knowledge/templates/practical-example-template.md) | Added a copyable Tutorial with plain opening, bounded disposable exercise, observable result, recovery, cleanup, understanding checks, and next link. | Opus 5.5 read-only review of prior template identified missing teaching and unrun-evidence labels. No tutorial commands were executed. | Novice contributor and learner trial. |
| [Troubleshooting guide template](knowledge/templates/troubleshooting-template.md) | Added a copyable symptom-first guide with read-only diagnostics, cause-confirmation results, stop signals, guarded recovery, and real-outcome verification. | Opus 5.5 read-only review of prior template identified missing result interpretation and escalation structure. No incident or recovery command was tested. | Contributor trial with a real documented symptom. |
| [Command reference template](knowledge/templates/command-reference-template.md) | Added a copyable Reference with version scope, state-change column, command inputs, expected signal, failure route, and official source placeholder. | Opus 5.5 read-only review of prior template identified how-to/reference confusion and missing side-effect mapping. No command was run. | Contributor trial with a versioned command family. |
| [Architecture decision record template](knowledge/templates/architecture-decision-record-template.md) | Added a copyable Decision Record with distinct decision state, plain-language summary, alternatives, consequences, and explicit reconsideration trigger. | Opus 5.5 read-only review of prior template identified fake ADR catalog title, missing trigger, and pressure to invent an owner. No decision was made through the new template. | Contributor trial on a real proposed decision. |

Opus 5.5 reviewed the revised templates twice. Its follow-up findings
led to complete frontmatter in each copyable block, quoted YAML titles,
explicit risk and recovery slots, and the frontmatter placeholder gate.
All six skeleton blocks were extracted and parsed as the intended OKF
types; no contributor trial or real task execution was inferred.

### Wave 117 (2026-10-05)

The last two AI guides now start with beginner models before product or
format details. The embedded OKF example is explicitly a draft teaching
subtree: invented generator, reviewer, usage, and freshness fields were
removed from its live frontmatter, and source references say what they
can and cannot establish. The synthetic Prometheus checker now validates
query-record shape while refusing to attest an untrusted execution.

| Concept | Teaching or accuracy pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Create AI tools for Claude and Codex](knowledge/ai/ai-tooling/create-ai-tools-for-claude-and-codex.md) | Explains the model-host-tool loop with one knowledge lookup, a diagram and text alternative, a surface chooser, access boundaries, and a paper exercise; removes broken runnable snippets. | Opus 5.5 reviewed the prior and revised guide; current Claude and OpenAI tool, skill, and project-guidance pages checked. No API or MCP tool was run. | Independent product/security review and novice tool-choice task. |
| [OKF v0.2](knowledge/ai/ai-tooling/knowledge-bases/okf-v0.2.md) | Adds a library model, bundle diagram, local-profile distinction, full concept-ID example, and correct nested receipt field; pins the specification. | Opus 5.5 reviewed the prior and revised guide; pinned OKF v0.2 specification checked. No separate bundle validation or reader task occurred. | Independent OKF review and novice format-reading task. |
| [Why this example has a separate guide](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/readme-concept.md) | Explains the example's scope and its real concept ID without implying a second version root or a reserved README. | Repository paths and OKF reserved-file rule checked. No reader task occurred. | Novice orientation task. |
| [Pod restarts in a time window](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/concepts/pod-restart-rate.md) | Repairs title and description; explains PromQL `increase`, validated prefix and window inputs, a query-to-receipt diagram, and why a synthetic receipt is not a measurement. | Opus 5.5 reviewed the prior and revised sample; kube-state-metrics Pod metrics and Prometheus `increase` docs checked. No Prometheus query ran. | Independent PromQL review and authorized synthetic-to-real attestation design. |
| [Retrieval budget example](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/concepts/retrieval-budget.md) | Defines a search-and-fetch budget with a library analogy, bounded Pod question, golden-question explanation, and MCP scope. | Opus 5.5 reviewed the prior and revised sample; MCP tools specification checked. No retrieval test or reader task occurred. | Measure a golden question with the actual search system. |
| [Source schema extraction example](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/concepts/source-schema-extraction.md) | Separates exact parser-owned facts from learner explanation and labels the invented API and renderer as examples. | OpenAPI v3.2.0 and JSON Schema 2020-12 official sources checked. No renderer or parser ran. | Run against a real versioned API description. |
| [Prometheus receipt-shape reference](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/references/attesters/prometheus-receipt-shape.md) | States that the checker refuses real attestation and names the missing executor and result trust chain. | Opus 5.5 reviewed the prior and revised checker; one plausible and one invalid synthetic receipt were inspected locally. No trusted execution occurred. | Independent attestation/security review and real executor design. |
| [Prometheus executor reference](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/references/executors/run-prometheus-query.md) | Replaces a receipt that contradicted its checker with a clearly invented, internally consistent one. | JSON example parsed and shape-checked locally; `attest()` returned false. No Prometheus connection or digest measurement occurred. | Trusted executor, verifiable result, and end-to-end run. |
| [JSON Schema source reference](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/references/sources/json-schema-2020-12.md) | Explains what the standard defines and why a particular API schema is still needed. | Official Draft 2020-12 page opened. No API schema was parsed. | Validate an actual API schema. |
| [kube-state-metrics source reference](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/references/sources/kube-state-metrics.md) | Points to the pinned Pod metric list and separates metric definition from cluster observation. | Official Pod metrics page and pinned revision checked. No cluster metric was queried. | Confirm availability in a real cluster. |
| [MCP source reference](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/references/sources/mcp-2026-07-28.md) | Points to the actual versioned tools page and separates protocol capabilities from retrieval policy. | Official 2026-07-28 tools page opened. No MCP server ran. | Test against a real client and server. |
| [OpenAPI source reference](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/references/sources/openapi-3-2.md) | Separates the format standard from an individual API's description. | Official OpenAPI v3.2.0 specification opened. No API description was parsed. | Validate an actual API document. |

Opus 5.5 gave read-only reviews before and after the edits. Its revised
review found the prefix mismatch, misleading log wording, index labels,
search-result access and revision gaps, and the MCP source-page mismatch;
these were corrected against the official sources. The sample checker
is a teaching guard, not a successful runtime attestation.

### Wave 118 (2026-10-06)

The Terraform language section now starts with a beginner explanation of
how one value moves from a caller or default through an input variable,
local value, resource, and root output. It uses the same no-cloud file as
the local state tutorial, so the explanation leads directly to an exercise.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [How values move through Terraform configuration](knowledge/terraform/language/how-values-move-through-terraform.md) | Plain-language definition, bounded `main.tf` walkthrough, limited order-card analogy, reference-flow diagram and text alternative, plan-time unknowns, output-name disambiguation, understanding questions, and official next steps. | Claude Opus 5.5 gave read-only design and revised-page reviews; the second pass corrected state-versus-override wording, evidence scope, module-output language, and the diagram's missing input. Current HashiCorp language, variable, local, resource, reference, output, type, and sensitive-data documentation was checked. The supporting `main.tf` was executed in the separate local-state tutorial run, and the diagram rendered and was inspected; no reader used this new explanation. | Independent domain review of the new page, novice value-tracing task, and review of the remaining language topics. |

### Wave 119 (2026-10-06)

The beginner Kubernetes route now separates Service label selection from
endpoint readiness and the request path. It uses the local `kb-web` files so
readers can connect the explanation to the exercise. The route also corrects
tool step numbers, shows the actual Service selector in command output, and
limits the conclusion from port-forward to one selected Pod.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [How a Kubernetes Service selects Pods](knowledge/kubernetes/core-objects/how-a-service-selects-pods.md) | Defines the selector, EndpointSlice, readiness, DNS, ClusterIP, and port roles; traces the existing two-replica example; uses a limited dispatch analogy, a selection-versus-traffic diagram and text alternative, understanding questions, and official next steps. | Claude Opus 5.5 gave read-only design and revised-page reviews. Current Kubernetes Service, EndpointSlice, readiness, DNS, proxy, Deployment, and port-forward documentation was checked. The diagram rendered and was inspected; no current cluster run or novice reader task occurred. | Independent domain review, a cluster-backed Service request and failed-rollout check, and novice label-to-endpoint task. |

### Wave 120 (2026-10-07)

The cloud section lacked an explanation before the provider and solution
guides. The new entry page gives a beginner a provider-neutral model and a
first route into the existing material.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [Cloud computing fundamentals](knowledge/cloud/cloud-computing-fundamentals.md) | Defines public cloud resources and the provider/customer split; limits the workshop analogy; walks through an invented photo site; adds a responsibility table, diagram and text alternative, misconception limits, understanding questions, and official next steps. | Claude Opus 5.5 gave read-only outline and draft reviews. The second review identified an overbroad cloud definition, absolute scaling wording, incomplete service-model table, weak analogy limits, and source mismatch in the example; these were corrected. NIST, Microsoft, and AWS primary documentation was checked. The revised diagram was rendered and inspected; no cloud account, live workload, bill, failure test, or novice reader task was used. | Independent domain review, novice responsibility-and-cost task, and a real workload review before operational advice. |

### Wave 121 (2026-10-07)

The AI section began with tooling, so newcomers encountered retrieval and
agents before the basic terms. The new entry page explains the vocabulary
through one invented library and sends readers to the deeper tooling routes.

| Concept | Teaching pass | Evidence actually recorded | Still needed |
| --- | --- | --- | --- |
| [AI fundamentals](knowledge/ai/ai-fundamentals.md) | Distinguishes AI systems, ML, generative AI, LLMs, assistants, and agents; separates training from using a model; uses a limited sign-painter analogy, an invented library, a diagram and text alternative, understanding questions, and official next steps. | Claude Opus 5.5 gave read-only design and draft reviews. The second review found privacy ambiguity, an unanswered agent question, model/application source mismatch, and diagram handoff errors; these were corrected. OECD, Google, Anthropic, and NIST primary sources were checked. The revised diagram rendered and was inspected; no model, tool, library service, or novice reader task ran. | Independent AI education and technical review, novice classification-and-trust task, and revision from observed confusion. |

### Not yet reviewed against the teaching standard

The generated catalog records 169 concepts, all marked `draft`. Every
catalog concept now has an initial teaching or format-integrity pass in
waves 1 to 121. This accounting does **not** mean that every explanation
has passed independent technical review, novice reader tasks, or live
operational tests. Selected waves received Opus review, but none completed
the full independent domain-review and reader-task gates.

The embedded OKF example under AI tooling uses reserved types for format
demonstration, so most teaching elements do not apply there.

| Area | Concepts in catalog | Initial pass recorded | Awaiting first pass |
| --- | --- | --- | --- |
| Bundle root (Start here, glossary) | 2 | 2 | 0 |
| AI, including the embedded OKF example | 21 | 21 | 0 |
| Cloud | 22 | 22 | 0 |
| Cross-topic guides | 16 | 16 | 0 |
| Databases | 11 | 11 | 0 |
| Decision records | 5 | 5 | 0 |
| DevOps | 2 | 2 | 0 |
| FinOps | 1 | 1 | 0 |
| Git | 17 | 17 | 0 |
| Kubernetes | 46 | 46 | 0 |
| Migrations | 9 | 9 | 0 |
| Programming languages | 3 | 3 | 0 |
| Security | 3 | 3 | 0 |
| Solutions architect | 1 | 1 | 0 |
| Templates | 5 | 5 | 0 |
| Terraform | 5 | 5 | 0 |
| **Total** | **169** | **169** | **0** |

All five Terraform and all 17 Git concepts have now received an initial
teaching pass. Their drafts still need independent review and reader tasks
before stronger trust claims.

### Focused review round 1 (2026-10-05)

Claude Opus 5.5 reviewed [OIDC fundamentals](knowledge/security/identity-federation/oidc-fundamentals.md)
and [IAM OIDC provider and STS web identity](knowledge/cloud/aws/security/iam-oidc-provider-and-sts-web-identity.md)
for security-sensitive ambiguity. The review identified overly broad GitHub
`sub` trust patterns, missing GitHub-side controls, unclear issuer and audience
checks, and citation gaps. The pages now distinguish name-based and immutable
GitHub subjects, branch/tag/pull-request/environment contexts, AWS's minimum
`sub` guard from a narrow role policy, and trust policy from role permissions.
Claims were checked against current OpenID Connect, GitHub, and AWS primary
documentation; both Mermaid diagrams were rendered and inspected. This is a
source and diagram review, not a live AWS execution, independent expert
sign-off, or novice reader task. Both concepts remain `draft`.

### Focused review round 2 (2026-10-05)

Claude Opus 5.5 reviewed [Git undo and recovery](knowledge/git/troubleshooting/undo-and-recovery.md)
for beginner safety. The review found that combined restore can delete a
newly added file, short status can hide an in-progress operation, and the
recovery-branch sequence could continue after a failed branch creation.
The guide now makes those stops visible, checks staged and unstaged state,
uses a branch-only reflog recovery, and explains how a local revert reaches
the team. [Solve Git issues](knowledge/git/commands/solve-issues.md) and
[Git fundamentals](knowledge/git/git-fundamentals.md) now point to the
corresponding safe procedures. Git 2.53.0 exercises in a disposable local
repository confirmed staged/unstaged restore, new-file deletion, tracked-file
recovery, soft reset with a preserved commit, and directory-scoped clean.
Official Git command references were checked. This is local command evidence,
not a novice reader trial or proof for every Git edge case; these pages
remain `draft`.

The same round corrected a moved AWS Redshift proof-of-concept reference
after the external-link CI found its old locale URL returning 404. The
canonical AWS page was opened and checked before changing the link.

### Focused review round 3 (2026-10-05)

Claude Opus 5.5 reviewed [Terraform core workflow](knowledge/terraform/commands/core-workflow.md)
and [Terraform state management](knowledge/terraform/fundamentals/state-management.md)
for beginner and operational risk. The workflow now checks Terraform version
and provider identity, keeps saved plans out of Git, teaches the plan marks,
and explains that a plan can evaluate provider and data-source code. The state
page now shows the nested `lifecycle { destroy = false }` syntax for a
`removed` block, distinguishes local state from backend metadata, and explains
ephemeral and write-only values without treating `sensitive` as state
encryption. Current HashiCorp and AWS primary references were checked. The
state diagram was rendered and visually inspected. The Terraform CLI is not
installed in this workspace, so no new Terraform execution is claimed; both
pages remain `draft` pending runtime and reader evidence.

### Focused review round 4 (2026-10-05)

Claude Opus 5.5 reviewed [Kafka delivery guarantees and failure
handling](knowledge/databases/kafka/delivery-guarantees-and-failure-handling.md)
twice for beginner and failure-path accuracy. The guide now explains how a
rebalance can replay an event without a process crash, when automatic commits
can skip unfinished work, why a manual commit uses the next offset, and how
producer results, replica settings, and dead-letter handoffs affect the
outcome. The failure-window diagram was adjusted so the database does not
appear to send an offset commit; the revised diagram was rendered and
inspected. Apache Kafka 4.1 design, producer, consumer, and topic-configuration
documentation was checked independently. No Kafka
broker, external database, crash or rebalance sequence, or novice reader
trial was run. The page remains `draft`.

### Focused review round 5 (2026-10-05)

Claude Opus 5.5 reviewed [the Crossplane AWS S3
lab](knowledge/kubernetes/crossplane/local-aws-s3-lab.md) and [provider
authentication](knowledge/kubernetes/crossplane/providers-and-authentication.md)
for executable and identity-boundary problems. The lab now checks its local
cluster context, isolates the AWS CLI's credential path, waits for the S3 and
family-provider APIs, compares the managed resource's external name and the
expected AWS owner, and makes deletion wait with a timeout. It also gives a
Secret replacement path for expired temporary credentials and requires
AWS-side deletion evidence before removing the provider. The explanation
now shows how the provider configuration selects a credential source and why
an attached Pod role does not override `source: Secret`.

Current Crossplane v2.4, Kubernetes `kubectl`, Upbound package, and AWS STS,
S3, and CLI references were checked independently. All Bash examples parsed
with `bash -n`. No kind, kubectl, Helm, AWS CLI, provider, S3 bucket, or
reader task was run in this workspace; both pages remain `draft` pending an
authorized sandbox exercise and novice review.

### Focused review round 6 (2026-10-05)

Claude Opus 5.5 reviewed [Deploying to
EKS](knowledge/cross-topic-guides/deploying-to-eks.md) twice for a beginner's
release and rollback decisions. The page now separates the Service selector
from endpoint readiness, explains private API endpoint reachability, ties
the intended image to the Deployment and running Pods, distinguishes a
Deployment rollout number from a source revision, and asks which build
answered each sampled user request. The rollback section records the earlier
image digest and source revision and explains that a Deployment undo cannot
restore changed ConfigMaps, Secrets, routing, data, or external effects.

Current Amazon EKS, ECR, and Kubernetes primary documentation was checked
independently. No AWS account, cluster, image, rollout, rollback, or reader
task was exercised. The page remains `draft`.

### Focused review round 7 (2026-10-05)

Claude Opus 5.5 reviewed the three Velero priority guides as a read-only
beginner exercise. The ConfigMap tutorial now selects only its labeled note,
since Kubernetes can create another ConfigMap in each namespace. It makes the
default writable backup location explicit, distinguishes an absent target note
from a literally empty namespace, and checks eventual cleanup. The EKS guide
now identifies the repository transfer Pods as another credential path and
names the CSI feature and snapshot-class selection rules. The migration guide
needed no material correction in this round.

Velero v1.18, the AWS plugin, and Kubernetes primary documentation were
checked independently. The exact installed Velero CLI, live cluster behavior,
AWS permissions, two-cluster restore, and novice reader tasks were not tested.
All three guides remain `draft`.

### Focused review round 8 (2026-10-06)

Claude Opus 5.5 read the Start here to Kubernetes fundamentals to local
deployment route as one beginner journey. The route now tells a reader how
to obtain the example files, distinguishes a local cluster from the first
image downloads, waits for the Node to be ready, names the expected nginx
page, and checks one selected Pod while the deliberate image rollout is
stuck. The port-forward check is explicitly scoped: it bypasses the
Service's virtual IP and does not prove every replica responds. A second
Opus read-only pass found the route still inferred Service behavior from
that Pod check, so it now asks readers to compare EndpointSlice readiness
with Pod IPs before and after recovery. The working-copy step refuses an
already occupied path, and a local port collision has a clear alternative.
It also makes the prior cluster run's evidence boundary explicit: the
current patch-file failure step has not been rerun in a cluster.

The kind, Kubernetes, and official nginx image documentation was checked
independently, and the example YAML was read for name and selector agreement.
The local Docker daemon is unavailable here, and `kind` and `kubectl` are
not installed, so this revision has no new cluster run or novice reader
test. The route remains `draft`.

### Focused review round 9 (2026-10-06)

Claude Opus 5.5 reviewed the Terraform local-state tutorial and its
support files read-only. The tutorial now shows the plan/apply/state
sequence visually, names expected resource and output changes, and
explains that the `-var` override in a saved plan does not change the
configuration default. It tells beginners how to recognize ignored
state and plan files, what a stale saved plan means, and why local
state and backup files remain after resource destruction.

The core command sequence was rerun in a disposable directory using
Terraform v1.13.1 from an archive that passed HashiCorp's published
SHA-256 check. Create, in-place update, plain plan back to the default,
destroy, final empty resource list, and the stale-plan refusal were
observed. HashiCorp command and `terraform_data` references were checked
independently. The new Mermaid timeline rendered and was inspected.
No cloud provider or novice reader was involved; the tutorial remains
`draft`.

### Focused review round 10 (2026-10-06)

Claude Opus 5.5 independently reviewed the first-visit relational versus
document database comparison. The revision now distinguishes indexed searches
of document arrays from full scans, compares PostgreSQL statement and
transaction atomicity with MongoDB single-document and multi-document
atomicity, and separates embedded from referenced reads. It no longer treats
copied product names as inherent to a document model when the example stores
only `sku`. Key terms appear before the comparison table, and the example
warns that readable JSON money and date values are not production BSON types.
The databases index routes a new reader through this comparison first.

Current PostgreSQL and MongoDB primary documentation was checked independently,
and one retrieval case was added. No database workload or novice reader trial
was run. The page remains `draft` and still needs observed reader feedback and
an independent technical review beyond this Opus pass.

### Focused review round 11 (2026-10-06)

Claude Opus 5.5 read the Gateway API and Ingress page alongside the new
Service-selection guide. The revision now separates the external request
path from Gateway API configuration relationships. It does not assume every
implementation traverses a Service ClusterIP: the Kubernetes documentation
permits a Service IP or backing EndpointSlices. The two-team example states
the listener's same-namespace attachment default and distinguishes
`allowedRoutes` from `ReferenceGrant` for a cross-namespace Service or
certificate Secret. It also explains listener TLS versus backend TLS,
separates `Accepted` from `ResolvedRefs`, and distinguishes the retired
Ingress NGINX controller from the still-supported Ingress API.

Current Kubernetes and Gateway API primary documentation was checked,
including the March 2026 retirement confirmation. The Mermaid diagram
rendered and was inspected, and a retrieval case was added. No gateway
implementation, public endpoint, or novice reader task was run. The page
remains `draft` pending implementation-specific feature checks, an external
request test, and reader feedback.

### Focused review round 12 (2026-10-06)

Claude Opus 5.5 reviewed the first-visit cost allocation guide and its AWS
tagging companion. Its original 100-unit example reported 90% decision
coverage without a matching metric, while its shared-cost rule measure could
never reveal a missing rule. The revised example separates direct cost mapped
by account and by resource metadata, centrally funded shared cost, shared
cost awaiting a rule, and cost with no consuming owner. It computes direct,
decision, unallocated, and shared-rule measures from those exact buckets.
Resource-tag compliance now uses eligible taggable cost, with excluded cost
shown separately.

The guide now sets report scope and cost basis before classifying lines,
records mapping precedence and policy effective dates, and explains why
retagging cannot create historical values that never existed. Current FinOps
Framework, FOCUS, and AWS primary sources were checked. The decision-tree
diagram rendered and was inspected, and a retrieval case was added. No real
provider bill, finance review, or novice reader task occurred. The page
remains `draft`.

### Focused review round 13 (2026-10-07)

Claude Opus 5.5 found a misleading suggestion in the AI retrieval guide: a
reranker cannot find a page missing from the candidate list. The revision
separates candidate retrieval, reranking, and exact identifier lookup. It
also filters access before ranking cutoffs, rechecks access at fetch,
distinguishes corpus from upstream producer revisions, and keeps the
condition with an illustrative table-row excerpt. Budget advice now asks
where evidence was lost before increasing a limit; its evaluation checklist
records candidates before final ranking. A retrieval case captures the
candidate-versus-reranker question. A second Opus review caught the excerpt
and measurement gaps before publication.

SQLite, Elasticsearch, and Azure primary documentation were checked. The
revised diagram rendered and was inspected. No search service, permissioned
corpus, ranking measurement, or novice reader test ran; the page remains
`draft`.

### Focused review round 14 (2026-10-07)

Claude Opus 5.5 found that the AI security guide did not say whose
permissions search and fetch must enforce. Its support-assistant example
could therefore be read as permission to use a broader service credential
for a public reader. The revision now uses the authenticated reader's
access at search and fetch, filters before ranking, explains that the model
may still follow hostile text, and puts approval and merge authority on a
separate path. It adds a case for an authorized reader whose data could
leave through an unwanted tool call or loaded outbound link. The test table
checks results, side channels, cache behavior, revocation, tool calls, and
outbound content. A retrieval case records the core question.

OWASP, Azure AI Search, MCP tools and security guidance, and NIST primary
documentation were checked. The revised diagram rendered and was inspected.
Opus reviewed the revised page and found no remaining high-severity issue;
the output-link and identity-passing follow-ups were incorporated. No live
private corpus, assistant, attack test, or novice reader task ran. The page
remains `draft`.

### Focused review round 15 (2026-10-07)

Claude Opus 5.5 found that the reference architecture diagram drew the
search index as coming directly from the knowledge Git commit. Pagefind
actually indexes rendered HTML after the static build. The revised reading
path now shows the separate website pin, source snapshot validation, HTML,
Pagefind, and the combined static artifact. Optional AI retrieval has its
own path. A Terraform-state question traces one real article through the
same stages without claiming a measured search ranking.

The change path now separates knowledge review and merge from the website
pin update, build checks, and review. It makes public release conditional
and explains that the dispatch is only a wake-up signal. The section index
labels its larger pipeline as the target design, and the website planning
README and rollout acknowledge the local scaffold while public repository
and hosting choices remain open. The local website files were inspected
directly because Claude Code's read-only review could not access the
sibling project. OKF, Git, Astro, Pagefind, MCP, and HashiCorp primary
documentation were checked. Both revised diagrams rendered and were
visually inspected. No new website build, sync run, public deployment, or
novice reader task occurred; the concept remains `draft`.

### Focused review round 16 (2026-10-07)

Reviewed the first-visit Git, Kubernetes, and Terraform fundamentals pages with
Claude Opus 5.5 before and after revision. The first review found six teaching
risks: Terraform state can contain provider-returned secrets even when no
secret appears in configuration; normal planning refreshes managed objects;
StatefulSet replacement Pods retain a stable name; EndpointSlice changes have
no fixed replacement order; a Git branch is a pointer to reachable commits;
and `origin/main` is a local, potentially stale remote-tracking branch. The
pages now explain these limits with revised examples, text alternatives, and
diagrams. Three new retrieval cases cover the source-backed questions.

HashiCorp Terraform, Kubernetes, and Git primary documentation were checked
for the corrections. The Git and Terraform diagrams were rendered and
visually inspected; the unchanged Kubernetes diagram was inspected too. The
second Opus review found no high-impact issue; its remaining beginner wording
suggestions were addressed, with Kubernetes endpoint wording kept aligned to
the official condition definitions. No live Terraform or Kubernetes run,
measured retrieval test, or novice reader task occurred. These existing pages
remain `draft`, and the teaching-wave inventory count is unchanged.

### Focused review round 17 (2026-10-07)

Reviewed the next two pages in the local beginner route: Terraform value flow
and Kubernetes Service selection. Claude Opus 5.5 found a material error in
the Terraform analogy: a saved variable-override plan was said to put a value
in state, although only apply records that result. The page now distinguishes
editing a default, planning with an override, applying the saved plan, and
planning again. It also explains why the `terraform_data.output` attribute
may be unknown during a plan despite known inputs. A claim about the exact
output of a prior local run was removed because the retained run record did
not support that detail.

The Kubernetes Service page now states the terminating-endpoint exception
using the official EndpointSlice condition wording and says plainly that
port-forward reaches one selected Pod without using the ClusterIP or Service
proxy route. HashiCorp and Kubernetes primary documentation was checked. A
second read-only Opus review found no remaining material issue; its small
standalone-wording suggestion was incorporated. Two retrieval cases record
the plan/state timing and port-forward questions. No new Terraform run,
Kubernetes cluster run, measured retrieval test, or novice reader task
occurred; both pages remain `draft`.

### Focused review round 18 (2026-10-07)

Revisited the shared glossary after the first-visit Git, Kubernetes,
Terraform, and AI concept revisions. Claude Opus 5.5 found definitions that
taught an outdated Terraform plan model, implied every Pod container shares
storage, and described a Git branch as a line of commits. The Service entry
also pointed to the broad fundamentals page instead of the dedicated
selection explanation. Those entries now match the linked concept pages and
current Git, Kubernetes, and HashiCorp primary references.

Added concise terms that the beginner pages already use but the glossary
did not define, including plan and apply, HEAD and remote-tracking branches,
Service selection and readiness, and AI training, inference, model, token,
assistant, and workflow. The starting table now separates continuous
Kubernetes reconciliation from Terraform's run-based planning. A second
read-only Opus review caught an object/controller mix-up for ReplicaSet, an
ambiguous Service name, weak routes for existing terms, and table ordering;
these were corrected. No new technical concept was added outside the glossary,
and the teaching-wave inventory is unchanged. This was an editorial and source
review; no novice term-finding session occurred. The glossary remains `draft`.

### Focused review round 19 (2026-10-07)

Triaged four short Explanation pages from the broader page inventory with
Claude Opus 5.5. The stateful-versus-stateless explanation was sound in this
review; three other pages needed precise corrections. The proof-of-concept
example now declares a decision rule before its invented search results and
tests a no-answer query separately from ten answerable queries. The security
group explanation now distinguishes AWS-created non-default groups, the VPC
default group, and Terraform AWS provider egress behavior. The bootstrapping
disambiguation now covers compiler and AWS CDK contexts and cites the specific
Terraform S3 backend documentation.

Claude Opus 5.5 reviewed the revised pages read-only and its follow-up
findings were incorporated. Current Google Cloud, Microsoft, AWS, HashiCorp,
Rust, and Bootstrap primary references were checked for the relevant claims.
Three retrieval cases record the changed questions. No PoC search experiment,
AWS or Terraform deployment, compiler build, measured retrieval run, or novice
reader task occurred. These pages remain `draft`, and the teaching-wave
inventory count is unchanged.

### Focused review round 20 (2026-10-07)

Reviewed three connected AI knowledge explanations with Claude Opus 5.5
before and after revision. The knowledge-base overview now traces a sourced
article through a Git branch, source review, a separate reviewed website
pin, rendered pages, and derived Pagefind search files. It explains how to
distinguish an old website pin from an error still present in source `main`
and gives contributors the actual local frontmatter and catalog steps.

The MCP explanation now shows the model's proposed tool call, the host's
control and possible approval, the client's exchange with the server, and
the host's final answer. It separates host conversation history from the
stateless per-request protocol and points older TypeScript examples to
the migration guide. The standards guide now shows OpenAPI Schema Objects
using JSON Schema concepts, cites the relevant MCP server and architecture
pages, and closes its assistant-to-reader path. Its RDF 1.2 Candidate
Recommendation Snapshot status was checked on 2026-10-07.

The official OKF, MCP, OpenAPI, AsyncAPI, W3C, Astro, and Pagefind pages were
checked for the changed claims. All three revised Mermaid diagrams rendered
and were visually inspected. Three static retrieval cases were added. The
separate website was inspected only to confirm its local scaffold status;
there was no live MCP server, public site release, measured retrieval run,
independent domain review, or novice reader task. All pages remain `draft`;
the teaching-wave inventory count is unchanged.

### Focused review round 21 (2026-10-07)

Reviewed the Git command router and its topic indexes with Claude Opus 5.5
before and after revision. Replaced an index analogy that implied staging
only stores selected changes with the fundamentals page's full-snapshot
model. The short-status example now names its two comparison boundaries,
shows `git add -- lesson.md`, and repeats the checks after staging. It
explains `--cached` and `--staged`, the path separator, and the `##` branch
header. The example was rerun in a disposable Git 2.53.0 repository.

Separated branch switching, merging, rebasing, fetching, pushing, checkout,
bisect, and object maintenance by effect and risk. Current Git manuals
confirmed switch's default protection for local changes, merge and rebase
behavior, status's optional index refresh, revision-range differences,
and bisect cleanup. A disposable bisect run confirmed detached `HEAD` and
restoration of the original branch. The command index now puts the task map
first, points newcomers to fundamentals, and returns to the bundle index.
Two static retrieval cases record the status and branch-operation questions.
No novice reader trial, independent Git domain review, remote history
operation, or full command-by-command runtime check occurred. The page
remains `draft`; the teaching-wave inventory count is unchanged.

### Focused review round 22 (2026-10-07)

Reviewed the EKS operations page with Claude Opus 5.5. Its initial review
identified a misleading access model and a troubleshooting branch that did
not fit an available Deployment. The revised invented incident checks the
target context and rollout revision, then shows how a Service selector
mismatch produces no lesson-API endpoints. The access section now separates
AWS token failures, Kubernetes `Unauthorized`, and `Forbidden` without
suggesting a broad permission grant. Other changes clarify image-pull versus
workload IAM, scheduling events before node changes, Pod Identity evidence,
the Pod Identity Agent and EKS Auth path, managed add-ons versus Auto Mode
capabilities, and lag in EKS health issues. Opus's second read-only pass
identified the missing agent check; that check and smaller wording issues
were corrected against AWS documentation.

AWS EKS, Amazon ECR, and Kubernetes primary documentation was checked for
the changed claims. One static retrieval case records the available
Deployment and empty-Service question. No account, cluster, Pod, network,
request, or novice reader trial was run. Independent EKS security review
and controlled incident exercises remain open; the page is still `draft`.

### Focused review round 23 (2026-10-08)

Reviewed the CrashLoopBackOff guide with Claude Opus 5.5. Corrected the
claim that a loop always means an application failure: an app container
under `restartPolicy: Always` can restart after a clean exit. The guide
now identifies the affected app, init, or sidecar container before
requesting its previous logs. It directs readers to termination and
waiting messages when application logs are absent, separates OOM evidence
from a mere exit code, and warns that missing events cannot rule out a
probe kill.
The revised diagram, cause table, and recovery step all follow this
evidence path. Recovery checks account for a replacement Pod name and
for a temporarily `Running` container between restarts. Opus's second
read-only review found that a Deployment Pod points first to a ReplicaSet;
the guide now follows that ownership chain, confirms rollout completion,
and observes recovery against the old container's survival time rather
than waiting through an unrelated backoff on a new Pod.

Current Kubernetes primary documentation was checked for the changed
claims. The Mermaid diagram rendered and was visually inspected. Two
static retrieval cases record the clean-exit and init-container
questions. No live cluster, disposable reproduction, independent
Kubernetes review, or novice reader task ran; the page remains `draft`.

### Focused review round 24 (2026-10-08)

Reviewed Kubernetes on AWS with Claude Opus 5.5. The photo API now
shows the Ingress-to-Service declaration and the two alternative ALB
traffic paths: instance targets through a Service NodePort and IP
targets directly to Pods. Standard EKS no longer implies that EKS
automatically installs a load-balancer controller, while Auto Mode
names the IngressClass and IngressClassParams handoff. The guide also
distinguishes Fargate from Pod Identity and EBS support, warns about
node-role credential fallback, and explains why one zonal EBS volume
is not shared storage for replicas. The pending-claim diagnosis now
accounts for `WaitForFirstConsumer`.

Current AWS and Kubernetes primary documentation was checked for the
changed claims. The Mermaid diagram rendered and was visually inspected.
Two static retrieval cases record the ALB path and Fargate storage and
identity questions. No AWS account, cluster, load balancer, Pod, volume,
request, independent EKS security review, or novice reader task ran;
the guide remains `draft`.

### Focused review round 25 (2026-10-08)

Reviewed the EKS tooling-cluster explanation with Claude Opus 5.5. It
now distinguishes local controllers, a self-managed controller in a
tooling cluster, and AWS-managed Argo CD attached to a management
cluster. The invented two-target diagram separates GitOps control from
user traffic and shows the target access configuration. A three-gate
table follows network reachability, authentication, and authorization;
the article also names the source and user access that lets someone
ask the controller to act. It corrects the impression that an Argo CD
Project narrows the underlying target credential, and adds Flux and
Argo impersonation limits, a conditional admission-webhook outage,
and a recovery check for automatic reconciliation of emergency edits.
Two linked guides received matching target-credential corrections.

Current AWS, Argo CD, Flux, and Kubernetes primary documentation was
checked. The Mermaid diagram rendered and was inspected. Two static
retrieval cases record the managed-private-target and broad-credential
questions. No EKS cluster, controller, private endpoint, target API,
outage, restore, user request, independent security review, or novice
reader task ran; the revised guides remain `draft`.

### Focused review round 26 (2026-10-08)

Reviewed the APISIX-on-EKS explanation with Claude Opus 5.5 and checked
its material claims against current Apache APISIX, Gateway API, and AWS
documentation. The invented request and Mermaid diagram now distinguish
the backend Service and EndpointSlice configuration reference from the
usual direct gateway-to-Pod request path. The guide explains instance
versus IP NLB targets, public exposure, TLS and port placement,
client-IP preservation, optional listener-port matching, and why a
route can be present on only some gateway Pods. The linked APISIX 404
guide now distinguishes an HTTP 404 from NLB network forwarding,
shows the backend endpoint configuration path, and names the
cross-namespace `ReferenceGrant` check. A second Opus audit caught a
Gateway API status error in the linked architecture guide: `Programmed`
belongs to the Gateway and listeners, while route status reports
`Accepted` and `ResolvedRefs`. The request and troubleshooting diagrams
rendered and were visually inspected. Four static retrieval cases record
the corrected Service, client-IP, NLB 404, and status questions.

Opus's first review could not fetch live documentation and marked
several version-specific claims uncertain. The changed statements were
checked independently in official sources; unverified suggestions were
not added. No EKS cluster, NLB, APISIX gateway, backend, live request,
independent security review, or novice reader task ran. The three
revised guides remain `draft`.

### Candidates for the next wave

- Run independent technical and security review of the priority operational
  guides, especially OIDC, cloud permissions, restore, and executable tasks;
  record findings and correct pages before claiming stable status.
- Recruit novice readers for the existing task protocol. Observe whether
  they can find a topic, explain its model, choose a safe next step, and
  locate the official source; record confusion and revise the pages.
- Try the contributor templates on a new Explanation, How-to Guide, and
  Reference with a real contributor. Record where copying or placement is
  unclear and revise the scalable topic-entry workflow.
- Test a real search and fetch path against the golden retrieval cases,
  including source revisions and access-filtered results.
- Use observed reader demand to choose the next topics, including a
  dedicated observability section and focused Terraform language pages
  if those gaps block learning.

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
