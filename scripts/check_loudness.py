#!/usr/bin/env python3
"""
Audio Loudness & True Peak Compliance Checker
Analyzes audio files using FFmpeg EBU R128 scanner to measure Integrated Loudness (LUFS),
Loudness Range (LRA), and True Peak (dBTP) against commercial streaming and broadcast standards.

TRANSPARENCY RULE:
Explicitly informs the user which file is being scanned and the exact command being run.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

TARGET_STANDARDS = {
    "Spotify / YouTube": {"target_lufs": -14.0, "max_tp": -1.0},
    "Apple Music (Sound Check)": {"target_lufs": -16.0, "max_tp": -1.0},
    "Tidal / Qobuz Hi-Fi": {"target_lufs": -14.0, "max_tp": -1.0},
    "Broadcast / Television (EBU R128)": {"target_lufs": -23.0, "max_tp": -1.0},
    "Cinema / Film Trailer": {"target_lufs": -24.0, "max_tp": -2.0}
}


def analyze_file(file_path: Path):
    if not file_path.exists():
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)

    print(f"\n========================================================")
    print(f" Audio Loudness & True Peak Compliance Analyzer")
    print(f" File: {file_path.name}")
    print(f" Path: {file_path.resolve()}")
    print(f"========================================================\n")

    print(f"ℹ️  [Notice to User]: Launching FFmpeg EBU R128 loudness analysis...")
    cmd = [
        "ffmpeg",
        "-nostats",
        "-i", str(file_path.resolve()),
        "-filter_complex", "ebur128=peak=true",
        "-f", "null",
        "-"
    ]
    print(f"Executing: {' '.join(cmd)}\n")

    result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    output = result.stderr

    # Parse Summary
    # Integrated loudness:
    #   I:         -14.2 LUFS
    #   Threshold: -24.3 LUFS
    # Loudness range:
    #   LRA:         7.8 LU
    # True peak:
    #   Peak:       -0.8 dBFS

    i_match = re.search(r"Integrated loudness:.*?I:\s*([+-]?\d+(?:\.\d+)?)\s*LUFS", output, re.DOTALL)
    lra_match = re.search(r"Loudness range:.*?LRA:\s*([+-]?\d+(?:\.\d+)?)\s*LU", output, re.DOTALL)
    tp_match = re.search(r"True peak:.*?Peak:\s*([+-]?\d+(?:\.\d+)?)\s*dBFS", output, re.DOTALL)

    if not i_match or not tp_match:
        print("❌ Could not parse EBU R128 measurements from audio stream.")
        print(output[-500:])
        sys.exit(1)

    lufs = float(i_match.group(1))
    lra = float(lra_match.group(1)) if lra_match else 0.0
    true_peak = float(tp_match.group(1))

    print(f"--- MEASUREMENT RESULTS ---")
    print(f"Integrated Loudness (LUFS): {lufs:+6.1f} LUFS")
    print(f"Loudness Range (LRA):       {lra: 6.1f} LU")
    print(f"Maximum True Peak:          {true_peak:+6.1f} dBTP")
    print(f"---------------------------\n")

    print(f"--- STREAMING PLATFORM EVALUATION ---")
    for platform, specs in TARGET_STANDARDS.items():
        diff = lufs - specs["target_lufs"]
        tp_ok = true_peak <= specs["max_tp"]

        if abs(diff) <= 0.5 and tp_ok:
            status = "✅ PERFECT COMPLIANCE"
        elif diff > 0.5:
            status = f"⚠️  TOO LOUD (Platform will turn down by {diff:.1f} dB)"
        elif diff < -1.5:
            status = f"ℹ️  QUIETER than target (Platform may apply gain by {-diff:.1f} dB)"
        else:
            status = "✅ GOOD (Minor acceptable tolerance)"

        if not tp_ok:
            status += f" | ❌ TRUE PEAK EXCEEDED (Max {specs['max_tp']} dBTP, Got {true_peak:.1f} dBTP - risk of DAC clipping)"

        print(f"• {platform:35s}: {status}")

    print(f"-------------------------------------\n")


def main():
    parser = argparse.ArgumentParser(description="Analyze audio file loudness compliance (EBU R128 / True Peak)")
    parser.add_argument("audio_file", type=str, help="Path to audio file (.wav, .flac, .mp3, etc.)")
    args = parser.parse_args()

    analyze_file(Path(args.audio_file))


if __name__ == "__main__":
    main()
