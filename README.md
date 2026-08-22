# RoshAWSProject
This is used for building AWS Infra.

## Branching guidance
For future work, follow the branch workflow described in [docs/branching-strategy.md](docs/branching-strategy.md).

## AWS Organizations deployment model
This repository is designed for a branch-based deployment flow:
- develop -> nonprod account
- main -> prod account

See [docs/aws-org-branching.md](docs/aws-org-branching.md) for the AWS Organizations and CircleCI setup.

## Projects

- [Serverless URL Shortener](projects/url-shortener/README.md) — API Gateway, Lambda, DynamoDB, Terraform, and CircleCI.
