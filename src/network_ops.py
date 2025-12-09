"""
network_ops.py
--------------
Files, Network & System Operations for StreamPy

This module demonstrates:
- Sending POST requests (report_error)
- Reading CSV user data
- Checking/creating cache folder (os module)
- Archiving old log files (zipfile)
- Custom Exception: RegionBlockError
"""

import os
import csv
import requests
import zipfile


# 1. Custom Exception
class RegionBlockError(Exception):
    """Raised when a user tries to access blocked content."""
    pass


# 2. Web Request: POST error report
def report_error(msg: str):
    """
    Sends an error message to a server using a POST request.
    """
    data = {"error": msg}
    url = "https://jsonplaceholder.typicode.com/posts"
    try:
        requests.post(url, data=data)
    except requests.RequestException as e:
        print(f"Request failed: {e}")


# 3. CSV Reading: Print first 5 usernames
def read_usernames():
    """
    Reads data/users.csv and prints the first 5 usernames.
    Skips header row.
    """
    path = "data/users.csv"

    if not os.path.exists(path):
        print("CSV file not found:", path)
        return

    with open(path, "r") as user_data:
        reader = csv.reader(user_data)
        next(reader)  # Skip header

        for i, row in enumerate(reader, start=1):
            print(row[0])  # username column
            if i == 5:
                break


# 4. OS & ZIP Operations
def manage_cache_and_logs():
    """
    - Ensure 'cache/' folder exists.
    - Archive old log files into logs_archive.zip.
    """
    cache_folder = "cache"

    # Create cache folder if missing
    if not os.path.exists(cache_folder):
        os.makedirs(cache_folder)
        print("[Cache] Created 'cache/' folder.")

    # Archive log files if available
    logs_folder = "logs"
    if os.path.exists(logs_folder):
        zip_path = "logs_archive.zip"

        with zipfile.ZipFile(zip_path, "w") as zipf:
            for file in os.listdir(logs_folder):
                full_path = os.path.join(logs_folder, file)
                if os.path.isfile(full_path):
                    zipf.write(full_path)
                    print(f"[ZIP] Archived: {file}")
    else:
        print("[Logs] No logs folder found, skipping archiving.")


# 5. Region Block Demo Function
def access_content(country: str):
    """
    Raises RegionBlockError for restricted regions.
    Example restricted region: 'US'
    """
    blocked_regions = ["US", "UK"]

    if country in blocked_regions:
        raise RegionBlockError(f"Content not available in your region: {country}")

    print(f"Content streamed successfully for region: {country}")

#demo
if __name__ == "__main__":
    report_error("Service not found error")
    read_usernames()

    manage_cache_and_logs()

    # Region block demonstration
    try:
        access_content("US")
    except RegionBlockError as e:
        print("Error:", e)