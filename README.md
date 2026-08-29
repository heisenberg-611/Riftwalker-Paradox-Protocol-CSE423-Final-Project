# Riftwalker: Paradox Protocol

**Course Context:** Computer Graphics 423 (CG423)  
**Project Goal:** A polished PyOpenGL/GLUT sci-fi first/third-person combat game demonstrating computer graphics techniques (hierarchical modeling, procedural generation, camera systems, lighting, particles, raycasting, and time manipulation).

---

## 🎮 Overview

In **Riftwalker: Paradox Protocol**, an astronaut equipped with an experimental **Rift-Chrono Suit** fights alien invaders across two distinct arenas:
1. **Kepler Relay** (Arena 1) - High-tech industrial relay station
2. **Sundered Rift** (Arena 2) - Floating cosmic asteroid wasteland

### Signature Mechanics
- **Rift Teleportation:** Seamless travel between arenas via linked Rift Beacons.
- **Chrono Slow:** Time dilation ability that slows down enemies and projectiles while the player moves normally.
- **Blink Teleport:** Short-range combat evasion dash.
- **Dual Camera System:** Toggle smoothly between 3rd-Person exploration and 1st-Person precision aiming.
- **Procedural Modeling:** Hierarchically articulated astronaut rig and procedurally generated multi-legged alien variants.

---

## 👥 Team Work Breakdown (M1–M4)

| Module | Member Responsibility | Core Deliverables |
|---|---|---|
| **M1** | Player & Camera | Astronaut rig, movement, FP/TP camera systems, Blink teleport |
| **M2** | Enemies & Combat | Alien generator, melee/ranged AI, Boss (Rift Guardian), raycast shooting |
| **M3** | World, Arenas & Teleport | Kepler Relay, Sundered Rift, environment generator, Rift Beacons |
| **M4** | Rendering & Integration | Graphics pipeline, lighting, particle systems, Chrono Slow, HUD, game state |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- PyOpenGL & PyOpenGL_accelerate
- NumPy

### Installation
```bash
pip install -r requirements.txt
```

### Running the Game / Sandbox
```bash
python -m src.main
```

### Controls
| Input | Action |
|---|---|
| `W`, `A`, `S`, `D` | Move (Forward, Left, Backward, Right) |
| `Mouse Movement` | Look / Aim (Pitch and Yaw) |
| `Left Click` / `Space` | Fire Hitscan Weapon |
| `V` / `C` | Toggle 1st Person / 3rd Person Camera |
| `Q` | Activate Chrono Slow (Time Dilation) |
| `F` | Interact / Teleport (near Rift Beacon) |
| `Shift` | Blink Teleport (Combat Dash) |
| `R` | Restart Game |
| `Esc` | Pause / Exit |
