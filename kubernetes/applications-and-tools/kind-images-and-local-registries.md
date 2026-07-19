# kind images and local registries

## Purpose

Use this guide when a local `kind` cluster cannot pull or see images that were built on the host machine.

## Mental model

`kind` runs Kubernetes nodes as containers. Building an image on the host does not automatically make that image available inside those node containers.

```text
Host Docker image cache
  !=
kind node container image store
```

## Options

| Option | Use when | Notes |
| --- | --- | --- |
| `kind load docker-image` | One-off local lab image. | Load the image into the target cluster nodes. |
| `kind load image-archive` | Image is saved as a tar archive. | Useful for offline or CI workflows. |
| Local registry | Many images or repeated builds. | Configure the cluster to pull from the local registry. |
| Private registry | Testing real registry auth behavior. | Configure credentials for nodes or pull to host and side-load. |

### Load an image

```bash
docker build -t orders-api:dev .
kind load docker-image orders-api:dev --name platform-lab
```

What it does: builds an image on the host and copies it into the named `kind` cluster.

> [!IMPORTANT]
> Include `--name` when the cluster is not named `kind`. Loading into the wrong cluster is a common reason Pods still report image pull errors.

### Use the loaded image in a Pod

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-api
spec:
  replicas: 1
  selector:
    matchLabels:
      app: orders-api
  template:
    metadata:
      labels:
        app: orders-api
    spec:
      containers:
        - name: orders-api
          image: orders-api:dev
          imagePullPolicy: IfNotPresent
```

What it does: keeps Kubernetes from trying to pull a local development image from a public registry when it already exists in the node image store.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `ImagePullBackOff` for local image | Cluster name, tag, and `imagePullPolicy`. |
| Node cannot pull private image | Node credentials or side-load workflow. |
| Image works in one cluster only | Image was loaded into only one named cluster. |
| App runs old code | Tag reuse and local image cache. |
| CI cannot access registry | Network path and registry certificate trust. |

## Related links

- Official documentation: [kind quick start image loading](https://kind.sigs.k8s.io/docs/user/quick-start/)
- Official documentation: [kind local registry](https://kind.sigs.k8s.io/docs/user/local-registry/)
- Official documentation: [kind private registries](https://kind.sigs.k8s.io/docs/user/private-registries/)
- [kind custom clusters](kind-custom-clusters.md)
- [Tooling cluster architecture](tooling-cluster-architecture.md)
- [Back to Kubernetes applications and tools](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
