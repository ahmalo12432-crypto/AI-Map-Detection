"""Image helper functions."""

from pathlib import Path
from uuid import uuid4

from PIL import Image


def safe_image_filename(original_name: str) -> str:
    """Return a collision-resistant image filename that preserves the suffix."""

    suffix = Path(original_name).suffix.lower() or ".png"
    return f"{Path(original_name).stem[:48]}-{uuid4().hex}{suffix}"


def open_rgb_image(path: Path) -> Image.Image:
    """Open an image file as RGB."""

    return Image.open(path).convert("RGB")
