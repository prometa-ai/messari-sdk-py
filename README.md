# messari-sdk-py

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](https://github.com/prometa-ai/messari-sdk-py)

**Lightweight, unofficial Python SDK for the Messari API**

A simple, elegant Python wrapper for the [Messari API](https://docs.messari.io/) that makes it easy to access cryptocurrency market data, news, and analytics.

> **⚠️ Note:** This is version **0.1.0** - currently only a subset of Messari API endpoints are implemented. More endpoints will be added in future releases.

---

## 🚀 Features

- **Simple & Intuitive**: Clean, Pythonic interface for Messari API calls
- **Type Hints**: Full type annotations for better IDE support
- **Error Handling**: Comprehensive exception hierarchy for API errors
- **Registry-Based**: Endpoint definitions in a centralized registry for easy maintenance
- **CLI Playground**: Interactive command-line tool to explore and test endpoints
- **Pagination Support**: Built-in helper for paginated responses
- **Lightweight**: Minimal dependencies (only `requests`)

---

## 📦 Installation

### Option 1: Install from Source (Recommended for now)

Since this package is not yet published to PyPI, install directly from the source:

```bash
# Clone the repository
git clone https://github.com/prometa-ai/messari-sdk-py.git
cd messari-sdk-py

# Install in editable mode
make install
```

This installs the package in "editable" mode, meaning changes to the source code will be immediately reflected without reinstalling.

### Option 2: Development Installation

If you want to contribute or modify the code, install with development dependencies:

```bash
make install-dev
```

This includes additional tools like:
- `pytest` - For running tests
- `ruff` - For linting and formatting
- `build` - For building distribution packages
- `twine` - For publishing to PyPI

### Option 3: Install from PyPI (Coming Soon)

Once published to PyPI, you'll be able to install with:

```bash
pip install messari-sdk-py
```

### Verify Installation

After installation, verify it works:

```bash
# Check if the package is installed
python -c "from messari_sdk import MessariClient; print('✓ Installation successful!')"

# Or try the playground CLI
messari-playground --help
```

---

## 🔑 Authentication

Get your free API key from [Messari](https://messari.io/api).

Set it as an environment variable:

```bash
export MESSARI_API_KEY="your-api-key-here"
```

Or pass it directly when creating the client:

```python
from messari_sdk import MessariClient

client = MessariClient(api_key="your-api-key-here")
```

---

## 📖 Quick Start

### Basic Usage

```python
from messari_sdk import MessariClient

# Initialize client (uses MESSARI_API_KEY from environment)
client = MessariClient()

# Get details for Bitcoin and Ethereum
assets = client.call(
    "assets.details",
    query_params={"assetIDs": "bitcoin,ethereum"}
)
print(client.pretty(assets))

# List top 20 centralized exchanges
exchanges = client.call(
    "exchanges.list",
    query_params={"type": "centralized", "limit": 20}
)
print(client.pretty(exchanges))

# Get latest crypto news
news = client.call(
    "news.feed",
    query_params={
        "assetIds": "bitcoin,ethereum",
        "limit": 10,
        "sort": 2  # DESC by publish time
    }
)
print(client.pretty(news))
```

### Using the Playground CLI

The SDK includes an interactive CLI for exploring endpoints:

```bash
# Interactive mode
messari-playground

# List all available endpoints
messari-playground list

# Describe a specific endpoint
messari-playground describe assets.details

# Call an endpoint directly
messari-playground call assets.list --query '{"limit": 5, "hasMarketData": true}'
```

---

## 🛠️ Currently Implemented Endpoints

### Assets (Market Data)
- ✅ `assets.list` - List all assets with filtering options
- ✅ `assets.details` - Get detailed information for specific assets

### Exchanges
- ✅ `exchanges.list` - List all exchanges with filters
- ✅ `exchanges.get` - Get specific exchange details

### News & Topics
- ✅ `news.feed` - Get paginated news feed with asset tagging
- ✅ `news.sources` - List all available news sources

> **Coming Soon:** Timeseries data, metrics, profiles, governance, and more!

---

## 📚 Examples

### Search for AI-related Assets

```python
from messari_sdk import MessariClient

client = MessariClient()

ai_assets = client.call(
    "assets.list",
    query_params={
        "search": "ai",
        "limit": 50,
        "hasMarketData": True
    }
)

for asset in ai_assets.get("data", []):
    print(f"{asset['name']} ({asset['symbol']})")
```

### Get Exchange Information

```python
# Get Binance details
binance = client.call(
    "exchanges.get",
    path_params={"exchangeIdentifier": "binance"}
)
print(client.pretty(binance))
```

### Filter News by Source

```python
# Get CoinDesk news sources
sources = client.call(
    "news.sources",
    query_params={
        "sourceName": "CoinDesk",
        "sourceTypes": "News",
        "limit": 10
    }
)
print(client.pretty(sources))
```

---

## 🏗️ Project Structure

```
messari-sdk-py/
├── src/
│   └── messari_sdk/
│       ├── __init__.py       # Package exports
│       ├── client.py         # Main MessariClient class
│       ├── registry.py       # Endpoint definitions
│       ├── exceptions.py     # Custom exceptions
│       ├── examples.py       # Usage examples
│       └── playground.py     # Interactive CLI tool
├── pyproject.toml            # Project metadata & dependencies
├── Makefile                  # Development commands
└── README.md                 # This file
```

---

## 🧪 Development

### Available Make Commands

```bash
make help          # Show all available commands
make install       # Install package
make install-dev   # Install with dev dependencies
make lint          # Run linting checks
make format        # Format code
make clean         # Clean build artifacts
make build         # Build distribution packages
make playground    # Run interactive playground
```

---

## 🐛 Error Handling

The SDK provides specific exceptions for different error scenarios:

```python
from messari_sdk import (
    MessariClient,
    MessariConfigError,    # Configuration errors (missing API key)
    MessariAuthError,      # Authentication errors (401, 403)
    MessariRateLimitError, # Rate limiting (429)
    MessariAPIError,       # General API errors
)

client = MessariClient()

try:
    data = client.call("assets.details", query_params={"assetIDs": "bitcoin"})
except MessariAuthError as e:
    print(f"Authentication failed: {e}")
except MessariRateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except MessariAPIError as e:
    print(f"API error: {e}")
```

---

## 📝 API Registry

All endpoints are defined in `registry.py` with:
- HTTP method
- URL path (with parameter templates)
- Path parameters
- Query parameters
- Description

This makes it easy to:
- Add new endpoints
- Validate parameters
- Generate documentation
- Build CLI tools

---

## 🤝 Next Steps

This is an early-stage project with lots of room for improvement:

- Add more Messari API endpoints
- Improve error handling
- Add unit tests
- Add async support

---

## 📄 License

This project is licensed under the MIT License.

---

## ⚠️ Disclaimer

This is an **unofficial** SDK and is not affiliated with or endorsed by Messari. Use at your own risk.

---


## 📧 Contact

**Prometa AI**  
Email: info@prometa.ai  
GitHub: [@prometa-ai](https://github.com/prometa-ai)

---

**Version 0.1.0** | Built with ❤️ for the crypto community
