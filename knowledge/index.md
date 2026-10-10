---
okf_version: "0.2"
---

# Engineering knowledge base

Start with something you want to understand. Choose a question below or browse
the topics. Pages explain an idea in plain language, show an example when it
helps, and link to official documentation for deeper study. The library is
growing; topic indexes distinguish published pages from planned coverage.

## Start by goal

| Goal | Start here | Outcome |
| --- | --- | --- |
| New here or want a local practice route | [Start here](start-here.md) | Choose one question or follow a Git, Kubernetes, and Terraform route without a cloud account. |
| Understand an unfamiliar word | [Glossary](glossary.md) | Read a short definition and follow its link to a deeper explanation. |
| Understand how Git tracks and shares changes | [Git fundamentals](git/git-fundamentals.md) | Picture the working tree, index, commits, branches, and remotes before running recovery commands. |
| Understand cloud computing before choosing a provider | [Cloud computing fundamentals](cloud/cloud-computing-fundamentals.md) | Explain the provider's role, your responsibilities, scaling, reliability, and usage-based cost. |
| Understand AI before choosing a tool | [AI fundamentals](ai/ai-fundamentals.md) | Separate ML, generative AI, language models, assistants, and agents; check outputs against sources. |
| Understand how a program runs | [Programming fundamentals](programming-languages/programming-fundamentals.md) | Trace source code, input, a function and condition, and output in a small Python example. |
| Understand Kubernetes before running commands | [Kubernetes fundamentals](kubernetes/fundamentals/kubernetes-fundamentals.md) | See how desired state, controllers, Pods, and Services fit together. |
| Recover safely from a Git mistake | [Git undo and recovery](git/troubleshooting/undo-and-recovery.md) | Inspect first, then choose the least-destructive recovery action. |
| Diagnose a Kubernetes workload | [Kubernetes troubleshooting](kubernetes/troubleshooting/index.md) | Move from symptom to safe diagnostics and recovery. |
| Understand Kubernetes Service traffic | [How a Kubernetes Service selects Pods](kubernetes/core-objects/how-a-service-selects-pods.md) | Trace labels, readiness, EndpointSlices, and in-cluster routing. |
| Learn Terraform safely | [Terraform fundamentals](terraform/fundamentals/terraform-fundamentals.md) | Understand plan, apply, and state; optionally trace [configuration values](terraform/language/how-values-move-through-terraform.md) before the [local state tutorial](terraform/examples/local-state-lifecycle/local-state-lifecycle.md). |
| Design a Crossplane platform API | [How Crossplane's components turn a request into a resource](kubernetes/crossplane/component-model.md) | After Kubernetes fundamentals, follow a request through XRD, XR, Composition, managed resource, and provider. |
| Plan backup or migration work | [Velero](migrations/velero/index.md) | Choose backup, restore, migration, and disaster-recovery guidance. |

## Reading and trust signals

- `draft` means useful material whose review is still open.
- `stable` means a page met the repository's recorded source and review rules
  and has a next review date. Check the official sources for current behavior.
- `deprecated` means do not use the page for new work; look for its replacement.
- An `initial outline` topic index names planned coverage and may have no
  articles yet. Start from a linked beginner explanation when one is offered.
- Each concept page shows its status. Sources, review evidence, and deadlines
  appear when they have been recorded; an absent review date is not proof of a
  fresh review.
- If an explanation or step is unclear, use the
  [documentation issue form](https://github.com/David-A18/MY-humble-knowledge-for-everyone/issues/new?template=documentation-error.yml)
  to name the page and describe the problem without private details.

## Engineering topics

- [Cloud](cloud/index.md) - Provider-neutral cloud guidance and AWS, Azure, Google Cloud, edge, and solution patterns.
- [Kubernetes](kubernetes/index.md) - Kubernetes concepts, operations, applications, Crossplane, and troubleshooting.
- [Git](git/index.md) - Version control, recovery, GitHub Actions, and delivery workflows.
- [Terraform](terraform/index.md) - Infrastructure as code, state, commands, examples, and maintenance.
- [Databases](databases/index.md) - Database modeling, Kafka, MongoDB, and platform choices.
- [Migrations](migrations/index.md) - Backup, restore, disaster recovery, and migration practices.
- [Security](security/index.md) - Identity federation and cross-platform security guidance.
- [FinOps](finops/index.md) - Cost visibility, allocation, and accountability.
- [DevOps](devops/index.md) - Delivery, automation, reliability, and code quality.
- [Programming languages](programming-languages/index.md) - Begin with a small Python program; three Bootstrap and bootstrapping articles follow, with broader language coverage planned.

## AI and architecture

- [AI](ai/index.md) - Beginner AI concepts, tooling, MCP, knowledge bases, and safe engineering use.
- [AI agents](ai-agents/index.md) - Planned agent route; begin with AI fundamentals, then follow its current tooling links.
- [LLM](llm/index.md) - Planned LLM route; begin with AI fundamentals, then explore current retrieval material in AI tooling.
- [ML](ml/index.md) and [MLOps](mlops/index.md) - Outlines only, with no articles yet; begin with AI fundamentals.
- [Solutions architect](solutions-architect/index.md) - Design trade-offs, proofs of concept, and architecture reviews.
- [Cross-topic guides](cross-topic-guides/index.md) - End-to-end workflows across technologies.

## Learning and reference material

- [Start here](start-here.md) - Choose a first question or follow the local practice route.
- [Glossary](glossary.md) - Short definitions, with deeper routes where a concept page exists.

## About and contribute

- [Decision records](decision-records/index.md) - Recorded repository and architecture decisions.
- [Templates](templates/index.md) - Diátaxis-aligned documentation starters.
- [Assets](assets/index.md) - Guidance for diagrams, images, and icons.
- [Bundle log](log.md) - Notable changes to this knowledge bundle.
