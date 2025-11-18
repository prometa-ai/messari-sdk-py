# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

import requests

from .exceptions import (
    MessariAPIError,
    MessariAuthError,
    MessariConfigError,
    MessariRateLimitError,
)
from .registry import MESSARI_API_REGISTRY

DEFAULT_BASE_URL = "https://api.messari.io"


class MessariClient:
    """
    Lightweight Messari API client.

    - Endpoint schema: MESSARI_API_REGISTRY
    - Generic call: MessariClient.call("assets.list", ...)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = 15,
        session: Optional[requests.Session] = None,
    ) -> None:
        """
        Parameters
        ----------
        api_key : str | None
            Messari API key. If None, uses MESSARI_API_KEY environment variable.
        base_url : str
            Messari API base URL (default: https://api.messari.io)
        timeout : int
            Requests timeout (seconds).
        session : requests.Session | None
            Shared session object; if None, a new Session is created internally.
        """
        if api_key is None:
            api_key = os.environ.get("MESSARI_API_KEY")

        if not api_key:
            raise MessariConfigError(
                "API key is missing. "
                "Either pass api_key explicitly or set MESSARI_API_KEY environment variable."
            )

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()

        self._common_headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "x-messari-api-key": self.api_key,
        }

    # -------------------------------
    #  Public helpers
    # -------------------------------

    def call(
        self,
        api_name: str,
        *,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        extra_headers: Optional[Dict[str, str]] = None,
        raw: bool = False,
    ) -> Any:
        """
        Generic caller that uses MESSARI_API_REGISTRY.

        Parameters
        ----------
        api_name : str
            Key of the endpoint in MESSARI_API_REGISTRY (e.g. "assets.list").
        path_params : dict
            Values for templated path variables (e.g. {"assetID": "bitcoin"}).
        query_params : dict
            Query string parameters (will be filtered according to registry).
        json_body : dict
            JSON body (for POST endpoints).
        extra_headers : dict
            Extra headers merged on top of COMMON_HEADERS.
        raw : bool
            If True, returns requests.Response object; otherwise returns response.json().

        Returns
        -------
        Any
            Parsed JSON response or raw response if raw=True.
        """
        if api_name not in MESSARI_API_REGISTRY:
            raise ValueError(f"Unknown api_name: {api_name}")

        spec = MESSARI_API_REGISTRY[api_name]
        method = spec["method"].upper()
        path_template = spec["path"]

        path_params = path_params or {}
        query_params = query_params or {}

        # Path substitution
        try:
            path = path_template.format(**path_params)
        except KeyError as e:
            raise ValueError(
                f"Missing path param {e} for {api_name} (path template: {path_template})"
            )

        url = f"{self.base_url}{path}"

        headers = dict(self._common_headers)
        if extra_headers:
            headers.update(extra_headers)

        filtered_qp = self._filter_query_params(api_name, query_params)

        resp = self.session.request(
            method=method,
            url=url,
            headers=headers,
            params=filtered_qp,
            json=json_body if method == "POST" and json_body is not None else None,
            timeout=self.timeout,
        )

        if raw:
            self._raise_for_status(resp, url=url)
            return resp

        self._raise_for_status(resp, url=url)

        # Avoid json() errors on empty response bodies
        if not resp.content:
            return None

        return resp.json()

    def paged_call(
        self,
        api_name: str,
        *,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        page_param: str = "page",
        max_pages: int = 5,
    ) -> list[Any]:
        """
        Very simple pagination helper. Appends each page's JSON result to a list.

        You must handle "is finished?" logic externally (e.g., returned list size < limit).

        Parameters
        ----------
        max_pages : int
            Maximum number of pages to fetch.

        Returns
        -------
        list
            List of response.json() outputs for each page.
        """
        results = []
        qp = dict(query_params or {})
        page = qp.get(page_param, 0)

        for _ in range(max_pages):
            qp[page_param] = page
            data = self.call(
                api_name,
                path_params=path_params,
                query_params=qp,
                json_body=json_body,
            )
            results.append(data)
            page += 1

        return results

    @staticmethod
    def pretty(obj: Any, max_len: int = 3000) -> str:
        """Returns a pretty-printed string for quick inspection (printing is up to you)."""
        text = json.dumps(obj, indent=2, ensure_ascii=False)
        if len(text) > max_len:
            return text[:max_len] + "\n... (truncated)"
        return text

    # -------------------------------
    #  Internal helpers
    # -------------------------------

    def _filter_query_params(self, api_name: str, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Filters and normalizes query params according to the registry whitelist."""
        spec = MESSARI_API_REGISTRY[api_name]
        allowed_qp = set(spec.get("query_params", []) or [])

        # If allowed_qp is empty → allow all keys (original behavior)
        if allowed_qp:
            raw = {k: v for k, v in query_params.items() if k in allowed_qp and v is not None}
        else:
            raw = {k: v for k, v in query_params.items() if v is not None}

        return self._normalize_query_params(raw)

    @staticmethod
    def _normalize_query_params(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Small quality improvement:
        - bool → "true"/"false"
        - None → don't send (already filtered)
        Other types are left as-is (str, int, list, etc.).
        """
        normalized: Dict[str, Any] = {}
        for k, v in params.items():
            if isinstance(v, bool):
                normalized[k] = "true" if v else "false"
            else:
                normalized[k] = v
        return normalized

    @staticmethod
    def _raise_for_status(resp: requests.Response, *, url: Optional[str] = None) -> None:
        """Raises appropriate exception based on HTTP status code."""
        if 200 <= resp.status_code < 300:
            return

        text = resp.text or ""
        try:
            body = resp.json()
        except Exception:
            body = None

        msg = text.strip() or f"HTTP {resp.status_code}"
        kwargs = {"error_body": body, "url": url}

        if resp.status_code in (401, 403):
            raise MessariAuthError(resp.status_code, msg, **kwargs)
        if resp.status_code == 429:
            raise MessariRateLimitError(resp.status_code, msg, **kwargs)

        raise MessariAPIError(resp.status_code, msg, **kwargs)
