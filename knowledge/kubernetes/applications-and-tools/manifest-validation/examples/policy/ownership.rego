package main

import rego.v1

deny contains msg if {
    not input.metadata.labels.team
    msg := "metadata.labels.team is required"
}
