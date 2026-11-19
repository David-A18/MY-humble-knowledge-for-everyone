"""Exercise real diff, schema, and policy tools without contacting a cluster."""

from pathlib import Path
import argparse
import copy
import json
import subprocess
import tempfile
import yaml

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run(*command, codes=(0,)):
    result = subprocess.run(list(command), capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    require(result.returncode in codes, "Command failed: " + " ".join(command) + "\n" + result.stdout + result.stderr)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for tool in ("dyff", "kubeconform", "conftest"):
        parser.add_argument("--" + tool, default=tool)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    versions = json.loads((HERE / "lab-versions.json").read_text(encoding="utf-8"))
    actual = {"dyff": run(args.dyff, "version").stdout.strip(),
              "kubeconform": run(args.kubeconform, "-v").stdout.strip(),
              "conftest": run(args.conftest, "--version").stdout.strip()}
    for tool in versions["tools"]:
        if tool["name"] in actual:
            require(tool["version"].removeprefix("v") in actual[tool["name"]], "Unexpected tool version: " + tool["name"])
    report = {"versions": actual, "schema_revision": versions["schema_revision"], "checks": {}}
    good, reordered, broken = (str(HERE / name) for name in ("service.json", "service-reordered.json", "service-broken.json"))
    textual = run("git", "diff", "--no-index", "--", good, reordered, codes=(1,))
    require(bool(textual.stdout.strip()), "Expected a textual formatting difference")
    report["checks"]["git_detects_formatting_change"] = True
    run(args.dyff, "between", "--set-exit-code", good, reordered)
    report["checks"]["dyff_ignores_mapping_order"] = True
    changed = run(args.dyff, "between", "--set-exit-code", good, broken, codes=(1,))
    require("targetPort" in changed.stdout and "81" in changed.stdout, "Semantic diff must expose changed targetPort")
    report["checks"]["dyff_detects_target_port"] = True
    with tempfile.TemporaryDirectory(prefix="kb-manifest-offline-") as directory:
        temporary = Path(directory)
        schema = ("https://raw.githubusercontent.com/yannh/kubernetes-json-schema/" + versions["schema_revision"]
                  + "/{{.NormalizedKubernetesVersion}}-standalone{{.StrictSuffix}}/{{.ResourceKind}}{{.KindSuffix}}.json")

        def validate(*files, codes=(0,)):
            result = run(args.kubeconform, "-strict", "-summary", "-output", "json", "-kubernetes-version",
                         versions["kubernetes"].removeprefix("v"), "-cache", str(temporary), "-schema-location", schema,
                         *map(str, files), codes=codes)
            return json.loads(result.stdout)

        positive = validate(HERE / "app.yaml", good, reordered, broken)
        require(positive["summary"]["valid"] == 4 and positive["summary"]["skipped"] == 0, "All four fixtures must pass schema validation")
        report["checks"]["schema_accepts_even_wrong_routing"] = True
        invalid = copy.deepcopy(yaml.safe_load((HERE / "app.yaml").read_text(encoding="utf-8")))
        invalid["spec"]["replicas"] = "two"
        path = temporary / "invalid-replicas.json"
        path.write_text(json.dumps(invalid), encoding="utf-8")
        negative = validate(path, codes=(1,))
        require(negative["summary"]["invalid"] == 1 and "replicas" in json.dumps(negative), "Reject invalid replicas type, not a network/schema-download error")
        report["checks"]["schema_rejects_invalid_type"] = True
        custom = temporary / "missing-schema.json"
        custom.write_text(json.dumps({"apiVersion": "learning.invalid/v1", "kind": "TeachingWidget", "metadata": {"name": "no-schema"}}), encoding="utf-8")
        unknown = validate(custom, codes=(1,))
        require(unknown["summary"]["errors"] == 1 and unknown["summary"]["skipped"] == 0, "Missing custom schema must remain a coverage error")
        report["checks"]["missing_schema_is_error"] = True
        run(args.conftest, "test", str(HERE / "app.yaml"), good, broken, "--policy", str(HERE / "policy"))
        report["checks"]["ownership_policy_accepts_owned_fixtures"] = True
        invalid["spec"]["replicas"] = 1
        del invalid["metadata"]["labels"]["team"]
        path.write_text(json.dumps(invalid), encoding="utf-8")
        denied = run(args.conftest, "test", str(path), "--policy", str(HERE / "policy"), codes=(1,))
        require("metadata.labels.team" in denied.stdout + denied.stderr, "Policy failure must name the ownership rule")
        report["checks"]["ownership_policy_rejects_missing_label"] = True
    report["status"] = "passed"
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
