# AWS architecture

Status: Initial outline

Architecture guidance, reference patterns, and design trade-offs for AWS workloads.

## Articles

| Article | Purpose |
| --- | --- |
| [Stateful vs. stateless](stateful-vs-stateless.md) | Ask what a replacement replica needs to recover and where that state lives. |
| [Stateless application patterns](stateless-application-patterns.md) | Move application compute toward replaceable replicas with externalized state. |
| [Stateful design decision checklist](stateful-design-decision-checklist.md) | Review state ownership, recovery, networking, data, and Kubernetes risks before production. |

## Expected content

- Well-Architected review notes.
- Multi-account patterns.
- High availability and disaster recovery.
- Reference architectures.
- Design review checklists.

## Official documentation

- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)

[Back to AWS index](../index.md) | [Back to root index](../../../../README.md)
