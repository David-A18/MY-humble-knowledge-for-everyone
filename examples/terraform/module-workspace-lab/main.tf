terraform {
  required_version = ">= 1.6.0, < 2.0.0"
}

variable "environment" {
  description = "Teaching label, deliberately restricted to non-production values."
  type        = string
  default     = "learning"
  validation {
    condition     = contains(["learning", "test"], var.environment)
    error_message = "Use learning or test for this local-only exercise."
  }
}

variable "services" {
  description = "Stable service keys; versions and positive integral replica counts."
  type = map(object({
    version  = string
    replicas = number
  }))
  default = {
    api    = { version = "1.0.0", replicas = 2 }
    worker = { version = "1.0.0", replicas = 1 }
  }
  validation {
    condition = alltrue([
      for service in values(var.services) :
      service.replicas >= 1 && floor(service.replicas) == service.replicas
    ])
    error_message = "Each service must have a positive whole-number replica count."
  }
}

module "release" {
  source   = "./child"
  for_each = var.services

  name            = each.key
  environment     = var.environment
  workspace       = terraform.workspace
  release_version = each.value.version
  replicas        = each.value.replicas
}

output "releases" {
  description = "Non-sensitive teaching records indexed by stable service names."
  value       = { for name, release in module.release : name => release.record }
}
