# AI Map Detection

AI Map Detection is a Python starter application for working with maps through:

- a desktop UI for loading, splitting, and searching map images;
- a REST API for automation and integrations;
- an extensible AI service layer for segmentation and semantic search.

The first implementation ships with deterministic local algorithms so the app runs without external services. The service layer can later be replaced with model-backed computer vision or embedding providers.

## Features

- Split map images into configurable tiles.
- Generate simple image-analysis metadata for every tile.
- Search tiles by filename, path, dominant color, brightness, edge density, and labels.
- Run a FastAPI REST server.
- Run a PySide6 desktop app.
- Use the same domain services from both UI and API.

## Project layout

```text
ai_map_detection/
  api/          FastAPI application and request/response schemas
  core/         Configuration, domain models, storage helpers
  desktop/     PySide6 desktop interface
  services/    Map tiling, AI analysis, and search services
  utils/       Shared image utilities
main.py         Command-line entrypoint for API and desktop modes
tests/          Pytest coverage for core services and API routes
```

## Requirements

- Python 3.11+

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

For development and tests:

```bash
python -m pip install -r requirements-dev.txt
```

## Run the REST API

```bash
python main.py api --host 127.0.0.1 --port 8000
```

Open the interactive API documentation at <http://127.0.0.1:8000/docs>.

## Run the desktop app

```bash
python main.py desktop
```

## Run tests

```bash
python -m pytest
```

## API examples

Upload and split a map image:

```bash
curl -F "file=@map.png" -F "tile_size=512" http://127.0.0.1:8000/maps/split
```

Search generated tiles:

```bash
curl "http://127.0.0.1:8000/search?query=bright%20green&limit=10"
```
