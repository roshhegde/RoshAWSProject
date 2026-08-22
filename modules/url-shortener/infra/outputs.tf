output "api_url" {
  description = "Base URL of the deployed HTTP API."
  value       = aws_apigatewayv2_api.http.api_endpoint
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.urls.name
}
