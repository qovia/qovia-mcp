import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from qovia import Qovia, QoviaError

CALLS = []


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _reply(self, status, body, headers=None):
        raw = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        CALLS.append(("GET", self.path, self.headers.get("Authorization")))
        if self.path.startswith("/v1/busy") and sum(1 for c in CALLS if c[1].startswith("/v1/busy")) < 2:
            return self._reply(429, {"error": {"code": "rate_limited", "message": "slow down", "request_id": "r0"}},
                               {"Retry-After": "0"})
        if self.path.startswith("/v1/missing"):
            return self._reply(400, {"error": {"code": "invalid_params", "message": "bad", "request_id": "r1",
                                               "support": "https://t.me/scott10081"}})
        page = int(self.path.split("page=")[1]) if "page=" in self.path else 1
        return self._reply(200, {"request_id": "r2", "data": {"items": [page], "has_more": page < 3},
                                 "meta": {"billed": True, "charged_usd": "0.005000", "empty": False}})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        CALLS.append(("POST", self.path, json.loads(self.rfile.read(length))))
        return self._reply(200, {"request_id": "r3", "data": {"items": []}, "meta": {"empty": True}})


@pytest.fixture
def client():
    CALLS.clear()
    server = HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield Qovia("sk-qovia-test", base_url=f"http://127.0.0.1:{server.server_port}")
    server.shutdown()


def test_get_unpacks_the_envelope(client):
    response = client.get("/v1/raw/xiaohongshu/search", keyword="coffee", sort=None, tags=["a", "b"])
    assert response.data["items"] == [1] and response.charged_usd == "0.005000" and not response.empty
    assert CALLS[0] == ("GET", "/v1/raw/xiaohongshu/search?keyword=coffee&tags=a%2Cb", "Bearer sk-qovia-test")


def test_post_sends_json(client):
    response = client.search("coffee", platforms=["weibo"])
    assert response.empty
    assert CALLS[0] == ("POST", "/v1/search", {"query": "coffee", "platforms": ["weibo"]})


def test_errors_raise_with_code_and_request_id(client):
    with pytest.raises(QoviaError) as caught:
        client.get("/v1/missing")
    assert (caught.value.status, caught.value.code, caught.value.request_id) == (400, "invalid_params", "r1")


def test_rate_limits_are_retried(client):
    assert client.get("/v1/busy").request_id == "r2"


def test_pages_stop_when_has_more_is_false(client):
    assert [r.data["items"][0] for r in client.pages("/v1/raw/x", max_pages=10)] == [1, 2, 3]


def test_a_key_is_required(monkeypatch):
    monkeypatch.delenv("QOVIA_API_KEY", raising=False)
    with pytest.raises(ValueError):
        Qovia()
