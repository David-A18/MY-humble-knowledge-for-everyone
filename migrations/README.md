# Migrations

Practical migration guidance for infrastructure, Kubernetes platforms, workloads, data, backup, restore, disaster recovery, and environment replication.

## Index

| Section | Focus |
| --- | --- |
| [Velero](velero/README.md) | Kubernetes backup, restore, disaster recovery, cluster migration, S3-compatible backup storage, and persistent volume protection. |

## Migration planning checklist

| Question | Why it matters |
| --- | --- |
| What is moving? | Cluster resources, application state, storage data, DNS, identities, and external dependencies may need different tools. |
| What is the RPO? | Defines how much data loss is acceptable if the migration or recovery point is used. |
| What is the RTO? | Defines how quickly the destination environment must become usable. |
| Is this a same-provider move? | Same-provider migrations can often use native snapshots; cross-provider moves usually need file-level or application-level data movement. |
| How will restore be tested? | A backup that has never been restored is only an assumption. |

## Expected future content

- Database migration patterns.
- Cloud account, region, and provider migration planning.
- Kubernetes upgrade and cluster replacement runbooks.
- Storage migration and disaster recovery decision guides.

[Back to root index](../README.md)
