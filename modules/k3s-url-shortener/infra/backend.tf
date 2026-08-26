terraform {
  backend "s3" {
    bucket         = "roshaws-url-shortener-terraform-state-212822970405"
    key            = "k3s-url-shortener/terraform.tfstate"
    region         = "ap-south-1"
    encrypt        = true
    dynamodb_table = "roshaws-url-shortener-terraform-locks"
  }
}