"""Install the lab's checksum-pinned Linux amd64 tools into an empty directory."""

from pathlib import Path
import argparse
import hashlib
import io
import json
import platform
import tarfile
import time
import urllib.request


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    args = parser.parse_args()
    if platform.system() != "Linux" or platform.machine() not in ("x86_64", "amd64"):
        raise SystemExit("This installer supports Linux amd64 only; use the documented manual versions elsewhere")
    target = args.directory.resolve()
    target.mkdir(parents=True, exist_ok=True)
    if any(target.iterdir()):
        raise SystemExit("Refusing to overwrite a nonempty tools directory")
    versions = json.loads(Path(__file__).with_name("lab-versions.json").read_text(encoding="utf-8"))
    for tool in versions["tools"]:
        for attempt in range(3):
            try:
                request = urllib.request.Request(tool["url"], headers={"User-Agent": "KnowledgeBaseLab"})
                with urllib.request.urlopen(request, timeout=90) as response:
                    data = response.read()
                break
            except OSError:
                if attempt == 2:
                    raise
                time.sleep(2)
        if hashlib.sha256(data).hexdigest() != tool["sha256"]:
            raise RuntimeError("Release checksum mismatch: " + tool["name"])
        if tool["archive"]:
            with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
                candidates = [member for member in archive.getmembers()
                              if member.isfile() and Path(member.name).name == tool["name"]]
                if len(candidates) != 1:
                    raise RuntimeError("Expected exactly one executable in " + tool["name"])
                data = archive.extractfile(candidates[0]).read()
        destination = target / tool["name"]
        destination.write_bytes(data)
        destination.chmod(0o755)
        print("Installed", tool["name"], tool["version"], "with verified release SHA256")


if __name__ == "__main__":
    main()
