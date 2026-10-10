# AWS architecture

Status: Initial outline

Architecture guidance, reference patterns, and design trade-offs for AWS workloads.

## Articles

| Article | Purpose |
| --- | --- |
| [Stateful vs. stateless](stateful-vs-stateless.md) | Ask what a replacement replica needs to recover and where that state lives. |
| [Stateless application patterns](stateless-application-patterns.md) | See how shared state and a queue let app replicas be replaced, and what partial failures still need handling. |
| [Stateful design decision checklist](stateful-design-decision-checklist.md) | Trace authoritative data through failure and recovery, then identify the evidence needed for RTO and RPO claims. |

## Expected content

- Well-Architected review notes.
- Multi-account patterns.
- High availability and disaster recovery.
- Reference architectures.
- Design review checklists.

## Official documentation

- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)

[Back to AWS index](../index.md) | [Back to knowledge index](../../../index.md)
