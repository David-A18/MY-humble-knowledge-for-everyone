"""Exercise real API diff and Service regression checks in a new private kind cluster."""

from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run(*command, codes=(0,), timeout=180, env=None):
    result = subprocess.run(list(command), capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout, env=env)
    require(result.returncode in codes, "Command failed: " + " ".join(command) + "\n" + result.stdout + result.stderr)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    versions = json.loads((HERE / "lab-versions.json").read_text(encoding="utf-8"))
    cluster = "kb-manifest-" + uuid.uuid4().hex[:10]
    context = "kind-" + cluster
    namespace = "manifest-lab"
    report = {"cluster": cluster, "checks": {}, "versions": {}, "status": "running"}
    with tempfile.TemporaryDirectory(prefix="kb-manifest-cluster-") as directory:
        temporary = Path(directory).resolve()
        require(temporary.is_relative_to(Path(tempfile.gettempdir()).resolve()), "Temporary directory escaped its root")
        kubeconfig = temporary / "kubeconfig"
        child_env = dict(os.environ, KUBECONFIG=str(kubeconfig))
        child_env.pop("KUBECTL_EXTERNAL_DIFF", None)
        created = False

        def kubectl(*command, **options):
            options.setdefault("env", child_env)
            return run("kubectl", "--kubeconfig", str(kubeconfig), "--context", context, *command, **options)

        def endpoint_ports():
            slices = json.loads(kubectl("get", "endpointslices", "-n", namespace, "-l", "kubernetes.io/service-name=web", "-o", "json").stdout)["items"]
            ready = [endpoint for item in slices for endpoint in item.get("endpoints", []) if endpoint.get("conditions", {}).get("ready") is True]
            ports = {port["port"] for item in slices if item.get("endpoints") for port in item.get("ports", [])}
            return len(ready), ports

        def wait_ports(port):
            deadline = time.monotonic() + 45
            while time.monotonic() < deadline:
                if endpoint_ports() == (1, {port}):
                    return
                time.sleep(1)
            raise RuntimeError("Ready EndpointSlice did not converge to expected target port " + str(port))

        def request(url, codes=(0,)):
            return kubectl("exec", "-n", namespace, "deployment/web", "--", "wget", "-T", "3", "-q", "-O", "-", url, codes=codes)

        def healthy():
            wait_ports(80)
            deadline = time.monotonic() + 45
            while time.monotonic() < deadline:
                result = request("http://web.manifest-lab.svc.cluster.local/", codes=(0, 1))
                if result.returncode == 0 and "Welcome to nginx!" in result.stdout:
                    return
                time.sleep(1)
            raise RuntimeError("Service DNS/ClusterIP HTTP did not recover")

        def chainsaw(test_dir, test_namespace, codes=(0,)):
            result = run("chainsaw", "test", "--test-dir", str(test_dir), "--test-file", "chainsaw-test.yaml",
                         "--namespace", test_namespace, "--kube-context", context, "--assert-timeout", "120s",
                         "--exec-timeout", "30s", "--cleanup-timeout", "120s", "--delete-timeout", "120s",
                         "--no-color", codes=codes, timeout=300, env=child_env)
            print(result.stdout + result.stderr)
            require(not kubectl("get", "namespace", test_namespace, "--ignore-not-found", "-o", "name").stdout.strip(), "Chainsaw namespace cleanup incomplete")
            return result

        try:
            report["versions"]["docker"] = json.loads(run("docker", "version", "--format", "{{json .Server}}").stdout)["Version"]
            report["versions"]["kind"] = run("kind", "version").stdout.strip()
            report["versions"]["kubectl"] = json.loads(run("kubectl", "version", "--client", "-o", "json").stdout)["clientVersion"]["gitVersion"]
            report["versions"]["chainsaw"] = run("chainsaw", "version").stdout.strip()
            for name in ("kind", "kubectl", "chainsaw"):
                pinned = next(t["version"] for t in versions["tools"] if t["name"] == name)
                require(pinned.removeprefix("v") in report["versions"][name], "Unexpected tool version: " + name)
            require(cluster not in run("kind", "get", "clusters").stdout.split(), "Refusing to reuse a cluster")
            created = True
            run("kind", "create", "cluster", "--name", cluster, "--kubeconfig", str(kubeconfig), "--image", versions["node_image"], "--wait", "120s", timeout=360)
            report["versions"]["kubernetes"] = json.loads(kubectl("version", "-o", "json").stdout)["serverVersion"]["gitVersion"]
            require(report["versions"]["kubernetes"] == versions["kubernetes"], "Unexpected Kubernetes server version")
            report["node_image"] = versions["node_image"]
            kubectl("create", "namespace", namespace)
            rendered = kubectl("kustomize", str(HERE)).stdout
            require("kind: Deployment" in rendered and "kind: Service" in rendered, "Kustomize must render both fixture objects")
            desired = temporary / "rendered.yaml"
            desired.write_text(rendered, encoding="utf-8")
            report["checks"]["kustomize_renders_deployment_and_service"] = True
            kubectl("apply", "--server-side", "--field-manager=kb-manifest-lab", "-n", namespace, "-f", str(desired))
            kubectl("rollout", "status", "deployment/web", "-n", namespace, "--timeout=180s")
            healthy()
            report["checks"]["baseline_service_dns_and_http"] = True
            base_diff = ("diff", "--server-side", "--field-manager=kb-manifest-lab", "-n", namespace, "-f")
            kubectl(*base_diff, str(HERE / "service.json"))
            kubectl(*base_diff, str(HERE / "service-reordered.json"))
            report["checks"]["live_diff_zero_for_baseline_and_reordered"] = True
            changed = kubectl(*base_diff, str(HERE / "service-broken.json"), codes=(1,))
            require("targetPort" in changed.stdout and "81" in changed.stdout, "API diff must expose proposed routing regression")
            report["checks"]["live_diff_one_for_changed_target_port"] = True
            failing_diff = temporary / "failing-diff.py"
            failing_diff.write_text("#!" + sys.executable + "\nimport sys\nprint('teaching diff process failure', file=sys.stderr)\nsys.exit(7)\n", encoding="utf-8")
            failing_diff.chmod(0o755)
            error_env = dict(child_env, KUBECTL_EXTERNAL_DIFF=str(failing_diff))
            error = kubectl(*base_diff, str(HERE / "service-broken.json"), codes=tuple(range(2, 256)), env=error_env)
            require("teaching diff process failure" in error.stderr, "Expected a real external diff error, not API failure")
            report["diff_error_exit_code"] = error.returncode
            report["checks"]["live_diff_error_distinct_from_difference"] = True
            service_before = json.loads(kubectl("get", "service", "web", "-n", namespace, "-o", "json").stdout)
            require(service_before["spec"]["ports"][0]["targetPort"] == 80, "Diff must not persist targetPort 81")
            report["checks"]["diff_does_not_persist_change"] = True
            kubectl("apply", "--server-side", "--field-manager=kb-manifest-lab", "-n", namespace, "-f", str(HERE / "service-broken.json"))
            wait_ports(81)
            kubectl("rollout", "status", "deployment/web", "-n", namespace, "--timeout=20s")
            require("Welcome to nginx!" in request("http://127.0.0.1/").stdout, "Application itself must remain healthy")
            service_ip = json.loads(kubectl("get", "service", "web", "-n", namespace, "-o", "json").stdout)["spec"]["clusterIP"]
            deadline = time.monotonic() + 30
            while time.monotonic() < deadline:
                broken = request("http://" + service_ip + "/", codes=(0, 1))
                if broken.returncode == 1 and "wget:" in broken.stderr:
                    break
                time.sleep(1)
            else:
                raise RuntimeError("Expected actual Service connection failure with healthy backend")
            require(any(term in broken.stderr.lower() for term in ("connection refused", "timed out", "timeout")), "Expected a connection diagnostic for the Service IP")
            report["http_failure_exit_code"] = broken.returncode
            report["checks"]["wrong_port_breaks_http_while_deployment_healthy"] = True
            drift = kubectl(*base_diff, str(HERE / "service.json"), codes=(1,))
            require("targetPort" in drift.stdout, "Desired good file must expose live routing drift")
            report["checks"]["live_drift_detected_after_mutation"] = True
            kubectl("apply", "--server-side", "--field-manager=kb-manifest-lab", "-n", namespace, "-f", str(HERE / "service.json"))
            healthy()
            kubectl(*base_diff, str(HERE / "service.json"))
            report["checks"]["restored_http_and_zero_diff"] = True
            # Same declarative test: positive with good inputs, negative with changed Service.
            chainsaw(HERE, "kb-chainsaw-good")
            report["checks"]["chainsaw_positive_http_and_cleanup"] = True
            negative_dir = temporary / "negative"
            negative_dir.mkdir()
            for name in ("app.yaml", "chainsaw-test.yaml"):
                shutil.copy2(HERE / name, negative_dir / name)
            shutil.copy2(HERE / "service-broken.json", negative_dir / "service.json")
            denied = chainsaw(negative_dir, "kb-chainsaw-bad", codes=(1,))
            diagnostic = (denied.stdout + denied.stderr).lower()
            require("wget:" in diagnostic and any(term in diagnostic for term in ("connection refused", "timed out", "timeout")), "Chainsaw must fail at the HTTP connection, not parsing/setup/DNS")
            report["checks"]["chainsaw_catches_routing_regression_and_cleans_up"] = True
            kubectl("delete", "namespace", namespace, "--wait=true", "--timeout=120s")
            require(not kubectl("get", "namespace", namespace, "--ignore-not-found", "-o", "name").stdout.strip(), "Lab namespace remained")
            report["checks"]["namespace_deleted"] = True
        except Exception as error:
            report["error"] = str(error)
            if kubeconfig.exists():
                for command in (("get", "pods", "-A", "-o", "wide"), ("get", "events", "-A", "--sort-by=.lastTimestamp")):
                    try:
                        diagnostic = kubectl(*command, codes=(0, 1), timeout=30)
                        print(diagnostic.stdout + diagnostic.stderr)
                    except Exception as diagnostic_error:
                        print("Diagnostics unavailable:", diagnostic_error)
            raise
        finally:
            try:
                if created:
                    run("kind", "delete", "cluster", "--name", cluster, "--kubeconfig", str(kubeconfig))
                    require(cluster not in run("kind", "get", "clusters").stdout.split(), "Task cluster remains")
                    remaining = run("docker", "ps", "-a", "--filter", "label=io.x-k8s.kind.cluster=" + cluster, "--format", "{{.Names}}").stdout.strip()
                    require(not remaining, "Task node containers remain")
                    report["checks"]["cluster_and_node_containers_deleted"] = True
            except Exception as cleanup_error:
                report["cleanup_error"] = str(cleanup_error)
                raise
            finally:
                report["status"] = "failed" if "error" in report or "cleanup_error" in report else "passed"
                if args.report:
                    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
                print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
