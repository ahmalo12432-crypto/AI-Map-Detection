"""Command-line entrypoint for AI Map Detection."""

import argparse

import uvicorn

from ai_map_detection.api.app import create_app
from ai_map_detection.desktop.app import run_desktop


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI Map Detection")
    subparsers = parser.add_subparsers(dest="command", required=True)

    api_parser = subparsers.add_parser("api", help="Run the REST API")
    api_parser.add_argument("--host", default="127.0.0.1")
    api_parser.add_argument("--port", type=int, default=8000)
    api_parser.add_argument("--reload", action="store_true")

    subparsers.add_parser("desktop", help="Run the desktop application")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "api":
        uvicorn.run(create_app(), host=args.host, port=args.port, reload=args.reload)
    elif args.command == "desktop":
        raise SystemExit(run_desktop())


if __name__ == "__main__":
    main()
