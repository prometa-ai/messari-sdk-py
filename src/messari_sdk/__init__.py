# -*- coding: utf-8 -*-
"""
messari-sdk-py
~~~~~~~~~~~~~~

Lightweight, unofficial Python SDK for the Messari API.

Usage:

    from messari_sdk import MessariClient

    client = MessariClient()
    data = client.call("assets.list", ...)

:copyright: (c) 2025 by Prometa AI.
:license: MIT, see LICENSE for more details.
"""

from .client import MessariClient
from .exceptions import (
    MessariAPIError,
    MessariAuthError,
    MessariConfigError,
    MessariError,
    MessariRateLimitError,
)
from .registry import MESSARI_API_REGISTRY

__version__ = "0.1.0"
__all__ = [
    "MessariClient",
    "MessariError",
    "MessariConfigError",
    "MessariAPIError",
    "MessariAuthError",
    "MessariRateLimitError",
    "MESSARI_API_REGISTRY",
]
