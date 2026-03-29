provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      repo      = "aditya-bootcamp"
      terraform = "true"
    }
  }
}

# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY


terraform {
  backend "s3" {
    bucket  = "state-bucket-768093818017"
    key     = "aditya/week6/infra/terraform.tfstate"
    region  = "ap-south-1"
    encrypt = true
  }
}