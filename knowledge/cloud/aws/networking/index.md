# AWS networking

Learn the address and routing model, choose connectivity and security boundaries, then inspect an existing network. The guides are source-reviewed drafts; offline CLI checks do not prove live connectivity.

## Learning and operating routes

| Guide | Outcome |
| --- | --- |
| [VPC and subnet fundamentals](vpc-and-subnet-fundamentals.md) | Understand AWS address space, subnet placement, exposure, and the boundaries between routing, filtering, and identity. |
| [Find the effective subnet route and next hop](route-tables-and-path-selection.md) | Resolve explicit versus main route-table associations and select the destination-specific path before changing networking. |
| [Internet gateways and NAT egress](internet-and-nat-egress.md) | Choose direct internet, zonal or regional NAT, IPv6 egress, or service endpoints with explicit availability and cost trade-offs. |
| [VPC endpoints and private DNS](vpc-endpoints-and-private-dns.md) | Distinguish gateway and interface endpoints and diagnose network, DNS, and authorization requirements for private AWS API access. |
| [Security groups](security-groups.md) | Understand ENI security-group rules, references, connection tracking, and a least-privilege verification sequence. |
| [Stateful networking and stateless subnet controls](stateful-networking.md) | Explain why return traffic and symmetric paths matter when security groups, NACLs, NAT, and appliances interact. |
| [Choose VPC and hybrid connectivity](vpc-connectivity-options.md) | Compare VPC peering, Transit Gateway, PrivateLink, VPN, and Direct Connect by reachability scope and operating responsibility. |
| [Read-only VPC inspection lab](network-inspection-lab.md) | Build an evidence map of an existing authorized VPC and explain one dependency path without provisioning or changing its resources. |
| [Diagnose AWS network connectivity failures](network-connectivity-troubleshooting.md) | Move from a failing DNS, TCP, TLS, or API request to the responsible VPC path or policy without broad firewall changes. |
| [CloudFront](cloudfront.md) | Design CloudFront request paths, cache isolation, origin protection, and verification for AWS applications and EKS backends. |

## Suggested sequence

Start with VPC/subnets → effective routes → egress/endpoints → security groups and ACLs. Choose peering/transit/hybrid connectivity only after the required reachability scope is clear. Complete the read-only lab to explain one existing dependency path; use the diagnostic runbook for a real failure.

CloudFront is the edge entry-path guide and links to the separate CDN and EKS material. Detailed Transit Gateway provisioning, hybrid DNS/BGP, endpoint-policy lockout recovery, and cloud-backed failover drills remain future focused procedures.

## Practice and evidence

Sources were reviewed on 2026-10-29. AWS CLI v2.38.5 validated fourteen unique EC2 command examples with offline output skeletons. STS and CloudFront received input-skeleton parsing only because generated output placeholders failed model constraints; see the [inspection lab evidence](network-inspection-lab.md#evidence-and-operating-boundary). No AWS account calls or network provisioning were executed. Record actual resources, permissions, observations, and cleanup before treating a sandbox walkthrough as runtime evidence.

- [AWS VPC composition with Crossplane](../../../kubernetes/crossplane/aws-vpc-platform-api.md)
- [Kubernetes on AWS](../../../cross-topic-guides/kubernetes-on-aws.md)
- [Back to AWS](../index.md)
- [Back to knowledge bundle](../../../index.md)
