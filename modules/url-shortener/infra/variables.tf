variable "aws_region" {
  description = "AWS Region for all resources."
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Short name used to identify resources."
  type        = string
  default     = "url-shortener"
}

variable "environment" {
  description = "Deployment environment supplied by the CI pipeline."
  type        = string
  default     = "nonprod"
}
