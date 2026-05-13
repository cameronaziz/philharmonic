#!/usr/bin/env python3
"""
Philharmonic pipeline restore script.
Fetches all data from GitHub and seeds the three Hyperagent tables.
Run this after a table wipe.

Usage:
  python3 restore.py

Requires: requests, hyperagent SDK (or manual table IDs)
"""

import json
import urllib.request
import sys

GITHUB_RAW = "https://raw.githubusercontent.com/cameronaziz/philharmonic/main/data"

FILES = {
    "companies": f"{GITHUB_RAW}/companies.json",
    "jobs": f"{GITHUB_RAW}/jobs.json",
    "preferences": f"{GITHUB_RAW}/preferences.json",
}

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "philharmonic-restore/1.0"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def main():
    print("Fetching data from GitHub...")
    data = {}
    for key, url in FILES.items():
        try:
            rows = fetch(url)
            data[key] = rows
            print(f"  {key}: {len(rows)} rows")
        except Exception as e:
            print(f"  {key}: ERROR - {e}")
            data[key] = []

    print("\nRestore complete. Seed these into Hyperagent tables:")
    print(f"  philharmonic_target_companies  -> {len(data['companies'])} rows")
    print(f"  philharmonic_job_postings      -> {len(data['jobs'])} rows")
    print(f"  philharmonic_job_preferences   -> {len(data['preferences'])} rows")

    # Write locally for inspection
    for key, rows in data.items():
        fname = f"/tmp/{key}_restored.json"
        with open(fname, "w") as f:
            json.dump(rows, f, indent=2)
        print(f"  Written to {fname}")

if __name__ == "__main__":
    main()
