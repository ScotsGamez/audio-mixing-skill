#!/usr/bin/env python3
"""
EasyEffects Preset Generator
Generates and installs calibrated EasyEffects JSON presets based on acoustic profiles,
driver specifications, and target listening environments.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

DEFAULT_PRESET_DIR = Path.home() / ".local" / "share" / "easyeffects" / "output"

# Built-in Calibrated Curves
PROFILES = {
    "cloud_alpha_master": {
        "description": "50mm Dual-Chamber Pro Master: Sub-bass extension without mud",
        "input_gain": -3.0,
        "bands": [
            {"freq": 32.0, "gain": 8.0, "q": 1.2, "type": "Bell"},
            {"freq": 64.0, "gain": 5.5, "q": 1.4, "type": "Bell"},
            {"freq": 125.0, "gain": -3.0, "q": 1.4, "type": "Bell"},
            {"freq": 250.0, "gain": -2.5, "q": 1.4, "type": "Bell"},
            {"freq": 500.0, "gain": 0.0, "q": 1.4, "type": "Bell"},
            {"freq": 1000.0, "gain": 1.5, "q": 1.3, "type": "Bell"},
            {"freq": 2000.0, "gain": 1.0, "q": 1.4, "type": "Bell"},
            {"freq": 4200.0, "gain": -2.5, "q": 2.2, "type": "Bell"},
            {"freq": 8000.0, "gain": 1.5, "q": 1.4, "type": "Bell"},
            {"freq": 16000.0, "gain": 3.0, "q": 0.8, "type": "High-shelf"},
        ],
        "maximizer": {"ceiling": -0.5, "release": 100.0, "threshold": 0.0}
    },
    "gaming_fps_clarity": {
        "description": "Competitive FPS: Footstep isolation, sub-rumble cut, 3kHz presence",
        "input_gain": 0.0,
        "bands": [
            {"freq": 32.0, "gain": -6.0, "q": 1.0, "type": "High-pass"},
            {"freq": 64.0, "gain": -3.0, "q": 1.4, "type": "Bell"},
            {"freq": 125.0, "gain": -2.0, "q": 1.4, "type": "Bell"},
            {"freq": 250.0, "gain": -3.5, "q": 1.5, "type": "Bell"},
            {"freq": 500.0, "gain": 0.0, "q": 1.4, "type": "Bell"},
            {"freq": 1400.0, "gain": 3.5, "q": 2.0, "type": "Bell"},
            {"freq": 3200.0, "gain": 4.5, "q": 2.2, "type": "Bell"},
            {"freq": 6000.0, "gain": -2.0, "q": 2.5, "type": "Bell"},
            {"freq": 10000.0, "gain": 1.0, "q": 1.0, "type": "High-shelf"},
        ],
        "maximizer": {"ceiling": -0.5, "release": 80.0, "threshold": 0.0}
    },
    "cinema_dialogue": {
        "description": "Movies & TV: Speech clarity boost, wide dynamic range taming",
        "input_gain": -1.5,
        "bands": [
            {"freq": 32.0, "gain": 2.0, "q": 1.2, "type": "Bell"},
            {"freq": 64.0, "gain": 1.5, "q": 1.4, "type": "Bell"},
            {"freq": 125.0, "gain": -1.5, "q": 1.4, "type": "Bell"},
            {"freq": 250.0, "gain": -2.0, "q": 1.4, "type": "Bell"},
            {"freq": 1000.0, "gain": 2.0, "q": 1.5, "type": "Bell"},
            {"freq": 2200.0, "gain": 3.5, "q": 1.8, "type": "Bell"},
            {"freq": 6000.0, "gain": -2.0, "q": 2.0, "type": "Bell"},
            {"freq": 12000.0, "gain": 1.5, "q": 0.9, "type": "High-shelf"},
        ],
        "maximizer": {"ceiling": -0.5, "release": 120.0, "threshold": 0.0}
    },
    "audiophile_harman": {
        "description": "Harman Target 2019 reference curve: +6dB sub-bass shelf, natural pinna gain",
        "input_gain": -3.5,
        "bands": [
            {"freq": 32.0, "gain": 6.5, "q": 0.7, "type": "Low-shelf"},
            {"freq": 64.0, "gain": 4.0, "q": 1.1, "type": "Bell"},
            {"freq": 125.0, "gain": 0.5, "q": 1.4, "type": "Bell"},
            {"freq": 250.0, "gain": 0.0, "q": 1.4, "type": "Bell"},
            {"freq": 500.0, "gain": 0.0, "q": 1.4, "type": "Bell"},
            {"freq": 1000.0, "gain": 0.0, "q": 1.4, "type": "Bell"},
            {"freq": 3000.0, "gain": 3.5, "q": 1.8, "type": "Bell"},
            {"freq": 6000.0, "gain": -1.5, "q": 2.0, "type": "Bell"},
            {"freq": 10000.0, "gain": 1.0, "q": 0.8, "type": "High-shelf"},
        ],
        "maximizer": {"ceiling": -0.5, "release": 100.0, "threshold": 0.0}
    }
}


def build_preset_json(profile_data):
    """Builds a complete EasyEffects output preset dictionary."""
    bands_dict = {}
    for idx, band in enumerate(profile_data["bands"]):
        band_key = f"band{idx}"
        b_type = band.get("type", "Bell")
        if b_type == "Low-shelf":
            mode = "RLC (BT)"
        elif b_type == "High-shelf":
            mode = "RLC (BT)"
        else:
            mode = "RLC (BT)"

        bands_dict[band_key] = {
            "frequency": float(band["freq"]),
            "gain": float(band["gain"]),
            "mode": mode,
            "mute": False,
            "q": float(band.get("q", 1.4)),
            "slope": "x1",
            "solo": False,
            "type": b_type
        }

    preset = {
        "output": {
            "blocklist": [],
            "equalizer": {
                "bypass": False,
                "input-gain": float(profile_data.get("input_gain", 0.0)),
                "output-gain": 0.0,
                "mode": "IIR",
                "num-bands": len(profile_data["bands"]),
                "split-channels": False,
                "left": bands_dict,
                "right": bands_dict
            },
            "plugins_order": ["equalizer"]
        }
    }

    if "maximizer" in profile_data:
        max_cfg = profile_data["maximizer"]
        preset["output"]["maximizer"] = {
            "bypass": False,
            "ceiling": float(max_cfg.get("ceiling", -0.5)),
            "release": float(max_cfg.get("release", 100.0)),
            "threshold": float(max_cfg.get("threshold", 0.0))
        }
        preset["output"]["plugins_order"].append("maximizer")

    return preset


def main():
    parser = argparse.ArgumentParser(description="Generate EasyEffects Presets")
    parser.add_argument("--profile", choices=list(PROFILES.keys()), default="cloud_alpha_master",
                        help="Pre-calibrated acoustic target profile")
    parser.add_argument("--name", type=str, help="Preset output name (e.g., 'Master - Cloud Alpha')")
    parser.add_argument("--install", action="store_true", help="Install directly into EasyEffects preset folder")
    parser.add_argument("--apply", action="store_true", help="Activate preset in EasyEffects immediately")
    parser.add_argument("--list-profiles", action="store_true", help="List available calibrated profiles")

    args = parser.parse_args()

    if args.list_profiles:
        print("Available Target Profiles:")
        for k, v in PROFILES.items():
            print(f"  • {k:20s}: {v['description']}")
        return

    profile_name = args.profile
    profile = PROFILES[profile_name]
    preset_title = args.name or f"AI Master - {profile_name.replace('_', ' ').title()}"

    preset_content = build_preset_json(profile)

    # Local presets directory inside the skill repo
    repo_preset_dir = Path(__file__).resolve().parent.parent / "presets"
    repo_preset_dir.mkdir(parents=True, exist_ok=True)
    local_file = repo_preset_dir / f"{preset_title}.json"

    with open(local_file, "w") as f:
        json.dump(preset_content, f, indent=4)
    print(f"✓ Saved preset to repository: {local_file}")

    if args.install or args.apply:
        DEFAULT_PRESET_DIR.mkdir(parents=True, exist_ok=True)
        installed_file = DEFAULT_PRESET_DIR / f"{preset_title}.json"
        with open(installed_file, "w") as f:
            json.dump(preset_content, f, indent=4)
        print(f"✓ Installed to EasyEffects: {installed_file}")

    if args.apply:
        try:
            subprocess.run(["easyeffects", "-l", preset_title], check=True)
            print(f"✓ Activated preset '{preset_title}' in EasyEffects!")
        except Exception as e:
            print(f"Notice: Could not auto-load via CLI ({e}). Load manually with: easyeffects -l \"{preset_title}\"")


if __name__ == "__main__":
    main()
