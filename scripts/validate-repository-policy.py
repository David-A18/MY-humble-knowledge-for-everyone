#!/usr/bin/env python3
"""Enforce the repository content policy: allowed files, safe Markdown, and safe links.

The policy is documented in governance/content-policy.md. This checker only reads
files; it never executes repository content, so it is safe to run on untrusted
pull-request checkouts with --root.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

KNOWLEDGE_EXTENSIONS = {".md"}
TEXT_EXTENSIONS = {
    ".md", ".py", ".mjs", ".ts", ".json", ".jsonc", ".jsonl", ".yaml", ".yml",
    ".toml", ".txt", ".tf", ".hcl", ".rego", ".csv", ".sha256", ".example",
}
NAMED_TEXT_FILES = {".gitignore", ".gitattributes", "Dockerfile", "CODEOWNERS", "LICENSE"}
EXECUTABLE_ALLOWED_PREFIXES = ("scripts/",)
# Inner extensions that disguise executables, archives, or media (for example report.pdf.md).
DANGEROUS_EXTENSIONS = {
    "exe", "dll", "so", "dylib", "bin", "com", "scr", "msi", "msp", "bat", "cmd", "ps1", "psm1",
    "vbs", "vbe", "jse", "wsf", "hta", "cpl", "jar", "apk", "app", "dmg", "pkg", "deb", "rpm",
    "iso", "img", "zip", "tar", "gz", "tgz", "bz2", "xz", "7z", "rar", "sh", "bash", "zsh",
    "lnk", "reg", "docm", "xlsm", "pptm", "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx",
    "png", "jpg", "jpeg", "gif", "webp", "bmp", "svg", "ico", "tif", "tiff", "heic",
    "mp4", "mov", "avi", "mkv", "webm", "wmv", "flv", "mp3", "wav", "ogg", "flac", "m4a",
}
MAX_BYTES_DEFAULT = 1_000_000
MAX_BYTES_KNOWLEDGE = 100_000
IGNORED_PREFIXES = (".git/", "node_modules/")

# Raw HTML is not needed in this text-only knowledge base; these elements are harmless.
ALLOWED_HTML = {"br", "details", "summary", "kbd", "sub", "sup"}
ALLOWED_SCHEMES = {"https", "mailto"}
HTTP_ALLOWED_HOSTS = {"localhost", "127.0.0.1", "example.com", "www.example.com"}
URL_SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd", "buff.ly", "rebrand.ly",
    "cutt.ly", "shorturl.at", "rb.gy", "t.ly", "tiny.cc", "lnkd.in", "s.id", "v.gd", "shorturl.com",
}
# Hosts that serve arbitrary user content; only individually approved URL prefixes pass.
RESTRICTED_HOSTS = {
    "youtube.com", "youtu.be", "vimeo.com", "dailymotion.com", "tiktok.com", "twitch.tv",
    "instagram.com", "facebook.com", "x.com", "twitter.com", "reddit.com", "imgur.com",
    "raw.githubusercontent.com", "gist.github.com", "gist.githubusercontent.com",
    "objects.githubusercontent.com", "user-images.githubusercontent.com",
    "drive.google.com", "docs.google.com", "dropbox.com", "mega.nz", "mediafire.com",
    "wetransfer.com", "pastebin.com", "paste.ee", "hastebin.com", "discord.gg", "t.me",
}
DOWNLOAD_EXTENSIONS = DANGEROUS_EXTENSIONS - {"pdf", "svg", "png", "jpg", "jpeg", "gif", "webp"}
BIDI_CONTROLS = re.compile("[\\u202a-\\u202e\\u2066-\\u2069\\u200e\\u200f\\u061c]")
INVISIBLE = re.compile("[\\u200b\\u200c\\u200d\\u2060\\ufeff]")

FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE = re.compile(r"(`+)(?:(?!\1).)+?\1")
HTML_TAG = re.compile(r"<(/?)([A-Za-z][A-Za-z0-9-]*)(\s[^<>]*)?/?>")
AUTOLINK = re.compile(r"<([a-zA-Z][a-zA-Z0-9+.-]*:[^<>\s]+)>")
IMAGE = re.compile(r"!\[[^\]]*\]\(([^)]*)\)|!\[[^\]]*\]\[[^\]]*\]")
LINK_DEST = re.compile(r"(?<!!)\[[^\]]*\]\(\s*<?([^)\s>]+)")
REF_DEF = re.compile(r"^\s*\[[^\]]+\]:\s*<?(\S+?)>?(?:\s|$)")
BARE_URL = re.compile(r"\b((?:https?|ftp)://[^\s<>()\[\]\"'`]+)", re.IGNORECASE)
IP_HOST = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$|^\[?[0-9a-f:]+\]?$", re.IGNORECASE)


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    rule: str
    message: str

    def render(self) -> str:
        location = f"{self.path}:{self.line}" if self.line else self.path
        return f"{location}: [{self.rule}] {self.message}"


def list_files(root: Path) -> list[tuple[str, str]]:
    """Return (mode, path) for tracked and untracked, non-ignored files."""
    try:
        staged = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-s", "-z"], capture_output=True, check=True
        ).stdout.decode("utf-8", "surrogateescape")
        others = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z", "--others", "--exclude-standard"],
            capture_output=True, check=True,
        ).stdout.decode("utf-8", "surrogateescape")
    except (OSError, subprocess.CalledProcessError):
        return walk_files(root)
    entries: dict[str, str] = {}
    for record in filter(None, staged.split("\0")):
        meta, path = record.split("\t", 1)
        entries[path] = meta.split()[0]
    for path in filter(None, others.split("\0")):
        entries.setdefault(path, mode_of(root / path))
    return sorted((mode, path) for path, mode in entries.items()
                  if not path.startswith(IGNORED_PREFIXES) and (root / path).exists() or mode == "160000")


def walk_files(root: Path) -> list[tuple[str, str]]:
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules"}]
        for name in filenames:
            full = Path(dirpath) / name
            found.append((mode_of(full), full.relative_to(root).as_posix()))
    return sorted(found)


def mode_of(path: Path) -> str:
    if path.is_symlink():
        return "120000"
    return "100755" if os.access(path, os.X_OK) and path.is_file() else "100644"


def load_list(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    return {line.split("#", 1)[0].strip().lower() for line in path.read_text(encoding="utf-8").splitlines()} - {""}


def check_file(root: Path, mode: str, rel: str) -> list[Finding]:
    findings: list[Finding] = []
    name = rel.rsplit("/", 1)[-1]
    suffix = Path(name).suffix.lower()
    if mode == "160000":
        return [Finding(rel, 0, "file-type", "git submodules are not allowed")]
    if mode == "120000":
        return [Finding(rel, 0, "file-type", "symbolic links are not allowed")]
    if mode == "100755" and not rel.startswith(EXECUTABLE_ALLOWED_PREFIXES):
        findings.append(Finding(rel, 0, "file-type", "executable permission is only allowed for maintained scripts/"))
    if rel.startswith("knowledge/") and suffix not in KNOWLEDGE_EXTENSIONS:
        findings.append(Finding(rel, 0, "file-type", "the knowledge bundle accepts Markdown (.md) files only; put runnable lab files in examples/"))
    elif suffix not in TEXT_EXTENSIONS and name not in NAMED_TEXT_FILES:
        findings.append(Finding(rel, 0, "file-type", f"file type {suffix or name!r} is not on the text-file allowlist"))
    inner = [part.lower() for part in name.split(".")[1:-1]]
    if any(part in DANGEROUS_EXTENSIONS for part in inner):
        findings.append(Finding(rel, 0, "file-type", "file name hides an executable, archive, document, or media extension"))

    data = (root / rel).read_bytes()
    limit = MAX_BYTES_KNOWLEDGE if rel.startswith("knowledge/") else MAX_BYTES_DEFAULT
    if len(data) > limit:
        findings.append(Finding(rel, 0, "file-size", f"{len(data)} bytes exceeds the {limit}-byte limit"))
    if b"\0" in data:
        return findings + [Finding(rel, 0, "binary", "binary content (NUL bytes) is not allowed")]
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return findings + [Finding(rel, 0, "binary", "file is not valid UTF-8 text")]
    for number, line in enumerate(text.splitlines(), 1):
        if BIDI_CONTROLS.search(line):
            findings.append(Finding(rel, number, "hidden-unicode", "bidirectional control character can disguise text or code"))
        if suffix == ".md" and INVISIBLE.search(line):
            findings.append(Finding(rel, number, "hidden-unicode", "invisible zero-width character in Markdown"))
    return findings


def prose_lines(markdown: str):
    """Yield (line_number, text) for Markdown outside fenced code, without inline code spans."""
    fence = ""
    in_frontmatter = markdown.startswith("---\n")
    for number, line in enumerate(markdown.splitlines(), 1):
        if in_frontmatter:
            if number > 1 and line.strip() == "---":
                in_frontmatter = False
            continue
        match = FENCE.match(line)
        if match:
            marker = match.group(1)[0]
            if not fence:
                fence = marker
            elif marker == fence:
                fence = ""
            continue
        if fence:
            continue
        yield number, INLINE_CODE.sub("", line)


def host_matches(host: str, domains: set[str]) -> bool:
    return any(host == domain or host.endswith("." + domain) for domain in domains)


def check_url(url: str, allowed_domains: set[str], allowed_prefixes: set[str] = frozenset()) -> str | None:
    url = url.rstrip(".,;:!?*_")
    parts = urlsplit(url)
    scheme = parts.scheme.lower()
    if scheme not in ALLOWED_SCHEMES and scheme != "http":
        return f"link scheme {scheme!r} is not allowed"
    if scheme == "mailto":
        return None
    host = (parts.hostname or "").lower()
    if not host:
        return "link has no host"
    if parts.username or parts.password or "@" in parts.netloc:
        return "links must not contain user information before the host"
    if scheme == "http" and host not in HTTP_ALLOWED_HOSTS:
        return "use https:// links (http:// is only allowed for localhost and example.com)"
    if host in HTTP_ALLOWED_HOSTS:
        return None
    if not host.isascii() or "xn--" in host:
        return "internationalized or punycode host names are not allowed (homograph risk)"
    if IP_HOST.match(host):
        return "links to raw IP addresses are not allowed"
    if host in URL_SHORTENERS:
        return "URL shorteners hide the destination; link to the real page"
    last = parts.path.rsplit("/", 1)[-1].lower()
    if "." in last and last.rsplit(".", 1)[-1] in DOWNLOAD_EXTENSIONS:
        return "links that download executables, archives, or media files are not allowed"
    if any(url.lower().startswith(prefix) for prefix in allowed_prefixes):
        return None
    if host_matches(host, RESTRICTED_HOSTS):
        return f"host {host!r} serves arbitrary user content; approve the exact URL in governance/policy/allowed-link-prefixes.txt"
    if not host_matches(host, allowed_domains):
        return f"domain {host!r} is not in governance/policy/allowed-link-domains.txt; a maintainer must review and add it"
    return None


def check_markdown(rel: str, markdown: str, allowed_domains: set[str], allowed_prefixes: set[str] = frozenset()) -> list[Finding]:
    findings: list[Finding] = []
    for number, line in prose_lines(markdown):
        if IMAGE.search(line):
            findings.append(Finding(rel, number, "media", "images are not allowed; describe the idea in text or use a Mermaid diagram"))
        urls = [m.group(1) for m in AUTOLINK.finditer(line)]
        without_autolinks = AUTOLINK.sub("", line)
        for tag in HTML_TAG.finditer(without_autolinks):
            name = tag.group(2).lower()
            attributes = tag.group(3) or ""
            if name not in ALLOWED_HTML:
                findings.append(Finding(rel, number, "raw-html", f"raw HTML <{name}> is not allowed outside code blocks"))
            elif attributes.strip():
                findings.append(Finding(rel, number, "raw-html", f"attributes on <{name}> are not allowed"))
        urls += [m.group(1) for m in LINK_DEST.finditer(line)]
        ref = REF_DEF.match(line)
        if ref:
            urls.append(ref.group(1))
        urls += [m.group(1) for m in BARE_URL.finditer(without_autolinks)]
        seen = set()
        for url in urls:
            if url in seen or not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", url):
                continue
            seen.add(url)
            problem = check_url(url, allowed_domains, allowed_prefixes)
            if problem:
                findings.append(Finding(rel, number, "link-safety", f"{problem}: {url[:120]}"))
    return findings


def validate(root: Path, policy_root: Path | None = None) -> list[Finding]:
    root = root.resolve()
    policy = (policy_root or root).resolve()
    allowed_domains = load_list(policy / "governance/policy/allowed-link-domains.txt")
    allowed_prefixes = load_list(policy / "governance/policy/allowed-link-prefixes.txt")
    findings: list[Finding] = []
    for mode, rel in list_files(root):
        file_findings = check_file(root, mode, rel)
        findings += file_findings
        blocking = any(f.rule in {"binary"} for f in file_findings) or mode in {"120000", "160000"}
        if rel.endswith(".md") and not blocking:
            text = unicodedata.normalize("NFC", (root / rel).read_text(encoding="utf-8"))
            findings += check_markdown(rel, text, allowed_domains, allowed_prefixes)
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", type=Path, help="repository checkout to scan (read-only)")
    parser.add_argument("--policy-root", type=Path, help="trusted checkout that supplies governance/policy lists (default: --root)")
    parser.add_argument("--json", type=Path, help="also write findings as JSON")
    args = parser.parse_args()
    findings = validate(args.root, args.policy_root)
    if args.json:
        args.json.write_text(json.dumps([f.__dict__ for f in findings], indent=2) + "\n", encoding="utf-8")
    for finding in findings:
        print(finding.render())
    if findings:
        print(f"Repository policy failed with {len(findings)} finding(s). See governance/content-policy.md.")
        return 1
    print("Repository policy passed: allowed file types, safe Markdown, and safe links.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
