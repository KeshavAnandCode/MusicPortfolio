#!/usr/bin/env python3
"""
Professional CSV generator for music portfolio.

Scans public/music directories and creates a master CSV with metadata fields.
Automatically fills title (from filename), artist, bitrate, sample rate, duration, and file creation date.
Stores paths relative to project root, with separate columns for FLAC and MP3.
"""

import os
import csv
from datetime import datetime
from mutagen import File as MutagenFile

# Project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Folders to scan for audio files
MUSIC_DIRS = {
    "flac": os.path.join(BASE_DIR, "public", "music", "flac"),
    "mp3": os.path.join(BASE_DIR, "public", "music", "mp3")
}

OUTPUT_CSV = os.path.join(BASE_DIR, "data", "music_metadata.csv")

# CSV columns
FIELDS = [
    "filename", "title", "artist", "movie", "genre", "date",
    "duration", "format", "bitrate", "sample_rate",
    "path_flac", "path_mp3", "desc"
]

DEFAULT_ARTIST = "Keshav Anand"

def generate_csv():
    rows = []

    # Collect all files by format
    files_dict = {"flac": {}, "mp3": {}}
    for fmt, dir_path in MUSIC_DIRS.items():
        for root, _, files in os.walk(dir_path):
            for f in files:
                if f.lower().endswith(f".{fmt}"):
                    relative_path = os.path.relpath(os.path.join(root, f), BASE_DIR).replace("\\", "/")
                    files_dict[fmt][f] = relative_path

    # Combine FLAC and MP3 by filename (without extension)
    all_filenames = set(
        [os.path.splitext(f)[0] for f in files_dict["flac"].keys()] +
        [os.path.splitext(f)[0] for f in files_dict["mp3"].keys()]
    )

    for base_name in all_filenames:
        # Determine available formats
        flac_file = f"{base_name}.flac"
        mp3_file = f"{base_name}.mp3"

        path_flac = files_dict["flac"].get(flac_file, "")
        path_mp3 = files_dict["mp3"].get(mp3_file, "")

        # Read metadata from one of the available files
        audio_path = os.path.join(BASE_DIR, path_flac or path_mp3)
        try:
            audio = MutagenFile(audio_path)
            bitrate = int(audio.info.bitrate / 1000) if hasattr(audio.info, "bitrate") else ""
            sample_rate = int(audio.info.sample_rate) if hasattr(audio.info, "sample_rate") else ""
            duration = int(audio.info.length) if hasattr(audio.info, "length") else ""
            audio_format = os.path.splitext(audio_path)[1][1:]  # extension without dot

            # Get file creation date (YYYY-MM-DD)
            creation_timestamp = os.path.getctime(audio_path)
            file_date = datetime.fromtimestamp(creation_timestamp).strftime("%Y-%m-%d")
        except Exception:
            bitrate = ""
            sample_rate = ""
            duration = ""
            audio_format = ""
            file_date = ""

        rows.append({
            "filename": base_name,
            "title": base_name,
            "artist": DEFAULT_ARTIST,
            "movie": "",
            "genre": "",
            "date": file_date,
            "duration": duration,
            "format": audio_format,
            "bitrate": bitrate,
            "sample_rate": sample_rate,
            "path_flac": path_flac,
            "path_mp3": path_mp3,
            "desc": ""
        })

    # Ensure data directory exists
    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

    # Write CSV
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ CSV exported to {OUTPUT_CSV}")

if __name__ == "__main__":
    generate_csv()