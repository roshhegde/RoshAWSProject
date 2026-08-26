variable "aws_region" {
  description = "AWS region for the learning node."
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Name prefix for the AWS resources."
  type        = string
  default     = "k3s-url-shortener"
}

variable "ssh_key_name" {
  description = "Existing EC2 key pair name used for SSH access."
  type        = string
}

variable "operator_cidr" {
  description = "Public IPv4 CIDR allowed to SSH and use the Kubernetes API."
  type        = string
}
