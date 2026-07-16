"""Application settings."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings shared by the desktop and API applications."""

    app_name: str = "AI Map Detection"
    data_dir: Path = Path("data")
    uploads_dir_name: str = "uploads"
    tiles_dir_name: str = "tiles"
    default_tile_size: int = 512

    model_config = SettingsConfigDict(env_prefix="AI_MAP_", env_file=".env")

    @property
    def uploads_dir(self) -> Path:
        return self.data_dir / self.uploads_dir_name

    @property
    def tiles_dir(self) -> Path:
        return self.data_dir / self.tiles_dir_name

    def ensure_directories(self) -> None:
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        self.tiles_dir.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_directories()
    return settings
