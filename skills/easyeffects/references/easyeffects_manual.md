# EasyEffects Architecture, Plugin Reference & Troubleshooting

This document details the underlying mechanics, plugin parameters, and troubleshooting techniques
for running EasyEffects as a system DSP processor on PipeWire and WirePlumber.

---

## 1. EasyEffects Daemon & Service Mode

EasyEffects runs as a background user daemon on modern Linux desktops:
```bash
systemctl --user status easyeffects
```

If it is not running or crashed, it can be launched in the background via:
```bash
easyeffects --service-mode &
```
Or restarted cleanly:
```bash
systemctl --user restart easyeffects
```

---

## 2. Core Output Plugins Reference

### 1. Equalizer (`equalizer`)
- **JSON Structure**:
  - `mode`: `"IIR"` (Infinite Impulse Response - low CPU and latency) or `"FFT"` (Linear phase).
  - `num-bands`: Typically 8, 10, or 32 bands.
  - `input-gain`: Preamp attenuation in dB (essential when applying positive boosts).
  - `output-gain`: Makeup gain in dB.
  - `left` / `right`: Dictionary of band objects (`band0`, `band1`, ...).
  - Band properties:
    - `frequency`: Center frequency in Hz (e.g., `32.0`, `1000.0`).
    - `gain`: Boost or cut in dB (e.g., `+11.5`, `-3.5`).
    - `q`: Quality factor (bandwidth width: lower = wider, higher = sharper surgical notch).
    - `type`: `"Bell"`, `"Low-shelf"`, `"High-shelf"`, `"High-pass"`, `"Low-pass"`.

### 2. Maximizer (`maximizer`)
- Acts as the safety limiter at the end of the chain.
- `ceiling`: Maximum allowed peak level (dBTP). Set to `-0.1` or `-0.5` dBTP.
- `threshold`: Threshold at which limiting begins (dB).
- `release`: Time in milliseconds to recover after a peak. Set to `5.0` to `20.0` ms for transparent transient control.

### 3. Autogain (`autogain`)
- Continuously calculates integrated loudness using the ITU-R BS.1770 algorithm and shifts output gain.
- `target`: Target loudness in LUFS (e.g. `-14.0` or `-12.0`).
- `silence-threshold`: Level below which no gain adjustments occur (usually `-70.0` dB).

### 4. Convolver (`convolver`)
- Implements FIR filtering by convolving the audio stream with an impulse response (IRS) file.
- Located in: `~/.local/share/easyeffects/irs/`.
- Crucial: Ensure sampling rates match (e.g. 48,000 Hz) to avoid pitch distortion.

---

## 3. Autoloading Presets by Audio Device

EasyEffects can automatically switch presets when you plug in or switch audio devices:
1. Open the EasyEffects UI $\rightarrow$ **PipeWire** $\rightarrow$ **Presets Autoloading**.
2. Select your Output Device (e.g. `alsa_output.pci-0000_00_1f.3.analog-stereo`).
3. Bind it to your active preset (`Cloud Alpha S - Clean Bass & Crystal Clarity`).
4. Select HDMI / Monitor Speaker device and bind it to a speaker preset.
Configured bindings are saved in: `~/.local/share/easyeffects/autoload/`.
