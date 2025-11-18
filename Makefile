.PHONY: help install install-dev test lint format clean build publish playground

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install package dependencies
	pip install -e .

install-dev:  ## Install package with development dependencies
	pip install -e ".[dev]"

test:  ## Run tests (placeholder for future implementation)
	@echo "Tests not yet implemented. Add pytest and tests in future versions."

lint:  ## Run linting checks (ruff)
	@if command -v ruff >/dev/null 2>&1; then \
		ruff check src/; \
	else \
		echo "ruff not installed. Install with: pip install ruff"; \
	fi

format:  ## Format code with ruff
	@if command -v ruff >/dev/null 2>&1; then \
		ruff format src/; \
	else \
		echo "ruff not installed. Install with: pip install ruff"; \
	fi

clean:  ## Clean build artifacts and cache files
	rm -rf build/ dist/ *.egg-info .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build:  ## Build distribution packages
	python -m build

publish:  ## Publish to PyPI (requires twine)
	python -m twine upload dist/*

playground:  ## Run the interactive playground CLI
	python -m messari_sdk.playground
