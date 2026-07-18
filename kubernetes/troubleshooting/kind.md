# kind troubleshooting

## Purpose

Diagnose common local Kubernetes problems when using `kind`.

## Common issues

| Symptom | Check | Likely cause |
| --- | --- | --- |
| Docker permission denied | Docker or container runtime access. | User cannot access the runtime socket. |
| `kubectl` points elsewhere | Current context. | Kubeconfig is not using the kind cluster. |
| ImagePullBackOff for local image | Whether the image was loaded into kind. | Local Docker image is not inside node containers. |
| Host port unavailable | Port mappings and host listeners. | Another process already owns the port. |
| Pods remain Pending | Node resources, selectors, taints, and PVCs. | Local cluster capacity or scheduling mismatch. |

## Useful commands

```bash
kind get clusters
kubectl config current-context
kind load docker-image <image>:<tag> --name <cluster>
kubectl get pods -A -o wide
```

What it does: confirms the active kind cluster, context, local image availability, and pod placement.

## Related links

- [kind custom clusters](../applications-and-tools/kind-custom-clusters.md)
- [kind documentation](https://kind.sigs.k8s.io/docs/)
- [Back to Kubernetes troubleshooting](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
