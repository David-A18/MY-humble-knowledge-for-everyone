#!/usr/bin/env python3
"""Fixture tests for scripts/moderate-content.py using a harmless synthetic term."""

from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("moderate-content.py")
spec = importlib.util.spec_from_file_location("moderate_content", SCRIPT)
module = importlib.util.module_from_spec(spec)
sys.modules["moderate_content"] = module
spec.loader.exec_module(module)

TERM = "zorblax"  # synthetic stand-in for a blocked word
PHRASE = "glim zorp"


def make_root(files: dict[str, str], exceptions: str = "") -> Path:
    root = Path(tempfile.mkdtemp())
    policy = root / "governance/policy"
    policy.mkdir(parents=True)
    term_hash = hashlib.sha256(TERM.encode()).hexdigest()
    phrase_hash = hashlib.sha256(PHRASE.encode()).hexdigest()
    (policy / "blocked-terms.sha256").write_text(f"# test\n{term_hash} profanity\n{phrase_hash} hate\n", encoding="utf-8")
    if exceptions:
        (policy / "moderation-exceptions.txt").write_text(exceptions.replace("HASH", term_hash), encoding="utf-8")
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    return root


def categories(files: dict[str, str], exceptions: str = "") -> list[tuple[str, int, str]]:
    return [(f["path"], f["line"], f["category"]) for f in module.scan(make_root(files, exceptions))]


assert categories({"knowledge/clean.md": "# Clean\n\nKubernetes Pods and Services.\n"}) == []
assert categories({"knowledge/a.md": "# A\n\nThis is zorblax.\n"}) == [("knowledge/a.md", 3, "profanity")]
assert categories({"knowledge/a.md": "ZORBLAX\n"}) == [("knowledge/a.md", 1, "profanity")], "case"
assert categories({"knowledge/a.md": "zórblåx\n"}) == [("knowledge/a.md", 1, "profanity")], "accents"
assert categories({"knowledge/a.md": "z0rbl4x\n"}) == [("knowledge/a.md", 1, "profanity")], "character substitution"
assert categories({"knowledge/a.md": "zorrrrblaaax\n"}) == [("knowledge/a.md", 1, "profanity")], "stretched letters"
assert categories({"knowledge/a.md": "z.o.r.b.l.a.x\n"}) == [("knowledge/a.md", 1, "profanity")], "split letters"
assert categories({"knowledge/a.md": "z o r b l a x\n"}) == [("knowledge/a.md", 1, "profanity")], "spaced letters"
assert categories({"examples/lab/app.py": "message = 'zorblax'\n"}) == [("examples/lab/app.py", 1, "profanity")], "code files"
assert categories({"knowledge/a.md": "glim   zorp\n"}) == [("knowledge/a.md", 1, "hate")], "phrases"
assert categories({"knowledge/a.md": "zorblaxian and prezorblax\n"}) == [], "no substring matches inside longer words"
assert categories({"knowledge/a.md": "zorblax\n"}, "knowledge/a.md HASH  # reviewed false positive\n") == [], "exceptions"
assert categories({"knowledge/b.md": "zorblax\n"}, "knowledge/a.md HASH\n") == [("knowledge/b.md", 1, "profanity")], "exceptions are per file"

findings = module.scan(make_root({"knowledge/a.md": "zorblax\n"}))
assert findings[0]["masked"] == "z******", "findings must not print the term"
assert "zorblax" not in str(findings)

result = subprocess.run(
    [sys.executable, str(SCRIPT), "--hash-terms", "sexual"], input="Zórblax\n", capture_output=True, text=True, check=True
)
assert result.stdout.strip() == f"{hashlib.sha256(TERM.encode()).hexdigest()} sexual"

# A pull request cannot weaken the scan by emptying its own term list when a trusted policy root is used.
untrusted = make_root({"knowledge/a.md": "zorblax\n"})
(untrusted / "governance/policy/blocked-terms.sha256").write_text("# emptied\n", encoding="utf-8")
assert module.scan(untrusted) == []
assert [f["category"] for f in module.scan(untrusted, policy_root=make_root({}))] == ["profanity"]

print("Content moderation fixtures passed.")
