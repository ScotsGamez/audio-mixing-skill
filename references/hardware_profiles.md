# Hardware Acoustic Profiles & Transducer Sizing

Acoustic calibration must account for the mechanical and physical properties of the transducer.
Different driver sizes and enclosure types impose hard physical limits on low-frequency reproduction,
harmonic distortion (THD), and soundstage dispersion.

---

## 1. Transducer Physics & Driver Sizing

Low frequency sound reproduction relies on volumetric air displacement ($V_d$):
$$V_d = S_d \times X_{\max}$$
where $S_d$ is diaphragm surface area and $X_{\max}$ is maximum linear peak excursion.

### Mathematical Comparison: 40mm vs 50mm vs 53mm Drivers
- **40mm Driver**: Diaphragm area $S_d \approx \pi \times 20^2 \approx 1256 \text{ mm}^2$
- **50mm Driver**: Diaphragm area $S_d \approx \pi \times 25^2 \approx 1963 \text{ mm}^2$ (+56.3% larger surface area)
- **53mm Driver**: Diaphragm area $S_d \approx \pi \times 26.5^2 \approx 2206 \text{ mm}^2$ (+75.6% larger surface area)

### Acoustic Impact:
1. **50mm+ Drivers**:
   - Because of the 56% larger surface area, the driver moves **36% less mechanical distance** to generate the exact same sub-bass SPL at 30–60 Hz as a 40mm driver.
   - Result: Much lower intermodulation and total harmonic distortion (THD) at high volumes. Can safely handle substantial sub-bass shelf boosts (+6 dB to +9 dB) without muddying or breaking up.
2. **40mm Drivers**:
   - Must push toward mechanical excursion limits ($X_{\max}$) to produce deep rumble.
   - Pushing heavy sub-bass (<40Hz) into a 40mm driver causes voice coil non-linearity, compressing the mids and creating audible distortion.
   - Recommendation: High-pass filter at 30–35 Hz; concentrate bass boost around 70–90 Hz (punch) instead of 30 Hz (rumble).
3. **Planar Magnetic Transducers**:
   - The entire diaphragm is suspended in a uniform magnetic field and driven evenly across its surface.
   - Near-zero bass distortion and linear phase extension down to 10 Hz.
   - Tolerates steep sub-bass EQ curves effortlessly.

---

## 2. Headphone Enclosure Architecture

### A. Closed-Back Headphones (e.g., Cloud Alpha, DT770, M50x)
- **Acoustics**: Trapped internal air volume acts as an acoustic spring. High passive isolation.
- **Inherent Flaws**: Internal acoustic reflections bounce off the plastic ear cups, creating a boxy resonance typically between **200 Hz and 400 Hz**, and a congested soundstage.
- **Dual-Chamber Design (Cloud Alpha Specific)**:
  - Uses separate physical chambers for bass versus mids/highs.
  - Reduces the modulation of mids by bass frequencies.
  - Allows aggressive sub-bass boosting without bleeding into the 1 kHz vocal territory, provided the 250 Hz box resonance is kept in check.
- **Target EQ Calibration**:
  - Cut 250 Hz by -2.5 dB to -3.5 dB (Q = 1.4) to remove the closed-cup "boxiness".
  - Boost 32–64 Hz for cinematic rumble.
  - Mild 1 kHz boost (+1.5 to +2 dB) to pull vocals forward.

### B. Open-Back Headphones (e.g., HD600, DT990, Sundara)
- **Acoustics**: Back of driver is open to the room. No cup reflections, wide natural soundstage.
- **Inherent Flaws**: Acoustic front-to-back phase cancellation causes a natural sub-bass roll-off below 50–70 Hz.
- **Target EQ Calibration**:
  - Low shelf filter at 65 Hz (+4 to +6 dB, Q=0.7) to restore Harman target sub-bass warmth.
  - High-frequency de-peaking: Open-backs often have treble spikes at 6 kHz or 8.5 kHz that need narrow notch cuts (-3 dB, Q=4.0).

---

## 3. Desktop Speakers & Nearfield Studio Monitors

When calibrating speakers (e.g. 3", 5", or 8" woofers on a desk or stands):

### Woofer Size Rules:
1. **3" to 4" Desktop Woofers**:
   - Physical bass cutoff: Roll-off begins sharply around 70–80 Hz.
   - Dangerous Mistake: Boosting 30–40 Hz will bottom out the small woofer cone and cause severe clipping.
   - Correct Tuning: High-pass at 60 Hz (18 dB/oct). Boost 90–120 Hz for perceived warmth.
2. **5" to 8" Studio Monitors**:
   - Clean extension down to 45–55 Hz (5") or 35–42 Hz (8").
   - Room Boundary Effect: Placing speakers close to a wall boosts bass by +3 dB; placing them in a corner boosts bass by +6 dB to +9 dB (quarter-space boundary loading).
   - Correct Tuning: If desk/wall loaded, apply a low-shelf cut (-2 to -4 dB below 120 Hz) to eliminate muddy acoustic boom.
