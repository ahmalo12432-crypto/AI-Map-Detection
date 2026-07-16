from pathlib import Path

from PIL import Image

from ai_map_detection.services.map_splitter import MapSplitter
from ai_map_detection.services.search import TileSearchEngine


def test_splitter_creates_tiles_and_metadata(tmp_path: Path) -> None:
    source = tmp_path / "map.png"
    Image.new("RGB", (130, 70), color=(20, 180, 40)).save(source)

    result = MapSplitter().split(source, tmp_path / "tiles", tile_size=64)

    assert result.image_width == 130
    assert result.image_height == 70
    assert len(result.tiles) == 6
    assert all(tile.path.exists() for tile in result.tiles)
    assert result.tiles[0].analysis.dominant_color == "green"
    assert "vegetation" in result.tiles[0].analysis.labels


def test_search_matches_analysis_metadata(tmp_path: Path) -> None:
    source = tmp_path / "map.png"
    Image.new("RGB", (64, 64), color=(20, 180, 40)).save(source)
    result = MapSplitter().split(source, tmp_path / "tiles", tile_size=64)

    hits = TileSearchEngine().search("green vegetation", result.tiles)

    assert hits
    assert hits[0].score > 0
    assert hits[0].tile.analysis.dominant_color == "green"
