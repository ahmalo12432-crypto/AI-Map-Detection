"""Local AI-style image analysis service.

This module intentionally uses deterministic image heuristics. It gives the API and
desktop app useful behavior now while keeping a clear seam for future ML model
integration.
"""

from PIL import Image, ImageFilter, ImageStat

from ai_map_detection.core.models import TileAnalysis


class AIAnalyzer:
    """Analyze map tiles and produce searchable metadata."""

    def analyze(self, image: Image.Image) -> TileAnalysis:
        rgb_image = image.convert("RGB")
        stat = ImageStat.Stat(rgb_image)
        mean_channels = stat.mean
        brightness = sum(mean_channels) / len(mean_channels)
        dominant_color = self._dominant_color(rgb_image)
        edge_density = self._edge_density(rgb_image)
        labels = self._labels(brightness, dominant_color, edge_density)
        description = (
            f"Tile with {dominant_color} dominant color, "
            f"{brightness:.1f} brightness, and {edge_density:.2f} edge density."
        )
        return TileAnalysis(
            dominant_color=dominant_color,
            brightness=round(brightness, 2),
            edge_density=round(edge_density, 4),
            labels=labels,
            description=description,
        )

    def _dominant_color(self, image: Image.Image) -> str:
        small = image.resize((1, 1))
        red, green, blue = small.getpixel((0, 0))
        if green > red * 1.15 and green > blue * 1.15:
            return "green"
        if blue > red * 1.15 and blue > green * 1.15:
            return "blue"
        if red > green * 1.15 and red > blue * 1.15:
            return "red"
        if max(red, green, blue) - min(red, green, blue) < 20:
            return "gray"
        return "mixed"

    def _edge_density(self, image: Image.Image) -> float:
        edges = image.convert("L").filter(ImageFilter.FIND_EDGES)
        histogram = edges.histogram()
        total_pixels = image.width * image.height
        strong_edges = sum(histogram[80:])
        return strong_edges / total_pixels if total_pixels else 0.0

    def _labels(self, brightness: float, dominant_color: str, edge_density: float) -> list[str]:
        labels = [dominant_color]
        labels.append("bright" if brightness >= 150 else "dark")
        if edge_density >= 0.2:
            labels.append("detailed")
        elif edge_density <= 0.05:
            labels.append("smooth")
        else:
            labels.append("moderate-detail")
        if dominant_color == "green":
            labels.append("vegetation")
        if dominant_color == "blue":
            labels.append("water")
        if dominant_color == "gray":
            labels.append("urban")
        return labels
