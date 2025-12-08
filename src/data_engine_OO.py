"""
data_engine.py (OOP Version)
----------------------------
This version uses full OOP structure for database, multiprocessing,
and threading operations.
"""

import time
import sqlite3
from multiprocessing import Process
from threading import Thread

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# ============================================================
# ORM Setup (Model)
# ============================================================

Base = declarative_base()

class SubscriptionPlan(Base):
    """ORM model for subscription plans."""
    __tablename__ = "subscription_plans"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"SubscriptionPlan(id={self.id}, name='{self.name}')"


# ============================================================
# Database Manager (OOP)
# ============================================================

class DatabaseManager:
    """Handles both ORM (SQLAlchemy) and raw SQL (sqlite3)."""

    def __init__(self, db_path="sqlite:///streampy.db"):
        self.engine = create_engine(db_path)
        self.Session = sessionmaker(bind=self.engine)

    def setup_database(self):
        """Create tables and seed Subscription Plans."""
        Base.metadata.create_all(self.engine)

        with self.Session() as session:
            if session.query(SubscriptionPlan).count() == 0:
                session.add_all([
                    SubscriptionPlan(name="Basic"),
                    SubscriptionPlan(name="Premium")
                ])
                session.commit()

    def seed_users(self):
        """Seed demo users using raw sqlite3 SQL."""
        with sqlite3.connect("streampy.db") as conn:
            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER,
                    name TEXT,
                    plan TEXT
                )
            """)

            cur.execute("SELECT COUNT(*) FROM users")
            if cur.fetchone()[0] == 0:
                users = [
                    (1, "Alice", "Premium"),
                    (2, "Bob", "Basic"),
                    (3, "Charlie", "Premium")
                ]
                cur.executemany("INSERT INTO users VALUES (?, ?, ?)", users)
                conn.commit()

    def get_premium_users(self):
        """Fetch Premium users using raw SQL."""
        with sqlite3.connect("streampy.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE plan=?", ("Premium",))
            return cur.fetchall()


# ============================================================
# Multiprocessing Manager (OOP)
# ============================================================

class VideoEncoder:
    """Handles CPU-heavy encoding using multiprocessing."""

    def __init__(self, files):
        self.files = files

    @staticmethod
    def encode_file(file_name):
        """Encoding function to run inside each process."""
        print(f"[Encoding] Started encoding {file_name} ...")
        time.sleep(2)
        print(f"[Encoding] Finished encoding {file_name}")

    def start_encoding(self):
        """Encodes all files in parallel."""
        processes = [
            Process(target=VideoEncoder.encode_file, args=(f,))
            for f in self.files
        ]

        for p in processes:
            p.start()

        for p in processes:
            p.join()

        print("[Encoding] All encoding tasks completed.")


# ============================================================
# Threading Manager (OOP)
# ============================================================

class SubtitleDownloader:
    """Handles subtitle download thread + main video buffering."""

    def __init__(self, file_name):
        self.file_name = file_name

    def download(self):
        """Task that runs on a separate thread."""
        print(f"[Thread] Downloading subtitles for {self.file_name} ...")
        time.sleep(1.5)
        print(f"[Thread] Subtitles downloaded for {self.file_name}")

    def simulate_stream(self):
        """Main thread buffers while subtitle thread downloads."""
        thread = Thread(target=self.download)
        thread.start()

        print("[Main] Video buffering... please wait.")
        time.sleep(1)
        print("[Main] Video is now playing!")

        thread.join()
        print("[Main] All tasks done.")


# ============================================================
# Facade Class (Optional but clean)
# ============================================================

class StreamPyEngine:
    """Central controller class to run all features."""

    def __init__(self):
        self.db = DatabaseManager()
        self.encoder = VideoEncoder(files=["video1.mp4", "video2.mp4", "video3.mp4"])
        self.subtitles = SubtitleDownloader(file_name="video1.mp4")

    def run(self):
        # Setup database
        self.db.setup_database()
        self.db.seed_users()

        # Show premium users
        print("\n--- Premium Users ---")
        print(self.db.get_premium_users())

        # Run multiprocessing
        print("\n--- Video Encoding ---")
        self.encoder.start_encoding()

        # Run threading
        print("\n--- Subtitle Download ---")
        self.subtitles.simulate_stream()


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    StreamPyEngine().run()