# Use Case Target Profiles & EQ Strategies

Audio tuning must adapt to the media being consumed. Below are the acoustic targets, EQ curves,
and DSP chain recommendations for different use cases.

---

## 1. Music Listening Profiles

### Profile A: Harman Target 2019 (Audiophile Standard)
- **Philosophy**: Simulates the acoustic response of high-end, acoustically treated studio monitors in a well-damped room.
- **Key Characteristics**:
  - Sub-bass shelf: +6 dB to +8 dB boost below 75 Hz (Q = 0.7).
  - Flat, linear midrange transition from 200 Hz to 1 kHz.
  - Pinna gain ear canal compensation: Smooth rise peaking around 3 kHz (+8 to +10 dB above baseline).
  - Natural gentle treble roll-off above 10 kHz.

### Profile B: Clean Deep Bass & Punch (Electronic, Hip-Hop, Pop)
- **Target Sound**: Shaking sub-bass without masking vocals or instrument separation.
- **Parametric Bands**:
  - 32 Hz: +8.0 dB (Bell/Shelf, Q=1.2) - deep physical vibration
  - 64 Hz: +5.0 dB (Bell, Q=1.4) - kick fundamental
  - 125 Hz: -3.0 dB (Bell, Q=1.4) - de-boom kick/bass overlap
  - 250 Hz: -2.5 dB (Bell, Q=1.4) - remove mud
  - 1 kHz: +1.5 dB (Bell, Q=1.2) - vocal presence
  - 8 kHz: +2.0 dB (Bell, Q=1.5) - crisp hi-hat definition
  - 16 kHz: +3.0 dB (High Shelf, Q=0.7) - air and separation

---

## 2. Competitive Gaming (FPS / Spatial Audio)

### Goal: Footstep Isolation & Positional Cues
- **The Problem in Gaming Audio**: Explosions, grenades, and vehicle engines occupy 30–150 Hz at high volume, triggering acoustic masking that completely conceals enemy footsteps and reload clicks.
- **Target Tuning**:
  - **Sub-Bass Attenuation**: High-pass filter at 45 Hz; cut 60–100 Hz by -4 dB to -6 dB. This strips explosive drone and rumble.
  - **Mud Cut**: Dip 250 Hz by -3 dB to clarify the stereo field.
  - **Footstep & Cue Isolation**:
    - Boost **1.2 kHz to 1.8 kHz** (+3.5 dB, Q=2.0) - Grass, gravel, and dirt footstep friction.
    - Boost **2.8 kHz to 3.6 kHz** (+4.5 dB, Q=2.5) - Concrete steps, metal reloads, pinna spatial localization.
  - **Treble Taming**: Dip 7 kHz by -2.5 dB to prevent weapon fire crack from deafening the player.

---

## 3. TV & Movies (Dialogue Intelligibility & Dynamic Taming)

### Goal: Clear Speech Without Jumping to Grab the Remote During Action Scenes
- **The Problem**: Cinema audio is mixed for commercial theater dynamic ranges (>25 dB dynamic variation). At home on headphones or desktop speakers, whispers are inaudible while gunshots and explosions blow out your eardrums.
- **Target DSP Chain**:
  1. **Compressor**:
     - Threshold: -18 dB
     - Ratio: 3:1 or 4:1
     - Attack: 15 ms
     - Release: 200 ms
     - Makeup Gain: +3.5 dB
     - Result: Lifts soft dialogue while clamping cinematic explosions.
  2. **Parametric EQ**:
     - Low Cut: 40 Hz (12 dB/oct)
     - Speech Clarity Boost: +3.0 dB at 1.8 kHz to 2.5 kHz (vocal formant region)
     - Sibilance Control: Mild notch at 6.5 kHz (-2 dB) to soften harsh broadcast sibilance.

---

## 4. Studio Reference & Mastering Monitor Mode

### Goal: Brutally Honest Transparency
- **Philosophy**: Neutral frequency response with zero cosmetic hype. Mix flaws, phase cancellation, and masking must be immediately audible.
- **Tuning**:
  - AutoEQ calibration to diffuse-field or IEF neutral target.
  - Flat response across 100 Hz – 10 kHz ($\pm 1.5 \text{ dB}$).
  - Maximizer set to strict 0.0 dB unity gain with -0.5 dB True Peak ceiling to catch overs.
