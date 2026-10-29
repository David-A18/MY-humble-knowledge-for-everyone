# Section quality progress

Review snapshot: 2026-10-29. This ledger tracks the ongoing section-by-section quality pass. A reviewed section has had its index and direct concepts inspected; it does not imply that its child sections, runtime examples, or every technical claim are production verified.

## Current batch: AWS networking

Scope: reviewed all three prior direct concepts (security groups, stateful networking, CloudFront), replaced the outline index with a learning path, and added seven focused concepts. The ten-guide section now covers address planning, effective routes, zonal/regional NAT, endpoints and private DNS, security boundaries, VPC/hybrid connectivity selection, a read-only lab, and symptom-driven diagnostics.

Official AWS sources reviewed on 2026-10-29. All ten concepts remain draft with unassigned ownership; no AWS account calls, infrastructure changes, or live packet/failover tests were performed. The section review is a content/navigation/evidence assessment, not a deployment attestation.

CLI evidence: v2.38.5 was executed locally. Twenty-six documented command occurrences reduce to sixteen unique commands. Fourteen EC2 commands passed offline output-skeleton validation. STS caller identity and CloudFront configuration passed input-skeleton parsing only: generated output placeholders failed ARN-length and origin-group-member constraints. Named profiles were omitted from offline tests; actual credentials/account authorization were not tested. This limitation is recorded in the lab and CloudFront guide.

Follow-ups: perform the read-only lab in an authorized account, record resolved DNS and actual path evidence, validate permitted/denied requests and planned failover, and add bounded Transit Gateway provisioning, hybrid DNS/BGP, and endpoint-policy lockout recovery procedures. No numeric cost estimate is asserted; current regional pricing and the actual traffic footprint are required for a deployment decision.

### AWS networking validation

| Check | Result |
| --- | --- |
| Repository profile and governance | All fifteen required validator/test commands passed, including the live GitHub label comparison. |
| Markdown and navigation | 384 files lint cleanly; local links, heading fragments, parent indexes, and reachability pass. |
| Catalog and retrieval cases | 232 concepts; reproducible catalog; 37 retrieval definitions validate. |
| External URLs | All 475 checked unique URLs returned HTTP 200 after redirects; external fragments were not tested. |
| Retrieval smoke checks | Eight targeted keyword queries retrieve their intended guide in the top five chunks; a fresh absent token returns `NO_EVIDENCE`. These are lexical smoke checks, not natural-language or model-answer quality evidence. |
| CLI / cloud | AWS CLI 2.38.5: fourteen output-skeleton checks and two parse-only checks as explained above; no cloud execution. |

A bounded correction in the linked CDN guide fixes the reversed cache-key explanation: missing representation-changing inputs risks mixed responses, while unnecessary inputs fragment cache. The edge section remains pending a full review.

## Previous batch: Kubernetes troubleshooting

Scope: the section index and all eleven direct guides. Four existing guides were expanded/refactored, seven focused guides added, and all direct routes connected. The symptom router now directs readers to DNS, Service routing, storage, scheduling, image pulls, rollouts, Gateway API/TLS, crashes, APISIX, or kind diagnostics.

Evidence: official Kubernetes, Gateway API, APISIX, and kind documentation reviewed on 2026-10-29. Each guide records its sources, expected observations, recovery boundaries, and return route. Source review is separate from runtime execution. All remain draft with an unassigned maintainer. Static validation results are recorded in the publication commit and CI.

Known follow-ups: reproduce these sequences in disposable clusters; record actual Kubernetes/controller versions and representative redacted outputs; exercise DNS/policy, topology/CSI, certificate, and rollback failures. No live Kubernetes, APISIX, kind, or storage-driver walkthrough was executed in this batch. The existing local regression lab is the practice route rather than another duplicate lab.

### Validation recorded for this batch

| Check | Result |
| --- | --- |
| Required repository checks | All fifteen validator/test commands passed, including live comparison of five GitHub labels. |
| Markdown and navigation | 377 files lint cleanly; relative targets, heading fragments, parent indexes, and reachability pass. |
| External URLs | All 446 checked unique URLs returned HTTP 200 after redirects; external fragments were not tested. |
| Catalog and retrieval cases | 225 concepts; reproducible catalog; all 29 retrieval-case definitions validate. Definition validation is not a measured natural-language retrieval score. |
| Local retrieval smoke check | Seven targeted keyword queries each retrieve their intended new guide in the top five chunks; a freshly generated absent token produces `NO_EVIDENCE`. No model generation was requested. |
| Runtime boundary | Python 3.13.17 and Node 24.22.1 ran local checks. Docker, kind, and Helm are unavailable; the installed kubectl executable is denied execution. Cluster behavior remains untested. |

The retrieval smoke check also exposed a tutorial issue: a hard-coded nonsense query matched its own indexed tutorial. The [RAG lab](knowledge/llm/rag/repository-lab.md) now generates the absent query at runtime. This is a bounded correction; the RAG section has not received a full section review in this cycle.

Next review: when upstream behavior changes, a reader reports a failure, or runtime evidence becomes available. Weekly upkeep selects one useful improvement; it does not imply a full technical review of every page each week.

## Next sections and completion criteria

| Priority | Section / task | Completion criterion |
| --- | --- | --- |
| P2 | [AWS networking follow-up](knowledge/cloud/aws/networking/index.md) | Execute the authorized read-only lab and controlled traffic/failover drills; expand transit/hybrid deployment and endpoint-policy recovery procedures. |
| P1 | [Terraform](knowledge/terraform/index.md) | Preserve the existing workflow/state/local lab; add focused module/provider/workspace guidance and remote-backend recovery boundaries instead of duplicating fundamentals. |
| P1 | [FinOps](knowledge/finops/index.md) | Build on cost allocation and AWS tagging; add budgets/anomaly response and a measured rightsizing example with explicit ownership and limits. |
| P2 | [AWS security](knowledge/cloud/aws/security/index.md) | Review existing OIDC/IRSA material and EKS comparison; record trust/permission evidence gaps before adding more identity summaries. |
| P2 | [Core reader journeys](knowledge/start-here.md) | Follow prerequisites and handoffs, record broken/confusing routes, and improve only evidenced gaps. |
| P2 | [New learning series](knowledge/index.md#expanded-learning-paths) | Recheck version-sensitive security/availability claims and add actual disposable-environment evidence when available. |

## Indexed-section inventory

The table is an on-disk snapshot of every knowledge directory index. Direct counts exclude reserved `index.md` and `log.md`. Pending means not reviewed in this quality cycle, not that the section is empty or defective. A parent stays pending when only one child is reviewed. Reconcile this inventory whenever directories are added or removed.

| Section | Direct concepts | Review state |
| --- | --- | --- |
| [ai/ai-tooling](knowledge/ai/ai-tooling/index.md) | 3 | Pending |
| [ai/ai-tooling/knowledge-bases/examples](knowledge/ai/ai-tooling/knowledge-bases/examples/index.md) | 0 | Pending |
| [ai/ai-tooling/knowledge-bases/examples/okf-v0.2/concepts](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/concepts/index.md) | 3 | Pending |
| [ai/ai-tooling/knowledge-bases/examples/okf-v0.2](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/index.md) | 1 | Pending |
| [ai/ai-tooling/knowledge-bases/examples/okf-v0.2/references/attesters](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/references/attesters/index.md) | 1 | Pending |
| [ai/ai-tooling/knowledge-bases/examples/okf-v0.2/references/executors](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/references/executors/index.md) | 1 | Pending |
| [ai/ai-tooling/knowledge-bases/examples/okf-v0.2/references](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/references/index.md) | 0 | Pending |
| [ai/ai-tooling/knowledge-bases/examples/okf-v0.2/references/sources](knowledge/ai/ai-tooling/knowledge-bases/examples/okf-v0.2/references/sources/index.md) | 4 | Pending |
| [ai/ai-tooling/knowledge-bases](knowledge/ai/ai-tooling/knowledge-bases/index.md) | 7 | Pending |
| [ai](knowledge/ai/index.md) | 0 | Pending |
| [ai-agents](knowledge/ai-agents/index.md) | 0 | Pending |
| [assets/diagrams](knowledge/assets/diagrams/index.md) | 0 | Pending |
| [assets/icons](knowledge/assets/icons/index.md) | 0 | Pending |
| [assets/images](knowledge/assets/images/index.md) | 0 | Pending |
| [assets](knowledge/assets/index.md) | 0 | Pending |
| [cloud/aws/architecture](knowledge/cloud/aws/architecture/index.md) | 3 | Pending |
| [cloud/aws/cdk/examples](knowledge/cloud/aws/cdk/examples/index.md) | 0 | Pending |
| [cloud/aws/cdk/examples/python](knowledge/cloud/aws/cdk/examples/python/index.md) | 0 | Pending |
| [cloud/aws/cdk/examples/typescript](knowledge/cloud/aws/cdk/examples/typescript/index.md) | 0 | Pending |
| [cloud/aws/cdk](knowledge/cloud/aws/cdk/index.md) | 5 | Pending |
| [cloud/aws/compute](knowledge/cloud/aws/compute/index.md) | 4 | Pending |
| [cloud/aws/databases](knowledge/cloud/aws/databases/index.md) | 3 | Pending |
| [cloud/aws/finops](knowledge/cloud/aws/finops/index.md) | 1 | Pending |
| [cloud/aws/fundamentals](knowledge/cloud/aws/fundamentals/index.md) | 0 | Pending |
| [cloud/aws/governance-and-access](knowledge/cloud/aws/governance-and-access/index.md) | 0 | Pending |
| [cloud/aws](knowledge/cloud/aws/index.md) | 0 | Pending |
| [cloud/aws/networking](knowledge/cloud/aws/networking/index.md) | 10 | Reviewed 2026-10-29; runtime and advanced procedures open |
| [cloud/aws/security](knowledge/cloud/aws/security/index.md) | 4 | Pending |
| [cloud/aws/solutions-architect](knowledge/cloud/aws/solutions-architect/index.md) | 0 | Pending |
| [cloud/aws/storage](knowledge/cloud/aws/storage/index.md) | 0 | Pending |
| [cloud/aws/troubleshooting](knowledge/cloud/aws/troubleshooting/index.md) | 0 | Pending |
| [cloud/azure](knowledge/cloud/azure/index.md) | 0 | Pending |
| [cloud/edge](knowledge/cloud/edge/index.md) | 4 | Pending |
| [cloud/gcloud](knowledge/cloud/gcloud/index.md) | 1 | Pending |
| [cloud](knowledge/cloud/index.md) | 0 | Pending |
| [cloud/solutions](knowledge/cloud/solutions/index.md) | 1 | Pending |
| [cross-topic-guides/examples/data-aggregation](knowledge/cross-topic-guides/examples/data-aggregation/index.md) | 0 | Pending |
| [cross-topic-guides/examples](knowledge/cross-topic-guides/examples/index.md) | 0 | Pending |
| [cross-topic-guides](knowledge/cross-topic-guides/index.md) | 18 | Pending |
| [databases](knowledge/databases/index.md) | 2 | Pending |
| [databases/kafka](knowledge/databases/kafka/index.md) | 5 | Pending |
| [databases/mongodb](knowledge/databases/mongodb/index.md) | 5 | Pending |
| [decision-records](knowledge/decision-records/index.md) | 5 | Pending |
| [devops/code-quality](knowledge/devops/code-quality/index.md) | 2 | Pending |
| [devops/development-environments/examples](knowledge/devops/development-environments/examples/index.md) | 0 | Pending |
| [devops/development-environments/examples/local/.devcontainer](knowledge/devops/development-environments/examples/local/.devcontainer/index.md) | 0 | Pending |
| [devops/development-environments/examples/local](knowledge/devops/development-environments/examples/local/index.md) | 0 | Pending |
| [devops/development-environments](knowledge/devops/development-environments/index.md) | 5 | Pending |
| [devops](knowledge/devops/index.md) | 0 | Pending |
| [finops](knowledge/finops/index.md) | 1 | Pending |
| [git/best-practices](knowledge/git/best-practices/index.md) | 0 | Pending |
| [git/commands](knowledge/git/commands/index.md) | 6 | Pending |
| [git/github-actions](knowledge/git/github-actions/index.md) | 9 | Pending |
| [git](knowledge/git/index.md) | 0 | Pending |
| [git/tricks](knowledge/git/tricks/index.md) | 0 | Pending |
| [git/troubleshooting](knowledge/git/troubleshooting/index.md) | 1 | Pending |
| [knowledge bundle](knowledge/index.md) | 2 | Pending |
| [kubernetes/applications-and-tools](knowledge/kubernetes/applications-and-tools/index.md) | 15 | Pending |
| [kubernetes/applications-and-tools/istio/examples](knowledge/kubernetes/applications-and-tools/istio/examples/index.md) | 0 | Pending |
| [kubernetes/applications-and-tools/istio](knowledge/kubernetes/applications-and-tools/istio/index.md) | 6 | Pending |
| [kubernetes/applications-and-tools/kro/examples](knowledge/kubernetes/applications-and-tools/kro/examples/index.md) | 0 | Pending |
| [kubernetes/applications-and-tools/kro](knowledge/kubernetes/applications-and-tools/kro/index.md) | 5 | Pending |
| [kubernetes/applications-and-tools/manifest-validation/examples](knowledge/kubernetes/applications-and-tools/manifest-validation/examples/index.md) | 0 | Pending |
| [kubernetes/applications-and-tools/manifest-validation/examples/policy](knowledge/kubernetes/applications-and-tools/manifest-validation/examples/policy/index.md) | 0 | Pending |
| [kubernetes/applications-and-tools/manifest-validation](knowledge/kubernetes/applications-and-tools/manifest-validation/index.md) | 5 | Pending |
| [kubernetes/applications-and-tools/platform-tooling](knowledge/kubernetes/applications-and-tools/platform-tooling/index.md) | 11 | Pending |
| [kubernetes/best-practices](knowledge/kubernetes/best-practices/index.md) | 0 | Pending |
| [kubernetes/commands](knowledge/kubernetes/commands/index.md) | 6 | Pending |
| [kubernetes/core-objects](knowledge/kubernetes/core-objects/index.md) | 2 | Pending |
| [kubernetes/crossplane](knowledge/kubernetes/crossplane/index.md) | 17 | Pending |
| [kubernetes/examples](knowledge/kubernetes/examples/index.md) | 0 | Pending |
| [kubernetes/examples/local-deployment-learning-path](knowledge/kubernetes/examples/local-deployment-learning-path/index.md) | 0 | Pending |
| [kubernetes/fundamentals](knowledge/kubernetes/fundamentals/index.md) | 1 | Pending |
| [kubernetes](knowledge/kubernetes/index.md) | 0 | Pending |
| [kubernetes/observability/examples](knowledge/kubernetes/observability/examples/index.md) | 0 | Pending |
| [kubernetes/observability](knowledge/kubernetes/observability/index.md) | 7 | Pending |
| [kubernetes/tricks](knowledge/kubernetes/tricks/index.md) | 0 | Pending |
| [kubernetes/troubleshooting](knowledge/kubernetes/troubleshooting/index.md) | 11 | Reviewed 2026-10-29; runtime follow-ups open |
| [llm](knowledge/llm/index.md) | 0 | Pending |
| [llm/rag/examples](knowledge/llm/rag/examples/index.md) | 0 | Pending |
| [llm/rag](knowledge/llm/rag/index.md) | 6 | Pending |
| [migrations](knowledge/migrations/index.md) | 0 | Pending |
| [migrations/velero](knowledge/migrations/velero/index.md) | 9 | Pending |
| [ml](knowledge/ml/index.md) | 0 | Pending |
| [mlops](knowledge/mlops/index.md) | 0 | Pending |
| [programming-languages](knowledge/programming-languages/index.md) | 1 | Pending |
| [security/identity-federation](knowledge/security/identity-federation/index.md) | 3 | Pending |
| [security](knowledge/security/index.md) | 0 | Pending |
| [solutions-architect](knowledge/solutions-architect/index.md) | 1 | Pending |
| [templates](knowledge/templates/index.md) | 5 | Pending |
| [terraform/best-practices](knowledge/terraform/best-practices/index.md) | 0 | Pending |
| [terraform/commands](knowledge/terraform/commands/index.md) | 1 | Pending |
| [terraform/examples](knowledge/terraform/examples/index.md) | 0 | Pending |
| [terraform/examples/local-state-lifecycle](knowledge/terraform/examples/local-state-lifecycle/index.md) | 1 | Pending |
| [terraform/fundamentals](knowledge/terraform/fundamentals/index.md) | 2 | Pending |
| [terraform](knowledge/terraform/index.md) | 0 | Pending |
| [terraform/language](knowledge/terraform/language/index.md) | 0 | Pending |
| [terraform/project-structure](knowledge/terraform/project-structure/index.md) | 0 | Pending |
| [terraform/troubleshooting](knowledge/terraform/troubleshooting/index.md) | 0 | Pending |

## Related planning

- [Quality standard and original checklist](knowledge-content-quality-expansion-plan.md)
- [Maintenance review queue](maintenance-review-queue.md)
- [Prioritized roadmap](ROADMAP.md)
- [Back to repository](README.md)
