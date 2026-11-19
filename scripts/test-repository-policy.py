#!/usr/bin/env python3
"""Fixture tests for scripts/validate-repository-policy.py."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("validate-repository-policy.py")
spec = importlib.util.spec_from_file_location("repository_policy", SCRIPT)
module = importlib.util.module_from_spec(spec)
sys.modules["repository_policy"] = module
spec.loader.exec_module(module)

DOMAINS = "docs.example.org\nkubernetes.io\n"
PREFIXES = "https://www.youtube.com/watch?v=approved\n"


def make_root(files: dict[str, str | bytes], executable: tuple[str, ...] = (), symlinks: dict[str, str] | None = None) -> Path:
    root = Path(tempfile.mkdtemp())
    policy = root / "governance/policy"
    policy.mkdir(parents=True)
    (policy / "allowed-link-domains.txt").write_text(DOMAINS, encoding="utf-8")
    (policy / "allowed-link-prefixes.txt").write_text(PREFIXES, encoding="utf-8")
    for rel, content in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
    for rel in executable:
        os.chmod(root / rel, 0o755)
    for rel, target in (symlinks or {}).items():
        os.symlink(target, root / rel)
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    return root


def rules(files: dict[str, str | bytes], **kwargs) -> list[str]:
    return sorted({finding.rule for finding in module.validate(make_root(files, **kwargs))})


def messages(files: dict[str, str | bytes]) -> str:
    return "\n".join(f.render() for f in module.validate(make_root(files)))


GOOD = "# Good\n\nSee [Pods](https://kubernetes.io/docs/concepts/workloads/pods/) and [local](other.md).\n"

# File types and binary content.
assert rules({"knowledge/a.md": GOOD, "examples/lab/app.py": "print('ok')\n"}) == []
assert rules({"knowledge/a.md": GOOD, "knowledge/run.py": "print('x')\n"}) == ["file-type"], "knowledge is Markdown-only"
assert rules({"examples/tool.exe": b"MZ\x90\x00"}) == ["binary", "file-type"]
assert rules({"examples/archive.zip": b"PK\x03\x04\x00"}) == ["binary", "file-type"]
assert rules({"examples/photo.png": b"\x89PNG\r\n\x1a\n\x00"}) == ["binary", "file-type"]
assert rules({"examples/run.sh": "echo hi\n"}) == ["file-type"], "shell scripts belong in Markdown code blocks"
assert rules({"knowledge/report.exe.md": "# R\n"}) == ["file-type"], "double extension"
assert rules({"examples/data.csv": b"a,b\n\xff\xfe\n"}) == ["binary"], "invalid UTF-8"
assert rules({"examples/run.py": "print('x')\n"}, executable=("examples/run.py",)) == ["file-type"]
assert rules({"scripts/check.py": "print('x')\n"}, executable=("scripts/check.py",)) == []
assert rules({"knowledge/a.md": GOOD}, symlinks={"knowledge/link.md": "/etc/passwd"}) == ["file-type"]
assert rules({"knowledge/big.md": "# B\n\n" + "word " * 30000}) == ["file-size"]

# Hidden Unicode.
assert rules({"examples/a.py": "access = 'user' # \u202e admin\n"}) == ["hidden-unicode"]
assert rules({"knowledge/a.md": "# A\n\nzero\u200bwidth\n"}) == ["hidden-unicode"]

# Raw HTML and media.
assert rules({"knowledge/a.md": "# A\n\n<script>alert(1)</script>\n"}) == ["raw-html"]
assert rules({"knowledge/a.md": "# A\n\n<iframe src=\"https://kubernetes.io\"></iframe>\n"}) == ["raw-html"]
assert rules({"knowledge/a.md": "# A\n\n<details><summary>More</summary>Text</details>\n"}) == []
assert rules({"knowledge/a.md": "# A\n\n<details open onclick=\"x()\">\n"}) == ["raw-html"]
assert rules({"knowledge/a.md": "# A\n\n![photo](https://kubernetes.io/a.png)\n"}) == ["media"]
assert rules({"knowledge/a.md": "# A\n\n![local](diagram.svg)\n"}) == ["media"]
assert rules({"knowledge/a.md": "# A\n\n```html\n<script src=\"x.js\"></script>\n<img src=\"https://evil.test/a.png\">\n```\n"}) == [], "code blocks are examples"
assert rules({"knowledge/a.md": "# A\n\nUse `<script>` tags carefully.\n"}) == [], "inline code is an example"

# Link safety.
assert rules({"knowledge/a.md": "# A\n\n[x](http://kubernetes.io/docs/)\n"}) == ["link-safety"], "https only"
assert rules({"knowledge/a.md": "# A\n\n[x](http://localhost:8080/)\n"}) == []
assert rules({"knowledge/a.md": "# A\n\n[x](javascript:alert(1))\n"}) == ["link-safety"]
assert rules({"knowledge/a.md": "# A\n\n[x](data:text/html;base64,PHNjcmlwdD4=)\n"}) == ["link-safety"]
assert rules({"knowledge/a.md": "# A\n\n[x](https://bit.ly/abc)\n"}) == ["link-safety"], "shorteners"
assert rules({"knowledge/a.md": "# A\n\n[x](https://203.0.113.7/login)\n"}) == ["link-safety"], "raw IPs"
assert rules({"knowledge/a.md": "# A\n\n[x](https://kubernetes.io@evil.test/)\n"}) == ["link-safety"], "user info"
assert rules({"knowledge/a.md": "# A\n\n[x](https://xn--kubrnetes-x2a.io/)\n"}) == ["link-safety"], "punycode"
assert rules({"knowledge/a.md": "# A\n\n[x](https://unknown.test/page)\n"}) == ["link-safety"], "unreviewed domain"
assert rules({"knowledge/a.md": "# A\n\nhttps://unknown.test/page\n"}) == ["link-safety"], "bare URLs"
assert rules({"knowledge/a.md": "# A\n\n<https://unknown.test/page>\n"}) == ["link-safety"], "autolinks"
assert rules({"knowledge/a.md": "# A\n\n[x][ref]\n\n[ref]: https://unknown.test/\n"}) == ["link-safety"], "reference links"
assert rules({"knowledge/a.md": "# A\n\n[x](https://docs.kubernetes.io/setup/)\n"}) == [], "subdomains of allowed domains"
assert rules({"knowledge/a.md": "# A\n\n[x](https://kubernetes.io/tool.exe)\n"}) == ["link-safety"], "download links"
assert rules({"knowledge/a.md": "# A\n\n[x](https://www.youtube.com/watch?v=other)\n"}) == ["link-safety"], "restricted host"
assert rules({"knowledge/a.md": "# A\n\n[x](https://www.youtube.com/watch?v=approved)\n"}) == [], "approved restricted URL"
assert rules({"knowledge/a.md": "# A\n\n```bash\ncurl https://unknown.test/install\n```\n"}) == [], "commands in code blocks"
assert "unknown.test" in messages({"knowledge/a.md": "# A\n\n[x](https://unknown.test/)\n"})

# A pull request cannot approve its own domains when a trusted policy root is used.
untrusted = make_root({"knowledge/a.md": "# A\n\n[x](https://unknown.test/)\n"})
(untrusted / "governance/policy/allowed-link-domains.txt").write_text("unknown.test\n", encoding="utf-8")
assert module.validate(untrusted) == []
assert [f.rule for f in module.validate(untrusted, policy_root=make_root({}))] == ["link-safety"]

print("Repository policy fixtures passed.")
