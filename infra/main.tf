provider "aws" {
  region = var.region
  default_tags {
    tags = {
      environment = "dev"
      owner       = local.vars.owner
      project     = "tha-vibhavari-bellutagi-assignment"
    }
  }
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.62.0"
    }
  }
}

locals {
  vars    = yamldecode(file("./input_vars.yaml"))
}