# Kubernetes common solutions

## Purpose

Diagnose frequent Kubernetes workload issues by moving from safe inspection commands to targeted fixes.

## First checks

Run these before changing resources:

```bash
kubectl config current-context
kubectl get pods -n <namespace> -o wide
kubectl get events -n <namespace> --sort-by=.lastTimestamp
kubectl get deploy,rs,sts,ds,job -n <namespace>
```

What it does: confirms the active cluster, shows workload state, reviews recent events, and lists common workload controllers.

## Symptoms and checks

| Symptom | First check | Likely cause |
| --- | --- | --- |
| Pod is `Pending` | `kubectl describe pod <pod> -n <namespace>` | Insufficient resources, node selector, taint, PVC, or quota issue. |
| Pod is `ImagePullBackOff` | `kubectl describe pod <pod> -n <namespace>` | Wrong image, missing tag, private registry auth, or registry outage. |
| Pod is `CrashLoopBackOff` | `kubectl logs <pod> -n <namespace> --previous` | App exits, missing config, failed dependency, or aggressive probe. |
| Service has no endpoints | `kubectl get endpoints,endpointslice -n <namespace>` | Selector mismatch or pods are not Ready. |
| DNS fails from a pod | `kubectl exec <pod> -n <namespace> -- nslookup <service>` | Wrong service name, namespace, CoreDNS, or network policy issue. |
| Rollout is stuck | `kubectl rollout status deployment/<name> -n <namespace>` | New pods failing readiness, image pull, scheduling, or quota. |
| Permission denied | `kubectl auth can-i <verb> <resource> -n <namespace>` | RBAC or EKS access mapping does not allow the action. |

## Pending pods

```bash
kubectl describe pod <pod-name> -n app
kubectl get nodes
kubectl describe node <node-name>
kubectl get resourcequota,limitrange -n app
```

What it does: checks scheduling events, node readiness, node capacity, taints, namespace quotas, and default limits.

Common fixes:

- Reduce or correct CPU and memory requests.
- Add capacity or wait for cluster autoscaling.
- Match node selectors, affinities, and tolerations to available nodes.
- Create or fix the referenced PersistentVolumeClaim.

## ImagePullBackOff

```bash
kubectl describe pod <pod-name> -n app
kubectl get secret -n app
kubectl get pod <pod-name> -n app -o jsonpath='{.spec.imagePullSecrets}{"\n"}'
```

What it does: reads image pull events, lists namespace Secrets, and checks whether the pod references image pull credentials.

Common fixes:

- Correct the registry, repository, or tag.
- Create or reference the correct image pull Secret.
- Confirm the node can reach the registry.
- Confirm the image exists in Amazon ECR or the selected registry.

## CrashLoopBackOff

```bash
kubectl logs <pod-name> -n app --previous
kubectl describe pod <pod-name> -n app
kubectl get configmap,secret -n app
```

What it does: reads logs from the previous crashed container, checks events and probes, and confirms referenced configuration objects exist.

Common fixes:

- Fix missing environment variables, files, or Secret keys.
- Increase startup probe timing for slow-starting applications.
- Correct liveness probe path, port, or initial delay.
- Fix application startup errors or dependency connection strings.

## Service or DNS issue

```bash
kubectl get svc,endpoints,endpointslice -n app
kubectl describe svc web -n app
kubectl get pods -n app --show-labels
kubectl run dns-test --rm -it --restart=Never --image=busybox:1.36 -- nslookup web.app.svc.cluster.local
```

What it does: checks whether the Service selects Ready pods and tests cluster DNS from a temporary pod.

Common fixes:

- Align the Service selector with pod labels.
- Fix readiness probe failures so pods become endpoints.
- Use the full service DNS name across namespaces.
- Review NetworkPolicies that may block traffic.

## Failed rollout

```bash
kubectl rollout status deployment/web -n app
kubectl describe deployment/web -n app
kubectl get rs,pods -n app -l app.kubernetes.io/name=web
kubectl get events -n app --sort-by=.lastTimestamp
```

What it does: checks Deployment progress, ReplicaSets, pods, and recent failures.

### Roll back when needed

```bash
kubectl rollout history deployment/web -n app
kubectl rollout undo deployment/web -n app
kubectl rollout status deployment/web -n app
```

What it does: reviews rollout revisions, reverts to the previous revision, and waits for the rollback.

> [!WARNING]
> Rollback changes live workload behavior. Capture the failing revision, image, and error before rollback when incident time allows.

## Permission errors in EKS

```bash
aws sts get-caller-identity
kubectl auth can-i get pods -n app
kubectl auth can-i update deployments -n app
```

What it does: confirms the AWS identity used for EKS authentication and asks Kubernetes whether that identity has the needed permissions.

Common fixes:

- Use the correct AWS profile or assumed role.
- Update EKS access entries or Kubernetes RBAC bindings.
- Confirm kubeconfig points to the intended EKS cluster.
- Check whether the namespace is correct.

> [!IMPORTANT]
> EKS authentication and Kubernetes authorization are separate layers. Passing AWS authentication does not automatically grant in-cluster permissions.

## Official documentation

- [Debug pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/)
- [Debug services](https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/)
- [Pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
- [Configure liveness, readiness, and startup probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [Amazon EKS access entries](https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html)

## Related links

- [CrashLoopBackOff](crashloopbackoff.md)
- [Back to Kubernetes troubleshooting](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
