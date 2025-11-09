#!/usr/bin/env python3
"""
Audio conversion utility: ALAC/other formats → FLAC (lossless) and MP3 (high-quality).

Outputs:
    public/music/flac/<name>.flac
    public/music/mp3/<name>.mp3

The script:
    • Accepts a single input file.
    • Produces lossless FLAC and high-quality MP3 (LAME V0).
    • Supports renaming output files via --name.
"""

import os
import subprocess
import argparse

FLAC_DIR = "public/music/flac"
MP3_DIR = "public/music/mp3"


def ensure_directories() -> None:
    """Create output directories if they do not exist."""
    os.makedirs(FLAC_DIR, exist_ok=True)
    os.makedirs(MP3_DIR, exist_ok=True)


def run_ffmpeg(command: list) -> None:
    """Execute an ffmpeg command and catch errors gracefully."""
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as error:
        print(f"Error: ffmpeg failed with message:\n{error}")
        raise SystemExit(1)


def convert_to_flac(input_file: str, output_file: str) -> None:
    """Convert the input file to a lossless FLAC file."""
    print(f"→ Converting to FLAC:\n  {input_file}\n  → {output_file}\n")
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-c:a", "flac",
        output_file
    ]
    run_ffmpeg(command)


def convert_to_mp3(input_file: str, output_file: str) -> None:
    """Convert the input file to a high-quality MP3 (LAME V0)."""
    print(f"→ Converting to MP3 (V0):\n  {input_file}\n  → {output_file}\n")
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-c:a", "libmp3lame",
        "-q:a", "0",
        output_file
    ]
    run_ffmpeg(command)


def main():
    parser = argparse.ArgumentParser(
        description="Convert a single audio file to FLAC and high-quality MP3."
    )
    parser.add_argument("file", help="Path to the input audio file")
    parser.add_argument(
        "--name",
        help="Optional output file name (without extension).",
        default=None
    )

    args = parser.parse_args()
    input_file = args.file

    if not os.path.isfile(input_file):
        print("Error: input file does not exist.")
        raise SystemExit(1)

    ensure_directories()

    original_base = os.path.splitext(os.path.basename(input_file))[0]
    output_base = args.name if args.name else original_base

    flac_path = os.path.join(FLAC_DIR, output_base + ".flac")
    mp3_path = os.path.join(MP3_DIR, output_base + ".mp3")

    convert_to_flac(input_file, flac_path)
    convert_to_mp3(input_file, mp3_path)

    print("✔ All conversions completed successfully.")


if __name__ == "__main__":
    main()