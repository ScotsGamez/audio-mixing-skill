# EasyEffects Community Presets (JackHack96 Integration)

This document catalogs curated presets from the renowned [JackHack96/EasyEffects-Presets](https://github.com/JackHack96/EasyEffects-Presets)
community project, explaining their DSP chains, use cases, and precautions.

---

## 1. Loudness + Autogain (`JackHack96 - Loudness+Autogain.json`)

### Core Philosophy: Fletcher-Munson Equal-Loudness Compensation
- **The Problem**: When listening to music at lower or conversational volumes, human hearing sensitivity drops steeply in the sub-bass (<100 Hz) and ultra-highs (>10 kHz). Listening without compensation feels hollow and thin.
- **The DSP Chain**:
  1. **Autogain**: Dynamically maintains an integrated loudness target of -12 LUFS using geometric mean MSI.
  2. **Bass Enhancer**: Generates sub-bass psychoacoustic harmonics with a 20 Hz floor and 100 Hz scope.
  3. **Upward Compressor**: Raises quiet ambient details while transparently managing peak signals.
  4. **Equalizer**: Smooth low-shelf and high-shelf contours to restore perceived warmth at low listening volumes.
- **Best For**: Late-night movie watching, background listening, or YouTube videos with wildly fluctuating volume levels.
- **User Precaution**: Because autogain boosts quiet passages, avoid using this preset during critical mixing and mastering decisions where honest, uncompressed dynamic range is essential.

---

## 2. Advanced Auto Gain (`JackHack96 - Advanced Auto Gain.json`)

### Core Philosophy: Seamless Multi-Source Leveling
- **The Problem**: Switching between Spotify, YouTube, Discord, and games often requires constant manual volume slider adjustments.
- **The DSP Chain**:
  - Precision autogain leveling target (-14 LUFS) paired with transparent multi-band limiting.
- **Best For**: General desktop multimedia, podcast listening, and voice calls.
