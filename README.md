# Audio Mixing & Hardware Calibration AI Skill

An agentic AI skill for intelligent audio mixing, mastering, acoustic transducer calibration (based on headphone driver size, speaker woofer diameter, and enclosure design), and Linux DSP profile generation (EasyEffects / PipeWire).

This repository is structured both as an **Antigravity AI Agent Skill** (`SKILL.md`) and a standalone audio engineering knowledge base that you can train, iterate on, and sync via GitHub.

---

## 🎧 Features

- **Transducer & Driver Physics**: Calibrates EQ and dynamics specifically for physical driver diameters (e.g., 40mm vs 50mm dual-chamber vs planar magnetic) to avoid excursion distortion.
- **Mastering Masters Knowledge Base**: Built on the foundations of Bob Katz's K-System, Fletcher-Munson equal-loudness contours, and modern EBU R128 / ITU-R BS.1770 LUFS streaming targets.
- **Target Profiles**:
  - **Music**: Harman Target 2019 reference, EDM sub-bass punch, vocal warmth, acoustic realism.
  - **Competitive Gaming**: Suppresses explosion rumble (<60Hz), clarifies directional footstep clicks (1.2–3.5kHz).
  - **Cinema & TV**: Vocal intelligibility enhancement and dynamic range compression for comfortable late-night viewing.
- **Linux DSP Integration**: Generates, installs, and activates calibrated JSON presets directly inside EasyEffects (`~/.local/share/easyeffects/output/`).

---

## 📁 Repository Structure

```
audio-mixing/
├── SKILL.md                          # Main AI Agent skill definition and runbook
├── README.md                         # Project documentation and GitHub setup guide
├── .gitignore
├── references/                       # The training knowledge base
│   ├── mastering_masters.md          # Bob Katz, Fletcher-Munson, LUFS, gain staging
│   ├── hardware_profiles.md          # 40mm vs 50mm vs planar, open vs closed, monitors
│   ├── use_case_targets.md           # EQ curves for Gaming, Movies, Music, Studio
│   ├── audiophile_curves.md          # Oratory1990, Harman 2019, Rtings, Cloud Alpha
│   └── easyeffects_dsp_pipeline.md   # EasyEffects signal flow and CLI automation
├── scripts/
│   └── generate_preset.py            # Automated preset compiler and EasyEffects installer
└── presets/                          # Version-controlled reference presets
    ├── Cloud Alpha - Pro Audiophile Master.json
    ├── Gaming - FPS Spatial Clarity.json
    ├── Cinema - Dialogue & Dynamic Control.json
    └── Audiophile - Harman 2019 Reference.json
```

---

## 🔗 Antigravity Skill Integration

This directory is symlinked into your global agent skills:
```bash
ln -s ~/Projects/audio-mixing ~/.agents/skills/audio-mixing
```
Antigravity automatically discovers the `audio-mixing` skill. Whenever you ask your AI assistant to calibrate sound, mix a track, or configure EasyEffects, the assistant activates this skill and follows the procedures in `SKILL.md`.

---

## 🚀 GitHub Connection & Iteration Workflow

### 1. Authenticate with GitHub CLI
Run the following in your terminal to authenticate via web browser:
```bash
gh auth login -p https -w
```
Follow the one-time code prompt in your web browser.

### 2. Set Your Git Identity (if not already set)
```bash
git config --global user.name "Your Name or GitHub Username"
git config --global user.email "your_email@example.com"
```

### 3. Create & Push the GitHub Repository
From inside `~/Projects/audio-mixing`:
```bash
cd ~/Projects/audio-mixing
git add .
git commit -m "feat: initial release of audio-mixing skill with hardware profiling and mastering runbooks"
gh repo create audio-mixing-skill --public --source=. --remote=origin --push
```

### 4. Continuous Iteration & "Training" the Skill
Whenever you test new curves, learn new mastering techniques from audio engineers, or find audiophile measurements (e.g. from AutoEQ or Reddit /r/oratory1990):
1. Add or edit notes in `references/audiophile_curves.md` or `references/mastering_masters.md`.
2. Generate and test presets using `python3 scripts/generate_preset.py --install --apply`.
3. Commit and push your iterations to GitHub:
   ```bash
   git add .
   git commit -m "feat(curve): update 50mm Cloud Alpha EQ profile with refined 135Hz cut"
   git push
   ```
Your AI assistant will immediately pick up and apply the updated knowledge in subsequent conversations!
