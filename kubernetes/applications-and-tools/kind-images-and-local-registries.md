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

## How it works

`kind` creates Docker containers that behave like Kubernetes nodes. Each node has its own container runtime image store. Kubernetes pulls images from a registry unless the image already exists on the node and the pull policy allows reuse.

```text
docker build on host
  -> host image cache
  -> kind load copies image into node containers
  -> Pod starts with imagePullPolicy: IfNotPresent or Never
```

For repeated development, a local registry can be faster because the nodes pull from a registry endpoint instead of receiving copied images one at a time.

## Components

| Component | What it does |
| --- | --- |
| Host Docker daemon | Builds and stores local images. |
| kind node container | Runs a Kubernetes node and has a separate image store. |
| Image tag | Name Kubernetes uses when resolving the image. |
| `imagePullPolicy` | Controls whether Kubernetes pulls or reuses a local image. |
| Local registry | Registry reachable by both host and cluster nodes. |
| Pull Secret | Kubernetes credential for private registry access. |

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

### Verify the image is visible

```bash
docker exec platform-lab-control-plane crictl images | grep orders-api
```

What it does: checks the node container's image store rather than only the host Docker image cache.

### Local registry workflow

```bash
docker tag orders-api:dev localhost:5001/orders-api:dev
docker push localhost:5001/orders-api:dev
```

What it does: pushes a development image to a local registry that a correctly configured `kind` cluster can pull from.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `ImagePullBackOff` for local image | Cluster name, tag, and `imagePullPolicy`. |
| Node cannot pull private image | Node credentials or side-load workflow. |
| Image works in one cluster only | Image was loaded into only one named cluster. |
| App runs old code | Tag reuse and local image cache. |
| CI cannot access registry | Network path and registry certificate trust. |

## Lab checklist

- Name the cluster explicitly.
- Build the image with a clear local tag.
- Load the image into the intended cluster or push it to the local registry.
- Set `imagePullPolicy` intentionally.
- Confirm the Pod spec uses the same tag that was loaded or pushed.
- Inspect the node image store when troubleshooting.
- Delete and recreate Pods after changing image availability.

## Related links

- Official documentation: [kind quick start image loading](https://kind.sigs.k8s.io/docs/user/quick-start/)
- Official documentation: [kind local registry](https://kind.sigs.k8s.io/docs/user/local-registry/)
- Official documentation: [kind private registries](https://kind.sigs.k8s.io/docs/user/private-registries/)
- [kind custom clusters](kind-custom-clusters.md)
- [Tooling cluster architecture](tooling-cluster-architecture.md)
- [Back to Kubernetes applications and tools](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
