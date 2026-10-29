---
type: Explanation
title: VPC endpoints and private DNS
description: Distinguish gateway and interface endpoints and diagnose network, DNS,
  and authorization requirements for private AWS API access.
tags:
- aws
- networking
- privatelink
- endpoints
- dns
status: draft
maturity: draft
audience: Cloud and platform engineering learners
maintainer: unassigned
sources:
- id: gateway-endpoints
  title: Gateway endpoints
  resource: https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html
- id: private-link
  title: What is AWS PrivateLink
  resource: https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html
- id: interface-endpoints
  title: Access AWS services through AWS PrivateLink
  resource: https://docs.aws.amazon.com/vpc/latest/privatelink/privatelink-access-aws-services.html
- id: interface-prerequisites
  title: Create an interface endpoint
  resource: https://docs.aws.amazon.com/vpc/latest/privatelink/create-interface-endpoint.html
- id: dns-attributes
  title: View and update VPC DNS attributes
  resource: https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns-updating.html
---

# VPC endpoints and private DNS

A VPC endpoint gives a specific service or resource a private access path. It does not make all AWS services reachable and does not grant the caller permission. Start by naming the dependency, API hostname, Region, client network, and intended authorization boundary.

## Gateway versus interface endpoints

| Aspect | Gateway endpoint | Interface endpoint for an AWS service |
| --- | --- | --- |
| Path | Route-table destination using an AWS service prefix list | Endpoint ENIs with private addresses reached through the network. |
| Typical scope here | S3 and DynamoDB | Supported AWS services, checked per service/Region. |
| PrivateLink | Does not use PrivateLink | Uses PrivateLink. |
| Filtering | Route association, endpoint policy, caller/resource policy, applicable network controls | Endpoint security group, applicable network controls, endpoint policy where supported, caller/resource policy. |
| Cost model | No additional gateway-endpoint charge | Provisioned endpoint hours per AZ plus data processing. |

Gateway endpoints add service routes to selected route tables; subnets using other route tables do not automatically benefit. They are not a transitive access mechanism for every peered or on-premises client.[^gateway-endpoints] PrivateLink also has resource and service-network endpoint types; this introductory path focuses on gateway and interface endpoints rather than treating those two as an exhaustive catalog.[^private-link]

## Understand the DNS path

With private DNS enabled for a supported interface endpoint, ordinary service names can resolve to its private ENI addresses in the VPC. This allows an SDK to keep its usual service hostname while using the private path.[^interface-endpoints] That is separate from a gateway endpoint's route-based path; an S3 public-looking DNS answer alone does not prove NAT is used.

Interface private DNS requires the appropriate VPC DNS resolution and hostname settings. Its ENI security group must admit the client's service traffic, commonly HTTPS; ACLs and client egress must also allow the flow.[^interface-prerequisites] Custom or hybrid DNS requires a deliberate forwarding design; do not assume an on-premises resolver can use a VPC-only DNS view automatically.

## Read the installed configuration

```bash
aws ec2 describe-vpc-endpoints --filters Name=vpc-id,Values=<vpc-id> --profile <profile> --region <region> --no-cli-pager
aws ec2 describe-vpc-attribute --vpc-id <vpc-id> --attribute enableDnsSupport --profile <profile> --region <region> --no-cli-pager
aws ec2 describe-vpc-attribute --vpc-id <vpc-id> --attribute enableDnsHostnames --profile <profile> --region <region> --no-cli-pager
```

What it does: shows endpoint type/state, service name, DNS entries, policy, route-table or ENI relationships, and both VPC DNS attributes.[^dns-attributes] Inspect the relevant endpoint's actual ENIs and security groups. Treat the returned policy and identifiers as internal configuration.

## Diagnose by layer

| Symptom | Check |
| --- | --- |
| Name resolves publicly unexpectedly | Private DNS setting, VPC attributes, client's resolver/forwarding, exact regional hostname. |
| Name resolves privately; TCP times out | Endpoint state, client route, ENI security group, ACL, client egress. |
| API responds with access denied | Actual caller, IAM/resource/endpoint policies, organization controls, and service-specific conditions. |
| Works in one subnet only | Gateway route-table association or interface ENI/network path differences. |
| Image pull still fails in a private EKS cluster | All required registry/storage/API dependencies and the image-pulling identity, not only one endpoint. |

A private network path is not identity proof. For EKS-to-S3 access, connect this model to [IRSA trust and permissions](../security/irsa-trust-and-permissions.md). Conditions restricting requests to endpoint IDs require lockout-aware planning; changing them is not a generic connectivity repair.

The inspection commands require no cloud cleanup. In a separate sandbox, remove task-owned endpoints only after migrating their consumers and associated policies; deleting an endpoint can remove the only remaining API path. Recheck DNS and the selected route after cleanup.

## Evidence and operating boundary

Official sources reviewed on 2026-10-29. AWS services evolve independently of the CLI. AWS CLI v2.38.5 validated the EC2 command examples using offline output skeletons. Those checks cover command inputs and the sample query, not account permissions, resource state, DNS, or packet delivery. No AWS account calls or infrastructure provisioning were executed for this revision. Replace angle-bracket placeholders before use, confirm account/Region, and keep network inventories private.

## Related routes

- [Read-only inspection lab](network-inspection-lab.md).
- [Connectivity troubleshooting](network-connectivity-troubleshooting.md).
- [Back to AWS networking](index.md)
- [Back to AWS](../index.md)

[^gateway-endpoints]: [Gateway endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html)
[^private-link]: [What is AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
[^interface-endpoints]: [Access AWS services through AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/privatelink-access-aws-services.html)
[^interface-prerequisites]: [Create an interface endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/create-interface-endpoint.html)
[^dns-attributes]: [View and update VPC DNS attributes](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns-updating.html)
