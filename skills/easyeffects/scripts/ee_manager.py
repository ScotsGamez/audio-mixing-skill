#!/usr/bin/env python3
"""
EasyEffects & PipeWire Health and Management Tool
Utility script for inspecting status, active presets, bypass state, and managing
EasyEffects configurations safely without preset sprawl.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

PRESET_DIR = Path.home() / ".local" / "share" / "easyeffects" / "output"


def run_cmd(cmd: list) -> str:
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return res.stdout.strip()
    except Exception as e:
        return ""


def check_status():
    print("\n========================================================")
    print(" EasyEffects & PipeWire DSP Health Status")
    print("========================================================\n")

    # 1. Check EasyEffects process
    pgrep = run_cmd(["pgrep", "-l", "easyeffects"])
    if "easyeffects" in pgrep:
        print(f"✓ EasyEffects Process:   RUNNING ({pgrep})")
    else:
        print("❌ EasyEffects Process:  NOT RUNNING (Start with: easyeffects --gapplication-service &)")

    # 2. Check Active Preset
    active_presets = run_cmd(["easyeffects", "-s"])
    print(f"✓ {active_presets}")

    # 3. Check Bypass State
    bypass_code = run_cmd(["easyeffects", "-b", "3"])
    if bypass_code == "1":
        print("⚠️  DSP State:            BYPASSED (Processing is disabled!)")
        print("   -> Enable with:       easyeffects -b 2")
    elif bypass_code == "2":
        print("✓ DSP State:             ACTIVE (Processing audio normally)")
    else:
        print(f"• DSP State Code:        {bypass_code}")

    # 4. Check Plugin Dependencies
    print("\n--- LV2 Plugin Dependencies ---")
    deps = {
        "zam-plugins-lv2": "Maximizer (ZaMaximX2)",
        "lsp-plugins-lv2": "Equalizer, Limiter, Compressor",
        "calf": "Bass Enhancer, Exciter",
    }
    for pkg, feature in deps.items():
        is_installed = subprocess.run(["pacman", "-Q", pkg], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0
        if is_installed:
            print(f"  ✓ {pkg:18s}: INSTALLED (Powers {feature})")
        else:
            print(f"  ❌ {pkg:18s}: MISSING! (Required for {feature})")
            print(f"     -> Install with: omarchy pkg add {pkg} (or: sudo pacman -S {pkg})")

    # 5. Check Installed Presets in Output Directory
    if PRESET_DIR.exists():
        presets = sorted([f.stem for f in PRESET_DIR.glob("*.json")])
        print(f"\n--- Installed Presets ({len(presets)} total) ---")
        for idx, p in enumerate(presets, 1):
            is_active = p in active_presets
            mark = " [ACTIVE]" if is_active else ""
            print(f"  {idx:2d}. {p}{mark}")
    else:
        print(f"❌ Preset directory does not exist: {PRESET_DIR}")

    print("\n========================================================\n")


def main():
    parser = argparse.ArgumentParser(description="EasyEffects DSP Manager")
    parser.add_argument("--status", action="store_true", help="Display full health and preset status")
    parser.add_argument("--load", type=str, help="Load a preset by name")
    parser.add_argument("--bypass-toggle", action="store_true", help="Toggle global DSP bypass")

    args = parser.parse_args()

    if args.load:
        print(f"ℹ️  Loading preset '{args.load}'...")
        res = run_cmd(["easyeffects", "-l", args.load])
        print(res or f"✓ Preset '{args.load}' loaded.")
        return

    if args.bypass_toggle:
        run_cmd(["easyeffects", "--bypass-toggle"])
        print("✓ Toggled global bypass.")
        check_status()
        return

    # Default to status
    check_status()


if __name__ == "__main__":
    main()
