# 🌌 Riftwalker: Paradox Protocol
> **CSE423 Computer Graphics & Multimedia Laboratory — Final Project Brief**  
> *A 3D Sci-Fi Dimensional Combat & Procedural Graphics Game*

---

## 📌 Executive Summary

**Riftwalker: Paradox Protocol** is a real-time 3D sci-fi action game built from scratch using **Python 3, PyOpenGL, and GLUT**, without the use of external commercial game engines (e.g., Unity, Unreal). 

The game balances **60% Advanced Computer Graphics techniques** (hierarchical matrix transformations, multi-source lighting, particle systems, 3D raycasting, dual-camera projections, 2D orthographic HUD overlay) with **40% Core Gameplay dynamics** (spatial arena teleportation, temporal time dilation, hitscan combat, wave survival, and a multi-phase boss encounter).

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                 CORE GAMEPLAY LOOP                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  [Arena 1: Kepler Relay] ──(Charge Chrono & Defeat Wave)──> [Linked Rift Beacon]        │
│                                                                    │                    │
│                                                          (Spatial Teleport)             │
│                                                                    ▼                    │
│  [Victory / Rank S-D] <──(Defeat Rift Guardian Boss)─────── [Arena 2: Sundered Rift]    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎨 Key Computer Graphics Techniques Demonstrated

The project demonstrates fundamental and advanced principles of the CSE423 curriculum:

| CG Technique | Implementation & Mathematical Foundation in Game |
|---|---|
| **Hierarchical 3D Modeling** | Nested matrix stacks (`glPushMatrix` / `glPopMatrix`) composing articulated characters (astronaut suit, limb swing animations) and faceted *Crystalline Void* aliens from basic geometric primitives (cubes, cylinders, spheres, cones, torus rings). |
| **Dual-Camera Coordinate Systems** | Seamless switching between **First-Person (FPS)** eye-level view and **Third-Person (TPS)** orbit/follow camera using `gluLookAt`, spherical coordinates ($\theta, \phi$), and trigonometric vector calculations. |
| **3D Vector Raycasting** | Pure Python ray-sphere and ray-AABB geometric intersection queries for instant hitscan laser weapon targeting and crosshair aim. |
| **Multi-Source Dynamic Lighting** | OpenGL fixed-function pipeline with ambient, diffuse, and specular components (`GL_LIGHT0` directional planetary sunlight, `GL_LIGHT1` dynamic point-light on glowing Rift Beacons and plasma projectiles). |
| **Particle Simulation Systems** | Real-time procedural particle emitters calculating gravity, velocity, fade lifetime, and color gradients for teleport vortex swirls, laser hit sparks, and death bursts. |
| **2D Orthographic HUD Overlay** | Dynamic viewport matrix switching (`glMatrixMode(GL_PROJECTION)`, `glOrtho`) for rendering 2D health bars, Chrono charge gauges, score counters, dynamic crosshairs, and objective prompts. |
| **Screen-Space Visual Filters** | Post-scene render overlays simulating optical effects (cyan screen flash during teleportation, cool-blue temporal tint during Chrono Slow). |

---

## 🎮 Core Gameplay Mechanics

### 1. Dual-Arena Progression & Spatial Teleportation
* **Arena 1 — Kepler Relay:** Metallic, industrial human relay station with walkways, barricades, and security towers.
* **Arena 2 — Sundered Rift:** Cosmic asteroid void with obsidian ground platforms and floating dimensional hazard crystals.
* **Linked Rift Beacon Platform (REQUIRED):** An interactive circular teleportation gate featuring animated rotating torus rings. Stepping on the platform and pressing `F` initiates a scene state transition with player coordinate resets, particle vortex bursts, and screen flash.

### 2. Chrono Slow (Time Dilation Engine)
* **Mechanic:** A combat-charged time manipulation ability.
* **Activation Gate:** Charged from 0% to **100%** by defeating enemies and landing hits. Activated with **`Q`**.
* **Effect:** Consumes the full charge (resets to 0%) and triggers **5 seconds of 30% time dilation** (`game_dt = real_dt * 0.30`).
* **Game Invariant:** Enemies and enemy plasma projectiles slow down to 30% speed, while the player moves, aims, and fires at 100% normal speed.

### 3. Combat System & Enemy Types
* **Player Weapon:** High-precision hitscan laser rifle with muzzle flash animations, dynamic crosshair hitmarkers, and impact sparks.
* **Rift Stalker (Melee):** Fast predatory shadow-hound made of sharp obsidian shards that charges and leaps at the player.
* **Rift Spitter (Ranged):** Hovering dimensional crystal prism with orbital rotating shard rings that strafes and launches plasma balls.
* **Rift Guardian (Boss):** Multi-phase final boss protected by 4 rotating orbital shield obelisks with radial energy shockwaves.

---

## ⌨️ Controls & Keybindings

| Key / Input | Action |
|---|---|
| **`W`, `A`, `S`, `D`** | Move Forward / Strafe Left / Move Backward / Strafe Right |
| **Mouse Movement** | Look / Aim (Pitch & Yaw Precision Aim) |
| **Arrow Keys (`←`, `→`, `↑`, `↓`)** | Continuous Smooth Camera Turn & Pitch |
| **Left Click** / **`Space`** | Fire Hitscan Laser Weapon |
| **`V`** / **`C`** | Toggle First-Person (1P) / Third-Person (3P) Camera |
| **`Q`** | Activate Chrono Slow (Requires 100% Charge) |
| **`F`** | Interact / Activate Rift Beacon Teleportation |
| **`E`** | Evasive Combat Blink Dash |
| **`F11`** | Toggle Fullscreen Mode (Fit Display) |
| **`R`** | Restart Game (Game Over / Victory screen) |
| **`Esc`** | Exit Game |


---

## 👥 Modular Architecture & Team Work Breakdown

To ensure clean separation of concerns and independent team development, the codebase is partitioned into 4 decoupled modules and a shared core math library:

```text
src/
├── main.py                     # Entry point (GLUT callbacks & game orchestration)
├── shared/                     # Shared vector math, collision geometry, timing, constants
│   ├── math3d.py               # Vector3 & matrix math
│   ├── collision.py            # Geometric sphere/AABB & raycast tests
│   └── game_time.py            # Dual-clock delta-time (real_dt vs game_dt)
│
├── M1_player_camera/           # [Member 1] Player rig, kinematics, 1P/3P cameras, viewmodel
├── M2_enemies_combat/          # [Member 2] Alien generator, AI state machine, boss, combat
├── M3_world_teleport/          # [Member 3] Kepler Relay, Sundered Rift, Rift Beacon platform
└── M4_rendering_gameplay/      # [Member 4] Master renderer, lighting, particles, Chrono, HUD
```

| Member / Module | Core Deliverables |
|---|---|
| **Member 1 (M1)** | Hierarchical astronaut rig with walking animation, FPS/TPS cameras, WASD kinematics, weapon 3D viewmodel mesh. |
| **Member 2 (M2)** | Procedural Crystalline Void alien generator, Melee Stalker AI, Ranged Spitter AI, Rift Guardian boss, raycast combat logic. |
| **Member 3 (M3)** | Kepler Relay arena, Sundered Rift arena, modular environment props, animated Rift Beacon teleportation platform. |
| **Member 4 (M4)** | Master OpenGL pipeline, dynamic multi-lighting, particle emitters, Chrono Slow manager, 2D orthographic HUD, game state. |

---

## 🛡️ Software Engineering & Git Standards

* **Strict Feature Branching:** Direct pushes to `main` are prohibited. All team contributions are submitted via isolated feature branches (`feature/mX-<task>`) and merged through GitHub Pull Requests.
* **Automated Unit Testing:** Full automated test suite verifying mathematical vector operations, collision geometry, Chrono charge gates, and state machines prior to every merge.
* **Zero External Engine Dependencies:** Built purely on Python 3 and PyOpenGL bindings with native macOS/Windows GLUT windowing.

---

## 🚀 How to Run the Game

### Prerequisites
* Python 3.9+
* PyOpenGL & GLUT

### Execution Command
From the root directory:
```bash
python3 src/main.py
```

### Run Automated Tests
```bash
python3 -m unittest discover -s tests
```
