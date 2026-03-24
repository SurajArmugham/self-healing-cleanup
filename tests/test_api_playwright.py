import threading
from wsgiref.simple_server import make_server

import pytest
from playwright.sync_api import sync_playwright

from app import create_app


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


def test_cleanup_api_success(api_server):
    with sync_playwright() as playwright:
        request_context = playwright.request.new_context(
            base_url=api_server,
            extra_http_headers={"x-api-key": "test-api-key"},
        )

        response = request_context.post(
            "/cleanup",
            json={"incident": "INC12345", "server": "local"},
        )

        request_context.dispose()

    assert response.status == 200
    payload = response.json()

    assert payload["incident"] == "INC12345"
    assert payload["server"] == "local"
    assert payload["status"] in {"success", "failed"}


def test_cleanup_api_rejects_invalid_api_key(api_server):
    with sync_playwright() as playwright:
        request_context = playwright.request.new_context(
            base_url=api_server,
            extra_http_headers={"x-api-key": "bad-key"},
        )

        response = request_context.post(
            "/cleanup",
            json={"incident": "INC12345", "server": "local"},
        )

        request_context.dispose()

    assert response.status == 401
    payload = response.json()
    assert payload["status"] == "unauthorized"
