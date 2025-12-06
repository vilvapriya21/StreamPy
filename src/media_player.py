"""
media_player.py
-----------------
This module demonstrates advanced OOP concepts for the StreamPy platform.

Features included:
- Inheritance using a parent class `Content`
- Polymorphism using the `play()` method in `Movie` and `Series`
- Encapsulation with a protected attribute `_stream_key`
- Magic Method: __repr__ for developer-friendly object representation
"""


class Content:
    """
    Parent class for all types of content in StreamPy.
    Holds basic information such as content ID, title, and a protected stream key.
    """

    def __init__(self, content_id: int, title: str):
        """
        Initialize a Content object.

        Args:
            content_id (int): Unique ID for the content.
            title (str): Title of the content.
        """
        self.content_id = content_id
        self.title = title
        self._stream_key = None  # Protected attribute

    def set_stream_key(self, key: str) -> None:
        """
        Set the protected stream key.

        Args:
            key (str): The stream key to assign.

        Notes:
            A simple type check is included as a basic validation step.
        """
        if not isinstance(key, str):
            raise TypeError("Stream key must be a string.")
        self._stream_key = key

    def get_stream_key(self) -> str:
        """
        Retrieve the protected stream key.

        Returns:
            str: The assigned stream key (or None if not set).
        """
        return self._stream_key


class Movie(Content):
    """
    Represents a movie in the StreamPy platform.
    Inherits from Content and overrides the play() method.
    """

    def play(self) -> None:
        """Simulate playing a movie."""
        print("Starting Film...")

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        return f"Movie(id={self.content_id}, title='{self.title}')"


class Series(Content):
    """
    Represents a TV series in the StreamPy platform.
    Inherits from Content and overrides the play() method.
    """

    def play(self) -> None:
        """Simulate playing a series episode."""
        print("Resuming S01E01...")

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        return f"Series(id={self.content_id}, title='{self.title}')"


# Demo section
if __name__ == "__main__":
    m = Movie(101, "Interstellar")
    s = Series(201, "Stranger Things")

    print(m)
    print(s)

    m.play()
    s.play()