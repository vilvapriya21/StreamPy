"""
recommendations.py
-------------------
Core data processing logic for the StreamPy platform.

This module demonstrates:
- Dictionary Comprehensions
- Higher-Order functions using functools.reduce
- Filtering movie lists for Kids Profiles
"""

from functools import reduce
from typing import List, Dict

# Sample movie data
movies_data = [
    {"title": "Interstellar", "genre": "Sci-Fi", "rating": "PG-13", "duration": 169},
    {"title": "Finding Nemo", "genre": "Animation", "rating": "G", "duration": 100},
    {"title": "The Conjuring", "genre": "Horror", "rating": "R", "duration": 112},
    {"title": "Avengers", "genre": "Action", "rating": "PG-13", "duration": 143},
    {"title": "Toy Story", "genre": "Animation", "rating": "G", "duration": 81},
]

def lookup_table(movies: List[Dict]) -> Dict[str, str]:
    """
    Returns a dictionary mapping movie titles to ratings.
    """
    return {m["title"]: m["rating"] for m in movies}

def total_duration(playlist: List[Dict]) -> int:
    """
    Returns the total duration of all movies in the playlist.
    """
    return reduce(lambda total, movie: total + movie["duration"], playlist, 0)

def kids_profile_filter(movies: List[Dict]) -> List[Dict]:
    """
    Filters out R-rated movies for Kids Profile.
    """
    return list(filter(lambda m: m["rating"] != "R", movies))

# Demo usage
if __name__ == "__main__":
    print("Lookup Table:", lookup_table(movies_data))
    print("Total Duration:", total_duration(movies_data))
    print("Kids Profile Movies:", kids_profile_filter(movies_data))