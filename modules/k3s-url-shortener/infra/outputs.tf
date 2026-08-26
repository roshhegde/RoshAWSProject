output "public_ip" {
  description = "Public IP address of the k3s node."
  value       = aws_instance.k3s.public_ip
}

output "ssh_command" {
  description = "SSH command for the k3s node."
  value       = "ssh -i ~/.ssh/REPLACE_WITH_KEY.pem ubuntu@${aws_instance.k3s.public_ip}"
}

output "kubeconfig_command" {
  description = "Copy and activate the remote kubeconfig on macOS or Linux."
  value       = "scp -i ~/.ssh/REPLACE_WITH_KEY.pem ubuntu@${aws_instance.k3s.public_ip}:.kube/config ~/.kube/config-k3s && export KUBECONFIG=~/.kube/config-k3s"
}
