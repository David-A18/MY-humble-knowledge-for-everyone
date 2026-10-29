terraform {
  required_version = ">= 1.6.0, < 2.0.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "= 2.9.1"
    }
  }
}

provider "local" {
  alias = "artifacts"
}

module "artifact" {
  source = "./child"
  providers = {
    local.writer = local.artifacts
  }
  target_file = abspath("${path.root}/artifact.json")
}

output "artifact_path" {
  value = module.artifact.path
}
