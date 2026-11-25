"""Exercise Terraform lock contention and stale-lock recovery on loopback."""

import argparse
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import subprocess
import tempfile
from threading import Event, Thread


class Backend(HTTPServer):
    state = None
    lock = None
    locked = Event()
    recovery_lock_id = None


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def reply(self, status, payload=b""):
        self.send_response(status)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def body(self):
        return self.rfile.read(int(self.headers.get("Content-Length", "0")))

    def do_GET(self):
        state = self.server.state
        if state is None:
            self.reply(404)
            return
        self.reply(200, state)

    def do_POST(self):
        self.server.state = self.body()
        self.reply(200)

    def do_LOCK(self):
        payload = self.body()
        if self.server.lock is not None:
            self.reply(423, self.server.lock)
            return
        self.server.lock = payload
        self.reply(200)
        self.server.locked.set()

    def do_UNLOCK(self):
        payload = self.body()
        requested_id = json.loads(payload)["ID"] if payload else self.server.recovery_lock_id
        if self.server.lock is None or requested_id != json.loads(self.server.lock)["ID"]:
            self.reply(409)
            return
        self.server.lock = None
        self.reply(200)


def run_lab(terraform, root, backend):
    endpoint = f"http://127.0.0.1:{backend.server_port}/state"
    config = """
terraform {
  backend "http" {}
}

resource "terraform_data" "example" {
  input = "lock-recovery-demo"
}
"""
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("TF_")}
    env.update(TF_HTTP_ADDRESS=endpoint, TF_HTTP_LOCK_ADDRESS=endpoint,
               TF_HTTP_UNLOCK_ADDRESS=endpoint, CHECKPOINT_DISABLE="1", NO_PROXY="127.0.0.1")

    def tf(client, *arguments, check=True):
        return subprocess.run([terraform, *arguments], cwd=root / client, env=env,
                              check=check, capture_output=True, text=True, timeout=30)

    for client in ("owner", "contender"):
        directory = root / client
        directory.mkdir()
        (directory / "main.tf").write_text(config, encoding="utf-8")
        tf(client, "init", "-input=false", "-no-color")

    tf("owner", "apply", "-auto-approve", "-input=false", "-no-color")
    baseline = backend.state
    if baseline is None or backend.lock is not None:
        raise RuntimeError("Expected a saved baseline and a released lock")
    backend.locked.clear()

    with subprocess.Popen([terraform, "apply", "-replace=terraform_data.example", "-no-color"], cwd=root / "owner",
                          env=env, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL) as owner:
        try:
            if not backend.locked.wait(15) or owner.poll() is not None:
                raise RuntimeError("Owner did not hold the lock")
            lock_id = json.loads(backend.lock)["ID"]
            blocked = tf("contender", "plan", "-input=false", "-no-color",
                         "-lock-timeout=2s", check=False)
            if blocked.returncode == 0 or lock_id not in blocked.stderr:
                raise RuntimeError(f"Contender did not report the owner lock: {blocked.stderr}")
            print("PASS: second client is blocked by the active owner")
        finally:
            if owner.poll() is None:
                owner.kill()
            owner.wait(timeout=10)

    if backend.lock is None or backend.state != baseline:
        raise RuntimeError("Expected an orphaned lock and unchanged baseline state")
    # Terraform 1.17.1 sends an empty UNLOCK body from a fresh client.
    # Allow it only for the orphan that the harness just confirmed.
    backend.recovery_lock_id = lock_id
    try:
        tf("contender", "force-unlock", "-force", lock_id)
    finally:
        backend.recovery_lock_id = None
    if backend.lock is not None or backend.state != baseline:
        raise RuntimeError("Unlock did not preserve state")
    print("PASS: orphaned lock cleared and state untouched")

    tf("contender", "apply", "-replace=terraform_data.example", "-auto-approve", "-input=false", "-no-color")
    listed = tf("owner", "state", "list").stdout.splitlines()
    if listed != ["terraform_data.example"] or backend.lock is not None or backend.state == baseline:
        raise RuntimeError(f"Unexpected shared state after recovery: {listed}")
    print("PASS: apply reacquired and released the lock; both clients see the resource")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--terraform", default="terraform")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="terraform-lock-recovery-") as directory, \
            Backend(("127.0.0.1", 0), Handler) as backend:
        server_thread = Thread(target=backend.serve_forever)
        server_thread.start()
        try:
            run_lab(args.terraform, Path(directory), backend)
        finally:
            backend.shutdown()
            server_thread.join()


if __name__ == "__main__":
    main()
