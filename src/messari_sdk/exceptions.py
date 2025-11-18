from __future__ import annotations

from typing import Optional


class MessariError(Exception):
    """Base exception for all Messari SDK related errors."""


class MessariConfigError(MessariError):
    """Raised when configuration (e.g., API key) is missing or invalid."""


class MessariAPIError(MessariError):
    """Raised for non-2xx HTTP responses."""

    def __init__(
        self,
        status_code: int,
        message: str,
        *,
        error_body: Optional[dict] = None,
        url: Optional[str] = None,
    ) -> None:
        self.status_code = status_code
        self.error_body = error_body
        self.url = url
        super().__init__(f"[{status_code}] {message}")


class MessariAuthError(MessariAPIError):
    """Authentication/authorization errors (401/403)."""


class MessariRateLimitError(MessariAPIError):
    """Rate limiting errors (429)."""
