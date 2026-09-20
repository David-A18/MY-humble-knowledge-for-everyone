---
type: "Explanation"
title: "Proof of Concept"
description: "A Proof of Concept, usually shortened to PoC, is a small, time-boxed effort"
tags: [solutions-architect, proof-of-concept]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
---

# Proof of Concept

## Purpose

A Proof of Concept, usually shortened to `PoC`, is a small, time-boxed effort
used to prove whether an idea, technology, integration, architecture, or
approach is feasible before committing to a larger project.

A good PoC answers a focused question:

> Can this work well enough under the constraints that matter?

It is not meant to be a full product, a polished user experience, or a permanent
production system. Its value is the evidence it creates.

## When to use this

- A team is unsure whether a technology can solve a real problem.
- A design has an important unknown, such as latency, cost, compatibility,
  security, scaling, migration effort, or operational complexity.
- Stakeholders need evidence before funding, approving, or prioritizing a
  bigger implementation.
- A new tool, framework, provider, vendor, API, or architecture pattern needs to
  be evaluated against practical constraints.
- The team needs to compare options before writing an Architecture Decision
  Record.

## Key ideas

| Concept | Meaning | Why it matters |
| --- | --- | --- |
| PoC | Proof of Concept; a focused experiment that tests feasibility. | Prevents committing to an idea that cannot work in practice. |
| Hypothesis | The specific claim the PoC is trying to prove or disprove. | Keeps the work focused and measurable. |
| Success criteria | The conditions that must be true for the PoC to be considered useful or successful. | Avoids subjective "it worked on my machine" conclusions. |
| Scope | The boundary of what the PoC will and will not test. | Prevents the PoC from growing into an unplanned product. |
| Time box | A fixed duration for the experiment. | Forces a decision with available evidence instead of endless exploration. |
| Disposable implementation | Code or infrastructure that may be thrown away after learning is complete. | Reduces pressure to make experimental work production-grade too early. |

## What a PoC does

A PoC reduces uncertainty. It turns a guess into evidence.

Common PoC goals include:

- prove that two systems can integrate;
- verify that a library, framework, cloud service, or vendor supports a required
  capability;
- measure rough performance, latency, throughput, or cost;
- check whether a security or compliance constraint blocks the approach;
- expose operational work such as monitoring, backups, deployment, rollback, and
  failure recovery;
- compare two or more implementation options;
- discover hidden complexity before the real project starts.

## What a PoC is not

| Not the same as | Difference |
| --- | --- |
| Production system | A PoC may ignore hardening, scale, monitoring, support, and long-term maintenance. |
| Prototype | A prototype often demonstrates user experience or interaction. A PoC proves feasibility. |
| MVP | A Minimum Viable Product is a usable product slice for real users. A PoC may never reach users. |
| Pilot | A pilot tests a more complete solution with a limited real-world audience. |
| Spike | A spike is a short research task, often in agile teams. A PoC is usually more evidence-oriented and demonstrable. |

These terms overlap in real conversations, so always ask what decision the work
is supposed to support.

## Vocabulary around PoCs

| Term | Plain meaning |
| --- | --- |
| `PoC` | Short for Proof of Concept. |
| `Feasibility` | Whether something can realistically work under the constraints that matter. |
| `Assumption` | Something the team believes but has not proven yet. |
| `Hypothesis` | A testable statement, such as "Service A can process 1,000 events per second with acceptable latency." |
| `Constraint` | A limit the solution must respect, such as budget, time, security policy, data residency, or platform compatibility. |
| `Trade-off` | A decision where improving one quality may worsen another, such as speed versus maintainability. |
| `Prototype` | An early model used to explore shape, interaction, or behavior. |
| `MVP` | Minimum Viable Product; the smallest useful product version that can deliver value to real users. |
| `Pilot` | A controlled real-world rollout to a limited group before a wider launch. |
| `Spike` | A short investigation used to learn enough to estimate, design, or decide. |
| `Throwaway code` | Code written to learn, not to become the production implementation. |
| `Hardening` | Work needed to make something secure, reliable, observable, scalable, and maintainable. |
| `Production-ready` | Suitable for real users or workloads with support, monitoring, security, recovery, and operational ownership. |
| `Decision record` | A document that records the chosen direction, context, alternatives, and consequences. |

## Good PoC question examples

| Weak question | Better PoC question |
| --- | --- |
| Can we use Kafka? | Can Kafka handle our expected event size and ordering needs with acceptable consumer lag during peak load? |
| Is this API good? | Can this API support our authentication, rate limit, pagination, and error-handling requirements? |
| Should we use Kubernetes? | Can this workload be deployed, scaled, monitored, and rolled back on Kubernetes with our current team skills? |
| Can we migrate this app? | Can the app run against the target database with acceptable query performance and no blocking feature gaps? |
| Is this vendor useful? | Can this vendor meet our security, integration, cost, support, and data-export requirements? |

## How to structure a PoC

### 1. State the decision

Write the decision the PoC is meant to support.

Example:

```text
Decide whether the team should use managed Kafka or a queue service for the
new event-processing workflow.
```

What it does: keeps the PoC tied to a concrete choice, not open-ended learning.

### 2. Define the hypothesis

Write the claim being tested.

Example:

```text
Managed Kafka can process the expected event volume with less than 2 seconds of
consumer lag during the peak-load scenario.
```

What it does: gives the PoC a claim that can be tested with data.

### 3. Set success criteria

Define what must be true for the PoC to support moving forward.

Example:

```text
The PoC is successful if:

- producer errors stay below 0.1%;
- consumer lag returns to normal within 5 minutes after a traffic spike;
- estimated monthly cost stays within the approved budget range;
- the deployment can be reproduced from documented steps.
```

What it does: makes the result measurable and reviewable.

### 4. Limit the scope

Write what is intentionally excluded.

Example:

```text
Out of scope:

- complete CI/CD pipeline;
- production alerting;
- full user interface;
- multi-region disaster recovery;
- long-term data retention tuning.
```

What it does: protects the PoC from becoming a hidden full project.

### 5. Build the smallest useful test

Build only enough to answer the question. That may be:

- a small service;
- a sample integration;
- a benchmark;
- a local lab;
- a cloud sandbox;
- a minimal UI flow;
- a migration trial;
- a vendor API test.

The implementation should be realistic enough to expose the important risk, but
small enough to finish quickly.

### 6. Record evidence

Useful PoC evidence includes:

- screenshots;
- diagrams;
- benchmark results;
- logs;
- cost estimates;
- failure notes;
- code snippets;
- commands used;
- vendor or official documentation links;
- a short recommendation.

### 7. Decide what happens next

Every PoC should end with a recommendation:

| Outcome | Meaning |
| --- | --- |
| Proceed | The idea is feasible enough to design and build properly. |
| Proceed with conditions | The idea works, but only if specific risks are handled. |
| Run another PoC | The first PoC answered one question but exposed another important unknown. |
| Stop | The idea is not feasible, too risky, too expensive, or not valuable enough. |
| Choose another option | A different tool, architecture, or approach fits better. |

## PoC deliverables

A useful PoC usually leaves behind:

- the decision or question tested;
- the hypothesis;
- success and failure criteria;
- short setup instructions;
- code, configuration, or diagrams when useful;
- test data or scenario description;
- results and observations;
- known gaps;
- risks discovered;
- recommendation;
- next steps.

If the PoC produces code, label whether the code is disposable or intended to be
evolved into production code.

> [!IMPORTANT]
> Do not let PoC code become production code by accident. If the team chooses to
> keep it, create explicit hardening work for security, tests, observability,
> reliability, documentation, ownership, and maintenance.

## Technical examples

### Frontend framework PoC

Question:

```text
Can Bootstrap support the dashboard layout and form components needed for the
internal admin tool without custom design-system work?
```

Success criteria:

- dashboard layout works on desktop and mobile;
- forms are accessible with labels and keyboard navigation;
- required components exist without heavy customization;
- CSS bundle size is acceptable for the application.

Likely deliverable: one or two representative screens, notes about missing
components, and a recommendation.

### API integration PoC

Question:

```text
Can the payment provider API support our checkout, refund, webhook, and audit
requirements?
```

Success criteria:

- authentication works in a sandbox;
- checkout and refund flows can be completed;
- webhook events are signed and can be verified;
- error cases are documented;
- rate limits are acceptable.

Likely deliverable: a small integration service, webhook verification notes, and
a decision summary.

### Infrastructure PoC

Question:

```text
Can Terraform create and update the target cloud resources safely with remote
state, locking, and reviewable plans?
```

Success criteria:

- remote state and locking work;
- `plan` output is understandable in review;
- resource changes can be reproduced from a clean checkout;
- drift can be detected;
- permissions follow least privilege.

Likely deliverable: a minimal Terraform module, setup notes, risk list, and
decision record input.

## Common mistakes

| Mistake | Why it hurts |
| --- | --- |
| No decision attached | The team learns something but still cannot decide what to do. |
| Scope is too broad | The PoC turns into an unplanned project. |
| Success criteria are vague | Stakeholders argue about whether the PoC succeeded. |
| Only happy path tested | The real risk appears later in production design. |
| No operational checks | The technology works in a demo but cannot be supported safely. |
| No cost check | A technically valid option may be financially unrealistic. |
| PoC code silently becomes production | Experimental shortcuts become long-term risk. |
| Results are not documented | The team loses the learning and repeats the same work later. |

## Review checklist

- What decision does this PoC support?
- What assumption is being tested?
- What is explicitly out of scope?
- What evidence will prove success or failure?
- What failure modes must be tested?
- What security, cost, reliability, and operational constraints matter?
- Who will review the result?
- What happens to the code or infrastructure after the PoC?
- Will the output become a decision record, backlog work, or a stop decision?

## Related links

- Back to solutions architect index: [README.md](index.md)
- Back to root index: [../README.md](../../README.md)
