# Section quality progress

Review snapshot: 2026-10-29. This ledger tracks the ongoing section-by-section quality pass. A reviewed section has had its index and direct concepts inspected; it does not imply that its child sections, runtime examples, or every technical claim are production verified.

## Current batch: FinOps and AWS FinOps

Reviewed both existing FinOps concepts and indexes, added eleven focused concepts plus two example indexes, and connected allocation, budgets/forecasts, anomalies, reporting/units, usage/rate optimization, Kubernetes costs, and AWS implementation routes. The four indexed FinOps directories have explicit learning and operational outcomes. All new concepts remain draft/unassigned.

FinOps Foundation, OpenCost, and AWS primary sources were reviewed on 2026-10-29. The guidance distinguishes delayed alerts from hard caps, resource tags from billing activation/backfill, recommendations from tested capacity changes, and modeled avoidance from realized financial results. The current Savings Plans type set and Data Exports options were checked rather than copied from older summaries.

The synthetic Python 3.13.17 lab passes thirteen tests: source/shared totals and credits reconcile, fractional cents use a declared boundary, rounding is deterministic, unknown ownership stays visible, invalid/mixed/duplicate data is rejected, zero units remain undefined, and quantity/rate effects are not double-counted. Its before/after demand example explicitly allows a rising total with an improved unit cost. All figures are teaching inputs, not customer data, price quotes, or observed savings.

AWS CLI 2.38.5 checked seven unique read-only examples offline: five output-skeleton validations and two input-parse-only checks. Budgets and anomaly subscriptions' generated outputs violated minimum-period/ARN constraints; no account-response or authentication result is inferred. Named profiles were omitted in offline checks. No AWS account call, export creation, notification, purchase, tag/backfill mutation, resource deletion, or workload optimization occurred.

Follow-ups require authorized notification delivery, real billing/report reconciliation, a representative controlled capacity/SLO test, actual commitment/financial interpretation, and attributable measured results. Kubernetes cost-tool deployment and provider-data adapters also need versioned environment evidence. The local CSV is deliberately not CUR/FOCUS data.

### FinOps validation

| Check | Recorded result |
| --- | --- |
| Repository checks | All fifteen required validator/test commands pass, including live GitHub label comparison. |
| Markdown and navigation | 414 files lint cleanly; links, heading fragments, parent indexes, and reachability pass. |
| Catalog and retrieval definitions | 255 concepts; reproducible catalog; 59 retrieval definitions validate. |
| External URLs | All 516 checked unique URLs returned HTTP 200 after redirects; external fragments were not tested. |
| Retrieval execution | All twelve new FinOps questions retrieve their expected route among the top five chunks; a fresh absent token returns `NO_EVIDENCE`. This is lexical retrieval evidence, not model-answer quality. |
| Local examples | The thirteen synthetic calculation tests pass with Python 3.13.17. Seven AWS CLI examples have the limited offline evidence described above; no account or production acceptance is inferred. |
| CI change | A dedicated workflow runs the synthetic tests and report on Python 3.13 in Linux. Hosted results must be inspected for the exact published commit. |

## Previous batch: Terraform

Reviewed all existing Terraform indexes and direct concepts, retained the workflow/state/fundamentals/local learning material, and added twelve focused concepts plus five code/lab indexes. The fourteen indexed Terraform directories now have explicit routes for language contracts, stable keys, modules, provider requirements/aliases, dependency locks, environment layout, workspaces, remote backends, diagnosis, review/CI, and practice. Reviewed means content/navigation/evidence assessment; the section is not uniformly runtime-verified production guidance.

Executed locally with Python 3.13.17 and Terraform 1.17.1 on Windows amd64. The Terraform archive SHA256 matched HashiCorp's published HTTPS list; its detached checksum signature was not verified. The provider lab installed hashicorp/local 2.9.1 with Terraform reporting HashiCorp signing; dependency checksum preparation included Windows amd64 and Linux amd64. Hosted CI runs the two new labs on Linux for each published revision; do not infer that result from local execution.

The module lab passes three Terraform contracts (one apply and two expected validation failures), rejects an invalid CLI plan with exit 1, observes changed/no-change outcomes 2/0, adds a stable key without replacing existing records, preserves two object IDs across address moves, separates default/preview state, and destroys both states' objects before deleting preview. The provider lab verifies its alias mapping, a local JSON artifact, locked installation, a no-change plan, destruction, and empty state. The original beginner lifecycle also passes init/validate/plan/apply/state/change/destroy with the new CLI baseline.

All new concepts remain draft/unassigned. Remote backend migration, competing writers, cloud IAM/provider behavior, provider-specific imports, real drift/recovery, hosted credentials, and artifact permission/approval checks remain explicit follow-ups. S3 backend snippets are source reviewed, not deployed; current documentation's opt-in S3 lock files and deprecated DynamoDB locking are distinguished from provider dependency locks.

### Terraform validation

| Check | Recorded result |
| --- | --- |
| Repository checks | All fifteen required validator/test commands pass, including live GitHub label comparison. |
| Markdown and navigation | 401 files lint cleanly; links, heading fragments, parent indexes, and reachability pass. |
| Catalog and retrieval definitions | 244 concepts; reproducible catalog; 47 retrieval definitions validate. |
| External URLs | All 490 checked unique URLs returned HTTP 200 after redirects; external fragments were not tested. |
| Retrieval execution | All eleven Terraform questions retrieve their expected route among the top five chunks; a fresh absent token returns `NO_EVIDENCE`. This is lexical retrieval evidence, not model-answer quality. |
| Local examples | Both new lab runners and the existing local state lifecycle pass with Terraform 1.17.1; provider installation, state/file cleanup, and no external resource creation are distinguished from remote acceptance. |
| CI change | The Terraform workflow pins 1.17.1, disables the CLI wrapper, and runs both local labs. Hosted results must be inspected for the exact published commit. |

## Previous batch: AWS networking

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
| P2 | [Terraform follow-ups](knowledge/terraform/index.md) | Execute bounded remote lock/migration/restore, provider import/drift, and hosted credential/artifact drills; preserve the local lab contracts and cleanup evidence. |
| P2 | [FinOps follow-ups](knowledge/finops/index.md) | Validate real notification/billing/workload outcomes and data adapters; preserve synthetic calculations as a separate evidence level. |
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
| [cloud/aws/finops](knowledge/cloud/aws/finops/index.md) | 5 | Reviewed 2026-10-29; real billing/workload evidence open |
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
| [finops/examples/cost-analysis-lab](knowledge/finops/examples/cost-analysis-lab/index.md) | 1 | Reviewed 2026-10-29; real billing/workload evidence open |
| [finops/examples](knowledge/finops/examples/index.md) | 0 | Reviewed 2026-10-29; real billing/workload evidence open |
| [finops](knowledge/finops/index.md) | 7 | Reviewed 2026-10-29; real billing/workload evidence open |
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
| [terraform/best-practices](knowledge/terraform/best-practices/index.md) | 1 | Reviewed 2026-10-29; remote/cloud procedures open |
| [terraform/commands](knowledge/terraform/commands/index.md) | 2 | Reviewed 2026-10-29; remote/cloud procedures open |
| [terraform/examples](knowledge/terraform/examples/index.md) | 0 | Reviewed 2026-10-29; remote/cloud procedures open |
| [terraform/examples/local-state-lifecycle](knowledge/terraform/examples/local-state-lifecycle/index.md) | 1 | Reviewed 2026-10-29; remote/cloud procedures open |
| [terraform/examples/module-workspace-lab/child](knowledge/terraform/examples/module-workspace-lab/child/index.md) | 0 | Reviewed 2026-10-29; remote/cloud procedures open |
| [terraform/examples/module-workspace-lab](knowledge/terraform/examples/module-workspace-lab/index.md) | 1 | Reviewed 2026-10-29; remote/cloud procedures open |
| [terraform/examples/module-workspace-lab/tests](knowledge/terraform/examples/module-workspace-lab/tests/index.md) | 0 | Reviewed 2026-10-29; remote/cloud procedures open |
| [terraform/examples/provider-alias-lab/child](knowledge/terraform/examples/provider-alias-lab/child/index.md) | 0 | Reviewed 2026-10-29; remote/cloud procedures open |
| [terraform/examples/provider-alias-lab](knowledge/terraform/examples/provider-alias-lab/index.md) | 1 | Reviewed 2026-10-29; remote/cloud procedures open |
| [terraform/fundamentals](knowledge/terraform/fundamentals/index.md) | 5 | Reviewed 2026-10-29; remote/cloud procedures open |
| [terraform](knowledge/terraform/index.md) | 0 | Reviewed 2026-10-29; remote/cloud procedures open |
| [terraform/language](knowledge/terraform/language/index.md) | 2 | Reviewed 2026-10-29; remote/cloud procedures open |
| [terraform/project-structure](knowledge/terraform/project-structure/index.md) | 2 | Reviewed 2026-10-29; remote/cloud procedures open |
| [terraform/troubleshooting](knowledge/terraform/troubleshooting/index.md) | 1 | Reviewed 2026-10-29; remote/cloud procedures open |

## Related planning

- [Quality standard and original checklist](knowledge-content-quality-expansion-plan.md)
- [Maintenance review queue](maintenance-review-queue.md)
- [Prioritized roadmap](ROADMAP.md)
- [Back to repository](README.md)
