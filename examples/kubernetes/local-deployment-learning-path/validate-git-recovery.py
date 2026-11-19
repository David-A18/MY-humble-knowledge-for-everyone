"""Exercise staged/unstaged Git recovery using a disposable manifest copy."""

from pathlib import Path
import json
import os
import shutil
import subprocess
import tempfile

source = Path(__file__).resolve().parent / "deployment.yaml"
env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
with tempfile.TemporaryDirectory(prefix="kb-git-learning-") as temporary:
    work = Path(temporary).resolve()
    if not work.is_relative_to(Path(tempfile.gettempdir()).resolve()):
        raise RuntimeError("Exercise directory escaped the temporary root")
    shutil.copy2(source, work / source.name)

    def git(*command, codes=(0,)):
        result = subprocess.run(["git", "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false", *command], cwd=work, env=env, text=True, encoding="utf-8", errors="replace", capture_output=True)
        if result.returncode not in codes:
            raise RuntimeError("Git exercise failed: " + " ".join(command) + "\n" + result.stdout + result.stderr)
        return result

    version = git("--version").stdout.strip()
    git("init", "-b", "learning")
    git("config", "user.name", "Local learning fixture")
    git("config", "user.email", "learner@example.invalid")
    git("add", "deployment.yaml")
    git("commit", "-m", "local teaching baseline")
    head = git("rev-parse", "HEAD").stdout
    baseline = (work / source.name).read_bytes()
    text = (work / source.name).read_text(encoding="utf-8")
    changed = text.replace("image: nginx:", "image: invalid-learning-image:", 1)
    if changed == text:
        raise RuntimeError("No deliberate fixture edit was made")
    (work / source.name).write_text(changed, encoding="utf-8", newline="\n")
    git("add", "deployment.yaml")
    git("diff", "--cached", "--quiet", codes=(1,))
    git("restore", "--staged", "deployment.yaml")
    git("diff", "--cached", "--quiet")
    git("diff", "--quiet", codes=(1,))
    if (work / source.name).read_bytes() == baseline:
        raise RuntimeError("Unstaging incorrectly discarded the working edit")
    git("restore", "deployment.yaml")
    if (work / source.name).read_bytes() != baseline or git("status", "--porcelain").stdout:
        raise RuntimeError("Working tree was not restored to the baseline")
    if git("rev-parse", "HEAD").stdout != head:
        raise RuntimeError("Recovery rewrote the teaching commit")

print(json.dumps({"git": version, "staged_edit_detected": True, "unstage_preserves_edit": True,
                  "restore_recovers_bytes": True, "head_unchanged": True,
                  "cleanup": "temporary repository removed; shared checkout untouched"}, indent=2))
