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
  - [ ] [Git troubleshooting](knowledge/git/troubleshooting/index.md) — safe
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
