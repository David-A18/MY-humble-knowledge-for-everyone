terraform {
  required_providers {
    local = {
      source                = "hashicorp/local"
      version               = ">= 2.9.1, < 3.0.0"
      configuration_aliases = [local.writer]
    }
  }
}

variable "target_file" {
  type = string
}

resource "local_file" "artifact" {
  provider = local.writer
  filename = var.target_file
  content = jsonencode({
    purpose = "local provider alias teaching example"
    secret  = false
  })
}

output "path" {
  value = local_file.artifact.filename
}
