# User Preferences & Manual Overrides

This file is your direct steering wheel. Any rules, personal sound preferences, or blacklists
you define here take the highest priority over all other references and default calculations.

---

## 1. Personal Sound Signature Preferences

- **Bass Preference**: Clean, deep physical sub-bass (30Hz–60Hz) with high punch, but **zero muddiness or muffling** in the 200Hz–400Hz range.
- **Midrange / Vocals**: Forward, crisp, and articulate vocal clarity. No hollow or veiled presentation.
- **Treble / Air**: Smooth, non-fatiguing high extension without harsh sibilance ("S" or "T" piercing).
- **Primary Gear**: HyperX Cloud Alpha (50mm dual-chamber drivers, closed-back) on PipeWire / EasyEffects.

---

## 2. Forbidden Techniques & Blacklist (The AI Must NEVER Do)

1. **No Clipping / Preamp Neglect**: Never apply positive EQ gains without corresponding negative input gain reduction or a True Peak safety ceiling (-0.5 dBTP).
2. **No Blind V-Shape Boosts**: Avoid generic consumer "smile" curves that boost mid-bass (100–200 Hz) and treble while hollowing out mids.
3. **No Stereo Widening on Sub-Bass**: Keep all low-end (<120 Hz) phase-correlated and centered.
4. **No Artificial 7.1 Virtual Surround**: Avoid phase-distorting virtual surround sound plugins for critical music listening.
5. **No Crossfeed**: Do not use crossfeed plugin; on closed-back Cloud Alpha headphones it smears stereo separation and creates a muffled, boxy midrange.
6. **No Heavy Harmonic Excitation on Full Mix**: Keep the signal path clean (`equalizer + maximizer`) to preserve pristine vocal clarity without artificial saturation mud.
7. **Maintain Upper Presence**: Ensure 4 kHz (+6 dB) and 8 kHz (+3 dB) are preserved so heavy sub-bass never veils vocals or instruments.
8. **In-Place Preset Updates Only (No Preset Sprawl)**: When adjusting or fine-tuning sound profiles, NEVER create unnecessary extra preset files. Keep the single active custom preset (`Cloud Alpha S - Kinetic Bass & Crystal Air.json`) updated in-place so the user's EasyEffects directory only contains this active preset and the default program presets.
9. **Maximum Safe Gain Ceilings (Anti-Blare Rule)**: On the HyperX Cloud Alpha S (50mm dual-chamber drivers), never boost the 20–35 Hz sub-bass band beyond **+8.0 dB**. Any positive gain above +8.0 dB causes mechanical voice-coil distortion and acoustic blaring in the earcups. Always clamp 31–35 Hz to $\le +8.0 \text{ dB}$ (optimal tuned baseline: +7.5 to +7.8 dB).

---

## 3. Manual Notes & Live Listening Log

Add your own listening feedback here as you test different profiles:
- *Example*: "Cloud Alpha sounds best with a -3.0 dB cut at 135 Hz and a +1.5 dB bump at 1.2 kHz for rock vocals."
