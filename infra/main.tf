provider "aws" {
  region = "eu-west-1"
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
  account_id     = local.vars["account_id"]
}