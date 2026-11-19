#!/usr/bin/env python3
"""Detect offensive, sexual, or hateful language in repository text.

Blocked terms are stored as SHA-256 hashes of their normalized form in
governance/policy/blocked-terms.sha256, so the repository does not display the
words themselves. Normalization removes accents, maps common character
substitutions (for example 0 -> o, 4 -> a, @ -> a), collapses stretched letters,
and rejoins letters split by spaces or punctuation (f.o.o -> foo).

The scanner only reads files, so it is safe to run on untrusted pull-request
checkouts with --root. Findings never print the matched word: they show a
masked form, the file, the line, and the category.

Maintainer commands:
  printf '%s\n' 'term' | python3 scripts/moderate-content.py --hash-terms CATEGORY
  printf '%s\n' 'term' | python3 scripts/moderate-content.py --check-terms
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

TERMS_FILE = "governance/policy/blocked-terms.sha256"
EXCEPTIONS_FILE = "governance/policy/moderation-exceptions.txt"
CATEGORIES = {"profanity", "sexual", "hate"}
TEXT_SUFFIXES = {
    ".md", ".py", ".mjs", ".ts", ".json", ".jsonc", ".jsonl", ".yaml", ".yml", ".toml",
    ".txt", ".tf", ".hcl", ".rego", ".csv", ".example",
}
SKIP_FILES = {TERMS_FILE}
LEET = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s", "!": "i"})
STRETCH = re.compile(r"([a-z])\1{2,}")
WORD = re.compile(r"[a-z]+")
# Letters separated by single punctuation or spaces, for example "f.o.o" or "f o o".
SPLIT_WORD = re.compile(r"(?<![a-z])(?:[a-z][\s._*-]){2,}[a-z](?![a-z])")


def fold(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return stripped.lower()


def normalize_token(token: str) -> str:
    folded = fold(token).translate(LEET)
    letters = "".join(ch for ch in folded if "a" <= ch <= "z")
    return STRETCH.sub(r"\1", letters)


def digest(term: str) -> str:
    return hashlib.sha256(term.encode("utf-8")).hexdigest()


def candidates(line: str) -> list[tuple[str, str]]:
    """Return (normalized candidate, original fragment) pairs for one line."""
    folded = fold(line)
    leet = folded.translate(LEET)
    found: list[tuple[str, str]] = []
    words = [(m.group(0), m.start(), m.end()) for m in WORD.finditer(leet)]
    for word, start, end in words:
        found.append((STRETCH.sub(r"\1", word), line[start:end] if len(line) == len(folded) else word))
    for first, second in zip(words, words[1:]):
        if leet[first[2]:second[1]].strip() == "":
            found.append((STRETCH.sub(r"\1", f"{first[0]} {second[0]}"), f"{first[0]} {second[0]}"))
    for match in SPLIT_WORD.finditer(leet):
        joined = re.sub(r"[^a-z]", "", match.group(0))
        found.append((STRETCH.sub(r"\1", joined), match.group(0)))
    return found


def load_terms(root: Path) -> dict[str, str]:
    terms: dict[str, str] = {}
    path = root / TERMS_FILE
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            value, category = line.split()
            terms[value] = category
    return terms


def load_exceptions(root: Path) -> set[tuple[str, str]]:
    path = root / EXCEPTIONS_FILE
    if not path.is_file():
        return set()
    exceptions = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            file_path, term_hash = line.split()
            exceptions.add((file_path, term_hash))
    return exceptions


def text_files(root: Path) -> list[str]:
    try:
        listed = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            capture_output=True, check=True,
        ).stdout.decode("utf-8", "surrogateescape").split("\0")
    except (OSError, subprocess.CalledProcessError):
        listed = [p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]
    return sorted(
        rel for rel in set(filter(None, listed))
        if rel not in SKIP_FILES and (Path(rel).suffix.lower() in TEXT_SUFFIXES or Path(rel).name == "Dockerfile")
        and (root / rel).is_file() and not (root / rel).is_symlink()
    )


def mask(fragment: str) -> str:
    letters = re.sub(r"[^A-Za-z]", "", fragment) or fragment
    return letters[0] + "*" * (len(letters) - 1)


def scan(root: Path, policy_root: Path | None = None) -> list[dict]:
    root = root.resolve()
    policy = (policy_root or root).resolve()
    terms = load_terms(policy)
    exceptions = load_exceptions(policy)
    findings = []
    for rel in text_files(root):
        try:
            text = (root / rel).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue  # the repository policy check reports non-UTF-8 files
        for number, line in enumerate(text.splitlines(), 1):
            reported = set()
            for candidate, fragment in candidates(line):
                value = digest(candidate)
                if value in terms and value not in reported and (rel, value) not in exceptions:
                    reported.add(value)
                    findings.append({
                        "path": rel, "line": number, "category": terms[value],
                        "masked": mask(fragment), "term_hash": value,
                    })
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=".", type=Path, help="checkout to scan (read-only)")
    parser.add_argument("--policy-root", type=Path, help="trusted checkout that supplies governance/policy lists (default: --root)")
    parser.add_argument("--json", type=Path, help="write findings as JSON")
    parser.add_argument("--hash-terms", metavar="CATEGORY", choices=sorted(CATEGORIES),
                        help="read terms from stdin and print hash lines for the blocked-term file")
    parser.add_argument("--check-terms", action="store_true", help="read terms from stdin and report whether each is blocked")
    args = parser.parse_args()

    if args.hash_terms or args.check_terms:
        known = load_terms(args.root.resolve()) if args.check_terms else {}
        for raw in sys.stdin.read().splitlines():
            term = " ".join(normalize_token(part) for part in raw.split())
            if not term:
                continue
            if args.hash_terms:
                print(f"{digest(term)} {args.hash_terms}")
            else:
                print(f"{'blocked' if digest(term) in known else 'not blocked'}: {mask(raw)}")
        return 0

    findings = scan(args.root, args.policy_root)
    if args.json:
        args.json.write_text(json.dumps(findings, indent=2) + "\n", encoding="utf-8")
    for finding in findings:
        print(f"{finding['path']}:{finding['line']}: [{finding['category']}] blocked term {finding['masked']}")
    if findings:
        print(f"Content moderation failed with {len(findings)} finding(s). See governance/content-policy.md.")
        return 1
    print("Content moderation passed: no blocked terms found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
