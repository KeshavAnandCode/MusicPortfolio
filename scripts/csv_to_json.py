#!/usr/bin/env python3
"""
Convert a CSV of music metadata to JSON.
"""

import csv
import json
import os

# Adjust these paths if needed
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_CSV = os.path.join(BASE_DIR, "data", "music_metadata.csv")
OUTPUT_JSON = os.path.join(BASE_DIR, "data", "music_metadata.json")

def csv_to_json(input_csv: str, output_json: str):
    data = []

    with open(input_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Optional: convert numeric fields to int
            for key in ["duration", "bitrate", "sample_rate"]:
                if key in row and row[key]:
                    row[key] = int(row[key])
            data.append(row)

    # Write JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"✅ JSON exported to {output_json}")

if __name__ == "__main__":
    csv_to_json(INPUT_CSV, OUTPUT_JSON)