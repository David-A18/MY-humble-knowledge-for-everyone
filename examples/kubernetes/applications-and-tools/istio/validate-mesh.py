"""Verify sidecar policy behavior in a new kind cluster with a private kubeconfig."""

import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import uuid

EXAMPLES = Path(__file__).resolve().parent


def run(*args, stdin=None, codes=(0,), timeout=180):
    result = subprocess.run(args, input=stdin, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=timeout)
    if result.returncode not in codes:
        raise RuntimeError(f"{args[0]} {args[1]} exited {result.returncode}\n{result.stderr}")
    return result


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    versions = json.loads((EXAMPLES / "lab-versions.json").read_text(encoding="utf-8"))
    tools = {tool["name"]: tool["version"] for tool in versions["tools"]}
    cluster = "kb-istio-" + uuid.uuid4().hex[:10]
    context = "kind-" + cluster
    report = {"cluster": cluster, "node_image": versions["node_image"], "checks": {}}
    jwt_spec = importlib.util.spec_from_file_location("jwt_lab", EXAMPLES / "jwt-lab.py")
    jwt_lab = importlib.util.module_from_spec(jwt_spec)
    sys.dont_write_bytecode = True
    jwt_spec.loader.exec_module(jwt_lab)
    with tempfile.TemporaryDirectory(prefix="kb-istio-") as directory:
        kubeconfig = str(Path(directory) / "kubeconfig")
        created = False

        def kube(*command, **kwargs):
            return run("kubectl", "--kubeconfig", kubeconfig, "--context", context, *command, **kwargs)

        def probe(pod, token=None, namespace="istio-lab"):
            config = "" if token is None else f'header = "Authorization: Bearer {token}"\n'
            result = kube("exec", "-i", "-n", namespace, pod, "-c", "client", "--",
                          "curl", "-sS", "--noproxy", "*", "--connect-timeout", "3", "--max-time", "5",
                          "-o", "/dev/null", "-w", "%{http_code}", "-K", "-",
                          "http://web.istio-lab.svc.cluster.local/",
                          stdin=config, codes=(0, 1, 7, 28, 52, 55, 56), timeout=20)
            if result.returncode == 0:
                return result.stdout.strip()
            if result.stdout.strip() == "000" and result.returncode in (52, 55, 56) and "curl:" in result.stderr:
                return "transport-rejected"
            return f"request-error-{result.returncode}"

        def verify(name, cases):
            deadline = time.monotonic() + 60
            while time.monotonic() < deadline:
                actual = [probe(*case[:-1]) for case in cases]
                if actual == [case[-1] for case in cases]:
                    report["checks"][name] = actual
                    return
                time.sleep(2)
            raise RuntimeError(f"{name} expected {[case[-1] for case in cases]}, observed {actual}")

        def apply(policy):
            kube("apply", "-f", "-", stdin=json.dumps(policy))

        try:
            require(cluster not in run("kind", "get", "clusters").stdout.split(), "Cluster already exists")
            require(tools["kind"] in run("kind", "version").stdout, "Unexpected kind version")
            client = json.loads(run("kubectl", "version", "--client", "-o", "json").stdout)
            require(client["clientVersion"]["gitVersion"] == tools["kubectl"], "Unexpected kubectl version")
            istioctl = json.loads(run("istioctl", "version", "--remote=false", "-o", "json").stdout)
            actual_istio = istioctl["clientVersion"]["version"]
            require(actual_istio == tools["istioctl"], f"Unexpected istioctl version: {actual_istio}")
            created = True
            run("kind", "create", "cluster", "--name", cluster, "--kubeconfig", kubeconfig,
                "--image", versions["node_image"], "--wait", "120s", timeout=360)
            server = json.loads(kube("version", "-o", "json").stdout)["serverVersion"]["gitVersion"]
            require(server == versions["kubernetes"], "Unexpected Kubernetes version")
            report["versions"] = dict(tools, kubernetes=server, python=sys.version.split()[0],
                                      docker=run("docker", "version", "--format", "{{.Server.Version}}").stdout.strip())
            print("Created", cluster, flush=True)
            run("istioctl", "--kubeconfig", kubeconfig, "--context", context,
                "install", "--set", "profile=minimal", "-y", timeout=360)
            kube("create", "namespace", "istio-lab")
            kube("create", "namespace", "plaintext-lab")
            kube("label", "namespace", "istio-lab", "istio-injection=enabled")
            kube("label", "namespace", "plaintext-lab", "istio-injection=disabled")
            kube("apply", "-n", "istio-lab", "-f", str(EXAMPLES / "workloads.yaml"))
            client_pod = json.loads(kube("get", "pod", "allowed", "-n", "istio-lab", "-o", "json").stdout)
            image = next(container["image"] for container in client_pod["spec"]["containers"]
                         if container["name"] == "client")
            plain = {"apiVersion": "v1", "kind": "Pod", "metadata": {"name": "plain", "namespace": "plaintext-lab"},
                     "spec": {"containers": [{"name": "client", "image": image, "command": ["sleep", "3600"]}]}}
            apply(plain)
            kube("rollout", "status", "deployment/web", "-n", "istio-lab", "--timeout=180s")
            kube("wait", "pod", "--all", "-n", "istio-lab", "--for=condition=Ready", "--timeout=180s")
            kube("wait", "pod/plain", "-n", "plaintext-lab", "--for=condition=Ready", "--timeout=180s")
            for namespace, expected in (("istio-lab", True), ("plaintext-lab", False)):
                pods = json.loads(kube("get", "pods", "-n", namespace, "-o", "json").stdout)["items"]
                require(bool(pods), f"No pods in {namespace}")
                for pod in pods:
                    containers = pod["spec"]["containers"] + pod["spec"].get("initContainers", [])
                    require(any(c["name"] == "istio-proxy" for c in containers) == expected,
                            f"Unexpected injection in {namespace}")
            report["checks"]["expected_sidecar_enrollment"] = True
            verify("baseline", [("allowed", None, "200"), ("denied", None, "200"),
                                ("plain", None, "plaintext-lab", "200")])
            token, _ = jwt_lab.generate(directory)
            policies = json.loads((Path(directory) / "policies.json").read_text(encoding="utf-8"))["items"]
            strict, authentication, authorization = policies
            apply(strict)
            verify("strict_mtls", [("allowed", None, "200"), ("plain", None, "plaintext-lab", "transport-rejected")])
            apply(authentication)
            verify("request_authentication", [("allowed", token, "200"), ("allowed", None, "200"),
                                              ("allowed", "invalid", "401")])
            apply(authorization)
            verify("combined_authorization", [("allowed", token, "200"), ("denied", token, "403"),
                                               ("allowed", None, "403"), ("allowed", "invalid", "401")])
            kube("delete", "namespace", "istio-lab", "plaintext-lab", "--timeout=120s")
            require(not kube("get", "namespace", "istio-lab", "plaintext-lab",
                             "--ignore-not-found", "-o", "name").stdout.strip(), "Namespaces remain")
            report["checks"]["namespaces_deleted"] = True
        finally:
            try:
                if created:
                    run("kind", "delete", "cluster", "--name", cluster, "--kubeconfig", kubeconfig)
                    require(cluster not in run("kind", "get", "clusters").stdout.split(), "Cluster remains")
                    require(not run("docker", "ps", "-a", "--filter", f"label=io.x-k8s.kind.cluster={cluster}",
                                    "--format", "{{.Names}}").stdout.strip(), "Node containers remain")
                    report["checks"]["cluster_and_nodes_deleted"] = True
            finally:
                output = json.dumps(report, indent=2) + "\n"
                if args.report:
                    args.report.write_text(output, encoding="utf-8")
                print(output, end="")


if __name__ == "__main__":
    main()
