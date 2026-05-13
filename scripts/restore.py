#!/usr/bin/env python3
"""
philharmonic/scripts/restore.py

Restores Hyperagent Tables from GitHub JSON backup.
Run this when tables are missing or wiped.

Usage:
  python3 restore.py --check        # check if tables exist
  python3 restore.py --restore      # restore from GitHub
  python3 restore.py --backup       # push current table state to GitHub
"""

import json
import sys
import subprocess
from datetime import datetime

GITHUB_REPO = "cameronaziz/philharmonic"
GITHUB_RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/data"

TABLE_IDS = {
    "companies": None,   # set after table creation
    "jobs": None,
    "preferences": None
}

def fetch_github_data(filename):
    url = f"{GITHUB_RAW_BASE}/{filename}"
    result = subprocess.run(
        ["curl", "-sf", url],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Failed to fetch {filename} from GitHub")
        return None
    return json.loads(result.stdout)

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"

    if mode == "--check":
        print("Checking GitHub backup availability...")
        for fname in ["companies.json", "jobs.json", "preferences.json"]:
            data = fetch_github_data(fname)
            if data:
                count = len(data.get("rows", []))
                print(f"  {fname}: {count} rows available")
            else:
                print(f"  {fname}: NOT FOUND")

    elif mode == "--restore":
        print("Restoring from GitHub backup...")
        companies = fetch_github_data("companies.json")
        if companies:
            print(f"  Loaded {len(companies['rows'])} companies")
            # Output as JSON for the agent to upsert into tables
            print(json.dumps({"action": "restore", "companies": companies["rows"]}))

if __name__ == "__main__":
    main()
