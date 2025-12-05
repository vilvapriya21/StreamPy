"""
data_engine.py
--------------
Concurrency & Database Operations for StreamPy

This module demonstrates:
- SQLAlchemy ORM model (SubscriptionPlan)
- sqlite3 raw SQL query
- Multiprocessing for CPU-heavy Video Encoding
- Threading for subtitle download
"""

import time
import sqlite3
from multiprocessing import Process
from threading import Thread

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# -------------------------------
# 1. SQLAlchemy ORM: SubscriptionPlan
# -------------------------------

Base = declarative_base()

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"SubscriptionPlan(id={self.id}, name='{self.name}')"


def setup_database():
    """Create the table and insert sample plans."""
    engine = create_engine("sqlite:///streampy.db")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Insert ONLY if table is empty
    if session.query(SubscriptionPlan).count() == 0:
        session.add_all([
            SubscriptionPlan(name="Basic"),
            SubscriptionPlan(name="Premium")
        ])
        session.commit()

    session.close()
    return engine


def fetch_premium_users():
    """
    Uses sqlite3 to demonstrate raw SQL query:
    Select all users on the 'Premium' plan.
    (Assumes a 'users' table exists with column 'plan')
    """
    conn = sqlite3.connect("streampy.db")
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT, plan TEXT)")
    cur.execute("INSERT INTO users VALUES (1, 'Alice', 'Premium')")
    cur.execute("INSERT INTO users VALUES (2, 'Bob', 'Basic')")
    cur.execute("INSERT INTO users VALUES (3, 'Charlie', 'Premium')")
    conn.commit()

    cur.execute("SELECT * FROM users WHERE plan='Premium'")
    result = cur.fetchall()

    conn.close()
    return result


# -------------------------------
# 2. Multiprocessing: Video Encoding
# -------------------------------

def encode_video(file_name):
    print(f"[Encoding] Started encoding {file_name} ...")
    time.sleep(2)  # Simulate CPU work
    print(f"[Encoding] Finished encoding {file_name}")


def run_video_encoding():
    files = ["video1.mp4", "video2.mp4", "video3.mp4"]
    processes = []

    for f in files:
        p = Process(target=encode_video, args=(f,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()  # wait for all encodings to finish

    print("[Encoding] All encoding tasks completed.")


# -------------------------------
# 3. Threading: Subtitle Download
# -------------------------------

def download_subtitles(file_name):
    print(f"[Thread] Downloading subtitles for {file_name} ...")
    time.sleep(1.5)  # simulate network latency
    print(f"[Thread] Subtitles downloaded for {file_name}")


def simulate_streaming():
    thread = Thread(target=download_subtitles, args=("video1.mp4",))
    thread.start()

    print("[Main] Video buffering... Please wait.")
    time.sleep(1)
    print("[Main] Video is now playing!")

    thread.join()  # ensure subtitle download finishes
    print("[Main] All tasks done.")


# -------------------------------
# Demo Run
# -------------------------------
if __name__ == "__main__":
    setup_database()

    print("\n--- Premium Users (Raw SQL) ---")
    print(fetch_premium_users())

    print("\n--- Multiprocessing (Video Encoding) ---")
    run_video_encoding()

    print("\n--- Threading (Subtitle Download) ---")
    simulate_streaming()