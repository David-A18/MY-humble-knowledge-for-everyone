"""Verify the beginner terraform_data lifecycle in an isolated local directory."""

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
cli = shutil.which(args.terraform) or str(Path(args.terraform).resolve())
source = Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix="kb-state-learning-") as temporary:
    work = Path(temporary).resolve()
    if not work.is_relative_to(Path(tempfile.gettempdir()).resolve()):
        raise RuntimeError("Exercise directory escaped the temporary root")
    for name in ("main.tf", ".gitignore"):
        shutil.copy2(source / name, work / name)
    env = {k: v for k, v in os.environ.items() if not k.startswith("TF_")}
    env.update(TF_INPUT="0", TF_IN_AUTOMATION="1", CHECKPOINT_DISABLE="1")
    config = work / "empty.tfrc"
    config.write_text("", encoding="utf-8")
    env["TF_CLI_CONFIG_FILE"] = str(config)

    def run(*command, codes=(0,)):
        result = subprocess.run([cli, *command], cwd=work, env=env, text=True, encoding="utf-8", errors="replace", capture_output=True)
        if result.returncode not in codes:
            raise RuntimeError("Terraform exercise failed: " + " ".join(command) + "\n" + result.stdout + result.stderr)
        return result

    def plan(name, *options, code):
        run("plan", "-input=false", "-no-color", "-detailed-exitcode", "-out=" + name, *options, codes=(code,))
        return json.loads(run("show", "-json", name).stdout)

    def managed(payload):
        return [r for r in payload.get("resource_changes", []) if r["mode"] == "managed"]

    version = json.loads(run("version", "-json").stdout)["terraform_version"]
    run("init", "-input=false", "-no-color")
    run("fmt", "-check")
    run("validate", "-no-color")
    first = managed(plan("create.tfplan", code=2))
    if len(first) != 1 or first[0]["address"] != "terraform_data.release" or first[0]["change"]["actions"] != ["create"]:
        raise RuntimeError("Expected exactly one local terraform_data create")
    run("apply", "-input=false", "-no-color", "create.tfplan")
    original = json.loads(run("show", "-json").stdout)["values"]["root_module"]["resources"][0]
    plan("unchanged.tfplan", code=0)
    changed = managed(plan("change.tfplan", "-var=release_version=1.1.0", code=2))
    if len(changed) != 1 or changed[0]["change"]["actions"] != ["update"]:
        raise RuntimeError("Version input should update in place")
    run("apply", "-input=false", "-no-color", "change.tfplan")
    state = json.loads(run("show", "-json").stdout)["values"]["root_module"]["resources"][0]
    output = json.loads(run("output", "-json").stdout)["release_summary"]["value"]
    if state["values"]["id"] != original["values"]["id"] or output["version"] != "1.1.0":
        raise RuntimeError("Expected same resource ID and updated release output")
    plan("same-input.tfplan", "-var=release_version=1.1.0", code=0)
    reverted_input = managed(plan("default-input.tfplan", code=2))
    if reverted_input[0]["change"]["after"]["input"]["version"] != "1.0.0":
        raise RuntimeError("CLI variable should not persist as configuration")
    destroy = managed(plan("destroy.tfplan", "-destroy", code=2))
    if len(destroy) != 1 or destroy[0]["change"]["actions"] != ["delete"]:
        raise RuntimeError("Destroy must affect only the teaching state object")
    run("apply", "-input=false", "-no-color", "destroy.tfplan")
    if run("state", "list").stdout.strip():
        raise RuntimeError("Cleanup did not leave empty managed state")

print(json.dumps({"terraform": version, "create": 1, "update_in_place": True, "no_change_exit": 0,
                  "changed_exit": 2, "cli_variable_not_persisted": True,
                  "cleanup": "managed state empty; temporary files removed; no external resources"}, indent=2))
