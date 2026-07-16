from pathlib import Path

from fastapi.testclient import TestClient
from PIL import Image

from ai_map_detection.api.app import create_app
from ai_map_detection.core.config import Settings


def test_health(tmp_path: Path) -> None:
    app = create_app(Settings(data_dir=tmp_path))
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_split_and_search_map(tmp_path: Path) -> None:
    image_path = tmp_path / "green-map.png"
    Image.new("RGB", (80, 80), color=(30, 170, 40)).save(image_path)
    app = create_app(Settings(data_dir=tmp_path / "data", default_tile_size=40))
    client = TestClient(app)

    with image_path.open("rb") as image_file:
        split_response = client.post(
            "/maps/split",
            files={"file": ("green-map.png", image_file, "image/png")},
            data={"tile_size": "40"},
        )

    assert split_response.status_code == 200
    assert len(split_response.json()["tiles"]) == 4

    search_response = client.get("/search", params={"query": "green vegetation"})

    assert search_response.status_code == 200
    assert search_response.json()
