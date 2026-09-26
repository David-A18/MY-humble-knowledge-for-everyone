terraform {
  required_version = ">= 1.4.0"
}

variable "environment" {
  type        = string
  description = "Learning environment name recorded in local Terraform state."
  default     = "learning"
}

variable "release_version" {
  type        = string
  description = "Example application version recorded in local Terraform state."
  default     = "1.0.0"
}

locals {
  app_name = "kb-local-example"
}

resource "terraform_data" "release" {
  input = {
    app_name    = local.app_name
    environment = var.environment
    version     = var.release_version
  }
}

output "release_summary" {
  description = "Values stored by the local Terraform data resource."
  value       = terraform_data.release.output
}
