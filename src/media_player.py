"""
media_player.py
-----------------
Core media playback logic for StreamPy.

Demonstrates:
- Inheritance via parent class `Content`
- Polymorphism with `play()` in Movie and Series
- Encapsulation using protected attribute `_stream_key` with property
- Magic methods for developer-friendly object representation
- Input validation and basic edge case handling
"""

from typing import Optional


class Content:
    """
    Base class for all media content.

    Attributes:
        content_id: Unique ID for the content
        title: Name of the content
        _stream_key: Protected attribute for streaming access
    """

    def __init__(self, content_id: int, title: str) -> None:
        """Initialize content with ID and title; validate inputs."""
        if not isinstance(content_id, int):
            raise TypeError("content_id must be an integer")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title must be a non-empty string")

        self.content_id: int = content_id
        self.title: str = title
        self._stream_key: Optional[str] = None  


    @property
    def stream_key(self) -> str:
        """Get the stream key; raise error if not set."""
        if self._stream_key is None:
            raise ValueError(f"Stream key for '{self.title}' not assigned")
        return self._stream_key

    @stream_key.setter
    def stream_key(self, key: str) -> None:
        """Set the stream key (must be a non-empty string)."""
        if not isinstance(key, str) or not key.strip():
            raise ValueError("Stream key must be a non-empty string")
        self._stream_key = key


class Movie(Content):
    """Represents a movie with a play() method."""

    def play(self) -> None:
        """Play the movie if stream key is set; otherwise, warn."""
        if self._stream_key is None:
            print(f"Cannot play '{self.title}': stream key not set")
        else:
            print("Starting Film...")

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Movie(id={self.content_id}, title='{self.title}')"


class Series(Content):
    """Represents a TV series with a play() method."""

    def play(self, episode: int = 1) -> None:
        """Play a specific episode if stream key is set; validate episode."""
        if not isinstance(episode, int) or episode < 1:
            print(f"Invalid episode number for '{self.title}'")
            return

        if self._stream_key is None:
            print(f"Cannot play '{self.title}': stream key not set")
        else:
            print(f"Resuming S01E{episode:02d}...")

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Series(id={self.content_id}, title='{self.title}')"


# Demo
if __name__ == "__main__":
    movie = Movie(101, "Interstellar")
    series = Series(201, "Stranger Things")

    print(movie)
    print(series)

    # Play without stream key
    movie.play()
    series.play()

    # Set stream keys (using property)
    movie.stream_key = "abc123xyz"
    series.stream_key = "serieskey456"

    # Play with stream keys
    movie.play()
    series.play(2)

    # Access stream keys (using property)
    print("Movie Stream Key:", movie.stream_key)
    print("Series Stream Key:", series.stream_key)