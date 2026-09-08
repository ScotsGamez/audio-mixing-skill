# Audio Mixing & Calibration Based on Speaker Size

This reference compiles technical principles and practical engineering rules extracted from industry-standard
resources on monitor sizing (Mike Senior's *Mixing Secrets for the Small Studio*, Genelec Monitor Setup Guides,
and ITU-R BS.775 recommendations).

---

## 1. Monitor Woofer Sizing & Physics

| Woofer Diameter | Effective Usable Bandwidth | Listening Distance | Ideal Room Environment | Low-End Acoustic Behavior |
| :--- | :--- | :--- | :--- | :--- |
| **3" to 4" (Desktop / Mini)** | 75 Hz – 20 kHz | 0.5 m – 1.0 m (Ultra-nearfield) | Small bedrooms, untreated spaces | Steep mechanical roll-off below 70 Hz. Zero true sub-bass. |
| **5" to 6" (Compact Nearfield)** | 50 Hz – 20 kHz | 1.0 m – 1.5 m (Standard nearfield) | Small to medium treated rooms | Clean down to ~55 Hz. Port resonance often bumps at 65–80 Hz. |
| **7" to 8" (Full-Range Nearfield)** | 35 Hz – 20 kHz | 1.5 m – 2.5 m (Nearfield / Midfield) | Medium to large acoustic rooms | Linear down to 38 Hz. Heavily excites room modes (standing waves). |
| **10"+ or Subwoofer Addition** | 20 Hz – 120 Hz | System dependent | Professionally treated studios | Shakes room boundaries; requires active bass traps and DSP alignment. |

---

## 2. Mixing Decisions Driven by Speaker Size

### A. The "Missing Fundamental" & Bass Saturation
- **The Physical Problem**: If you mix on 8" monitors or headphones capable of reproducing 30 Hz, you might leave the sub-bass clean and deep. However, when played back on a 3" phone/smart speaker or 4" desktop monitors, **the bassline completely disappears**.
- **The Engineering Solution**:
  - Exploit the psychoacoustic **Missing Fundamental effect**. The human brain will reconstruct the pitch of a 40 Hz fundamental if its 2nd (80 Hz) and 3rd (120 Hz) harmonics are present.
  - Apply subtle saturation, overdrive, or MaxxBass/Bass Enhancer harmonics in the 80–200 Hz region. This ensures the bass translates with weight on 4" speakers while preserving deep rumble on full-range systems.

### B. The "Grotbox" / Auratone Technique (Mike Senior)
- **Concept**: Mixing exclusively on pristine full-range monitors can hide balance flaws because the ear is dazzled by deep sub-bass and airy highs.
- **The Technique**:
  - Periodically switch to a small 4"–5" single-driver monitor (e.g. Auratone 5C or Avantone MixCube) without a tweeter or crossover filter.
  - This forces you to get the critical midrange (**250 Hz – 4 kHz**) balanced: vocal level, snare crack, and guitar presence. If the mix works on limited-range 4" speakers, it translates everywhere.

### C. High-Pass Protection (Low-Cut Filters)
- **Acoustic Danger**: Pushing high-energy sub-bass (20–40 Hz) into 3" or 4" speakers forces the small voice coil to move beyond its linear excursion limit ($X_{\max}$). This generates mud, intermodulation distortion, and excessive heat without producing any audible sub-bass.
- **Rule**: High-pass filter small monitors at **55–65 Hz (18 dB/oct)** in DSP to unburden the cone and allow cleaner midrange reproduction.

---

## 3. Room Boundary Loading by Speaker Placement (Genelec Acoustic Rules)

Placing speakers near walls or desk surfaces artificially boosts low-frequency energy due to acoustic boundary loading:

```
           Corner Placement: +9 dB to +12 dB Sub-Bass
                 ┌───────────────┐
                 │ \           / │
                 │  \  WALL   /  │
                 │   \       /   │
                 └───────┬───────┘
                         │
     Wall Placement:     ▼     Free Space (Away from walls):
     +3 dB to +6 dB Bass       Flat Frequency Response
```

### Boundary Calibration Rules:
1. **Desktop Reflection**: Desk surfaces create a severe reflection comb-filter between **160 Hz and 250 Hz**. Dip 200 Hz by -2 dB to -4 dB (Q=2.0) on desktop speakers.
2. **Against a Wall (<0.5m)**: Apply a **-3 dB to -4 dB Low-Shelf Cut** below 100 Hz to counteract half-space boundary gain.
3. **In a Corner**: Apply a **-6 dB Low-Shelf Cut** below 100 Hz to eliminate quarter-space boomy resonance.

---

## 4. EasyEffects Calibration for Desktop Speakers vs. Headphones

When switching EasyEffects from Headphone mode to Desktop Speaker mode:

```bash
# Example DSP adjustments for 3"-4" Desktop Speakers:
# 1. High-pass filter at 55Hz (protect small woofers)
# 2. Desk reflection cut: -2.5dB at 200Hz
# 3. Harmonic enhancer: Add 2nd/3rd harmonics for bass definition
# 4. Vocal clarity bump: +2.0dB at 2.5kHz
```
