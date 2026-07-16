"""Tile search service."""

from ai_map_detection.core.models import MapTile, SearchHit


class TileSearchEngine:
    """Simple semantic-style search over tile metadata."""

    def search(self, query: str, tiles: list[MapTile], limit: int = 20) -> list[SearchHit]:
        terms = [term.lower() for term in query.split() if term.strip()]
        if not terms:
            return []

        hits: list[SearchHit] = []
        for tile in tiles:
            score, reasons = self._score_tile(terms, tile)
            if score > 0:
                hits.append(SearchHit(tile=tile, score=round(score, 3), reasons=reasons))

        hits.sort(key=lambda hit: hit.score, reverse=True)
        return hits[:limit]

    def _score_tile(self, terms: list[str], tile: MapTile) -> tuple[float, list[str]]:
        haystack = " ".join(
            [
                tile.source_filename,
                str(tile.path),
                tile.analysis.dominant_color,
                tile.analysis.description,
                *tile.analysis.labels,
            ]
        ).lower()
        score = 0.0
        reasons: list[str] = []

        for term in terms:
            if term in haystack:
                score += 1.0
                reasons.append(f"matched '{term}' in metadata")

        if "bright" in terms and tile.analysis.brightness >= 150:
            score += 0.7
            reasons.append("tile is bright")
        if "dark" in terms and tile.analysis.brightness < 150:
            score += 0.7
            reasons.append("tile is dark")
        if {"detail", "detailed", "roads", "road"}.intersection(terms):
            score += min(tile.analysis.edge_density * 2, 1.0)
            reasons.append("edge density suggests detailed map features")

        return score, reasons
