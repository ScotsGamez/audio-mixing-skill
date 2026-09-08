# EasyEffects DSP Pipeline & Linux Audio Tuning Guide

EasyEffects is the premier PipeWire DSP suite on Linux. This guide covers preset management,
CLI automation, and the optimal signal chain for audiophile listening and mixing.

---

## 1. Preset Locations & CLI Control

EasyEffects stores output presets in JSON format:
```
~/.local/share/easyeffects/output/<Preset_Name>.json
```

### Essential Commands:
- **List Presets**:
  ```bash
  easyeffects -p
  ```
- **Load a Preset by Name**:
  ```bash
  easyeffects -l "Cloud Alpha - Pro Master Bass (Zero Muffle)"
  ```
- **Toggle Global Bypass**:
  ```bash
  easyeffects --bypass-toggle
  ```
- **Inspect Last Loaded Presets**:
  ```bash
  easyeffects -s
  ```

---

## 2. The Golden DSP Signal Chain Order

The order of DSP plugins matters fundamentally. Applying EQ after heavy compression will alter the compressed dynamics, while running EQ before a limiter ensures that EQ peaks are caught safely.

### Optimal Order for Playback & Mixing:
```
Audio Stream (Music / Game / Movie)
       │
       ▼
1. Equalizer (Input Gain attenuation + Surgical Cuts & Tonal Shaping)
       │
       ▼
2. Bass Enhancer (Optional: Psychoacoustic Harmonics for small speakers)
       │
       ▼
3. Compressor (Optional: Dynamic Range control for Movies/Gaming)
       │
       ▼
4. Maximizer / Brickwall Limiter (Safety ceiling at -0.5 dB True Peak)
       │
       ▼
DAC / PipeWire Sink (Headphones / Speakers)
```

### Safety Maximizer / Limiter Settings:
To ensure that positive EQ boosts never introduce DAC clipping or harsh digital distortion:
```json
"maximizer": {
    "ceiling": -0.5,
    "release": 100.0,
    "threshold": 0.0
}
```
If significant positive gain is applied in the equalizer (e.g. +6 dB sub-bass), set the equalizer `"input-gain"` to `-3.0` or `-4.0` dB as pre-headroom compensation.
