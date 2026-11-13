from __future__ import annotations

import hashlib
import json
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


class HttpError(RuntimeError):
    pass


class HttpClient:
    """Small cached JSON GET client built on the standard library.

    Every successful response is written to a content-addressed cache file so a
    rerun never re-hits the API for the same URL, which keeps long verification
    passes resumable and rate-limit friendly.
    """

    def __init__(
        self,
        cache_dir: Path,
        user_agent: str,
        min_interval: float = 0.2,
        ttl_hours: float = 168,
    ):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.user_agent = user_agent
        self.min_interval = min_interval
        self.ttl = ttl_hours * 3600
        self._lock = threading.Lock()
        self._last_request = 0.0

    def _throttle(self) -> None:
        with self._lock:
            wait = self._last_request + self.min_interval - time.time()
            if wait > 0:
                time.sleep(wait)
            self._last_request = time.time()

    def _cache_path(self, url: str) -> Path:
        digest = hashlib.sha1(url.encode("utf-8")).hexdigest()
        return self.cache_dir / f"{digest}.json"

    def get_json(
        self,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        use_cache: bool = True,
        ttl_hours: float | None = None,
    ):
        if params:
            query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
            url = f"{url}?{query}"
        path = self._cache_path(url)
        ttl = ttl_hours * 3600 if ttl_hours is not None else self.ttl
        if use_cache and path.exists() and (time.time() - path.stat().st_mtime) < ttl:
            try:
                return json.loads(path.read_text(encoding="utf-8"))["data"]
            except (json.JSONDecodeError, KeyError):
                pass
        data = self._request(url, headers or {})
        payload = {
            "url": url,
            "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "data": data,
        }
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return data

    def _request(self, url: str, headers: dict):
        request_headers = {"User-Agent": self.user_agent, "Accept": "application/json"}
        request_headers.update(headers)
        last_error: Exception | None = None
        for attempt in range(5):
            self._throttle()
            request = urllib.request.Request(url, headers=request_headers)
            try:
                with urllib.request.urlopen(request, timeout=90) as response:
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                last_error = exc
                if exc.code in (429, 500, 502, 503, 504):
                    retry_after = exc.headers.get("Retry-After")
                    delay = float(retry_after) if retry_after else min(2 ** attempt * 2, 60)
                    time.sleep(delay)
                    continue
                body = exc.read().decode("utf-8", "replace")[:300]
                raise HttpError(f"HTTP {exc.code} for {url}: {body}") from exc
            except (urllib.error.URLError, TimeoutError) as exc:
                last_error = exc
                time.sleep(min(2 ** attempt * 2, 60))
        raise HttpError(f"request failed after retries: {url} ({last_error})")
