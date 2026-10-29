run "release_contract" {
  command = apply
  variables {
    environment = "test"
  }
  assert {
    condition     = toset(keys(output.releases)) == toset(["api", "worker"])
    error_message = "Expected exactly the two stable service keys."
  }
  assert {
    condition     = output.releases.api.environment == "test" && output.releases.api.replicas == 2
    error_message = "The child module must preserve the caller's release contract."
  }
}

run "reject_production_label" {
  command = plan
  variables {
    environment = "production"
  }
  expect_failures = [var.environment]
}

run "reject_fractional_replicas" {
  command = plan
  variables {
    services = {
      api = { version = "1.0.0", replicas = 0.5 }
    }
  }
  expect_failures = [var.services]
}
