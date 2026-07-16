"""FastAPI application factory."""

from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from ai_map_detection.core.config import Settings, get_settings
from ai_map_detection.core.models import MapTile, SearchHit, SplitResult
from ai_map_detection.core.repository import TileRepository
from ai_map_detection.services.map_splitter import MapSplitter
from ai_map_detection.services.search import TileSearchEngine
from ai_map_detection.utils.images import safe_image_filename


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    settings.ensure_directories()
    repository = TileRepository()
    splitter = MapSplitter()
    search_engine = TileSearchEngine()

    app = FastAPI(title=settings.app_name, version="0.1.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/maps/split", response_model=SplitResult)
    async def split_map(
        file: UploadFile = File(...),
        tile_size: int = Form(default=settings.default_tile_size),
    ) -> SplitResult:
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Only image uploads are supported")
        if tile_size <= 0:
            raise HTTPException(status_code=400, detail="tile_size must be greater than zero")

        upload_path = settings.uploads_dir / safe_image_filename(file.filename or "map.png")
        upload_path.write_bytes(await file.read())
        result = splitter.split(upload_path, settings.tiles_dir / Path(upload_path).stem, tile_size)
        repository.add_result(result)
        return result

    @app.get("/tiles", response_model=list[MapTile])
    def list_tiles() -> list[MapTile]:
        return repository.list_tiles()

    @app.get("/search", response_model=list[SearchHit])
    def search(query: str, limit: int = 20) -> list[SearchHit]:
        return search_engine.search(query=query, tiles=repository.list_tiles(), limit=limit)

    return app


app = create_app()
