"""PySide6 desktop user interface."""

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from ai_map_detection.core.config import get_settings
from ai_map_detection.core.repository import TileRepository
from ai_map_detection.services.map_splitter import MapSplitter
from ai_map_detection.services.search import TileSearchEngine


class MainWindow(QMainWindow):
    """Main desktop window for splitting and searching map images."""

    def __init__(self) -> None:
        super().__init__()
        self.settings = get_settings()
        self.repository = TileRepository()
        self.splitter = MapSplitter()
        self.search_engine = TileSearchEngine()
        self.selected_map: Path | None = None

        self.setWindowTitle(self.settings.app_name)
        self.resize(900, 620)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout()

        self.file_label = QLabel("No map selected")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.file_label)

        choose_button = QPushButton("Choose map image")
        choose_button.clicked.connect(self.choose_map)
        layout.addWidget(choose_button)

        self.tile_size = QSpinBox()
        self.tile_size.setRange(64, 4096)
        self.tile_size.setSingleStep(64)
        self.tile_size.setValue(self.settings.default_tile_size)
        self.tile_size.setPrefix("Tile size: ")
        layout.addWidget(self.tile_size)

        split_button = QPushButton("Split and analyze map")
        split_button.clicked.connect(self.split_selected_map)
        layout.addWidget(split_button)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search tiles, e.g. bright green roads")
        self.search_input.returnPressed.connect(self.search_tiles)
        layout.addWidget(self.search_input)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_tiles)
        layout.addWidget(search_button)

        self.results = QListWidget()
        layout.addWidget(self.results)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def choose_map(self) -> None:
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Choose map image",
            str(Path.home()),
            "Images (*.png *.jpg *.jpeg *.tif *.tiff *.bmp)",
        )
        if filename:
            self.selected_map = Path(filename)
            self.file_label.setText(str(self.selected_map))

    def split_selected_map(self) -> None:
        if self.selected_map is None:
            self.results.addItem("Choose a map image first.")
            return
        output_dir = self.settings.tiles_dir / self.selected_map.stem
        result = self.splitter.split(self.selected_map, output_dir, self.tile_size.value())
        self.repository.add_result(result)
        self.results.clear()
        self.results.addItem(f"Created {len(result.tiles)} tiles from {result.source_filename}.")
        for tile in result.tiles:
            self.results.addItem(
                f"r{tile.row} c{tile.column}: {tile.analysis.description} ({tile.path})"
            )

    def search_tiles(self) -> None:
        hits = self.search_engine.search(self.search_input.text(), self.repository.list_tiles())
        self.results.clear()
        if not hits:
            self.results.addItem("No matching tiles found.")
            return
        for hit in hits:
            self.results.addItem(
                f"{hit.score:.2f} | r{hit.tile.row} c{hit.tile.column} | "
                f"{', '.join(hit.reasons)} | {hit.tile.path}"
            )


def run_desktop() -> int:
    app = QApplication([])
    window = MainWindow()
    window.show()
    return app.exec()
