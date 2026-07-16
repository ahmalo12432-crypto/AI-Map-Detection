"""Domain models for map processing."""

from pathlib import Path
from uuid import uuid4

from pydantic import BaseModel, Field


class TileAnalysis(BaseModel):
    """AI-style metadata extracted from a map tile."""

    dominant_color: str
    brightness: float = Field(ge=0, le=255)
    edge_density: float = Field(ge=0, le=1)
    labels: list[str] = Field(default_factory=list)
    description: str


class MapTile(BaseModel):
    """A single generated tile and its metadata."""

    id: str = Field(default_factory=lambda: uuid4().hex)
    source_filename: str
    path: Path
    row: int
    column: int
    x: int
    y: int
    width: int
    height: int
    analysis: TileAnalysis


class SplitResult(BaseModel):
    """Result returned after splitting a map image."""

    source_filename: str
    image_width: int
    image_height: int
    tile_size: int
    tiles: list[MapTile]


class SearchHit(BaseModel):
    """Search result for a tile."""

    tile: MapTile
    score: float
    reasons: list[str]
