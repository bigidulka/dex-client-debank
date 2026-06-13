from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from importlib import resources
from typing import Any, Mapping

import httpx

Json = dict[str, Any]


class APIError(RuntimeError):
    def __init__(self, message: str, *, status_code: int | None = None, payload: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload


def drop_empty(values: Mapping[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in values.items() if v is not None and v != ""}


@dataclass(slots=True)
class SignedHTTPClient:
    base_url: str = "https://api.debank.com"
    timeout: float = 30.0
    headers: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")
        self._client = httpx.Client(timeout=self.timeout, headers=self.headers)

    def close(self) -> None:
        self._client.close()

    def sign_headers(self, path: str, params: Mapping[str, Any], method: str = "GET") -> dict[str, str]:
        script = resources.files("dex_client_debank").joinpath("sign_headers.js")
        payload = json.dumps({"path": path, "params": dict(params), "method": method}, separators=(",", ":"))
        raw = subprocess.check_output(["node", str(script), payload], text=True, timeout=self.timeout)
        return json.loads(raw)

    def get(self, path: str, *, params: Mapping[str, Any] | None = None) -> Json:
        if not path.startswith("/"):
            path = "/" + path
        clean_params = drop_empty(params or {})
        headers = self.sign_headers(path, clean_params, "GET")
        response = self._client.get(self.base_url + path, params=clean_params, headers=headers)
        text = response.text
        if response.status_code < 200 or response.status_code >= 300:
            raise APIError(f"GET {path} failed with HTTP {response.status_code}", status_code=response.status_code, payload=text[:1000])
        try:
            payload = response.json()
        except ValueError as exc:
            raise APIError(f"GET {path} returned non-json", status_code=response.status_code, payload=text[:1000]) from exc
        if isinstance(payload, dict) and payload.get("error_code") not in (None, 0):
            raise APIError(f"DeBank API error {payload.get('error_code')}: {payload.get('error_msg')}", status_code=response.status_code, payload=payload)
        return payload
