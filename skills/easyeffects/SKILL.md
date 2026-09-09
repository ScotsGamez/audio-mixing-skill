---
name: easyeffects
description: >-
  Comprehensive Linux DSP control, PipeWire audio stream management, and EasyEffects configuration.
  Use when configuring, tuning, or troubleshooting EasyEffects presets, equalizer curves, limiters,
  autogain, crossfeed, convolver impulse responses (IRS), managing the EasyEffects daemon,
  or automating device-specific audio routing on PipeWire and WirePlumber.
---

# EasyEffects & PipeWire DSP Engineering Skill

This skill empowers the agent to act as a system-level Linux audio and DSP engineer. It handles
the installation, real-time configuration, in-place tuning, and troubleshooting of **EasyEffects**
on **PipeWire** and **WirePlumber**.

---

## 1. Quick CLI Cheat-Sheet

| Action | Command | Purpose |
| :--- | :--- | :--- |
| **List Output Presets** | `easyeffects -p` | Shows all installed presets. |
| **Show Current Preset** | `easyeffects -s` | Displays active input and output presets. |
| **Load a Preset** | `easyeffects -l "<Preset Name>"` | Switches the active DSP preset in real time. |
| **Check Bypass State** | `easyeffects -b 3` | Returns `1` (bypassed) or `2` (active processing). |
| **Toggle Bypass** | `easyeffects --bypass-toggle` | Instantly A/B tests raw audio vs. processed audio. |
| **Service Status** | `systemctl --user status easyeffects` | Checks if the background daemon is healthy. |
| **PipeWire Sinks Status** | `wpctl status` | Checks audio device nodes and default output sink. |

---

## 2. Mandatory Rules for Preset Modifications

To keep the user's environment stable, clean, and safe:

1. **Prior Notice & Preview Protocol**:
   - Always inform the user before modifying an active preset.
   - Print a clear preview of the frequency bands, gains, and safety limiter settings.
2. **In-Place Updates Only (No Preset Sprawl)**:
   - When tuning or adjusting the user's sound profile, **never create a new uniquely-named preset file**.
   - Always overwrite the active preset (e.g. `Cloud Alpha S - Clean Bass & Crystal Clarity.json`) in-place.
   - The user's EasyEffects directory must only contain their single active profile and stock program defaults.
3. **Headroom & Safety Limiting**:
   - Equalizer boosts must be offset by adequate preamp attenuation or a brickwall True Peak limiter.
   - Maximizer ceiling must be set between **-0.1 dBTP and -0.5 dBTP** to prevent DAC inter-sample clipping and protect headphone transducers.

---

## 3. EasyEffects Directory Architecture

All EasyEffects configurations reside under standard XDG paths:

```
~/.local/share/easyeffects/
├── output/                   # Output presets (*.json) applied to headphones/speakers
├── input/                    # Input presets (*.json) applied to microphones
├── autoload/                 # Device-specific automatic profile rules
└── irs/                      # Convolver impulse response files (*.irs, *.wav)

~/.config/easyeffects/
└── db/                       # Runtime settings and last-loaded preset state
```

---

## 4. Key DSP Plugins & Tuning Guidelines

### A. Parametric Equalizer (`equalizer`)
- Primary tonal shaping tool.
- Supports 1 to 32 bands per channel with filter types: `Bell` (Peaking), `Low-shelf`, `High-shelf`, `High-pass`, `Low-pass`.
- **Mode**: Use `RLC (BT)` or `IIR` for low-latency, phase-accurate performance.

### B. Maximizer / Brickwall Limiter (`maximizer`)
- Mandatory safety shield at the end of the DSP chain.
- Catches positive EQ overshoot and prevents analog DAC clipping.
- **Recommended Settings**:
  - `ceiling`: `-0.1` to `-0.5` dBTP
  - `threshold`: `-1.0` to `-2.0` dB
  - `release`: `5.0` ms to `20.0` ms (transparent transient recovery)

### C. Autogain (`autogain`)
- Automatically normalizes fluctuating volume across YouTube, Discord, and media players.
- Target: `-14.0` LUFS (streaming standard) or `-12.0` LUFS (casual listening).
- *Warning*: Disable during critical mixing or mastering sessions.

### D. Convolver (`convolver`)
- Applies real-world acoustic room or headphone impulse responses (IRS).
- Files stored in `~/.local/share/easyeffects/irs/`.
- Ensure IR sampling rate matches system PipeWire rate (usually 48 kHz).

---

## 5. Troubleshooting & Diagnostics Runbook

### Issue 1: Audio Sounds Muffled or Boxy
1. Check if `crossfeed` is active. Crossfeed blends stereo channels below 700 Hz; on closed-back headphones, this collapses the soundstage. **Disable crossfeed**.
2. Check if `bass_enhancer` has excessive harmonics. Harmonic exciters bleed into the vocal midrange. **Disable bass_enhancer**.
3. Check 250 Hz in the Equalizer. Apply a surgical dip (-2.5 dB to -3.5 dB, Q=1.4) to remove closed-cup resonance.

### Issue 2: Audio Stuttering, Crackles, or xruns
1. Inspect PipeWire status: `pw-top` or `wpctl status`.
2. Ensure EasyEffects is not running redundant heavy plugins (e.g. Convolver with massive partition sizes alongside heavy multi-band compressors).
3. Check buffer quantum:
   ```bash
   pw-metadata -n settings 0 clock.force-quantum 1024
   ```

### Issue 3: EasyEffects Processing Stopped Working
1. Check if global bypass is engaged:
   ```bash
   easyeffects -b 3
   # If output is 1, enable processing:
   easyeffects -b 2
   ```
2. Verify WirePlumber default sink routing:
   ```bash
   wpctl status
   ```
3. Restart daemon if unresponsive:
   ```bash
   systemctl --user restart easyeffects
   ```
