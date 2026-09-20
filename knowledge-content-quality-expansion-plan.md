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
