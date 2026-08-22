# AWS Organizations and branch-based deployment

This repository is set up to use a simple branch-to-environment model:

- develop -> nonprod
- main -> prod

## AWS Organizations setup
1. Create an AWS Organizations root.
2. Create two OUs:
   - nonprod
   - prod
3. Add one AWS account to each OU.
4. Create an IAM role in each account that CircleCI can assume, for example:
   - CircleCIRole
5. Grant that role permissions to manage the Terraform resources you want to deploy.

## CircleCI environment variables
Add these in CircleCI project settings or a shared context:

- AWS_NONPROD_ROLE_ARN
- AWS_PROD_ROLE_ARN
- AWS_DEFAULT_REGION

## Branch mapping
- Pushes or merges to develop deploy to the nonprod account.
- Pushes or merges to main deploy to the prod account.
- The commit message can still select a module, for example:
  - tf_init,s3
  - tf_init,ec2
  - tf_init,url-shortener
