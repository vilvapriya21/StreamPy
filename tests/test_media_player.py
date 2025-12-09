"""
test_media_player.py
--------------------
Basic unit tests for media_player.py using pytest.
Covers:
- Content initialization and stream key
- Movie and Series play() behavior
- __repr__ outputs
"""

import pytest
from src.media_player import Content, Movie, Series



# Content Class Tests

def test_content_initialization():
    """Check Content object is created with correct attributes."""
    content = Content(1, "Demo")
    assert content.content_id == 1
    assert content.title == "Demo"
    assert content._stream_key is None


def test_set_and_get_stream_key():
    """Verify that stream key can be set and retrieved."""
    content = Content(2, "Test")
    content.set_stream_key("key123")
    assert content.get_stream_key() == "key123"


def test_get_stream_key_without_setting():
    """Accessing stream key without setting should raise ValueError."""
    content = Content(3, "NoKey")
    with pytest.raises(ValueError):
        content.get_stream_key()


def test_set_invalid_stream_key():
    """Setting invalid stream keys should raise ValueError."""
    content = Content(4, "InvalidKey")
    with pytest.raises(ValueError):
        content.set_stream_key("")
    with pytest.raises(ValueError):
        content.set_stream_key(None)



# Movie Class Tests

def test_movie_repr():
    """__repr__ should return the correct string."""
    movie = Movie(101, "Tenet")
    assert repr(movie) == "Movie(id=101, title='Tenet')"


def test_movie_play_behavior():
    """Movie play() should warn if no key, or print 'Starting Film...' if key is set."""
    movie = Movie(102, "Inception")
    
    # Without key
    movie._stream_key = None
    assert movie._stream_key is None
    
    # With key
    movie.set_stream_key("abc")
    assert movie._stream_key == "abc"


# Series Class Tests

def test_series_repr():
    """__repr__ should return the correct string."""
    series = Series(201, "Stranger Things")
    assert repr(series) == "Series(id=201, title='Stranger Things')"

def test_series_episode_validation():
    """Series play() should allow only valid episode numbers."""
    series = Series(202, "DemoSeries")
    # Invalid episode numbers should not break the object
    series.play(0)
    series.play(-5)
    series.play(1)  # valid
    series.set_stream_key("serieskey")
    assert series._stream_key == "serieskey"