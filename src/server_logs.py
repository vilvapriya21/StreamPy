"""
server_logs.py
----------------
Demonstrates:

- Decorators for execution-time logging with error capture
- Threshold-based logging (WARNING if runtime > 1 second)
- Deque for maintaining recently watched items
- defaultdict for grouping comments by video ID
"""

import logging
import time
import os
from functools import wraps
from collections import deque, defaultdict
from typing import Callable, Any


# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)


# Logging Configuration
logging.basicConfig(
    filename="logs/server.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


# Decorator for execution-time measurement + exception logging
def log_execution(func: Callable) -> Callable:
    """
    Logs how long a function takes to execute.
    - Logs WARNING if runtime > 1 second
    - Logs INFO otherwise
    - Logs ERROR if the function raises an exception
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.time()

        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logger.error(f"{func.__name__} failed: {e}")
            raise  # Re-raise so calling code still sees the failure

        duration = time.time() - start
        message = f"{func.__name__} took {duration:.2f} seconds"

        if duration > 1:
            logger.warning(message)
        else:
            logger.info(message)

        return result

    return wrapper


#function to demonstrate log_execution
@log_execution
def slow_function() -> None:
    """Function used for demonstrating decorator behavior."""
    time.sleep(2)
    print("Function executed.")


# Recently Watched (deque implementation)
class RecentlyWatched:
    """
    Maintains a fixed-size list of recently watched video titles.
    Automatically discards the oldest entry when full.
    """

    def __init__(self, max_items: int = 5) -> None:
        if max_items <= 0:
            raise ValueError("max_items must be greater than zero.")
        self.history: deque[str] = deque(maxlen=max_items)

    def add(self, video_title: str) -> None:
        """Add a non-empty video title to the history."""
        if not isinstance(video_title, str):
            raise TypeError("video_title must be a string.")
        if not video_title.strip():
            raise ValueError("video_title cannot be empty.")

        self.history.append(video_title)

    def get_history(self) -> list[str]:
        """Return a list of recently watched items."""
        return list(self.history)


# Comment Store (defaultdict implementation)
class CommentStore:
    """
    Stores user comments grouped by video ID using defaultdict(list).
    Structure:
        {
            "VID23": ["Nice!", "Awesome"],
            "VID88": ["Good documentary"]
        }
    """

    def __init__(self) -> None:
        self.comments: defaultdict[str, list[str]] = defaultdict(list)

    def add_comment(self, video_id: str, comment: str) -> None:
        """Add a validated comment under a specific video ID."""

        if not isinstance(video_id, str):
            raise TypeError("video_id must be a string.")
        if not video_id.strip():
            raise ValueError("video_id cannot be empty.")

        if not isinstance(comment, str):
            raise TypeError("comment must be a string.")
        if not comment.strip():
            raise ValueError("comment cannot be empty.")

        self.comments[video_id].append(comment)

    def get_comments(self, video_id: str) -> list[str]:
        """Return comments for a specific video ID."""
        return self.comments.get(video_id, [])

    def all_comments(self) -> dict[str, list[str]]:
        """Return all grouped comments."""
        return dict(self.comments)


#Demo
if __name__ == "__main__":

    # Decorator Demo
    slow_function()

    # Recently Watched Demo
    rw = RecentlyWatched()
    for vid in ["Movie1", "Movie2", "Movie3", "Movie4", "Movie5", "Movie6"]:
        rw.add(vid)
    print("Recently Watched:", rw.get_history())

    # CommentStore Demo
    cs = CommentStore()
    cs.add_comment("VID101", "Great episode!")
    cs.add_comment("VID101", "Waiting for the next one...")
    cs.add_comment("VID202", "Amazing cinematography!")

    print("Comments for VID101:", cs.get_comments("VID101"))
    print("All comments:", cs.all_comments())