import importlib
import json
import os
from unittest.mock import Mock


os.environ["TABLE_NAME"] = "test-short-urls"
handler = importlib.import_module("src.handler")


def http_event(method, path, body=None, path_parameters=None):
    return {
        "rawPath": path,
        "body": body,
        "pathParameters": path_parameters,
        "requestContext": {
            "domainName": "abc.execute-api.us-east-1.amazonaws.com",
            "http": {"method": method},
        },
    }


def test_create_short_url_writes_url_and_returns_201(monkeypatch):
    fake_table = Mock()
    monkeypatch.setattr(handler, "table", fake_table)
    monkeypatch.setattr(handler, "generate_code", lambda: "abc1234")

    result = handler.lambda_handler(
        http_event("POST", "/shorten", json.dumps({"url": "https://example.com/docs"})), None
    )

    assert result["statusCode"] == 201
    assert json.loads(result["body"])["short_url"].endswith("/abc1234")
    assert fake_table.put_item.call_args.kwargs["Item"]["original_url"] == "https://example.com/docs"


def test_create_short_url_rejects_invalid_url(monkeypatch):
    fake_table = Mock()
    monkeypatch.setattr(handler, "table", fake_table)

    result = handler.lambda_handler(http_event("POST", "/shorten", json.dumps({"url": "ftp://bad"})), None)

    assert result["statusCode"] == 400
    fake_table.put_item.assert_not_called()


def test_redirect_returns_302(monkeypatch):
    fake_table = Mock()
    fake_table.get_item.return_value = {"Item": {"original_url": "https://example.com"}}
    monkeypatch.setattr(handler, "table", fake_table)

    result = handler.lambda_handler(http_event("GET", "/abc1234", path_parameters={"short_code": "abc1234"}), None)

    assert result["statusCode"] == 302
    assert result["headers"]["location"] == "https://example.com"
