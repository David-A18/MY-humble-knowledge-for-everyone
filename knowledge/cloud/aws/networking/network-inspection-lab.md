---
type: Tutorial
title: Read-only VPC inspection lab
description: Build an evidence map of an existing authorized VPC and explain one dependency
  path without provisioning or changing its resources.
tags:
- aws
- networking
- lab
- aws-cli
status: draft
maturity: draft
audience: Cloud and platform engineering learners
maintainer: unassigned
sources:
- id: vpc-model
  title: How Amazon VPC works
  resource: https://docs.aws.amazon.com/vpc/latest/userguide/how-it-works.html
- id: route-tables
  title: Subnet route tables
  resource: https://docs.aws.amazon.com/vpc/latest/userguide/subnet-route-tables.html
- id: dns-attributes
  title: View and update VPC DNS attributes
  resource: https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns-updating.html
- id: sts-identity
  title: AWS CLI get-caller-identity
  resource: https://docs.aws.amazon.com/cli/latest/reference/sts/get-caller-identity.html
---

# Read-only VPC inspection lab

Complete this lab to explain an existing workload's network path. The outcome is a private evidence worksheet, not a new VPC. Use an existing sandbox VPC whose owner permits read-only inspection. This revision validates command syntax offline; account-backed results must be recorded when you perform the lab.

## Prerequisites and safety boundary

Use AWS CLI v2, an authenticated named profile, the intended account/Region, and permission for the relevant EC2 describe operations. STS caller-identity confirmation requires valid authentication but no explicit allow for that action.[^sts-identity] The author checked examples with CLI v2.38.5. Do not print credentials or attach full inventories to public issues. No commands here create gateways, capture logs, launch instances, or change IAM.

The commands below use Bash variable assignments. In PowerShell, set equivalent `$KB_PROFILE`, `$KB_REGION`, and other variables using PowerShell syntax. Replace illustrative resource IDs with your own authorized resources.

```bash
KB_PROFILE=kb-sandbox-readonly
KB_REGION=eu-west-1
KB_VPC=vpc-0123456789abcdef0
KB_SUBNET=subnet-0123456789abcdef0
aws --version
aws sts get-caller-identity --profile "$KB_PROFILE" --region "$KB_REGION" --no-cli-pager
```

What it does: selects the lab inputs and displays the active AWS principal. Compare the account with the approved sandbox before continuing. Stop on an unexpected account; changing a Region does not change account identity.

## 1. Map placement and address space

```bash
aws ec2 describe-vpcs --vpc-ids "$KB_VPC" --profile "$KB_PROFILE" --region "$KB_REGION" --no-cli-pager
aws ec2 describe-subnets --filters "Name=vpc-id,Values=$KB_VPC" --profile "$KB_PROFILE" --region "$KB_REGION" --no-cli-pager
```

What it does: reads the network boundary and subnet placement.[^vpc-model] Record the workload subnet, AZ, address family, and available IPv4 capacity. Expected result: your selected subnet belongs to the selected VPC. If absent, recheck IDs, permissions, account, and Region rather than creating replacements.

## 2. Find the route table actually in use

```bash
aws ec2 describe-route-tables --filters "Name=association.subnet-id,Values=$KB_SUBNET" --profile "$KB_PROFILE" --region "$KB_REGION" --no-cli-pager
aws ec2 describe-route-tables --filters "Name=vpc-id,Values=$KB_VPC" Name=association.main,Values=true --profile "$KB_PROFILE" --region "$KB_REGION" --no-cli-pager
```

What it does: identifies an explicit subnet association and the main-table fallback.[^route-tables] Expected result: exactly one effective subnet table. An empty explicit-association query can be normal. Choose one approved dependency hostname, resolve it from the workload's network, and write down the matched destination route and return-path owner. Do not probe documentation IP examples.

## 3. Explain egress and private dependencies

```bash
aws ec2 describe-nat-gateways --filter "Name=vpc-id,Values=$KB_VPC" --profile "$KB_PROFILE" --region "$KB_REGION" --no-cli-pager
aws ec2 describe-vpc-endpoints --filters "Name=vpc-id,Values=$KB_VPC" --profile "$KB_PROFILE" --region "$KB_REGION" --no-cli-pager
aws ec2 describe-vpc-attribute --vpc-id "$KB_VPC" --attribute enableDnsSupport --profile "$KB_PROFILE" --region "$KB_REGION" --no-cli-pager
aws ec2 describe-vpc-attribute --vpc-id "$KB_VPC" --attribute enableDnsHostnames --profile "$KB_PROFILE" --region "$KB_REGION" --no-cli-pager
```

What it does: inventories NATs, endpoints, and DNS settings without adding them.[^dns-attributes] Expected result: an explained path for the chosen dependency, not necessarily a NAT or endpoint in every VPC. Identify gateway-route versus interface-ENI access, or document that no suitable path exists. Use the focused guides to interpret the fields instead of inferring reachability from `available` state alone.

## 4. Inspect the workload boundary

Use the actual source ENI and its attached groups, rather than every group in the account.

```bash
aws ec2 describe-network-interfaces --network-interface-ids <eni-id> --profile "$KB_PROFILE" --region "$KB_REGION" --no-cli-pager
aws ec2 describe-security-group-rules --filters Name=group-id,Values=<security-group-id> --profile "$KB_PROFILE" --region "$KB_REGION" --no-cli-pager
aws ec2 describe-network-acls --filters "Name=association.subnet-id,Values=$KB_SUBNET" --profile "$KB_PROFILE" --region "$KB_REGION" --no-cli-pager
```

What it does: connects the workload's network identity to its attached security groups and effective subnet ACL. Expected result: a plausible forward/reply policy for the chosen protocol/port. If permissions are denied, request narrowly scoped read access; do not broaden the resource's own network rules to fix an inspection-role problem.

## Completion, failure analysis, and cleanup

Your worksheet should answer: who/where is the client, what does the name resolve to there, which route/target wins, how does the reply return, which network controls apply, and which application/IAM checks remain? State any missing evidence. A worksheet is configuration evidence; label a permitted real application test separately if you run one with the owner's authorization.

For a paper failure exercise, explain what would change if the subnet's explicit route association were absent, a more-specific destination selected a different target, or an endpoint security group rejected HTTPS. Do not introduce those failures into a live account for this read-only lab.

No cloud resources were created, so there is no infrastructure to destroy. Close temporary access sessions and remove only lab-owned local output files after retaining the redacted worksheet as appropriate. Never delete the inspected VPC, shared endpoints, or groups as lab cleanup.

## Evidence and operating boundary

Official sources reviewed on 2026-10-29. AWS services evolve independently of the CLI. Section checks covered 26 command occurrences: fourteen unique EC2 commands passed offline output-skeleton validation. The STS and CloudFront examples passed input-skeleton parsing only; generated output placeholders failed ARN-length and origin-group-list constraints in CLI v2.38.5. Named profiles were omitted from offline checks; authentication and account permissions were not exercised. No AWS account calls or infrastructure provisioning were executed for this revision. Replace angle-bracket placeholders before use, confirm account/Region, and keep network inventories private.

## Related routes

- [VPC fundamentals](vpc-and-subnet-fundamentals.md).
- [Network troubleshooting](network-connectivity-troubleshooting.md).
- [Back to AWS networking](index.md)
- [Back to AWS](../index.md)

[^vpc-model]: [How Amazon VPC works](https://docs.aws.amazon.com/vpc/latest/userguide/how-it-works.html)
[^route-tables]: [Subnet route tables](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-route-tables.html)
[^dns-attributes]: [View and update VPC DNS attributes](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns-updating.html)

[^sts-identity]: [AWS CLI get-caller-identity](https://docs.aws.amazon.com/cli/latest/reference/sts/get-caller-identity.html)
