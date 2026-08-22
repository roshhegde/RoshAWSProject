variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "acl" {
  description = "Canned ACL for the S3 bucket"
  type        = string
  default     = "private"
}

variable "versioning_enabled" {
  description = "Enable S3 bucket versioning"
  type        = bool
  default     = true
}

variable "force_destroy" {
  description = "Allow bucket to be destroyed even if non-empty"
  type        = bool
  default     = false
}

variable "tags" {
  description = "Additional tags to apply to the bucket"
  type        = map(string)
  default     = {}
}

variable "default_tags" {
  description = "Default tags applied to every resource"
  type        = map(string)
  default = {
    Environment = "Dev"
    ManagedBy   = "Terraform"
    Owner       = "Roshan"
  }
}

variable "environment" {
  description = "Deployment environment supplied by the CI pipeline."
  type        = string
  default     = "nonprod"
}
