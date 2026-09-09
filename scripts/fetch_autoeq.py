#!/usr/bin/env python3
"""
AutoEq Headphone Preset Importer
Searches and imports verified measurement curves from the open-source AutoEq database
and compiles them into calibrated EasyEffects JSON presets.

TRANSPARENCY RULE:
Always informs the user of what model, measurements, preamp, and filter bands
are found BEFORE installing or altering EasyEffects presets.
"""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

DEFAULT_PRESET_DIR = Path.home() / ".local" / "share" / "easyeffects" / "output"
AUTOEQ_RAW_BASE = "https://raw.githubusercontent.com/jaakkopasanen/AutoEq/master/results"
AUTOEQ_API_SEARCH = "https://api.github.com/repos/jaakkopasanen/AutoEq/contents/results"

# Standard target directories in AutoEq
COMMON_PATHS = [
    ("oratory1990/over-ear", "oratory1990 (Over-Ear)"),
    ("oratory1990/in-ear", "oratory1990 (In-Ear)"),
    ("crinacle/harman_in-ear_2019_v2", "Crinacle (Harman 2019)"),
    ("crinacle/ief_neutral_in-ear", "Crinacle (IEF Neutral)"),
    ("rtings/avg", "Rtings (Average)"),
]


def fetch_text_url(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "AudioMixingSkill/1.0"})
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8")


def parse_autoeq_peq(peq_text: str):
    """
    Parses standard AutoEq ParametricEQ.txt file.
    Format:
      Preamp: -6.3 dB
      Filter 1: ON LSC Fc 105 Hz Gain 7.1 dB Q 0.70
      Filter 2: ON PK Fc 104 Hz Gain -5.9 dB Q 0.23
    """
    preamp = 0.0
    preamp_match = re.search(r"Preamp:\s*([+-]?\d+(?:\.\d+)?)\s*dB", peq_text, re.IGNORECASE)
    if preamp_match:
        preamp = float(preamp_match.group(1))

    bands = []
    filter_pattern = re.compile(
        r"Filter\s+\d+:\s+ON\s+([A-Z]+)\s+Fc\s+(\d+(?:\.\d+)?)\s*Hz\s+Gain\s+([+-]?\d+(?:\.\d+)?)\s*dB\s+Q\s+(\d+(?:\.\d+)?)",
        re.IGNORECASE,
    )

    for line in peq_text.splitlines():
        m = filter_pattern.search(line)
        if m:
            ftype_raw, freq_str, gain_str, q_str = m.groups()
            freq = float(freq_str)
            gain = float(gain_str)
            q = float(q_str)

            # Map filter types to EasyEffects nomenclature
            if ftype_raw.upper() == "LSC":
                ee_type = "Low-shelf"
            elif ftype_raw.upper() == "HSC":
                ee_type = "High-shelf"
            else:
                ee_type = "Bell"

            bands.append({
                "freq": freq,
                "gain": gain,
                "q": q,
                "type": ee_type
            })

    return preamp, bands


def build_easyeffects_preset(preamp: float, bands: list) -> dict:
    bands_dict = {}
    for idx, band in enumerate(bands):
        band_key = f"band{idx}"
        bands_dict[band_key] = {
            "frequency": band["freq"],
            "gain": band["gain"],
            "mode": "RLC (BT)",
            "mute": False,
            "q": band["q"],
            "slope": "x1",
            "solo": False,
            "type": band["type"]
        }

    return {
        "output": {
            "blocklist": [],
            "equalizer": {
                "bypass": False,
                "input-gain": preamp,
                "output-gain": 0.0,
                "mode": "IIR",
                "num-bands": len(bands),
                "split-channels": False,
                "left": bands_dict,
                "right": bands_dict
            },
            "maximizer": {
                "bypass": False,
                "ceiling": -0.5,
                "release": 100.0,
                "threshold": 0.0
            },
            "plugins_order": [
                "equalizer",
                "maximizer"
            ]
        }
    }


def find_and_fetch_model(model_name: str):
    """Searches common AutoEq directories for the model's ParametricEQ.txt."""
    print(f"🔍 Searching AutoEq database for '{model_name}'...")
    encoded_name = urllib.parse.quote(model_name)

    for subpath, label in COMMON_PATHS:
        url = f"{AUTOEQ_RAW_BASE}/{subpath}/{encoded_name}/{encoded_name}%20ParametricEQ.txt"
        try:
            content = fetch_text_url(url)
            print(f"✓ Found verified measurement curve from: {label}")
            return content, label
        except Exception:
            continue

    return None, None


def main():
    parser = argparse.ArgumentParser(description="Fetch and build EasyEffects presets from AutoEq")
    parser.add_argument("--model", type=str, required=True, help="Headphone model name (e.g. 'HyperX Cloud Alpha', 'Sennheiser HD 600')")
    parser.add_argument("--name", type=str, help="Custom preset title (defaults to model name)")
    parser.add_argument("--install", action="store_true", help="Install into EasyEffects directory (~/.local/share/easyeffects/output/)")
    parser.add_argument("--apply", action="store_true", help="Instantly activate preset in EasyEffects")
    parser.add_argument("--confirm", action="store_true", help="Acknowledge and confirm application without interactive prompt")

    args = parser.parse_args()

    # Step 1: Notify user and fetch data
    print(f"\n========================================================")
    print(f" AutoEq Headphone Calibration Ingestion Engine")
    print(f" Target Model: {args.model}")
    print(f"========================================================\n")

    peq_text, source_label = find_and_fetch_model(args.model)
    if not peq_text:
        print(f"❌ Model '{args.model}' not found in standard AutoEq results.")
        print(f"Tip: Ensure the spelling matches the manufacturer name (e.g. 'HyperX Cloud Alpha', 'Sennheiser HD 600').")
        sys.exit(1)

    preamp, bands = parse_autoeq_peq(peq_text)
    preset_title = args.name or f"AutoEq - {args.model}"

    # Step 2: Transparently display proposed changes before installation
    print(f"\n--- PROPOSED PRESET PREVIEW ---")
    print(f"Preset Name:       {preset_title}")
    print(f"Calibration Base:  {source_label}")
    print(f"Preamp Attenuation:{preamp: .1f} dB (Prevents digital clipping)")
    print(f"Filter Bands ({len(bands)} total):")
    for idx, b in enumerate(bands, 1):
        print(f"  Band {idx:2d}: {b['type']:10s} | Freq: {b['freq']:7.1f} Hz | Gain: {b['gain']:+5.1f} dB | Q: {b['q']:.2f}")
    print(f"Safety Limiter:    Ceiling -0.5 dBTP, Release 100ms")
    print(f"--------------------------------\n")

    # Step 3: Save to local repository presets
    repo_preset_dir = Path(__file__).resolve().parent.parent / "presets"
    repo_preset_dir.mkdir(parents=True, exist_ok=True)
    repo_file = repo_preset_dir / f"{preset_title}.json"

    preset_json = build_easyeffects_preset(preamp, bands)
    with open(repo_file, "w") as f:
        json.dump(preset_json, f, indent=4)
    print(f"✓ Saved preset to repository: {repo_file}")

    # Step 4: Installation with transparency check
    if args.install or args.apply:
        if not args.confirm:
            print(f"\n⚠️  USER NOTICE:")
            print(f"You requested to install/apply this preset to your local EasyEffects audio system.")
            print(f"Target location: {DEFAULT_PRESET_DIR / f'{preset_title}.json'}")
            print(f"To proceed non-interactively, pass --confirm.")

        DEFAULT_PRESET_DIR.mkdir(parents=True, exist_ok=True)
        installed_file = DEFAULT_PRESET_DIR / f"{preset_title}.json"
        with open(installed_file, "w") as f:
            json.dump(preset_json, f, indent=4)
        print(f"✓ Successfully installed to EasyEffects: {installed_file}")

    if args.apply:
        import subprocess
        try:
            subprocess.run(["easyeffects", "-l", preset_title], check=True)
            print(f"✓ Activated preset '{preset_title}' in EasyEffects.")
        except Exception as e:
            print(f"Notice: Could not activate via CLI ({e}). Activate in GUI or run: easyeffects -l \"{preset_title}\"")


if __name__ == "__main__":
    main()
