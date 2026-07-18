# kind custom clusters

## Purpose

Use this page to create local Kubernetes clusters with `kind` for development, CI, and platform-tooling labs.

## What kind is

`kind` runs local Kubernetes clusters using container nodes. It is useful for local development, CI tests, controller development, and labs that should not require a cloud cluster.

## Common customizations

| Customization | Use it for |
| --- | --- |
| Multi-node topology | Test scheduling, node labels, and control-plane behavior. |
| Extra port mappings | Expose local ingress or services to the host. |
| Extra mounts | Share local files with cluster nodes. |
| Node image version | Test a specific Kubernetes version. |
| Local registry | Use locally built application images without remote pushes. |

## Example

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
    extraPortMappings:
      - containerPort: 30080
        hostPort: 8080
        protocol: TCP
  - role: worker
```

What it does: creates a two-node local cluster and maps host port `8080` to a node port for local testing.

## Related links

- [kind quick start](https://kind.sigs.k8s.io/docs/user/quick-start/)
- [kind configuration](https://kind.sigs.k8s.io/docs/user/configuration/)
- [kind troubleshooting](../troubleshooting/kind.md)
- [Tooling clusters](tooling-clusters.md)
- [Back to Kubernetes applications and tools](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
