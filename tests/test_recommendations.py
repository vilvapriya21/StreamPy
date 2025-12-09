"""
test_recommendations.py
-----------------------
Unit tests for recommendations.py: lookup_table, total_duration, kids_profile_filter.
Uses pytest to validate expected behavior for typical, edge, and invalid input cases.
"""

import pytest
from src.recommendations import lookup_table, total_duration, kids_profile_filter


# lookup_table tests

def test_lookup_table_basic():
    """Check basic title-to-rating mapping."""
    movies = [
        {"title": "A", "rating": "PG"},
        {"title": "B", "rating": "R"}
    ]
    result = lookup_table(movies)
    assert result == {"A": "PG", "B": "R"}


def test_lookup_table_missing_fields():
    """Check behavior when title or rating is missing."""
    movies = [
        {"rating": "PG"},          # missing title
        {"title": "X"},            # missing rating
        {}                         # missing both
    ]
    result = lookup_table(movies)
    assert result == {
        "Unknown": "PG",
        "X": "NR",
        "Unknown": "NR"
    }


def test_lookup_table_strips_whitespace():
    """Check that extra spaces in title/rating are removed."""
    movies = [
        {"title": "   Space   ", "rating": " PG-13 "}
    ]
    result = lookup_table(movies)
    assert result == {"Space": "PG-13"}


# total_duration tests

def test_total_duration_basic():
    """Sum of durations for normal numeric inputs."""
    playlist = [
        {"duration": 100},
        {"duration": 50}
    ]
    assert total_duration(playlist) == 150


def test_total_duration_missing_key():
    """Missing duration defaults to 0."""
    playlist = [
        {"duration": 100},
        {}
    ]
    assert total_duration(playlist) == 100


def test_total_duration_non_numeric():
    """Non-numeric or None duration is treated as 0."""
    playlist = [
        {"duration": "200"},
        {"duration": "abc"},
        {"duration": None},
    ]
    assert total_duration(playlist) == 200


def test_total_duration_negative_values():
    """Negative duration is treated as 0."""
    playlist = [
        {"duration": -50},
        {"duration": 120}
    ]
    assert total_duration(playlist) == 120


# kids_profile_filter tests 

def test_kids_filter_basic():
    """R-rated movies are removed."""
    movies = [
        {"rating": "PG-13"},
        {"rating": "R"},
        {"rating": "G"}
    ]
    result = kids_profile_filter(movies)
    assert len(result) == 2
    assert {"rating": "R"} not in result


def test_kids_filter_case_insensitive():
    """Filter works regardless of case."""
    movies = [{"rating": "r"}]
    result = kids_profile_filter(movies)
    assert result == []


def test_kids_filter_with_whitespace():
    """Filter works with extra whitespace."""
    movies = [{"rating": "  R  "}]
    result = kids_profile_filter(movies)
    assert result == []


def test_kids_filter_missing_rating():
    """Movies without rating are not filtered."""
    movies = [{}]
    result = kids_profile_filter(movies)
    assert result == [{}]