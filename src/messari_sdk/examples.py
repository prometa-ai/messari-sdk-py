# -*- coding: utf-8 -*-
from __future__ import annotations

from .client import MessariClient


def example_assets(client: MessariClient) -> None:
    """Some asset call examples."""
    # 1.1) Details of btc, eth, sol
    asset_details = client.call(
        "assets.details",
        query_params={
            "assetIDs": "bitcoin,ethereum,solana",
        },
    )
    print(client.pretty(asset_details))

    # 1.2) Assets whose name/slug contain "ai"
    ai_assets = client.call(
        "assets.list",
        query_params={
            "search": "ai",
            "limit": 50,
            "hasMarketData": True,
        },
    )
    print(client.pretty(ai_assets))


def example_exchanges(client: MessariClient) -> None:
    """Some exchange call examples."""
    # 1.1) Top 20 centralized exchanges
    cex_list = client.call(
        "exchanges.list",
        query_params={
            "type": "centralized",
            "limit": 20,
        },
    )
    print(client.pretty(cex_list))

    # 1.2) Return basic metadata and 24h metrics of binance
    exchange = client.call(
        "exchanges.get",
        path_params={
            "exchangeIdentifier": "binance",
        },
    )
    print(client.pretty(exchange))


def example_news_topics(client: MessariClient) -> None:
    """Some news call examples."""
    # 1.1) BTC & ETH news for the last 24 hours
    btc_eth_news = client.call(
        "news.feed",
        query_params={
            "assetIds": "bitcoin,ethereum",
            "publishedAfter": "2025-11-15T00:00:00Z",
            "publishedBefore": "2025-11-16T00:00:00Z",
            "limit": 50,
            "sort": 2,
        },
    )
    print(client.pretty(btc_eth_news))

    # 1.2) Last 50 news sources from CoinDesk
    sources = client.call(
        "news.sources",
        query_params={
            "sourceName": "CoinDesk",
            "sourceTypes": "News",
            "limit": 50,
        },
    )
    print(client.pretty(sources))
