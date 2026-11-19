terraform {
  required_version = ">= 1.6.0, < 2.0.0"
}

variable "name" {
  type = string
}
variable "environment" {
  type = string
}
variable "workspace" {
  type = string
}
variable "release_version" {
  type = string
}
variable "replicas" {
  type = number
}

locals {
  record = {
    name        = var.name
    environment = var.environment
    workspace   = var.workspace
    version     = var.release_version
    replicas    = var.replicas
  }
}

resource "terraform_data" "release" {
  input = local.record
}

output "record" {
  value = terraform_data.release.output
}
