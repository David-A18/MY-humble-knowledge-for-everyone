"""Compare a deprecated API client against adjacent disposable kind versions."""

import json
import os
from pathlib import Path
import subprocess
import tempfile
import uuid

IMAGES = {
    "v1.31.6": "28b7cbb993dfe093c76641a0c95807637213c9109b761f1d422c2400e22b8e87",
    "v1.32.2": "f226345927d7e348497136874b6d207e0b32cc52154ad8323129352923a3142f",
}
API = "/apis/flowcontrol.apiserver.k8s.io"
OBJECT = "flowschemas/catch-all"


def call(*args, check=True, capture=False):
    return subprocess.run(args, check=check, capture_output=capture, text=True, timeout=360)


def probe(name, api_version):
    return call(
        "docker", "exec", f"{name}-control-plane", "kubectl",
        "--kubeconfig=/etc/kubernetes/admin.conf", "get", "--raw",
        f"{API}/{api_version}/{OBJECT}", check=False, capture=True,
    )


def get_object(result, api_version):
    if result.returncode:
        raise RuntimeError(result.stderr.strip())
    obj = json.loads(result.stdout)
    if obj["apiVersion"] != f"flowcontrol.apiserver.k8s.io/{api_version}" or obj["metadata"]["name"] != "catch-all":
        raise RuntimeError(f"Unexpected FlowSchema for {api_version}")
    return obj["metadata"]["uid"]


def run_cluster(version, digest, kubeconfig):
    name = f"upgrade-{uuid.uuid4().hex[:10]}"
    try:
        call("kind", "create", "cluster", "--name", name, "--kubeconfig", str(kubeconfig),
             "--image", f"kindest/node:{version}@sha256:{digest}", "--wait", "120s")
        version_result = call("docker", "exec", f"{name}-control-plane", "kubectl",
                              "--kubeconfig=/etc/kubernetes/admin.conf", "version",
                              "-o", "json", capture=True)
        if json.loads(version_result.stdout)["serverVersion"]["gitVersion"] != version:
            raise RuntimeError(f"Unexpected API server version for {name}")
        old = probe(name, "v1beta3")
        if version == "v1.31.6":
            old_uid = get_object(old, "v1beta3")
            if old_uid != get_object(probe(name, "v1"), "v1"):
                raise RuntimeError("Baseline API versions returned different objects")
            print(f"PASS {version}: both API versions expose the same baseline object", flush=True)
        else:
            if old.returncode == 0 or "Error from server (NotFound)" not in old.stderr:
                raise RuntimeError(f"Expected the removed API to return NotFound: {old.stderr}")
            print(f"PASS {version}: the legacy client gets NotFound", flush=True)
            get_object(probe(name, "v1"), "v1")
            print(f"PASS {version}: the corrected client reads through v1", flush=True)
    finally:
        call("kind", "delete", "cluster", "--name", name, "--kubeconfig", str(kubeconfig))
        remaining = call("kind", "get", "clusters", capture=True).stdout.splitlines()
        if name in remaining:
            raise RuntimeError(f"Disposable cluster still exists: {name}")
        print(f"PASS {version}: disposable cluster removed", flush=True)


def main():
    os.environ["KIND_EXPERIMENTAL_PROVIDER"] = "docker"
    with tempfile.TemporaryDirectory(prefix="kubernetes-upgrade-") as directory:
        for version, digest in IMAGES.items():
            run_cluster(version, digest, Path(directory) / "config")


if __name__ == "__main__":
    main()
