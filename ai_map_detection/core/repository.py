"""In-memory repository for processed tiles."""

from ai_map_detection.core.models import MapTile, SplitResult


class TileRepository:
    """Store split results for the current process."""

    def __init__(self) -> None:
        self._tiles: list[MapTile] = []
        self._results: list[SplitResult] = []

    def add_result(self, result: SplitResult) -> None:
        self._results.append(result)
        self._tiles.extend(result.tiles)

    def list_tiles(self) -> list[MapTile]:
        return list(self._tiles)

    def list_results(self) -> list[SplitResult]:
        return list(self._results)
