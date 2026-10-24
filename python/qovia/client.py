"""A small, dependency-free client: one method per HTTP verb, the response envelope unpacked, errors raised.

Every success is {"request_id", "data", "meta"}; every error is {"error": {"code", "message", "request_id",
"support"}}. Calls are billed only when they return data, and meta says what each one cost.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Any

DEFAULT_BASE_URL = "https://api.qovia.ai"
USER_AGENT = "qovia-python/0.1.0"


class QoviaError(Exception):
    """An error answer from the API. Branch on `code` (see https://qovia.ai/docs/), never on the message."""

    def __init__(self, status: int, code: str, message: str, request_id: str | None = None,
                 retry_after: float | None = None) -> None:
        super().__init__(f"{status} {code}: {message}")
        self.status = status
        self.code = code
        self.message = message
        self.request_id = request_id
        self.retry_after = retry_after


@dataclass
class Response:
    """One successful call: the data plus what it cost."""

    request_id: str
    data: Any
    meta: dict[str, Any] = field(default_factory=dict)

    @property
    def empty(self) -> bool:
        """True when nothing was found (and nothing was charged)."""
        return bool(self.meta.get("empty"))

    @property
    def charged_usd(self) -> str:
        return str(self.meta.get("charged_usd", "0"))

    @property
    def balance_usd(self) -> str | None:
        value = self.meta.get("balance_usd")
        return None if value is None else str(value)


class Qovia:
    """Client for https://api.qovia.ai.

    api_key: defaults to the QOVIA_API_KEY environment variable. Create one at
             https://qovia.ai/console/?tab=keys (new accounts get 50 trial calls).
    max_retries: retries on 429 and 503 answers, honouring Retry-After (calls that fail are never charged).
    """

    def __init__(self, api_key: str | None = None, *, base_url: str = DEFAULT_BASE_URL, timeout: float = 60,
                 max_retries: int = 2) -> None:
        self.api_key = api_key or os.environ.get("QOVIA_API_KEY")
        if not self.api_key:
            raise ValueError("pass api_key or set QOVIA_API_KEY (create a key at https://qovia.ai/console/?tab=keys)")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

    # ------------------------------------------------------------------ calls

    def get(self, path: str, **params: Any) -> Response:
        """Call a GET endpoint, e.g. client.get("/v1/raw/douyin/video", item_id="...")."""
        query = {key: _query_value(value) for key, value in params.items() if value is not None}
        url = self._url(path) + ("?" + urllib.parse.urlencode(query) if query else "")
        return self._send("GET", url, None)

    def post(self, path: str, body: dict[str, Any] | None = None, **fields: Any) -> Response:
        """Call a POST endpoint with a JSON body, e.g. client.post("/v1/search", query="coffee")."""
        payload = {**(body or {}), **fields}
        return self._send("POST", self._url(path), json.dumps(payload).encode())

    def account(self) -> Response:
        """Balance, plan and rate limit for this key. Not charged."""
        return self.get("/v1/account")

    def search(self, query: str, **filters: Any) -> Response:
        """Cross-platform search over Chinese public sources (POST /v1/search)."""
        return self.post("/v1/search", query=query, **filters)

    def pages(self, path: str, *, page_param: str = "page", start: int = 1, max_pages: int = 10,
              **params: Any):
        """Yield page after page of a page-numbered GET endpoint until has_more is false or max_pages."""
        for page in range(start, start + max_pages):
            response = self.get(path, **{**params, page_param: page})
            yield response
            if response.empty or not (isinstance(response.data, dict) and response.data.get("has_more")):
                return

    # ------------------------------------------------------------------ plumbing

    def _url(self, path: str) -> str:
        return self.base_url + ("" if path.startswith("/") else "/") + path

    def _send(self, method: str, url: str, body: bytes | None) -> Response:
        headers = {"Authorization": f"Bearer {self.api_key}", "User-Agent": USER_AGENT, "Accept": "application/json"}
        if body is not None:
            headers["Content-Type"] = "application/json"
        attempt = 0
        while True:
            request = urllib.request.Request(url, data=body, method=method, headers=headers)
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as answer:
                    envelope = json.load(answer)
                return Response(envelope.get("request_id", ""), envelope.get("data"), envelope.get("meta") or {})
            except urllib.error.HTTPError as answer:
                error = _error_from(answer)
                if error.status in (429, 503) and attempt < self.max_retries:
                    attempt += 1
                    time.sleep(error.retry_after if error.retry_after is not None else 2 ** attempt)
                    continue
                raise error from None


def _query_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (list, tuple)):
        return ",".join(str(item) for item in value)
    return str(value)


def _error_from(answer: urllib.error.HTTPError) -> QoviaError:
    retry_after = answer.headers.get("Retry-After") if answer.headers else None
    try:
        retry = float(retry_after) if retry_after else None
    except ValueError:
        retry = None
    try:
        payload = json.loads(answer.read() or b"{}")
    except ValueError:
        payload = {}
    error = payload.get("error") if isinstance(payload, dict) else None
    if isinstance(error, dict):
        return QoviaError(answer.code, str(error.get("code", "error")), str(error.get("message", "")),
                          error.get("request_id"), retry)
    return QoviaError(answer.code, "http_error", str(payload.get("detail") or answer.reason), None, retry)
