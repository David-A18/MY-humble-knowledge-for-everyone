"""Exercise a WebApp graph and its lifecycle in a new disposable kind cluster."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import urllib.request

import yaml

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run(*command, codes=(0,), timeout=180):
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8",
                            errors="replace", timeout=timeout)
    require(result.returncode in codes, "Command failed: " + " ".join(command) + "\n" + result.stderr)
    return result


def wait_for(description, check, timeout=120):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        result = check()
        if result:
            return result
        time.sleep(2)
    raise RuntimeError("Timed out waiting for " + description)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    versions = json.loads((HERE / "lab-versions.json").read_text(encoding="utf-8"))
    report = {"checks": {}, "versions": {"python": sys.version.split()[0], "kro": versions["kro"]}}
    with tempfile.TemporaryDirectory(prefix="kb-kro-") as directory:
        temporary = Path(directory)
        # The temporary directory gives this run its cluster name and private kubeconfig.
        cluster = temporary.name
        kubeconfig = str(temporary / "kubeconfig")
        context = "kind-" + cluster
        report["cluster"] = cluster
        created = False

        def kube(*command, **options):
            return run("kubectl", "--kubeconfig", kubeconfig, "--context", context, *command, **options)

        def object_(kind, name, namespace="kro-lab"):
            command = ["get", kind, name, "--ignore-not-found", "-o", "json"]
            if namespace:
                command.extend(["-n", namespace])
            result = kube(*command)
            return json.loads(result.stdout) if result.stdout.strip() else {}

        def ready(instance):
            return any(c["type"] == "Ready" and c["status"] == "True"
                       for c in instance.get("status", {}).get("conditions", []))

        def patch(spec):
            kube("patch", "webapp", "demo", "-n", "kro-lab", "--type=merge",
                 "-p", json.dumps({"spec": spec}))

        def healthy(replicas):
            deployment = object_("deployment", "demo")
            status = deployment.get("status", {})
            if not (deployment.get("spec", {}).get("replicas") == replicas
                    and status.get("observedGeneration") == deployment.get("metadata", {}).get("generation")
                    and status.get("updatedReplicas") == replicas
                    and status.get("availableReplicas") == replicas):
                return False
            instance = object_("webapp", "demo")
            service = object_("service", "demo")
            if not ready(instance) or instance.get("status", {}).get("endpoint") != service.get("spec", {}).get("clusterIP"):
                return False
            result = kube("exec", "-n", "kro-lab", "deployment/demo", "--",
                          "wget", "-T", "5", "-q", "-O", "-", "http://demo.kro-lab.svc.cluster.local/",
                          codes=(0, 1))
            return result.returncode == 0 and "Welcome to nginx!" in result.stdout

        try:
            require(cluster not in run("kind", "get", "clusters").stdout.split(), "Cluster already exists")
            for tool in versions["tools"]:
                if tool["name"] == "kind":
                    actual = run("kind", "version").stdout.strip()
                    require(tool["version"] in actual, "Unexpected kind version")
                else:
                    actual = json.loads(run("kubectl", "version", "--client", "-o", "json").stdout)["clientVersion"]["gitVersion"]
                    require(actual == tool["version"], "Unexpected kubectl version")
                report["versions"][tool["name"]] = actual
            report["versions"]["docker"] = run("docker", "version", "--format", "{{.Server.Version}}").stdout.strip()
            created = True
            run("kind", "create", "cluster", "--name", cluster, "--kubeconfig", kubeconfig,
                "--image", versions["node_image"], "--wait", "120s", timeout=360)
            report["versions"]["kubernetes"] = json.loads(kube("version", "-o", "json").stdout)["serverVersion"]["gitVersion"]
            require(report["versions"]["kubernetes"] == versions["kubernetes"], "Unexpected server version")
            asset = versions["controller_manifest"]
            with urllib.request.urlopen(asset["url"], timeout=90) as response:
                raw = response.read()
            require(hashlib.sha256(raw).hexdigest() == asset["sha256"], "Controller manifest checksum mismatch")
            install = temporary / "controller.yaml"
            install.write_bytes(raw)
            kube("create", "namespace", "kro-system")
            kube("apply", "-n", "kro-system", "-f", str(install))
            kube("apply", "-f", str(HERE / "controller-access.yaml"))
            kube("rollout", "status", "deployment/kro", "-n", "kro-system", "--timeout=180s")
            controller = object_("deployment", "kro", "kro-system")
            controller_image = controller["spec"]["template"]["spec"]["containers"][0]["image"]
            require(controller_image.endswith(":v" + versions["kro"]), "Unexpected controller image")
            report["controller_image"] = controller_image
            report["checks"]["pinned_controller_ready"] = True
            kube("apply", "-f", str(HERE / "webapp-rgd.yaml"))
            wait_for("generated WebApp CRD", lambda: bool(object_("crd", "webapps.kro.run", "")))
            kube("wait", "--for=condition=Established", "crd/webapps.kro.run", "--timeout=120s")
            kube("wait", "--for=condition=Ready", "rgd/webapp", "--timeout=120s")
            report["checks"]["definition_and_generated_api_ready"] = True
            kube("create", "namespace", "kro-lab")
            kube("apply", "-n", "kro-lab", "-f", str(HERE / "webapp.yaml"))
            wait_for("one replica, graph readiness and Service HTTP", lambda: healthy(1), 180)
            report["checks"]["baseline_http_and_status_endpoint"] = True
            invalid = yaml.safe_load((HERE / "webapp.yaml").read_text(encoding="utf-8"))
            invalid["metadata"]["name"] = "invalid"
            invalid["spec"]["replicas"] = 0
            invalid_path = temporary / "invalid.yaml"
            invalid_path.write_text(yaml.safe_dump(invalid), encoding="utf-8")
            rejected = kube("apply", "-n", "kro-lab", "-f", str(invalid_path), codes=(1,))
            require("replicas" in rejected.stderr and any(term in rejected.stderr.lower() for term in ("minimum", "greater than or equal")),
                    "Expected generated-schema minimum rejection")
            report["checks"]["invalid_instance_rejected_by_generated_schema"] = True
            patch({"replicas": 2})
            wait_for("two healthy replicas", lambda: healthy(2), 180)
            report["checks"]["instance_change_scales_children"] = True
            old_uid = object_("service", "demo")["metadata"]["uid"]
            kube("delete", "service", "demo", "-n", "kro-lab")
            wait_for("recreated Service", lambda: object_("service", "demo").get("metadata", {}).get("uid") not in (None, old_uid))
            wait_for("HTTP after Service recreation", lambda: healthy(2))
            report["checks"]["deleted_service_recreated_and_http_recovers"] = True
            image = yaml.safe_load((HERE / "webapp.yaml").read_text(encoding="utf-8"))["spec"]["image"]
            patch({"image": "nginx:kb-kro-intentionally-missing"})

            def failed_image():
                deployment = object_("deployment", "demo")
                if deployment.get("spec", {}).get("template", {}).get("spec", {}).get("containers", [{}])[0].get("image") != "nginx:kb-kro-intentionally-missing":
                    return False
                pods = json.loads(kube("get", "pods", "-n", "kro-lab", "-o", "json").stdout)["items"]
                for pod in pods:
                    for container in pod.get("status", {}).get("containerStatuses", []):
                        waiting = container.get("state", {}).get("waiting", {})
                        if waiting.get("reason") in ("ErrImagePull", "ImagePullBackOff"):
                            message = waiting.get("message", "").lower()
                            if any(term in message for term in ("not found", "notfound", "manifest unknown")):
                                return not ready(object_("webapp", "demo"))
                return False

            wait_for("image-not-found and non-ready graph", failed_image, 180)
            report["checks"]["missing_image_blocks_graph_readiness"] = True
            patch({"image": image})
            wait_for("restored image, graph and HTTP", lambda: healthy(2), 180)
            report["checks"]["restored_image_recovers_graph_and_http"] = True
            kube("delete", "webapp", "demo", "-n", "kro-lab", "--timeout=120s")
            wait_for("managed Deployment and Service deletion",
                     lambda: not object_("deployment", "demo") and not object_("service", "demo"))
            report["checks"]["instance_deletion_removes_children"] = True
            kube("delete", "rgd", "webapp", "--timeout=120s")
            kube("delete", "namespace", "kro-lab", "--timeout=120s")
            require(not kube("get", "namespace", "kro-lab", "--ignore-not-found", "-o", "name").stdout.strip(),
                    "Lab namespace remains")
            report["checks"]["lab_namespace_deleted"] = True
        except Exception as error:
            report["error"] = str(error)
            raise
        finally:
            try:
                if created:
                    run("kind", "delete", "cluster", "--name", cluster, "--kubeconfig", kubeconfig)
                    require(cluster not in run("kind", "get", "clusters").stdout.split(), "Cluster remains")
                    require(not run("docker", "ps", "-a", "--filter", f"label=io.x-k8s.kind.cluster={cluster}",
                                    "--format", "{{.Names}}").stdout.strip(), "Node containers remain")
                    report["checks"]["cluster_and_nodes_deleted"] = True
            except Exception as cleanup_error:
                report["cleanup_error"] = str(cleanup_error)
                raise
            finally:
                report["status"] = "failed" if "error" in report or "cleanup_error" in report else "passed"
                output = json.dumps(report, indent=2) + "\n"
                if args.report:
                    args.report.write_text(output, encoding="utf-8")
                print(output, end="")


if __name__ == "__main__":
    main()
