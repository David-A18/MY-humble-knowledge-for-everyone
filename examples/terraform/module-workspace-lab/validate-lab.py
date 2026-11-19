"""Exercise the bundled module/workspace lab in a disposable local directory."""
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

    run("init", "-input=false", "-no-color")
    run("validate", "-no-color")
    test = run("test", "-no-color")
    assert "3 passed" in test.stdout, test.stdout
    results.append({"terraform_tests": "3 passed: release contract and two expected validation failures"})
    rejected = run("plan", "-input=false", "-no-color", "-var=environment=production", codes=(1,))
    assert "Use learning or test" in rejected.stderr
    results.append({"invalid_input_plan": "exit 1; invalid environment rejected"})
    code, initial = plan("create.tfplan", codes=(2,))
    assert len(managed(initial)) == 2
    assert all(change["change"]["actions"] == ["create"] for change in managed(initial))
    run("apply", "-input=false", "-no-color", "create.tfplan")
    code, unchanged = plan("unchanged.tfplan", codes=(0,))
    default_state = json.loads(run("show", "-json").stdout)
    original_ids = {m["address"]: m["resources"][0]["values"]["id"] for m in default_state["values"]["root_module"]["child_modules"]}
    code, added = plan("add.tfplan", "-var-file=add-service.tfvars.example", codes=(2,))
    assert sum(change["change"]["actions"] == ["create"] for change in managed(added)) == 1
    assert all(change["change"]["actions"] in (["create"], ["no-op"]) for change in managed(added))
    results.append({"stable_keys": "adding batch plans one create, no replacement of api/worker", "plan_codes": [2, 0, 2]})

    child = work / "child/main.tf"
    text = child.read_text(encoding="utf-8").replace('"terraform_data" "release"', '"terraform_data" "entry"').replace("terraform_data.release.output", "terraform_data.entry.output")
    text += '\nmoved {\n  from = terraform_data.release\n  to   = terraform_data.entry\n}\n'
    child.write_text(text, encoding="utf-8")
    code, moved = plan("move.tfplan")
    assert sum("previous_address" in change for change in managed(moved)) == 2
    assert all(change["change"]["actions"] == ["no-op"] for change in managed(moved))
    run("apply", "-input=false", "-no-color", "move.tfplan")
    moved_state = json.loads(run("show", "-json").stdout)
    moved_ids = {m["address"]: m["resources"][0]["values"]["id"] for m in moved_state["values"]["root_module"]["child_modules"]}
    assert original_ids == moved_ids
    results.append({"moved_block": "two address moves preserve both object IDs; no create/delete"})

    run("workspace", "new", "preview")
    empty = run("state", "list", codes=(0, 1))
    assert (empty.returncode == 0 and not empty.stdout.strip()) or (empty.returncode == 1 and "No state file was found" in empty.stderr)
    code, preview = plan("preview.tfplan", codes=(2,))
    assert all(change["change"]["actions"] == ["create"] for change in managed(preview))
    run("apply", "-input=false", "-no-color", "preview.tfplan")
    records = json.loads(run("output", "-json", "releases").stdout)
    assert records["api"]["workspace"] == "preview"
    run("destroy", "-input=false", "-auto-approve", "-no-color")
    assert not run("state", "list").stdout.strip()
    run("workspace", "select", "default")
    code, default = plan("default.tfplan", codes=(0,))
    run("workspace", "delete", "preview")
    run("destroy", "-input=false", "-auto-approve", "-no-color")
    assert not run("state", "list").stdout.strip()
    results.append({"workspace_isolation": "preview starts empty; default unchanged; both states destroyed; preview deleted"})

print(json.dumps({"results": results, "cleanup": "temporary copy removed; no external infrastructure"}, indent=2))
