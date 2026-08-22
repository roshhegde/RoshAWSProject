"""AWS Lambda handler for the serverless URL shortener."""

import base64
import json
import os
import secrets
from urllib.parse import urlparse

import boto3

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])


def response(status_code, body=None, headers=None):
    """Return an API Gateway HTTP API (payload v2) response."""
    result = {"statusCode": status_code, "headers": headers or {}}
    if body is not None:
        result["body"] = json.dumps(body)
        result["headers"]["content-type"] = "application/json"
    return result


def is_valid_url(value):
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def generate_code():
    """Generate a compact, URL-safe seven-character code."""
    return base64.urlsafe_b64encode(secrets.token_bytes(6)).decode().rstrip("=")[:7]


def create_short_url(event):
    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return response(400, {"message": "Request body must be valid JSON."})

    original_url = body.get("url")
    if not isinstance(original_url, str) or not is_valid_url(original_url):
        return response(400, {"message": "'url' must be a valid http or https URL."})

    short_code = generate_code()
    table.put_item(
        Item={"short_code": short_code, "original_url": original_url},
        ConditionExpression="attribute_not_exists(short_code)",
    )
    base_url = f"https://{event['requestContext']['domainName']}"
    return response(201, {"short_code": short_code, "short_url": f"{base_url}/{short_code}"})


def redirect(event):
    short_code = event["pathParameters"]["short_code"]
    item = table.get_item(Key={"short_code": short_code}).get("Item")
    if item is None:
        return response(404, {"message": "Short URL not found."})

    return response(302, headers={"location": item["original_url"], "cache-control": "no-store"})


def lambda_handler(event, _context):
    """Route POST /shorten and GET /{short_code}."""
    method = event["requestContext"]["http"]["method"]
    if method == "POST" and event["rawPath"] == "/shorten":
        return create_short_url(event)
    if method == "GET" and event.get("pathParameters", {}).get("short_code"):
        return redirect(event)
    return response(404, {"message": "Route not found."})
