"""
data_engine.py
--------------
Concurrency and database operations for StreamPy.

Demonstrates:
- SQLAlchemy ORM model
- Raw SQL with sqlite3
- Multiprocessing (video encoding)
- Threading (subtitle download)
"""

import time
import sqlite3
from multiprocessing import Process
from threading import Thread
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLAlchemy ORM
Base = declarative_base()

class SubscriptionPlan(Base):
    """ORM model for subscription plans."""
    __tablename__ = "subscription_plans"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"SubscriptionPlan(id={self.id}, name='{self.name}')"

def setup_database():
    """Initialize DB and create subscription plan table if missing."""
    engine = create_engine("sqlite:///streampy.db")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    with Session() as session:
        if session.query(SubscriptionPlan).count() == 0:
            session.add_all([
                SubscriptionPlan(name="Basic"),
                SubscriptionPlan(name="Premium")
            ])
            session.commit()
    return engine

# SQLite raw SQL - seed users separately
def seed_users():
    """Insert demo users if the table is empty."""
    with sqlite3.connect("streampy.db") as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER,
                name TEXT,
                plan TEXT
            )
        """)
        # Check if table is empty
        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            users = [
                (1, "Alice", "Premium"),
                (2, "Bob", "Basic"),
                (3, "Charlie", "Premium")
            ]
            cur.executemany("INSERT INTO users VALUES (?, ?, ?)", users)
            conn.commit()

def fetch_premium_users():
    """Return all users with Premium plan."""
    with sqlite3.connect("streampy.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE plan=?", ("Premium",))
        return cur.fetchall()

# Multiprocessing
def encode_video(file_name):
    """Simulate CPU-heavy video encoding."""
    print(f"[Encoding] Started encoding {file_name} ...")
    time.sleep(2)
    print(f"[Encoding] Finished encoding {file_name}")

def run_video_encoding():
    """Run multiple encoding tasks in parallel."""
    files = ["video1.mp4", "video2.mp4", "video3.mp4"]
    processes = [Process(target=encode_video, args=(f,)) for f in files]

    for p in processes: p.start()
    for p in processes: p.join()
    print("[Encoding] All encoding tasks completed.")

# Threading
def download_subtitles(file_name):
    """Simulate subtitle download."""
    print(f"[Thread] Downloading subtitles for {file_name} ...")
    time.sleep(1.5)
    print(f"[Thread] Subtitles downloaded for {file_name}")

def simulate_streaming():
    """Download subtitles in a thread while main thread buffers video."""
    thread = Thread(target=download_subtitles, args=("video1.mp4",))
    thread.start()
    print("[Main] Video buffering... Please wait.")
    time.sleep(1)
    print("[Main] Video is now playing!")
    thread.join()
    print("[Main] All tasks done.")

# Demo
if __name__ == "__main__":
    setup_database()
    seed_users()

    print("\n--- Premium Users ---")
    print(fetch_premium_users())

    print("\n--- Multiprocessing (Encoding) ---")
    run_video_encoding()

    print("\n--- Threading (Subtitles) ---")
    simulate_streaming()