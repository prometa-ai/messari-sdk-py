# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import sys
from textwrap import indent
from typing import Any, Dict, Optional

from .client import MessariClient
from .exceptions import MessariConfigError
from .registry import MESSARI_API_REGISTRY


def print_error(msg: str) -> None:
    print(f"[ERROR] {msg}", file=sys.stderr)


def list_endpoints(prefix: Optional[str] = None) -> None:
    keys = sorted(MESSARI_API_REGISTRY.keys())
    if prefix:
        keys = [k for k in keys if k.startswith(prefix)]

    if not keys:
        print("No endpoints found (prefix filter may be too narrow).")
        return

    print("Available Messari endpoints:")
    for k in keys:
        spec = MESSARI_API_REGISTRY[k]
        desc = spec.get("description", "") or ""
        print(f" - {k} [{spec['method']} {spec['path']}]")
        if desc:
            print("   " + desc[:1200] + ("..." if len(desc) > 1200 else ""))


def describe_endpoint(api_name: str) -> None:
    spec = MESSARI_API_REGISTRY.get(api_name)
    if not spec:
        print_error(f"Unknown api_name: {api_name}")
        return

    print(f"Endpoint: {api_name}")
    print(f"Method : {spec['method']}")
    print(f"Path   : {spec['path']}")
    print()

    if spec.get("path_params"):
        print("Path Params:")
        for p in spec["path_params"]:
            print(f"  - {p}")
    else:
        print("Path Params: (none)")
    print()

    if spec.get("query_params"):
        print("Query Params:")
        for p in spec["query_params"]:
            print(f"  - {p}")
    else:
        print("Query Params: (none)")
    print()

    if spec.get("body_params"):
        print("Body Params:")
        for p in spec["body_params"]:
            print(f"  - {p}")
    else:
        print("Body Params: (none)")
    print()

    desc = spec.get("description") or ""
    if desc:
        print("Description:")
        print(indent(desc, "  "))


def parse_json_arg(label: str, value: Optional[str]) -> Optional[Dict[str, Any]]:
    if not value:
        return {}
    try:
        parsed = json.loads(value)
        if parsed is None:
            return {}
        if not isinstance(parsed, dict):
            print_error(
                f'{label} JSON must be an object/dict (e.g. \'{{"key": "value"}}\'). '
                f"Received type: {type(parsed)}"
            )
            return None
        return parsed
    except json.JSONDecodeError as e:
        print_error(f"{label} JSON could not be parsed: {e}")
        return None


def call_endpoint(
    client: MessariClient,
    api_name: str,
    path_json: Optional[str],
    query_json: Optional[str],
    body_json: Optional[str],
) -> None:
    if api_name not in MESSARI_API_REGISTRY:
        print_error(f"Unknown api_name: {api_name}")
        return

    path_params = parse_json_arg("path", path_json)
    if path_params is None:
        return

    query_params = parse_json_arg("query", query_json)
    if query_params is None:
        return

    json_body = parse_json_arg("body", body_json)
    if json_body is None:
        return

    print(f"[INFO] Calling {api_name}...")
    try:
        resp = client.call(
            api_name,
            path_params=path_params,
            query_params=query_params,
            json_body=json_body if json_body else None,
        )
    except Exception as e:
        print_error(f"Error during API call: {e}")
        return

    print("[INFO] Response (first 3000 characters pretty-printed):")
    print(client.pretty(resp))


def interactive_menu(client: MessariClient) -> None:
    while True:
        print("\n=== Messari Playground ===")
        print("1) List endpoints")
        print("2) Describe endpoint schema")
        print("3) Call endpoint")
        print("0) Exit")
        choice = input("Your choice (0-3): ").strip()

        if choice == "0":
            print("Exiting...")
            return

        elif choice == "1":
            prefix = input("Optional prefix (e.g. 'assets.' / leave blank): ").strip() or None
            list_endpoints(prefix)

        elif choice == "2":
            api_name = input("Endpoint name (e.g. assets.list): ").strip()
            if not api_name:
                print_error("Endpoint name cannot be empty.")
                continue
            describe_endpoint(api_name)

        elif choice == "3":
            api_name = input("Endpoint name (e.g. assets.list): ").strip()
            if not api_name:
                print_error("Endpoint name cannot be empty.")
                continue

            print(
                "Enter JSON for path params "
                '(e.g. {"assetID": "bitcoin", "datasetSlug": "price"}) or leave blank:'
            )
            path_json = input("> ").strip() or None

            print(
                "Enter JSON for query params "
                '(e.g. {"start": "2025-11-01T00:00:00Z", "end": "2025-11-08T00:00:00Z"}) '
                "or leave blank:"
            )
            query_json = input("> ").strip() or None

            print("Enter JSON for body params (for POST endpoints) or leave blank:")
            body_json = input("> ").strip() or None

            call_endpoint(client, api_name, path_json, query_json, body_json)

        else:
            print_error("Invalid choice.")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Messari API Playground (unofficial Messari SDK CLI)."
    )
    subparsers = parser.add_subparsers(dest="command", help="Choose a command")

    p_list = subparsers.add_parser("list", help="List all endpoints (with optional prefix)")
    p_list.add_argument(
        "--prefix",
        type=str,
        default=None,
        help="Endpoint name prefix filter (e.g. 'assets.', 'funding.').",
    )

    p_desc = subparsers.add_parser("describe", help="Show the schema of a specific endpoint.")
    p_desc.add_argument(
        "api_name",
        type=str,
        help="Endpoint key (e.g. 'assets.list').",
    )

    p_call = subparsers.add_parser("call", help="Call the selected endpoint.")
    p_call.add_argument(
        "api_name",
        type=str,
        help="Endpoint key (e.g. 'assets.list').",
    )
    p_call.add_argument(
        "--path",
        type=str,
        default=None,
        help='Path params JSON (e.g. \'{"assetID": "bitcoin", "datasetSlug": "price"}\')',
    )
    p_call.add_argument(
        "--query",
        type=str,
        default=None,
        help=(
            "Query params JSON (e.g. "
            '\'{"start": "2025-11-01T00:00:00Z", "end": "2025-11-08T00:00:00Z"}\''
        ),
    )
    p_call.add_argument(
        "--body",
        type=str,
        default=None,
        help="Body params JSON (e.g. '{\"messages\": [...]}' for POST calls)",
    )

    return parser


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    try:
        client = MessariClient()  # API key from environment
    except MessariConfigError as e:
        print(f"[ERROR] {e}")
        print("Please set MESSARI_API_KEY or pass --api-key argument.")
        sys.exit(1)

    if not args.command:
        interactive_menu(client)
        return

    if args.command == "list":
        list_endpoints(args.prefix)
    elif args.command == "describe":
        describe_endpoint(args.api_name)
    elif args.command == "call":
        call_endpoint(client, args.api_name, args.path, args.query, args.body)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
