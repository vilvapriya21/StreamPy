"""
recommendations.py
-------------------
Functional Programming & Data Processing file for the StreamPy platform.
Includes:
- lookup table generation
- playlist duration calculation
- kid-friendly movie filtering
"""

from functools import reduce
from typing import List, Dict, Any

# Sample dataset used across the module.
MOVIES_DATA: List[Dict[str, Any]] = [
    {"title": "Interstellar", "genre": "Sci-Fi", "rating": "PG-13", "duration": 169},
    {"title": "Finding Nemo", "genre": "Animation", "rating": "G", "duration": 100},
    {"title": "The Conjuring", "genre": "Horror", "rating": "R", "duration": 112},
    {"title": "Avengers", "genre": "Action", "rating": "PG-13", "duration": 143},
    {"title": "Toy Story", "genre": "Animation", "rating": "G", "duration": 81},
]


def lookup_table(movies: List[Dict[str, Any]]) -> Dict[str, str]:
    """Return a {title: rating} lookup dictionary."""
    return {movie.get("title", "Unknown"): movie.get("rating", "NR") for movie in movies}


def total_duration(playlist: List[Dict[str, Any]]) -> int:
    """Calculate the total duration (in minutes) of all movies in a playlist."""
    return reduce(lambda total, movie: total + movie.get("duration", 0), playlist, 0)


def kids_profile_filter(movies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return only movies that are not rated 'R'."""
    return list(filter(lambda m: m.get("rating", "").upper() != "R", movies))

#demo 
if __name__ == "__main__":
    print("Lookup Table:", lookup_table(MOVIES_DATA))
    print("Total Duration:", total_duration(MOVIES_DATA))
    print("Kids Profile Movies:", kids_profile_filter(MOVIES_DATA))