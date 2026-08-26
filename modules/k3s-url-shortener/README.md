# k3s URL Shortener

A single-node Kubernetes learning project running on one AWS `t3.micro`.

## Project layout

The Terraform files are split by responsibility:

```text
infra/
|-- backend.tf          S3 state and DynamoDB locking
|-- provider.tf         Terraform and AWS provider requirements
|-- data.tf             Ubuntu AMI lookup
|-- security_group.tf   SSH, Kubernetes API, and NodePort rules
|-- instance.tf         EC2 node and k3s bootstrap script
|-- variables.tf        Region, key pair, and operator IP inputs
`-- outputs.tf          Node connection details
```

Terraform state is stored remotely and encrypted in S3 at:

```text
s3://roshaws-url-shortener-terraform-state-212822970405/k3s-url-shortener/terraform.tfstate
```

The DynamoDB table `roshaws-url-shortener-terraform-locks` prevents concurrent Terraform operations.

The old `infra/terraform.tfstate` file may still be present locally from the initial setup, but it is no longer the active state file. It is ignored by Git and can be removed after confirming the S3 object exists.

## Step 1: Provision the node

This step creates an Ubuntu EC2 instance and installs k3s. It does not deploy the application yet.

Find your public IPv4 address:

```bash
curl -4 ifconfig.me
```

Create `infra/terraform.tfvars` locally and do not commit it:

```hcl
ssh_key_name = "your-existing-ec2-key-pair"
operator_cidr = "YOUR_PUBLIC_IP/32"
```

Then run:

```bash
terraform -chdir=infra init
terraform -chdir=infra fmt -check
terraform -chdir=infra validate
terraform -chdir=infra plan
```

Review the plan before applying it:

```bash
terraform -chdir=infra apply
```

## Step 2: Connect to Kubernetes

After the instance is ready, copy the kubeconfig using the output command. Replace the placeholder PEM filename first:

```bash
scp -i ~/.ssh/your-key.pem ubuntu@PUBLIC_IP:.kube/config ~/.kube/config-k3s
export KUBECONFIG=~/.kube/config-k3s
kubectl get nodes
```

The node should become `Ready` after k3s finishes installing.

## Cleanup

Destroy the node when finished to avoid ongoing AWS charges:

```bash
terraform -chdir=infra destroy
```
