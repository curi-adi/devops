terraform {
  backend "s3" {
    bucket = "state-bucket-YOUR_ACCOUNT_ID"
    key    = "aditya/week11/lambda-terraform-projects/terraform.tfstate"
    region = "ap-south-1"
  }
}

provider "aws" {
  region = "ap-south-1"
}
