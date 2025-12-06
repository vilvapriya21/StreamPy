"""
recommendations.py
-------------------
Core data processing logic for the StreamPy platform.

This module demonstrates essential data-processing techniques such as
dictionary comprehensions, higher-order functions using functools.reduce,
and filtering movie lists for kid-friendly profiles.
"""

from functools import reduce
from typing import List, Dict, Any


# Sample movie dataset used throughout this module.
MOVIES_DATA: List[Dict[str, Any]] = [
    {"title": "Interstellar", "genre": "Sci-Fi", "rating": "PG-13", "duration": 169},
    {"title": "Finding Nemo", "genre": "Animation", "rating": "G", "duration": 100},
    {"title": "The Conjuring", "genre": "Horror", "rating": "R", "duration": 112},
    {"title": "Avengers", "genre": "Action", "rating": "PG-13", "duration": 143},
    {"title": "Toy Story", "genre": "Animation", "rating": "G", "duration": 81},
]


def lookup_table(movies: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Create a lookup table that maps movie titles to content ratings.

    This function uses a dictionary comprehension to transform a list of movie
    dictionaries into a lightweight lookup structure useful for quick rating
    references.

    Args:
        movies: A list of dictionaries where each dictionary represents a movie
            with metadata including title and rating.

    Returns:
        A dictionary mapping each movie title to its rating label.
    """
    return {movie.get("title", "Unknown"): movie.get("rating", "NR") for movie in movies}


def total_duration(playlist: List[Dict[str, Any]]) -> int:
    """
    Calculate the total duration of a playlist.

    This function demonstrates the use of the higher-order function
    functools.reduce to accumulate the total runtime of all movies in the
    playlist.

    Args:
        playlist: A list of movie dictionaries containing a numeric "duration"
            field for each movie.

    Returns:
        The total duration of all movies in the playlist, measured in minutes.
    """
    return reduce(lambda total, movie: total + movie.get("duration", 0), playlist, 0)


def kids_profile_filter(movies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter out movies that are not suitable for a kid-friendly profile.

    This function uses the built-in filter() function to exclude movies rated
    "R", ensuring that only age-appropriate titles remain in the returned list.
    The rating check is case-insensitive.

    Args:
        movies: A list of movie dictionaries including a "rating" field.

    Returns:
        A list containing only movies that are not rated "R".
    """
    return list(filter(lambda movie: movie.get("rating", "").upper() != "R", movies))


if __name__ == "__main__":
    print("Lookup Table:", lookup_table(MOVIES_DATA))
    print("Total Duration:", total_duration(MOVIES_DATA))
    print("Kids Profile Movies:", kids_profile_filter(MOVIES_DATA))