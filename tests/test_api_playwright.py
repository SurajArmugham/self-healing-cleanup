import json
import threading
from wsgiref.simple_server import make_server

import pytest
from playwright.sync_api import sync_playwright

from app import create_app


# 🔹 Fixture: Start API server
@pytest.fixture
def api_server(monkeypatch):
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


# 🔹 Fixture: Playwright client factory (single lifecycle)
@pytest.fixture
def api_client_factory(api_server):
    with sync_playwright() as playwright:

        def create_client(api_key):
            return playwright.request.new_context(
                base_url=api_server,
                extra_http_headers={
                    "Content-Type": "application/json",
                    "x-api-key": api_key,
                },
            )

        yield create_client


# 🔹 Helper payload
def get_payload():
    return {
        "incident": "INC12345",
        "server": "local"
    }


# 🔹 Test: Successful cleanup
def test_cleanup_api_success(api_client_factory):
    client = api_client_factory("test-api-key")

    try:
        response = client.post(
            "/cleanup",
            data=json.dumps(get_payload())
        )

        # ✅ Read BEFORE disposing client
        status = response.status
        payload = response.json()

    finally:
        client.dispose()

    assert status == 200
    assert payload["incident"] == "INC12345"
    assert payload["server"] == "local"
    assert payload["status"] in {"success", "failed"}


# 🔹 Test: Invalid API key
def test_cleanup_api_rejects_invalid_api_key(api_client_factory):
    client = api_client_factory("bad-key")

    try:
        response = client.post(
            "/cleanup",
            data=json.dumps(get_payload())
        )

        # ✅ Read BEFORE disposing client
        status = response.status
        payload = response.json()

    finally:
        client.dispose()

    assert status == 401
    assert payload["status"] == "unauthorized"
