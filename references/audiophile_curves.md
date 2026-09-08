# Audiophile Curves & Measurement Database

This reference documents verified acoustic curves from pro audio measurement laboratories
(Oratory1990, Crinacle IEF, Rtings, Harman Acoustic Research) and audiophile community consensus.

---

## 1. The Reference Curves

### A. Harman Over-Ear Target (2018/2019)
Developed by Dr. Sean Olive and Todd Welti at Harman International based on blind listener preference tests across diverse age groups and audio expertise levels.
- **Key Characteristics**:
  - Sub-bass shelf: +6 dB to +8 dB rise below 105 Hz
  - Linear lower midrange (200 Hz – 1 kHz)
  - Ear-gain peak at 3.0 kHz (+9 dB relative to 1 kHz)
  - Smooth treble decay with ~10 dB drop by 15 kHz relative to 3 kHz peak

### B. IEF Neutral (In-Ear Fidelity / Crinacle)
- Focused on strict timbral accuracy without artificial bass boost.
- Ideal for critical mixing decisions, tracking acoustic instruments, and verifying tonal balance.

---

## 2. Headphone Profile: HyperX Cloud Alpha (50mm Dual-Chamber)

The HyperX Cloud Alpha uses 50mm dynamic drivers with dual chamber ear cups.

### Stock Acoustic Flaws (Measured by Oratory1990 / Rtings):
1. **Upper Bass / Low-Mid Bloom (120 Hz – 200 Hz)**: Built-in +3.5 dB elevation creates a slight warm boxiness.
2. **Sub-Bass Roll-off (<40 Hz)**: Natural acoustic leak from pleather pads causes a gradual roll-off below 45 Hz.
3. **Treble Resonance Spike (4.2 kHz – 5 kHz)**: Sharp +4 dB peak causing slight sibilant edge on female vocals.

### Community & Audiophile Calibrated Parametric Correction:
| Filter # | Type | Frequency (Hz) | Gain (dB) | Q-Factor | Target Effect |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Band 1** | Low Shelf | 32.0 | +7.5 | 0.8 | Deep physical sub-bass extension |
| **Band 2** | Bell | 64.0 | +5.0 | 1.3 | Punch & body without muddiness |
| **Band 3** | Bell | 135.0 | -3.5 | 1.5 | Removes upper bass bloat and boom |
| **Band 4** | Bell | 250.0 | -2.0 | 1.4 | Eliminates closed-cup resonance |
| **Band 5** | Bell | 1,000.0 | +1.5 | 1.2 | Vocal clarity and instrument forwardness |
| **Band 6** | Bell | 4,200.0 | -3.0 | 2.5 | Tames treble resonance peak |
| **Band 7** | High Shelf | 10,000.0 | +2.5 | 0.7 | Smooth audiophile air and soundstage width |

---

## 3. How to Ingest & Train on New Audiophile Data

To add new audiophile measurements or forum consensus curves into this repository:
1. **Find the Data**: Pull parametric values from Oratory1990 (Reddit /r/oratory1990), AutoEq repository, or Crinacle measurements.
2. **Add Profile**: Create an entry under `references/audiophile_curves.md` with:
   - Model name & driver diameter (e.g. 40mm, 50mm, planar).
   - Problem frequencies & listener impressions.
   - Exact Parametric EQ table (Frequency, Gain, Q, Filter Type).
3. **Generate Preset**: Run `python3 scripts/generate_preset.py` to create the EasyEffects JSON preset.
4. **Commit & Push to GitHub**: Commit the new data so your AI skill retains the learned knowledge across all sessions.
