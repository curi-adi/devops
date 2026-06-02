terraform {
  backend "s3" {
    bucket = "state-bucket-YOUR_ACCOUNT_ID"
    key    = "jan26-devops-bootcamp/week8/infra/terraform.tfstate"
    region = "ap-south-1"
  }
}