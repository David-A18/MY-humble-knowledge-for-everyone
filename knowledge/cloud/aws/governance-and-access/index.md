# AWS governance and human access

Design account boundaries and workforce access, then verify provisioning, guardrails, review and recovery. These source-reviewed drafts complement the [AWS security path](../security/index.md); they do not replace its IAM request evaluation, credential or workload-identity material.

## Learning and operational routes

| Outcome | Guide |
| --- | --- |
| Choose accounts and common control paths | [Account and OU design](account-and-ou-design.md) — Boundaries, ownership, management/delegated administration and change impact. |
| Understand workforce federation | [Identity Center and human federation](identity-center-and-human-federation.md) — Instance type, SAML/SCIM, permission sets versus account access manager. |
| Operate baseline account-role templates | [Permission sets and assignments](permission-sets-and-assignments.md) — Provisioning, policies, generated-role references and removal. |
| Establish the actual CLI caller | [Human CLI sessions](cli-sso-and-role-sessions.md) — Refreshable SSO, model-specific login and separate session lifetimes. |
| Bound organization access | [Policy guardrails](organization-policy-guardrails.md) — SCP/RCP scope, inherited allow/deny and staged recovery. |
| Delegate IAM work | [Delegated IAM administration](delegated-iam-administration.md) — Boundaries, policy versions, trust, tags and PassRole escalation paths. |
| Prepare exceptional recovery | [Root and emergency access](root-and-emergency-access.md) — Centralized member-root tasks, protected root credentials and outage dependencies. |
| Provision and retire accounts | [Account vending and lifecycle](account-vending-and-lifecycle.md) — Organizations, Control Tower, AFT, acceptance and residual obligations. |
| Review and remove human access | [Access reviews and offboarding](access-review-and-offboarding.md) — Overlapping direct/group paths, approvals, issued sessions and completion evidence. |
| Diagnose an access/control failure | [Governance troubleshooting](governance-access-troubleshooting.md) — Directory, assignment, provisioning, credentials, policy path and recovery authority. |
| Practice inventory reconciliation | [Examples](examples/index.md) — Synthetic joins, review expiry, uncertainty and fourteen local regression tests. |

## Evidence and remaining work

Primary sources reviewed on 2026-11-10. The local Python lab was executed with Python 3.13.17 and uses only synthetic data; no account calls or organization/identity changes occurred. Its output is potential assignment exposure under declared input assumptions, not effective IAM authorization or proof of revoked access. All concepts remain draft/unassigned.

Follow up in authorized test accounts with actual directory/assignment collection, login and allowed/denied operations, provisioning/role-reference changes, staged SCP/RCP tests, emergency activation and session containment. Account creation/closure and IdP setup need their own bounded lifecycle evidence. See the [section review ledger](../../../../section-quality-progress.md).

## Connected routes

- [IAM policy evaluation](../security/iam-policy-evaluation-and-least-privilege.md), [credential lifecycle](../security/credential-providers-and-session-lifecycle.md), and [incident response](../security/security-incident-response.md).
- [EKS human identity and RBAC](../../../security/identity-federation/eks-human-identity-and-rbac.md) — Human account access is separate from cluster authorization.
- [EKS workload identity](../../../cross-topic-guides/eks-workload-identity.md) — IRSA/Pod Identity remain workload routes.
- [FinOps](../finops/index.md) — Account ownership, cost allocation and notification evidence.

[Back to AWS](../index.md) | [Back to knowledge](../../../index.md)
