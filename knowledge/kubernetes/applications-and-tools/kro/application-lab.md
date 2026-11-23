---
type: Tutorial
title: Local kro application-composition lab
description: Create and operate a WebApp API that composes a Deployment and Service.
tags:
- kubernetes
- kro
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: pinned-kro-installation-instructions
  resource: https://kro.run/0.9.4/docs/getting-started/Installation/
  title: Pinned kro installation instructions
- id: kro-v0-9-4-examples
  resource: https://github.com/kubernetes-sigs/kro/tree/v0.9.4/examples
  title: kro v0.9.4 examples
- id: kro-readiness
  resource: https://kro.run/0.9.4/docs/concepts/rgd/resource-definitions/readiness/
  title: kro 0.9.4 readiness
- id: kro-access
  resource: https://kro.run/0.9.4/docs/advanced/access-control/
  title: kro 0.9.4 access control
- id: kro-deletion
  resource: https://kro.run/0.9.4/docs/advanced/instance-deletion/
  title: kro 0.9.4 instance deletion
---

# Local kro application-composition lab

Create a small WebApp API that manages a Deployment and Service together. Change the WebApp to scale the application, break and restore its image, and observe how kro repairs or deletes its children.

For example, this instance asks the generated API for two web-server replicas.

~~~yaml
apiVersion: kro.run/v1alpha1
kind: WebApp
metadata:
  name: demo
spec:
  replicas: 2
~~~

What it does: supplies the user-facing input to the ResourceGraphDefinition, or RGD. kro evaluates that definition and reconciles the underlying Deployment and Service. The supplied definition provides the default server image.

## Prepare a disposable cluster

Run all commands below from the repository root. Use Linux amd64, Docker and Python in an isolated environment. The [example files](../../../../examples/kubernetes/applications-and-tools/kro/README.md) include the definition, instance, controller permissions, version pins and runner.

The runner creates a unique kind cluster and private kubeconfig. It installs the checksum-verified raw controller manifest for the selected release. The release manifest grants basic permissions. The supplied aggregated ClusterRole adds access to this lab's WebApp, Deployment and Service types. These permissions apply across namespaces, so use a dedicated cluster. [^pinned-kro-installation-instructions][^kro-access]

~~~bash
python -m pip install PyYAML==6.0.3
tools_dir=$(mktemp -d)
python examples/kubernetes/applications-and-tools/manifest-validation/install-tools.py \
  --directory "$tools_dir" \
  --versions examples/kubernetes/applications-and-tools/kro/lab-versions.json
export PATH="$tools_dir:$PATH"
python examples/kubernetes/applications-and-tools/kro/validate-lab.py
~~~

What it does: installs the pinned kind and kubectl binaries into an empty tools directory, then performs the composition, failure, recovery and cleanup exercise. It prints observed versions and each assertion. An assertion failure fails the command and triggers cluster cleanup.

## Follow definition, instance and children

The runner waits for the controller, the RGD's Ready condition and the generated WebApp CRD before creating an instance. A controller Pod becoming ready is only the first stage.

| Stage | Expected observation |
| --- | --- |
| Register the definition | The RGD becomes ready and the WebApp CRD is established. |
| Create the WebApp | One replica becomes available, the instance becomes ready and its status endpoint matches the Service IP. |
| Send a request | An in-cluster request through Service DNS returns the NGINX page. |
| Supply replicas zero | The generated API rejects the value below the schema minimum. |
| Scale through the instance | The Deployment converges to two updated, available replicas. |
| Delete the Service | kro recreates it with a new UID, updates the endpoint and restores HTTP access. |
| Supply a missing image | A Pod reports image-not-found and the graph loses readiness. |
| Restore the pinned image | Updated replicas, graph readiness and Service HTTP recover. |
| Delete the instance | The managed Deployment and Service disappear before namespace cleanup. |
| Finish | The namespace, kind cluster and its node containers are absent. |

The Service references the Deployment selector through a CEL expression. That reference establishes a dependency. The Deployment's readyWhen expressions check its observed generation, updated replicas and available replicas. Dependent processing waits for those conditions. [^kro-readiness][^kro-v0-9-4-examples]

Without explicit workload readiness expressions, a created resource with resolved references may be considered ready while its application is starting. A readiness predicate also needs to cover updates. Existing available replicas can keep serving while the newly requested image fails.

## Inspect a failed stage

For an interactive session in your own disposable cluster, replace LAB_CONTEXT with its context name.

~~~bash
kubectl --context LAB_CONTEXT get rgd webapp -o yaml
kubectl --context LAB_CONTEXT get webapp demo -n kro-lab -o yaml
kubectl --context LAB_CONTEXT get deployment,service,pod -n kro-lab
kubectl --context LAB_CONTEXT get events -n kro-lab --sort-by=.lastTimestamp
kubectl --context LAB_CONTEXT logs deployment/kro -n kro-system
~~~

What it does: follows definition validation, instance conditions, child health, events and controller diagnostics. The automated runner deletes its private cluster on exit, so inspect its failure report first when using that route.

An API discovery error points to the definition or generated CRD. A forbidden operation points to controller or caller permissions. A registry timeout is a different failure from the deliberately missing image. The runner requires an image-not-found diagnostic before accepting the negative case.

Update the WebApp instance as the input to kro. A second deployment tool managing the same child fields can create ownership conflicts. Keep definition and instance changes versioned so a repair can be reproduced.

## Delete through the parent API

The lab deletes the WebApp and checks that its Deployment and Service disappear while the namespace still exists. This exercises kro's instance cleanup path. Namespace deletion alone removes namespaced resources and provides weaker evidence of parent lifecycle behavior. Keep the controller running while its instances and finalizers are reconciled. [^kro-deletion]

After instance cleanup, the runner deletes the RGD and namespace, then removes the task cluster and checks for remaining labeled node containers. Remove your own tool installation and redirected reports after retaining results.

## Evidence and limits

Sources reviewed on 2026-11-23 against kro 0.9.4 documentation. The fixed teaching baseline uses kind 0.30.0, kubectl 1.34.1, Kubernetes 1.34.0, PyYAML 6.0.3 and the versioned raw controller manifest. The NGINX image uses a content digest. The [recorded pull-request run](https://github.com/David-A18/MY-humble-knowledge-for-everyone/actions/runs/45145546874) passed all eleven runtime assertions on 2026-11-23. Its [report](../../../../examples/kubernetes/applications-and-tools/kro/runtime-evidence.json) records Docker 28.0.4 and Python 3.13.18 alongside the selected tool and controller versions. Subsequent revisions need their own workflow results.

The workflow covers one namespaced local graph. Cloud resources, external references, graph-version migration and multi-tenant permissions require additional scenarios. Review definition-author and controller privileges before adapting this example to a shared platform.

## Related links

- [kro lab files](../../../../examples/kubernetes/applications-and-tools/kro/README.md)
- [Lifecycle diagnosis](lifecycle-and-troubleshooting.md)
- [Back to kro](index.md) | [Back to Kubernetes](../../index.md)

[^pinned-kro-installation-instructions]: [kro 0.9.4 installation](https://kro.run/0.9.4/docs/getting-started/Installation/).
[^kro-v0-9-4-examples]: [kro 0.9.4 examples](https://github.com/kubernetes-sigs/kro/tree/v0.9.4/examples).
[^kro-readiness]: [Readiness and dependency handling](https://kro.run/0.9.4/docs/concepts/rgd/resource-definitions/readiness/).
[^kro-access]: [Controller access modes](https://kro.run/0.9.4/docs/advanced/access-control/).
[^kro-deletion]: [Instance deletion](https://kro.run/0.9.4/docs/advanced/instance-deletion/).
