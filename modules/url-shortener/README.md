# Serverless URL Shortener

A portfolio project that turns long URLs into short redirect links. It is deployed with Terraform and validated/deployed by CircleCI.

## Architecture

`Client -> API Gateway HTTP API -> Lambda -> DynamoDB`

Lambda logs go to a CloudWatch Log Group with a seven-day retention period. DynamoDB uses on-demand billing so there is no idle database instance.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/shorten` | Create a short URL from `{ "url": "https://example.com" }` |
| `GET` | `/{short_code}` | Respond with a `302` redirect |

## Local checks

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
terraform -chdir=infra init -backend=false
terraform -chdir=infra fmt -check -recursive
terraform -chdir=infra validate
```

## First deployment

1. Configure the AWS CLI with a least-privilege developer identity and set your desired region in `infra/variables.tf`.
2. Run `terraform -chdir=infra init`, then `terraform -chdir=infra apply`.
3. Copy the `api_url` output and test it:

```bash
curl -X POST "$API_URL/shorten" \
  -H 'content-type: application/json' \
  -d '{"url":"https://example.com"}'
```

4. Test the returned `short_url` in a browser or with `curl -I`.

## CircleCI setup

This project uses the repository-level [CircleCI configuration](../../.circleci/config.yml). Add dedicated URL-shortener test, validation, and deployment jobs there rather than creating a second configuration file inside this project. Configure CircleCI OpenID Connect to allow the deployment role to be assumed; do not store long-lived AWS access keys in CircleCI.

The current repository pipeline selects this stack when the commit message contains `tf_init,url-shortener`. It validates the configuration, publishes a `terraform-plan.txt` artifact, and requires manual approval before applying changes on `develop` or `main`.

Before enabling the deploy job, add a remote Terraform backend (S3 plus DynamoDB state locking) so local and CI state cannot diverge.

## Cost cleanup

When you finish experimenting, run:

```bash
terraform -chdir=infra destroy
```

Confirm that the CloudWatch Log Group and DynamoDB table are deleted. API Gateway, Lambda invocations, DynamoDB requests, and logs can all create charges after relevant free allowances or credits are exhausted.
