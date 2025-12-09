"""
test_server_logs.py
-------------------
Basic unit tests for server_logs.py using pytest.

Covers:
- RecentlyWatched deque behavior
- CommentStore defaultdict behavior
- log_execution decorator runs
"""

import pytest
import time
from src.server_logs import RecentlyWatched, CommentStore, log_execution


# RecentlyWatched Tests

def test_recently_watched_add_and_history():
    """Adding videos should be stored in history up to max length."""
    rw = RecentlyWatched(max_items=3)
    rw.add("Movie1")
    rw.add("Movie2")
    rw.add("Movie3")
    assert rw.get_history() == ["Movie1", "Movie2", "Movie3"]

    # Adding another should remove the oldest (Movie1)
    rw.add("Movie4")
    assert rw.get_history() == ["Movie2", "Movie3", "Movie4"]


def test_recently_watched_invalid_input():
    """Adding invalid titles should raise errors."""
    rw = RecentlyWatched()
    with pytest.raises(ValueError):
        rw.add("")  # empty string
    with pytest.raises(TypeError):
        rw.add(123)  # not a string



# CommentStore Tests

def test_comment_store_add_and_get():
    """Comments should be grouped by video ID and retrievable."""
    cs = CommentStore()
    cs.add_comment("VID1", "Great!")
    cs.add_comment("VID1", "Loved it")
    cs.add_comment("VID2", "Nice episode")

    assert cs.get_comments("VID1") == ["Great!", "Loved it"]
    assert cs.get_comments("VID2") == ["Nice episode"]
    assert cs.get_comments("VID3") == []  # no comments for VID3

def test_comment_store_invalid_input():
    """Invalid video_id or comment should raise errors."""
    cs = CommentStore()
    with pytest.raises(ValueError):
        cs.add_comment("", "Comment")  # empty video_id
    with pytest.raises(ValueError):
        cs.add_comment("VID1", "")     # empty comment
    with pytest.raises(TypeError):
        cs.add_comment(123, "Comment") # video_id not string
    with pytest.raises(TypeError):
        cs.add_comment("VID1", 456)    # comment not string


# log_execution Decorator Test

def test_log_execution_runs():
    """Decorator should run a function and return result."""
    
    @log_execution
    def fast_func():
        return 42

    @log_execution
    def slow_func_demo():
        time.sleep(1.1)
        return "done"

    # Check return values
    assert fast_func() == 42
    assert slow_func_demo() == "done"