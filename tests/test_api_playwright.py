import json
import threading
from wsgiref.simple_server import make_server

import pytest
from playwright.sync_api import sync_playwright

from app import create_app


# 🔹 Fixture: Start API server
@pytest.fixture
def api_server(monkeypatch):
    # Override API key for testing
    monkeypatch.setattr("app.config.API_KEY", "test-api-key")

    app = create_app()
    server = make_server("127.0.0.1", 0, app)
    host, port = server.server_address

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    base_url = f"http://{host}:{port}"
    yield base_url

    server.shutdown()
    thread.join(timeout=5)


# 🔹 Fixture: Playwright API client
@pytest.fixture
def api_client(api_server):
    with sync_playwright() as playwright:
        context = playwright.request.new_context(
            base_url=api_server,
            extra_http_headers={
                "Content-Type": "application/json",
                "x-api-key": "test-api-key",
            },
        )
        yield context
        context.dispose()


# 🔹 Helper payload
def get_payload():
    return {
        "incident": "INC12345",
        "server": "local"
    }


# 🔹 Test: Successful cleanup
def test_cleanup_api_success(api_client):
    response = api_client.post(
        "/cleanup",
        data=json.dumps(get_payload())
    )

    assert response.status == 200
    payload = response.json()

    assert payload["incident"] == "INC12345"
    assert payload["server"] == "local"
    assert payload["status"] in {"success", "failed"}


# 🔹 Test: Invalid API key
def test_cleanup_api_rejects_invalid_api_key(api_server):
    with sync_playwright() as playwright:
        context = playwright.request.new_context(
            base_url=api_server,
            extra_http_headers={
                "Content-Type": "application/json",
                "x-api-key": "bad-key",
            },
        )

        response = context.post(
            "/cleanup",
            data=json.dumps(get_payload())
        )

        context.dispose()

    assert response.status == 401
    payload = response.json()
    assert payload["status"] == "unauthorized"
