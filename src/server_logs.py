import logging
import time
from functools import wraps
from collections import deque,defaultdict

logging.basicConfig(
    filename="logs/server.log",  # all logs go into this file
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
def log_execution(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start=time.time()
        result=func(*args,**kwargs)
        end=time.time()
        function_runtime=end-start
        if(function_runtime>1):
            logging.warning(f"{func.__name__} took {function_runtime:.2f} seconds")
        else:
            logging.info(f"{func.__name__} took {function_runtime:.2f} seconds")
        
        return result
    
    return wrapper

@log_execution
def slow_function():
    time.sleep(2)
    print("function exceuted")


"""
Collections utilities for media server:
- RecentlyWatched: maintains the last 5 watched items (deque)
- CommentStore: groups user comments by video ID using defaultdict(list)
"""

from collections import deque, defaultdict


class RecentlyWatched:
    """
    Maintains a list of the last 5 watched items.
    Oldest items are removed automatically.
    """

    def __init__(self, max_items=5):
        self.history = deque(maxlen=max_items)

    def add(self, video_title: str):
        """Add a video to the recently watched list."""
        self.history.append(video_title)

    def get_history(self):
        """Return the list of recently watched videos."""
        return list(self.history)


class CommentStore:
    """
    Stores comments grouped by video ID using defaultdict(list).
    Example: { "VID23": ["Nice video!", "Loved it!"] }
    """

    def __init__(self):
        self.comments = defaultdict(list)

    def add_comment(self, video_id: str, comment: str):
        """Add a comment for a specific video."""
        self.comments[video_id].append(comment)

    def get_comments(self, video_id: str):
        """Get all comments for a video ID."""
        return self.comments.get(video_id, [])

    def all_comments(self):
        """Return the whole comments dictionary."""
        return dict(self.comments)


# ------------------------------------------
# Example usage (Run only when file executed)
# ------------------------------------------
if __name__ == "__main__":
    #log_execution example
    slow_function()
    
    # Recently Watched Example
    rw = RecentlyWatched()
    for vid in ["Movie1", "Movie2", "Movie3", "Movie4", "Movie5", "Movie6"]:
        rw.add(vid)

    print("Recently Watched:", rw.get_history())
    # Output → ['Movie2', 'Movie3', 'Movie4', 'Movie5', 'Movie6']

    # Comments Example
    cs = CommentStore()
    cs.add_comment("VID101", "Great episode!")
    cs.add_comment("VID101", "Waiting for the next one.")
    cs.add_comment("VID202", "Amazing movie!")

    print("Comments for VID101:", cs.get_comments("VID101"))
    print("All comments:", cs.all_comments())
