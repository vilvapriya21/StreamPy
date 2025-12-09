"""
recommendations.py
-------------------
Functional utilities for StreamPy: lookup tables, playlist duration, kids filter.
"""

import logging
import json
from functools import reduce
from typing import List, Dict, Any
from pathlib import Path

# Configure logging
LOG_FILE = Path(__file__).parent.parent / "logs" / "recommendations.log"
LOG_FILE.parent.mkdir(exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Path to the JSON data file
MOVIES_FILE = Path(__file__).parent.parent / "data" / "movies.json"


def load_movies() -> List[Dict[str, Any]]:
    """Load movies from JSON file. Returns empty list if file is missing or invalid."""
    try:
        with open(MOVIES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("Movies file not found: %s", MOVIES_FILE)
    except json.JSONDecodeError:
        logging.error("Invalid JSON in movies file: %s", MOVIES_FILE)
    return []


def _safe_duration(value: Any) -> int:
    """Convert value to non-negative int; invalid or negative -> 0. Logs warning if conversion fails."""
    try:
        num = int(value)
        if num < 0:
            logging.warning("Negative duration encountered: %s. Converted to 0.", value)
            return 0
        return num
    except (TypeError, ValueError):
        logging.warning("Invalid duration value encountered: %s. Converted to 0.", value)
        return 0


def lookup_table(movies: List[Dict[str, Any]]) -> Dict[str, str]:
    """Return {title: rating} dictionary. Input: list of movie dicts."""
    return {
        str(movie.get("title", "Unknown")).strip() or "Unknown":
        str(movie.get("rating", "NR")).strip() or "NR"
        for movie in movies
    }


def total_duration(playlist: List[Dict[str, Any]]) -> int:
    """Sum durations of all movies safely, treating missing or invalid values as 0."""
    return reduce(
        lambda total, movie: total + _safe_duration(movie.get("duration", 0)),
        playlist,
        0
    )


def kids_profile_filter(movies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return list of movies excluding R-rated content. Case-insensitive, whitespace-safe."""
    return list(
        filter(
            lambda m: str(m.get("rating", "")).strip().upper() != "R",
            movies
        )
    )


if __name__ == "__main__":
    MOVIES_DATA = load_movies()
    print("Lookup Table:", lookup_table(MOVIES_DATA))
    print("Total Duration:", total_duration(MOVIES_DATA))
    print("Kids Profile Movies:", kids_profile_filter(MOVIES_DATA))