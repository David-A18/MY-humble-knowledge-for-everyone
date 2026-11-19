"""Run deploy/failure/recovery checks in a new task-owned kind cluster."""

from pathlib import Path
import argparse
import json
import re
import subprocess
import tempfile
import time
import urllib.request
import uuid

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--report", type=Path, help="Optional synthetic runtime report; never includes kubeconfig")
args = parser.parse_args()
source = Path(__file__).resolve().parent
versions = json.loads((source / "lab-versions.json").read_text(encoding="utf-8"))
cluster = "kb-journey-" + uuid.uuid4().hex[:10]
context = "kind-" + cluster
namespace = "kb-learning"
selector = "app.kubernetes.io/name=kb-web"
report = {"cluster": cluster, "checks": {}, "status": "running"}


def run(*command, codes=(0,), timeout=240):
    result = subprocess.run(list(command), capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    if result.returncode not in codes:
        raise RuntimeError("Command failed: " + " ".join(command) + "\n" + result.stdout + result.stderr)
    return result


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


with tempfile.TemporaryDirectory(prefix="kb-kind-learning-") as temporary:
    work = Path(temporary).resolve()
    require(work.is_relative_to(Path(tempfile.gettempdir()).resolve()), "Temporary directory escaped intended root")
    kubeconfig = work / "kubeconfig"
    created = False

    def kubectl(*command, **options):
        return run("kubectl", "--kubeconfig", str(kubeconfig), "--context", context, *command, **options)

    def pods():
        return json.loads(kubectl("get", "pods", "-n", namespace, "-l", selector, "-o", "json").stdout)["items"]

    def ready(pod):
        return not pod["metadata"].get("deletionTimestamp") and any(c["type"] == "Ready" and c["status"] == "True" for c in pod.get("status", {}).get("conditions", []))

    def verify_service():
        current = [p for p in pods() if ready(p)]
        require(len(current) == 2, "Expected exactly two ready workload Pods")
        slices = json.loads(kubectl("get", "endpointslices", "-n", namespace, "-l", "kubernetes.io/service-name=kb-web", "-o", "json").stdout)["items"]
        targets = {e["targetRef"]["name"] for s in slices for e in s.get("endpoints", []) if e.get("conditions", {}).get("ready") is True}
        require(targets == {p["metadata"]["name"] for p in current}, "Ready EndpointSlices must match both workload Pods")
        body = kubectl("exec", "-n", namespace, current[0]["metadata"]["name"], "--", "wget", "-q", "-O", "-", "http://kb-web.kb-learning.svc.cluster.local/").stdout
        require("Welcome to nginx!" in body, "Cluster DNS/Service HTTP request did not return the teaching page")
        return current

    try:
        report["docker"] = json.loads(run("docker", "version", "--format", "{{json .Server}}").stdout)["Version"]
        report["kind"] = run("kind", "version").stdout.strip()
        client = json.loads(run("kubectl", "version", "--client", "-o", "json").stdout)
        report["kubectl"] = client["clientVersion"]["gitVersion"]
        require(versions["kind"] in report["kind"] and report["kubectl"] == versions["kubectl"], "Installed tools differ from the teaching version contract")
        require(cluster not in run("kind", "get", "clusters").stdout.split(), "Refusing to reuse an existing cluster")
        created = True
        run("kind", "create", "cluster", "--name", cluster, "--kubeconfig", str(kubeconfig), "--image", versions["node_image"], "--wait", "120s", timeout=360)
        kubectl("wait", "--for=condition=Ready", "node", "--all", "--timeout=120s")
        report["kubernetes"] = json.loads(kubectl("version", "-o", "json").stdout)["serverVersion"]["gitVersion"]
        report["node_image"] = versions["node_image"]
        for name in ("namespace.yaml", "deployment.yaml", "service.yaml"):
            kubectl("apply", "-f", str(source / name))
        kubectl("rollout", "status", "deployment/kb-web", "-n", namespace, "--timeout=180s")
        original = json.loads(kubectl("get", "deployment", "kb-web", "-n", namespace, "-o", "json").stdout)
        expected_image = original["spec"]["template"]["spec"]["containers"][0]["image"]
        require("@sha256:" in expected_image, "Teaching workload image must use a content digest")
        report["workload_image"] = expected_image
        verify_service()
        report["checks"]["two_ready_endpoints_and_cluster_service_http"] = True

        # A Service port-forward selects a Pod; test it separately from ClusterIP/DNS.
        forward_log = work / "port-forward.log"
        with forward_log.open("w", encoding="utf-8") as output:
            process = subprocess.Popen(["kubectl", "--kubeconfig", str(kubeconfig), "--context", context, "port-forward", "service/kb-web", ":80", "-n", namespace, "--address=127.0.0.1"], stdout=output, stderr=subprocess.STDOUT, text=True)
            try:
                deadline = time.monotonic() + 30
                match = None
                while time.monotonic() < deadline:
                    match = re.search(r"Forwarding from 127\.0\.0\.1:(\d+)", forward_log.read_text(encoding="utf-8"))
                    if match:
                        break
                    require(process.poll() is None, "Port-forward process exited before binding")
                    time.sleep(0.2)
                require(match is not None, "Port-forward did not bind a local port")
                opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
                with opener.open("http://127.0.0.1:" + match[1], timeout=10) as response:
                    require(response.status == 200 and b"Welcome to nginx!" in response.read(), "Port-forward HTTP failed")
                report["checks"]["pod_port_forward_http"] = True
            finally:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=10)

        kubectl("patch", "deployment", "kb-web", "-n", namespace, "--type=strategic", "--patch-file", str(source / "failing-image-patch.yaml"))
        deadline = time.monotonic() + 120
        not_found = False
        while time.monotonic() < deadline:
            for pod in pods():
                for container in pod.get("status", {}).get("containerStatuses", []):
                    waiting = container.get("state", {}).get("waiting", {})
                    message = waiting.get("message", "").lower()
                    if waiting.get("reason") in ("ErrImagePull", "ImagePullBackOff") and any(term in message for term in ("not found", "notfound", "manifest unknown")):
                        not_found = True
            if not_found:
                break
            time.sleep(3)
        require(not_found, "Expected registry image-not-found evidence; timeout/DNS/rate-limit alone is not the intended failure")
        kubectl("rollout", "status", "deployment/kb-web", "-n", namespace, "--timeout=20s", codes=(1,))
        verify_service()
        report["checks"]["image_not_found_and_failed_rollout_with_old_pods_serving"] = True
        kubectl("rollout", "undo", "deployment/kb-web", "-n", namespace)
        kubectl("rollout", "status", "deployment/kb-web", "-n", namespace, "--timeout=120s")
        recovered = json.loads(kubectl("get", "deployment", "kb-web", "-n", namespace, "-o", "json").stdout)
        require(recovered["spec"]["template"]["spec"]["containers"][0]["image"] == expected_image, "Rollback did not restore the pinned image")
        verify_service()
        report["checks"]["rollback_restores_image_endpoints_and_http"] = True
        kubectl("delete", "namespace", namespace, "--wait=true", "--timeout=120s")
        require(not kubectl("get", "namespace", namespace, "--ignore-not-found", "-o", "name").stdout.strip(), "Namespace remained after cleanup")
        report["checks"]["namespace_deleted"] = True
    except Exception as error:
        report["error"] = str(error)
        if kubeconfig.exists():
            for command in (("get", "pods", "-n", namespace, "-o", "wide"), ("get", "events", "-n", namespace, "--sort-by=.lastTimestamp")):
                diagnostic = kubectl(*command, codes=(0, 1))
                print(diagnostic.stdout + diagnostic.stderr)
        raise
    finally:
        if created:
            run("kind", "delete", "cluster", "--name", cluster, "--kubeconfig", str(kubeconfig))
            require(cluster not in run("kind", "get", "clusters").stdout.split(), "Task cluster remained in kind inventory")
            remaining = run("docker", "ps", "-a", "--filter", "label=io.x-k8s.kind.cluster=" + cluster, "--format", "{{.Names}}").stdout.strip()
            require(not remaining, "Task-owned node containers remained after deletion")
            report["checks"]["cluster_and_node_containers_deleted"] = True
        report["status"] = "failed" if "error" in report else "passed"
        if args.report:
            args.report.resolve().write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2))
