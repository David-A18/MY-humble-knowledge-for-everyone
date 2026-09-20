# Knowledge-base readiness review

Review date: 2026-09-20
Reviewed revision: `4d1c0de` on `develop`

## Decision

The knowledge base is **not perfect yet** for either people or AI agents. It
is, however, a strong and usable structural foundation: the corpus is a valid
OKF v0.2 bundle, navigation is complete, local links resolve, Markdown is
clean, and the repository has useful authoring and maintenance rules.

It is ready to be used as a **draft engineering reference and learning
library**. It is not ready to be presented as a uniformly reviewed,
current, and reproducible authority. The next work should make the existing
high-value material trustworthy and easy to follow before expanding into new
subject areas.

## Scope and method

This review inspected the current `knowledge/` bundle, repository routes,
templates, contributor rules, validation scripts, workflows, and the
maintainer review queue. It also followed the main reader routes from the
repository landing page and inspected the local Git, Kubernetes, and Terraform
learning paths.

The following current checks passed:

```text
python3 scripts/validate-okf.py knowledge
node scripts/validate-local-links.mjs
npx markdownlint-cli2 "**/*.md"
```

The review did not execute every cloud, Kubernetes, database, or vendor
command. A passing structural check proves that navigation and Markdown are
sound; it does not prove that every technical claim or command still behaves
as documented.

## Current evidence

| Measure | Result | What it means |
| --- | ---: | --- |
| Markdown files in `knowledge/` | 235 | A substantial portable corpus. |
| Reserved `index.md` files | 77 | Every knowledge directory has an entry point. |
| Curated concepts with required OKF profile | 156 | Every non-reserved Markdown concept is parseable. |
| Local-link, fragment, index, and reachability errors | 0 | Readers and agents can traverse the Markdown graph. |
| Markdown-lint errors | 0 | The writing format has a clean automated baseline. |
| Concepts marked `draft` | 146 | The status is honest, but most content has not completed a review cycle. |
| Concepts marked `stable` | 10 | Seven belong to the embedded OKF example; three are ordinary curated guides. |
| Concepts with structured sources | 3 | All three are inside the embedded OKF example. |
| Concepts with structured verification or freshness data | 10 | All ten are inside the embedded OKF example. |
| Concepts with an assigned maintainer | 0 | No current person or team owns a review deadline. |
| Concepts typed `Explanation` | 112 | The Diátaxis classification is heavily skewed and needs editorial review. |
| Concepts typed `Tutorial` | 1 | Several practical learning experiences are not surfaced as tutorial concepts. |
| Concepts under 150 words | 22 | Ten are intentional OKF-example records; the remaining short pages are mostly outlines or incomplete guides. |

The bundle is technically valid, but the data above shows the distinction
between **machine-readable structure** and **machine-readable trust**. The
former is complete; the latter has only been demonstrated by the example
bundle.

## What already works well

### Navigation is reliable

[The bundle index](knowledge/index.md) gives people and agents a concise map
of major areas. Parent indexes expose their direct children, focused pages use
relative links, and the local-link validator checks targets, heading fragments,
index presence, and reachability. This is an excellent foundation for both
GitHub browsing and agent retrieval.

### There is a real safe beginner route

[Start here](knowledge/start-here.md), [the local Kubernetes learning
path](knowledge/cross-topic-guides/local-deployment-learning-path.md), and
[Git recovery](knowledge/git/troubleshooting/undo-and-recovery.md) provide a
meaningful local-first journey. They include prerequisites, expected results,
intentional failure, recovery, warnings, and cleanup. This is the right model
for future tutorials.

### The repository has a healthy maintenance foundation

The OKF validator, local-link validator, Markdown lint, issue forms, review
queue, source-ingestion area, contributor guide, licensing split, and
`develop` branch checks give contributors a coherent operating model. The
[maintenance review queue](maintenance-review-queue.md) already names the ten
operational guides that should be reviewed first.

### The scope is honest

Most material is marked `draft`, and the most developed areas are visibly
Kubernetes, Crossplane, AWS/EKS, Git, Kafka, MongoDB, and Velero. Keeping thin
areas visible as planned coverage is better than making unsupported claims of
completeness.

## Findings and exact next actions

### P0 — Repair post-migration command paths and the Terraform quality gate

The Markdown-link validator cannot inspect paths embedded in shell commands,
JSON examples, or YAML snippets. The OKF move left nine references to the old
root-level layout. They make examples or future agent integrations point at
paths that no longer exist.

| File | Required correction |
| --- | --- |
| [local Kubernetes path](knowledge/cross-topic-guides/local-deployment-learning-path.md) | Change `cp kubernetes/examples/...` to `cp knowledge/kubernetes/examples/...`. |
| [Terraform local-state tutorial](knowledge/terraform/examples/local-state-lifecycle/index.md) | Change both `cp terraform/examples/...` paths to `cp knowledge/terraform/examples/...`. |
| [daily Git commands](knowledge/git/commands/daily-commands.md) | Change `git ls-files git/commands` and `git add git/commands/daily-commands.md` to their `knowledge/git/...` paths. |
| [provenance guide](knowledge/ai/ai-tooling/knowledge-bases/provenance-trust-and-freshness.md) | Update the sample concept path to begin with `knowledge/`. |
| [retrieval guide](knowledge/ai/ai-tooling/knowledge-bases/retrieval-and-context-efficiency.md) | Update the JSON sample path to begin with `knowledge/`. |
| [MCP guide](knowledge/ai/ai-tooling/model-context-protocol.md) | Update the `readKnowledgeEntry` sample path to begin with `knowledge/`. |
| [GitHub Actions example](knowledge/git/github-actions/examples-and-use-cases.md) | Update the illustrative `terraform/**` change filter to `knowledge/terraform/**` when it describes this repository. |
| [Terraform workflow](.github/workflows/terraform-format.yml) | Change `find terraform` and `terraform fmt ... terraform` to `knowledge/terraform`. The current workflow is green because it finds no root `terraform/` directory and skips the actual example. |
| [PR template](.github/PULL_REQUEST_TEMPLATE.md) | Replace the obsolete `README.md`-index checklist item with `index.md` for knowledge directories. |

Add a fence-aware command-path validator after these fixes. It should flag
references to moved top-level knowledge directories inside executable Markdown
fences. This closes the quality gap that local-link validation cannot see.

**Done when:** the affected examples work from the repository root, the
Terraform workflow formats `knowledge/terraform`, the PR template reflects
OKF, and the new validator has fixtures for an old and a valid path.

### P1 — Turn trust and freshness into real metadata

The three ordinary `stable` guides—Git undo and recovery, Terraform core
workflow, and Terraform state management—contain useful human-readable review
blocks. None has structured `sources`, `verified`, or `stale_after` metadata.
Every such record currently belongs to the intentionally illustrative OKF
example, so an AI consumer cannot distinguish actual reviewed guidance from
ordinary draft content reliably.

Review the ten priority guides already named in the maintenance queue. For each
guide, record only evidence that really happened, using official sources and a
real review date. A reviewed operational concept should look like this:

```yaml
sources:
  - id: terraform-cli
    resource: https://developer.hashicorp.com/terraform/cli
    title: Terraform CLI documentation
verified:
  - by: human:maintainer-handle
    at: 2026-09-20T12:00:00Z
stale_after: 2026-12-19
```

Use source IDs in keyed claim footnotes for material claims. Keep `status:
draft` when a page lacks this evidence. Change to `stable` only after the
source, review, scope, and deadline are recorded. For high-risk guides, state
whether evidence is source-reviewed, locally executed, sandbox-executed, or
reader-tested.

Assign an actual maintainer or maintainer team at this time. Normalize the
existing values (`unassigned` and `Unassigned`) while doing this work.

**Done when:** all ten priority guides have an owner, current official sources,
an actual verification record, a review deadline, and a clear evidence scope.

### P1 — Separate navigation indexes from reader concepts

OKF reserves `index.md` for navigation, which deliberately has no concept
metadata. Several important reader outcomes currently live inside indexes,
making them invisible to metadata-driven retrieval and impossible to classify
or review as concepts.

The clearest cases are:

- [Kubernetes fundamentals](knowledge/kubernetes/fundamentals/index.md), a
  297-word explanation used by the beginner route.
- [Terraform local state lifecycle](knowledge/terraform/examples/local-state-lifecycle/index.md), a
  622-word tutorial with a real local execution record.

Move each learning outcome to a named concept beside the index, such as
`kubernetes-fundamentals.md` and `local-state-lifecycle.md`. Leave the index
as a short directory map and add the full OKF profile, Diátaxis type, sources,
evidence, and related links to the moved concept. Apply the same rule when an
index grows beyond orientation and direct-child navigation.

**Done when:** every substantial procedure, tutorial, reference, or explanation
has its own non-reserved Markdown file and complete profile metadata.

### P1 — Complete reader journeys before adding new areas

The main route is usable but uneven. `AI agents`, `LLM`, `ML`, `MLOps`,
`FinOps`, Azure, several Terraform sections, and several Kubernetes sections
are planned indexes with little or no focused content. They are useful roadmaps
for maintainers, but they are not yet satisfying destinations for readers.

Do not try to fill every topic. Finish these small, high-value journeys first:

1. **Local platform foundations:** retain the current Git → Kubernetes → local
   deployment → Terraform route; repair the P0 paths and run it from a fresh
   checkout.
2. **Kubernetes diagnosis:** turn `kubectl basics` into a complete how-to with
   prerequisites, decision sequence, expected outputs, failure signals, and
   safe stop conditions; link it to `CrashLoopBackOff` and common solutions.
3. **Terraform fundamentals:** add one short explanation of providers,
   resources, state, and plan/apply, then route readers to the local tutorial.
4. **Cloud cost basics:** either create one actionable FinOps guide using
   existing AWS cost-allocation material or mark FinOps clearly as planned in
   the top-level index.
5. **AI-agent boundary:** define the first practical agent workflow and make
   the relationship among AI tooling, AI agents, LLMs, ML, and MLOps explicit.

Keep unbuilt areas as short "planned coverage" indexes. Do not call them
complete, and do not create placeholder articles merely to increase counts.

**Done when:** a new reader can complete the local route, follow one
troubleshooting route, and choose a next learning path without encountering an
empty or misleading destination.

### P2 — Apply Diátaxis as an editorial decision, not just metadata

`Explanation` accounts for 112 of 156 concepts, while only one concept is a
`Tutorial`. This is a useful migration baseline, not a finished content design.
Many operational pages appear to have been classified mechanically rather than
by their primary reader outcome.

For every page touched during the review cycle, choose exactly one outcome:

- A **Tutorial** teaches a bounded journey and verifies a result.
- A **How-to Guide** completes one task from an assumed starting point.
- A **Reference** is scannable, precise, and complete enough to consult.
- An **Explanation** teaches concepts and trade-offs without pretending to be
  a procedure.
- A **Troubleshooting Guide** starts from a symptom and ends in a safe
  diagnosis or recovery.

Remove duplicated hand-written `Status`, `Audience`, `Page type`, and
`Maintainer` blocks when the data belongs in frontmatter. Where a page needs
reader-facing review information, render it consistently from the same
metadata or label it as evidence scope. This avoids contradictions such as a
frontmatter `How-to Guide` with an inline `Page type: Reference`.

**Done when:** types match reader intent, practical guides have the required
sections, and frontmatter is the single source of truth for lifecycle fields.

### P2 — Make the bundle measurable for AI retrieval

The current index graph is enough for deterministic traversal. It does not yet
prove that an agent finds the right concept efficiently, honors draft or stale
content, or cites evidence correctly.

Add a small, versioned golden-question set outside the curated corpus, for
example `tests/retrieval-cases.yaml`. Start with the ten tasks already used in
the reader-test guide. Each case should include the question, expected concept
path, expected source IDs when present, required status behavior, and an
acceptable top-k rank.

Generate a non-canonical catalog from frontmatter for retrieval tools. It
should contain the bundle revision, path, title, description, type, tags,
status, maturity, owner, review deadline, and source IDs. Do not hand-edit it;
rebuild it in CI from `knowledge/`.

Test the following separately:

1. Index traversal and path resolution.
2. Metadata filtering, including draft, deprecated, and stale behavior.
3. Retrieval ranking for the golden questions.
4. Answer grounding and citation correctness where a source record exists.
5. Context budget: documents and tokens read before reaching evidence.

**Done when:** a repeatable test can show whether an agent finds the intended
guide within the agreed budget, rather than relying on anecdotal success.

### P2 — Measure the human experience before building a site

The current repository surface is adequate while content and trust work are in
progress. The right next decision is not a documentation website; it is
evidence from real readers.

Run the existing reader-test protocol with three to five intended readers.
Start them from [Start here](knowledge/start-here.md), use the ten tasks in the
[facilitator guide](reader-test-facilitator-guide.md), record only anonymous
results, and turn repeated blockers into small documentation issues.

Use the results to decide whether GitHub navigation is sufficient or whether a
static site needs full-text search, a task-based landing page, version badges,
or another discovery aid.

**Done when:** the repository has recorded reader results, repeated blockers,
and fixes linked to the evidence.

## Upgrade sequence

| Phase | Work | Exit criterion |
| --- | --- | --- |
| 0 — Restore migration integrity | Fix the nine path references, Terraform workflow scope, and PR template; add command-path validation. | Commands and CI point only at canonical `knowledge/` paths. |
| 1 — Establish trust | Review the ten priority guides, assign owners, record structured sources, verification, and deadlines. | Every selected guide has honest machine-readable trust information. |
| 2 — Make learning reliable | Extract substantial index content, repair the local path, complete the Kubernetes diagnosis and Terraform foundation routes. | A fresh reader can complete the local route and choose a next route. |
| 3 — Improve AI retrieval | Create a generated catalog and golden retrieval tests. | An agent's discovery, filtering, and evidence behavior is measurable. |
| 4 — Expand deliberately | Use reader demand and review capacity to select the next focused articles. | New content has an owner, source plan, and correct Diátaxis outcome before drafting. |

## Definition of a mature knowledge base

Treat this as the operational standard for a future `stable` corpus:

- Every reader-facing procedure is independently addressable as a concept, not
  hidden in an index.
- Every stable, technical claim has current official sources and a real review
  record.
- Every operational guide states prerequisites, intended result, safety,
  validation, recovery, and cleanup when applicable.
- Every concept has a real owner or an explicit, consistently formatted
  unowned status with an active review queue.
- Every learning route has been run by intended readers and every runnable
  tutorial has execution evidence.
- Retrieval tests prove that agents can find authoritative, non-stale evidence
  before drafting an answer.
- CI validates OKF metadata, internal links, command paths, rendered Markdown,
  generated catalog freshness, issue forms, and actual Terraform examples.

## Final assessment

People can navigate the knowledge base today, and the local beginner journey
shows real practical value. AI agents can parse its metadata and traverse its
link graph reliably. Neither audience should yet assume that every topic is
complete, current, owned, source-backed, or runnable.

The path to a high-quality knowledge base is clear: repair the move defects,
review the existing priority guides, extract concepts from indexes, validate
reader journeys, and then measure agent retrieval. That sequence will improve
usefulness and trust much faster than adding more unreviewed topics.

## Related links

- [Knowledge bundle](knowledge/index.md)
- [Knowledge-base improvement plan](knowledge-base-improvement-plan.md)
- [Maintenance review queue](maintenance-review-queue.md)
- [Reader test facilitator guide](reader-test-facilitator-guide.md)
- [Contributor guide](CONTRIBUTING.md)
- [AI agent guide](AGENTS.md)
- [Back to repository index](README.md)
