# S3 Module

Simple reusable Terraform module to create an S3 bucket with optional versioning and tags.

Usage example:

```
module "bucket" {
  source             = "../modules/s3"
  bucket_name        = "my-example-bucket"
  versioning_enabled = true
  tags = {
    Project = "example"
  }
}
```

Notes:
- Do not commit `.terraform` directories or provider binaries.
- The module merges `default_tags` with `tags` passed in.
