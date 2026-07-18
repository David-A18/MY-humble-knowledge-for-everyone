# Security groups

## Purpose

Document practical behavior and troubleshooting checks for AWS security groups.

## Key ideas

| Concept | Operational meaning |
| --- | --- |
| Stateful filtering | Return traffic for allowed inbound or outbound traffic is automatically allowed. |
| Attached to elastic network interfaces | Security groups apply to ENIs used by resources such as EC2 instances and load balancers. |
| Rules are allow-only | Security groups do not define explicit deny rules. |

## Troubleshooting checklist

- [ ] Confirm the source and destination IPs, ports, and protocol.
- [ ] Check inbound rules on the destination security group.
- [ ] Check outbound rules on the source security group.
- [ ] Check route tables, network ACLs, and host firewalls if security group rules look correct.
- [ ] Confirm the resource is using the expected security group.

> [!TIP]
> Security groups are only one layer of network access. Route tables, network ACLs, DNS, application listeners, and operating system firewalls can still block traffic.

## Related links

- [AWS security group documentation](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)
- [Back to AWS networking](README.md)
- [Back to AWS index](../README.md)
- [Back to root index](../../../README.md)
