# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any, Dict

"""
registry.py

Central endpoint registry for the Messari API.
This module defines all supported API routes along with their
HTTP method, path template, and optional path/query/body parameters.

All descriptions and comments below are custom-written for this SDK.
"""

MESSARI_API_REGISTRY: Dict[str, Dict[str, Any]] = {
    # =================================================================================================
    #  ASSETS — High-level market information for thousands of digital assets.
    #  Includes price data, metadata, supply figures, and various coverage indicators.
    # =================================================================================================
    "assets.list": {
        "method": "GET",
        "path": "/metrics/v2/assets",
        "path_params": [],
        "query_params": [
            "category",  # string | optional               - Filter by asset category (e.g. "Cryptocurrency", "Networks", "Financial Services")
            "sector",  # string | optional               - Filter by sector/industry classification (e.g. "Smart Contract Platform", "Stablecoins", "Payments")
            "search",  # string | optional               - Full-text search on symbol, name or slug (e.g. "ai", "bit", "sol")
            "limit",  # int    | optional | default: 10 - Page size (number of items per page)
            "page",  # int    | optional | default: 1  - Page index (1-based)
            "hasDiligence",  # bool   | optional               - Restrict to assets with diligence coverage
            "hasIntel",  # bool   | optional               - Restrict to assets with intel/events coverage
            "hasMarketData",  # bool   | optional               - Restrict to assets with market data
            "hasNews",  # bool   | optional               - Restrict to assets with tagged news
            "hasProposals",  # bool   | optional               - Restrict to assets with governance proposals
            "hasResearch",  # bool   | optional               - Restrict to assets with research reports
            "hasTokenUnlocks",  # bool   | optional               - Restrict to assets with token-unlock data
            "hasFundraising",  # bool   | optional               - Restrict to assets with fundraising data
        ],
        "description": (
            "Returns a paginated collection of assets with optional filters for category, sector, keyword "
            "search and various data-coverage flags. Useful for discovery lists, scanners and filters."
        ),
    },
    "assets.details": {
        "method": "GET",
        "path": "/metrics/v2/assets/details",
        "path_params": [],
        "query_params": [
            "assetIDs",  # string | optional | default: "bitcoin,ethereum" - Comma-separated list of slugs or UUIDs
        ],
        "description": (
            "Retrieves detailed information for one or more assets (max 20), including pricing, metadata, supply "
            "figures, returns and other headline market metrics."
        ),
    },
    # =================================================================================================
    #  EXCHANGES — Spot and derivatives exchange metadata including normalized activity metrics.
    # =================================================================================================
    "exchanges.list": {
        "method": "GET",
        "path": "/metrics/v1/exchanges",
        "path_params": [],
        "query_params": [
            "limit",  # int          | optional | default: 10 - Page size (number of exchanges per page)
            "pageSize",  # int          | optional               - Legacy page size parameter (prefer 'limit')
            "page",  # int          | optional | default: 1  - Page index (1-based)
            "type",  # enum<string> | optional               - Exchange type ("centralized" or "decentralized")
            "typeRankCutoff",  # number       | optional               - Upper bound for 30-day ranking/score
        ],
        "description": (
            "Returns a paginated list of exchanges, with optional filters for exchange type and ranking. "
            "Provides high-level metadata with recent activity indicators."
        ),
    },
    "exchanges.get": {
        "method": "GET",
        "path": "/metrics/v1/exchanges/{exchangeIdentifier}",
        "path_params": [
            "exchangeIdentifier",  # string | required | default: "binance" - Exchange slug or unique identifier
        ],
        "query_params": [],
        "description": (
            "Fetches a single exchange by its identifier, returning metadata and recent volume metrics."
        ),
    },
    # =================================================================================================
    #  NEWS — Aggregated crypto-focused news feed and source-directory endpoints.
    # =================================================================================================
    "news.feed": {
        "method": "GET",
        "path": "/news/v1/news/feed",
        "path_params": [],
        "query_params": [
            "publishedBefore",  # string        | optional | default: "2025-11-06T23:59:59Z" - Upper bound of publish window (RFC3339 or unix ms)
            "publishedAfter",  # string        | optional | default: "2025-11-05T00:00:00Z" - Lower bound of publish window (RFC3339 or unix ms)
            "sourceTypes",  # enum<string>  | optional                                   - Source type filter ("News", "Blog", "Forum")
            "sourceIds",  # list<string>  | optional                                   - One or more source identifiers
            "assetIds",  # list<string>  | optional                                   - Limit to articles tagged with specific assets
            "sort",  # enum<integer> | optional | default: 2                      - Sort by publish time (1=ASC, 2=DESC)
            "limit",  # int           | optional | default: 10                     - Page size (number of articles per page)
            "page",  # int           | optional | default: 0                      - Page index (0-based)
        ],
        "description": (
            "Returns a paginated crypto news feed with optional filters for time range, source type, "
            "source IDs and tagged assets. Ideal for dashboards or asset-specific news views."
        ),
    },
    "news.sources": {
        "method": "GET",
        "path": "/news/v1/news/sources",
        "path_params": [],
        "query_params": [
            "sourceName",  # string       | optional | default: "CoinDesk" - Substring filter on human-readable source name
            "sourceTypes",  # enum<string> | required                       - Source type filter ("News", "Blog", "Forum")
            "limit",  # int          | required | default: 10         - Page size (number of sources per page)
            "page",  # int          | required | default: 0          - Page index (0-based)
        ],
        "description": (
            "Lists news sources available in the Messari news system, with filters for name and type. "
            "Useful for building source pickers or diagnostics."
        ),
    },
}
