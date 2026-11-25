# Terraform lock recovery rehearsal

Run from the repository root with Python 3 and Terraform 1.17.1 on PATH.

```bash
python examples/terraform/lock-recovery/run.py
```

What it does: creates two temporary Terraform working directories and one
in-memory HTTP state backend bound to loopback. One client holds the lock at
the apply approval prompt, while the other tries to plan. The runner stops the
first process, clears its orphaned lock, and verifies that a replacement
apply updates the shared state and releases its lock. The server and temporary
working directories are cleaned up at exit.

```text
PASS: second client is blocked by the active owner
PASS: orphaned lock cleared and state untouched
PASS: apply reacquired and released the lock; both clients see the resource
```

Terraform 1.17.1 sends an empty HTTP unlock body from a fresh client. The
fixture accepts it only inside the test's explicit recovery window, after
the owner has exited and the expected lock has been checked. This server is
a disposable exercise with synthetic state and no cloud services. Use the
recovery instructions for your actual backend.

- [State lock recovery guide](../../../knowledge/terraform/troubleshooting/state-lock-recovery.md)
- [Terraform examples](../README.md)
