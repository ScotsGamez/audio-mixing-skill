---
name: audio-mixing
description: >-
  Expert audio mixing, mastering, and playback calibration assistant. Use when the user asks for
  audio mixing, mastering, headphone or speaker calibration, tuning EQ based on driver size or room acoustics,
  configuring EasyEffects/PipeWire sound profiles, or optimizing audio for gaming, music, or movies.
---

# Audio Mixing & Hardware Calibration Skill

This skill turns the agent into an audiophile mixing engineer and DSP acoustic calibrator. It bridges
pro-audio mastering principles (Bob Katz K-System, Fletcher-Munson compensation, EBU R128/LUFS standards,
Harman target curves) with real-world hardware profiles (speaker size, headphone driver diameter, enclosure type)
and Linux DSP software (EasyEffects on PipeWire).

All iteration, reference datasets, presets, and audiophile community findings are version-controlled in this
repository and synced to GitHub.

## 0. Manual Curation & Source Manifest

Before providing recommendations or generating DSP profiles:
1. Consult [user_preferences.md](./references/user_preferences.md) for user-defined sound signatures, gear specifics, and hard blacklists (which take absolute priority).
2. Check [curation_manifest.json](./references/curation_manifest.json) to verify which source materials are active.
3. Incorporate verified principles from:
   - [curated_pdf_guides.md](./references/community_notes/curated_pdf_guides.md) (iZotope, Owsinski, Izhaki, Vitek)
   - [speaker_size_and_monitoring.md](./references/speaker_size_and_monitoring.md) (Genelec, Mike Senior, ITU-R woofer physics & boundary loading)
   - [reddit_audiophile_insights.md](./references/community_notes/reddit_audiophile_insights.md) (/r/headphones, /r/mixingmastering, /r/oratory1990)
   - [easyeffects_community_presets.md](./references/community_notes/easyeffects_community_presets.md) (JackHack96 curated presets)

### Mandatory Transparency & Prior Notice Protocol
Before executing any action that affects the system, reads local audio files, or touches external networks, the agent **MUST inform the user in advance**:
1. **Network & AutoEq Lookups**: Tell the user before querying GitHub/AutoEq: *"I am about to search the AutoEq database for [Model Name]..."*
2. **Preset Preview Before Writing**: Always print a clear preview of the proposed DSP settings (Preamp gain, frequency bands, gain values, Q factors, safety limiter) *before* installing presets into `~/.local/share/easyeffects/output/`.
3. **Live Playback Switching**: Inform the user before running `easyeffects -l <name>` that active playback will be switched.
4. **Audio File Inspection**: State which file is being scanned and why before running FFmpeg EBU R128 loudness analysis.
5. **In-Place Updates Only (No Preset Sprawl)**: When adjusting or fine-tuning sound profiles, NEVER generate a new uniquely named preset file. Overwrite the user's active preset (`Cloud Alpha S - Clean Bass & Crystal Clarity.json`) in-place so EasyEffects only ever contains this single active preset and the default program presets.

---

## 1. Interactive Intake & Diagnostic Workflow

When a user requests audio tuning, mixing advice, or a preset, gather the necessary context through
an interactive interview if not already provided:

### Key Diagnostic Questions:
1. **Output Hardware & Specs**:
   - What device is being used? (e.g., Headphones: HyperX Cloud Alpha, Sennheiser HD600, Beyerdynamic DT990; or Studio Monitors / Desktop Speakers).
   - Driver size: e.g., 40mm vs 50mm dynamic drivers, planar magnetic, or speaker woofer diameter (3", 5", 8").
   - Enclosure type: Closed-back (resonant chamber, seal-dependent bass) vs Open-back (airy, diffuse soundstage, bass roll-off) vs ported/sealed speakers.
2. **Expected Audio Content**:
   - **Music**: Target genre (EDM/Hip-hop for sub-bass punch, Rock/Metal for guitars & transient snare impact, Classical/Jazz for dynamic range & instrumental separation).
   - **Competitive Gaming**: Spatial positioning, footstep frequency isolation (1kHz - 3.5kHz), gunshot sub-rumble suppression.
   - **TV & Movies**: Speech intelligibility (vocal band boost at 1.5-2.5kHz), dynamic range compression to avoid ear fatigue during explosions.
   - **Production Mixing / Mastering**: Clean reference monitor profile (Harman target or diffuse field neutral, 0 dB colored bias).
3. **User Perception & Sound Goals**:
   - Current issues: "too muffled", "piercing highs", "muddy mids", "weak sub-bass", "fatiguing speech"?
   - Desired sound signature: Deep rumble without mud, punchy bass, crystal highs, warm analog presence, or flat studio reference.

---

## 2. Acoustic Rules of Thumb by Driver Size & Enclosure

Refer to [hardware_profiles.md](./references/hardware_profiles.md) for full physical specifications:

| Driver / Transducer | Acoustic Behavior & Limitations | Recommended DSP Strategy |
| :--- | :--- | :--- |
| **40mm Dynamic (Headphones)** | Fast transient response, but steep mechanical excursion limit. Boosting <40Hz causes distortion/mud. | High-pass at 30Hz; focus bass energy in punch region (60–90Hz); dip 250Hz. |
| **50mm Dynamic (e.g. Cloud Alpha)** | Capable of high excursion and linear sub-bass down to 20Hz. Dual chamber isolates bass resonance. | Generous sub-bass shelf (32Hz–64Hz); surgical cut at 125–250Hz to eliminate boxiness; smooth 1–2kHz boost for vocal clarity. |
| **Planar Magnetic** | Virtually zero bass distortion, flat extension down to 10Hz, ultra-fast attack. | Can take heavy sub-bass shelves (+8dB to +10dB) with zero muddying. Smooth out upper treble peaks (6kHz–9kHz). |
| **Small Speakers (3" - 4" woofers)** | Physically unable to reproduce <60Hz cleanly; port resonance often peaks around 80-100Hz. | Steep high-pass at 55Hz (protect woofer); slight dip at box resonance (100–160Hz); gentle mid boost for vocal projection. |
| **Medium Monitors (5" - 8" woofers)** | Good extension down to 40-48Hz; vulnerable to room boundary bass loading (+3dB to +6dB near walls). | Compensate for boundary proximity (low-shelf cut at 100Hz if against a wall); tame flutter echoes around 2–4kHz. |

### Mandatory Safe Gain Ceiling Limits (Anti-Blare Protection):
Never exceed these physical positive gain thresholds during EQ tuning:
- **50mm Dual-Chamber (Cloud Alpha S)**: Sub-Bass (20–35 Hz) clamped to **$\le +8.0$ dB MAX**. Punch (40–80 Hz) clamped to **$\le +7.5$ dB MAX**. Exceeding +8.0 dB at 32 Hz causes driver voice-coil saturation and earcup blaring!
- **40mm Dynamic**: 20–35 Hz clamped to **$\le +5.5$ dB MAX**.
- **Planar Magnetic**: Sub-Bass clamped to **$\le +9.5$ dB MAX**.
- **3"–4" Desktop Speakers**: Sub-bass boost **FORBIDDEN (0 dB / Cut only)**; high-pass mandatory at 55 Hz.

---

## 3. Mastering & Audiophile Principles ("The Masters")

Refer to [mastering_masters.md](./references/mastering_masters.md) for detailed reference notes:

- **Fletcher-Munson (Equal-Loudness Contours)**: The human ear is significantly less sensitive to low (sub-bass) and very high (air) frequencies at moderate listening levels (65–75 dB SPL). At lower volumes, a gentle "smile" or Harman bass shelf sounds natural, while flat sounds thin.
- **Bob Katz K-System & Headroom**: Always preserve headroom. When applying positive EQ gains (e.g., +6dB bass boost), always apply an equivalent input gain reduction (-6dB) or employ a brickwall safety limiter with a -0.5 dBTP ceiling to avoid digital clipping.
- **Eliminating Mud (The 200–400 Hz Trap)**: Over 80% of "muffled" audio complaints stem from acoustic build-up in the 200–400 Hz range. Cutting this octave by -2 to -4 dB with a moderate Q (1.2–1.5) cleans the soundstage and opens up vocal separation.
- **Loudness Standards**: For mastering output, target:
  - Streaming (Spotify, YouTube): -14 LUFS, -1.0 dBTP
  - Apple Music: -16 LUFS, -1.0 dBTP
  - Cinema / Dynamic Video: -23 to -24 LUFS, -2.0 dBTP

---

## 4. EasyEffects / Linux DSP Integration

EasyEffects output presets are stored in JSON format inside:
`~/.local/share/easyeffects/output/<Preset_Name>.json`

### Standard Signal Chain:
1. **Input Gain**: Compensates for positive EQ boosts (e.g., -3 dB to prevent digital clipping).
2. **Parametric Equalizer**: 8 to 32 bands tailored to driver size and use case.
3. **Bass Enhancer** (Optional): Psychoacoustic sub-harmonics for speakers/headphones lacking physical extension.
4. **Compressor** (Optional for TV/Movies/Gaming): Tames dynamic spikes and brings up low-level dialogue.
5. **Maximizer / Limiter**: Brickwall ceiling at -0.5 dBTP to prevent DAC saturation.

### Bundled Automation Helpers:
1. **Calibrated Preset Generator**:
   ```bash
   python3 scripts/generate_preset.py --profile cloud_alpha_master --name "My Preset" --install
   ```
2. **AutoEq Importer (with preview notice)**:
   ```bash
   python3 scripts/fetch_autoeq.py --model "HyperX Cloud Alpha" --install --confirm
   ```
3. **FFmpeg EBU R128 Loudness Scanner**:
   ```bash
   python3 scripts/check_loudness.py /path/to/audio_file.wav
   ```
4. **Switching & Inspecting Presets**:
   ```bash
   easyeffects -p                     # List presets
   easyeffects -l "My Preset"         # Activate preset
   ```

---

## 5. Iterating & Continuous Training via GitHub

This skill is designed to evolve:
1. **Audiophile Data Intake**: When testing new curves (Oratory1990 AutoEQ measurements, Harman target updates, Head-Fi forum consensus), record the findings into `references/audiophile_curves.md`.
2. **New Presets**: Save validated configurations into `presets/`.
3. **Version Control**: Commit each iteration with descriptive messages:
   ```bash
   git add references/ presets/ scripts/
   git commit -m "feat(preset): add 50mm dual-chamber competitive FPS curve with 250Hz notch"
   git push
   ```
