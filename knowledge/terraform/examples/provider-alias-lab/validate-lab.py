"""Validate the bundled local-file provider alias and dependency lock in a temporary copy."""
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--terraform", default="terraform")
args = parser.parse_args()
source = Path(__file__).resolve().parent
cli = shutil.which(args.terraform) or str(Path(args.terraform).resolve())
results = []

with tempfile.TemporaryDirectory(prefix="kb-terraform-") as temporary:
    work = Path(temporary).resolve()
    if not work.is_relative_to(Path(tempfile.gettempdir()).resolve()):
        raise RuntimeError("Temporary run escaped the intended temporary directory")
    shutil.copytree(source, work, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".terraform", "*.tfstate*", "terraform.tfstate.d", "*.tfplan", "artifact.json", "__pycache__"))
    env = {key: value for key, value in os.environ.items() if not key.startswith("TF_")}
    env.update(TF_INPUT="0", TF_IN_AUTOMATION="1", CHECKPOINT_DISABLE="1")
    config = work / "empty.tfrc"
    config.write_text("", encoding="utf-8")
    env["TF_CLI_CONFIG_FILE"] = str(config)

    def run(*command, codes=(0,)):
        result = subprocess.run([cli, *command], cwd=work, env=env,
                                capture_output=True, text=True, encoding="utf-8", errors="replace")
        if result.returncode not in codes:
            raise RuntimeError("Terraform command failed: " + " ".join(command) + "\n" + result.stdout + result.stderr)
        return result

    def plan(name, *options, codes=(0, 2)):
        result = run("plan", "-input=false", "-no-color", "-detailed-exitcode", "-out=" + name, *options, codes=codes)
        payload = json.loads(run("show", "-json", name).stdout)
        return result.returncode, payload

    def managed(payload):
        return [change for change in payload.get("resource_changes", []) if change["mode"] == "managed"]

    results.append({"terraform": json.loads(run("version", "-json").stdout)["terraform_version"]})
    run("fmt", "-recursive", "-check")

    run("init", "-input=false", "-no-color", "-lockfile=readonly")
    run("validate", "-no-color")
    code, initial = plan("create.tfplan", codes=(2,))
    assert len(managed(initial)) == 1
    assert managed(initial)[0]["provider_name"] == "registry.terraform.io/hashicorp/local"
    run("apply", "-input=false", "-no-color", "create.tfplan")
    artifact = work / "artifact.json"
    assert json.loads(artifact.read_text(encoding="utf-8"))["secret"] is False
    code, unchanged = plan("unchanged.tfplan", codes=(0,))
    configuration = initial["configuration"]["root_module"]["module_calls"]["artifact"]["module"]
    assert configuration["resources"][0]["provider_config_key"] == "local.artifacts"
    lock = (work / ".terraform.lock.hcl").read_text(encoding="utf-8")
    assert 'version     = "2.9.1"' in lock
    results.append({"provider": "hashicorp/local 2.9.1", "alias": "root local.artifacts -> child local.writer", "plan_codes": [2, 0], "artifact": "local JSON file created and parsed"})
    run("destroy", "-input=false", "-auto-approve", "-no-color")
    assert not artifact.exists()
    assert not run("state", "list").stdout.strip()

print(json.dumps({"results": results, "cleanup": "artifact destroyed, state empty, temporary copy removed"}, indent=2))
