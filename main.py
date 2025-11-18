from messari_sdk import MessariClient


def main():
    # Export API key from environment variable (set it from terminal command; or read it from .env file.
    # If latter, use dotenv package and pass it to MessariClient constructor)

    # export MESSARI_API_KEY="YOUR_API_KEY"

    client = MessariClient()

    data = client.call(
        "news.feed",
        query_params={
            "assetIds": "bitcoin,ethereum",
            "publishedAfter": "2025-11-15T00:00:00Z",
            "publishedBefore": "2025-11-16T00:00:00Z",
            "limit": 50,
            "sort": 2,
        },
    )
    print(client.pretty(data))


if __name__ == "__main__":
    main()
