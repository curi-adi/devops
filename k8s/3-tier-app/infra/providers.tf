provider "aws" {
  region = "ap-south-1"
}

# Uses ~/.kube/config which is set up by aws eks update-kubeconfig in the workflow.
# The kubeconfig exec authenticator calls aws eks get-token on every API call,
# so the token never expires during long Helm installs.
provider "kubernetes" {
  config_path = "~/.kube/config"
}

provider "helm" {
  kubernetes = {
    config_path = "~/.kube/config"
  }
}
