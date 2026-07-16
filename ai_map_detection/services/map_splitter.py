"""Map splitting service."""

from pathlib import Path

from ai_map_detection.core.models import MapTile, SplitResult
from ai_map_detection.services.ai_analyzer import AIAnalyzer
from ai_map_detection.utils.images import open_rgb_image


class MapSplitter:
    """Split a map image into tiles and analyze each tile."""

    def __init__(self, analyzer: AIAnalyzer | None = None) -> None:
        self.analyzer = analyzer or AIAnalyzer()

    def split(self, image_path: Path, output_dir: Path, tile_size: int) -> SplitResult:
        if tile_size <= 0:
            raise ValueError("tile_size must be greater than zero")

        output_dir.mkdir(parents=True, exist_ok=True)
        image = open_rgb_image(image_path)
        tiles: list[MapTile] = []

        for row, y in enumerate(range(0, image.height, tile_size)):
            for column, x in enumerate(range(0, image.width, tile_size)):
                width = min(tile_size, image.width - x)
                height = min(tile_size, image.height - y)
                tile_image = image.crop((x, y, x + width, y + height))
                tile_path = output_dir / f"{image_path.stem}_r{row}_c{column}.png"
                tile_image.save(tile_path)
                tiles.append(
                    MapTile(
                        source_filename=image_path.name,
                        path=tile_path,
                        row=row,
                        column=column,
                        x=x,
                        y=y,
                        width=width,
                        height=height,
                        analysis=self.analyzer.analyze(tile_image),
                    )
                )

        return SplitResult(
            source_filename=image_path.name,
            image_width=image.width,
            image_height=image.height,
            tile_size=tile_size,
            tiles=tiles,
        )
