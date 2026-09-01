# 🌌 Riftwalker: Paradox Protocol
> **CSE423 Computer Graphics & Multimedia Laboratory — Final Project Brief**  
> *A 3D Sci-Fi Dimensional Combat & Procedural Graphics Game*

---

## 📌 Executive Summary

**Riftwalker: Paradox Protocol** is a real-time 3D sci-fi action game built from scratch using **Python 3, PyOpenGL, and GLUT**, without the use of external commercial game engines (e.g., Unity, Unreal). 

The game balances **60% Advanced Computer Graphics techniques** (hierarchical matrix transformations, multi-source lighting, particle systems, 3D raycasting, dual-camera projections, 2D orthographic HUD overlay) with **40% Core Gameplay dynamics** (structured wave combat, tactical arena hazards, spatial arena teleportation, temporal time dilation, combo scoring, and a multi-phase boss encounter).

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                 CORE GAMEPLAY LOOP                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  [Arena 1: Kepler Relay] ──(Clear Waves 1-3 & Evade Hazards)──> [Unlock Rift Beacon]    │
│                                                                        │                │
│                                                              (Spatial Teleport)         │
│                                                                        ▼                │
│  [Victory / Rank S-D] <──(Defeat Boss)── [Arena 2: Waves 1-3 & Void Traps]              │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎨 Key Computer Graphics Techniques Demonstrated

The project demonstrates fundamental and advanced principles of the CSE423 curriculum:

| CG Technique | Implementation & Mathematical Foundation in Game |
|---|---|
| **Hierarchical 3D Modeling** | Nested matrix stacks (`glPushMatrix` / `glPopMatrix`) composing articulated characters (astronaut suit, limb swing animations, weapon aim) and faceted *Crystalline Void* aliens from basic geometric primitives (cubes, cylinders, spheres, cones, torus rings). |
| **Dual-Camera Coordinate Systems** | Seamless switching between **First-Person (FPS)** eye-level view (with 3D blaster viewmodel) and **Third-Person (TPS)** over-the-shoulder follow camera using `gluLookAt`, spherical coordinates ($\theta, \phi$), and trigonometric vector calculations. |
| **3D Vector Raycasting & Tracers** | Pure Python ray-sphere and ray-AABB geometric intersection queries for instant hitscan laser weapon targeting, accompanied by dual-pass 3D visual laser tracer beams. |
| **Multi-Source Dynamic Lighting** | OpenGL fixed-function pipeline with ambient, diffuse, and specular components (`GL_LIGHT0` directional planetary sunlight, `GL_LIGHT1` dynamic point-lights on glowing Rift Beacons, hazards, and plasma projectiles). |
| **Particle Simulation Systems** | Real-time procedural particle emitters calculating gravity, velocity, fade lifetime, and color gradients for teleport vortex swirls, laser hit sparks, muzzle flashes, and death bursts. |
| **2D Orthographic HUD Overlay** | Dynamic viewport matrix switching (`glMatrixMode(GL_PROJECTION)`, `glOrtho`) for rendering 2D health bars, Chrono charge gauges, weapon cycling cooldown bars, live wave objectives, combo multipliers, and boss health bars. |
| **Screen-Space Visual Filters** | Post-scene render overlays simulating optical effects (cyan screen flash during teleportation, cool-blue temporal tint during Chrono Slow). |

---

## 🎮 Core Gameplay Mechanics

### 1. Structured Wave Combat & Dual-Arena Progression
* **Arena 1 — Kepler Relay (Close Quarters & Cover):** Metallic outpost with tight corridors, moving laser barriers, and electrified floor zones. Features 3 escalating combat waves.
* **Arena 2 — Sundered Rift (Vast Open Void):** Cosmic asteroid plateau with long sightlines, rotating energy beams, and rift damage zones. Features 3 intense waves leading into the boss fight.
* **Tactical Rift Beacon Platform (REQUIRED):** Interactive teleportation gate locked during combat waves. Unlocks upon arena wave clearance, allowing tactical repositioning and inter-arena teleportation (`F` key).

### 2. Chrono Slow (Time Dilation Engine)
* **Mechanic:** A combat-charged time manipulation ability.
* **Activation Gate:** Charged from 0% to **100%** by defeating enemies and landing hits. Activated with **`Q`**.
* **Effect:** Consumes the full charge (resets to 0%) and triggers **5 seconds of 30% time dilation** (`game_dt = real_dt * 0.30`).
* **Game Invariant:** Enemies, hazards, and enemy plasma projectiles slow down to 30% speed, while the player moves, aims, and fires at 100% normal speed.

### 3. Combo Scoring & Enemy Encounters
* **Combo Multipliers:** Rapid consecutive kills within a 3.5s window grant `COMBO x1` $\rightarrow$ `COMBO x4` score multipliers. Taking damage reduces the combo.
* **Rift Stalker (Melee):** Swift predator with sinusoidal zig-zag evasion and sudden melee lunge bursts.
* **Rift Spitter (Ranged):** Standoff hovering prism with rotating shard rings that strafes and fires targeted plasma volleys.
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
