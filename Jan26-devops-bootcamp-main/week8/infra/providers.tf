terraform {
  backend "s3" {
    bucket = "state-bucket-768093818017"
    key    = "jan26-devops-bootcamp/week8/infra/terraform.tfstate"
    region = "ap-south-1"
  }
}