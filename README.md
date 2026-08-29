# Riftwalker: Paradox Protocol

**Course Context:** Computer Graphics 423 (CG423)

**Project Goal:** A polished PyOpenGL/GLUT sci-fi first/third-person combat game demonstrating computer graphics techniques (hierarchical modeling, procedural generation, camera systems, lighting, particles, raycasting, and Chrono Slow time dilation).

---

## 🎮 Overview

In **Riftwalker: Paradox Protocol**, an astronaut equipped with an experimental **Rift-Chrono Suit** fights alien invaders across two distinct arenas:

1. **Kepler Relay** (Arena 1) - High-tech industrial relay station

2. **Sundered Rift** (Arena 2) - Floating cosmic asteroid wasteland

### Signature Mechanics

* **Rift Teleportation:** Teleport between arenas via linked Rift Beacons, with a short visual transition and player repositioning.

* **Chrono Slow:** 5-second time dilation ability. Enemies and projectiles move at approximately 30% speed while the player remains at normal speed. The ability requires 100% Chrono Charge and resets to 0% after activation.

* **Blink Teleport (Stretch):** Optional short-range combat evasion dash.

* **Dual Camera System:** Toggle smoothly between 3rd-Person exploration and 1st-Person precision aiming.

* **Procedural Modeling:** Hierarchically articulated astronaut rig and procedurally generated multi-legged alien variants.

---

## 👥 Team Work Breakdown (M1–M4)

| Module | Member Responsibility    | Core Deliverables                                                                                  |
| ------ | ------------------------ | -------------------------------------------------------------------------------------------------- |
| **M1** | Player & Camera          | Astronaut rig, movement, FP/TP camera systems, weapon viewmodel, Blink teleport (stretch)          |
| **M2** | Enemies & Combat         | Alien generator, melee/ranged AI, boss (Rift Guardian), raycast shooting, combat and hit detection |
| **M3** | World, Arenas & Teleport | Kepler Relay, Sundered Rift, environment generation, Rift Beacons, arena teleportation             |
| **M4** | Rendering & Integration  | Graphics pipeline, lighting, particle systems, Chrono Slow, HUD, score/rank, game state            |

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8+
* PyOpenGL & PyOpenGL_accelerate
* NumPy

### Installation

```bash
pip install -r requirements.txt
```

### Running the Game / Sandbox

```bash
python -m src.main
```

### Controls

| Input                  | Action                                                |
| ---------------------- | ----------------------------------------------------- |
| `W`, `A`, `S`, `D`     | Move (Forward, Left, Backward, Right)                 |
| `Mouse Movement`       | Look / Aim (Pitch and Yaw)                            |
| `Left Click` / `Space` | Fire Hitscan Weapon                                   |
| `V`                    | Toggle 1st Person / 3rd Person Camera                 |
| `Q`                    | Activate Chrono Slow (Requires 100% Charge, lasts 5s) |
| `F`                    | Interact / Teleport near Rift Beacon                  |
| `Shift`                | Blink Teleport (Stretch Feature)                      |
| `R`                    | Restart Game                                          |
| `Esc`                  | Exit Game                                             |

---

## 🛡️ Git Workflow & Main Branch Protection Policy

To protect the stability of the master build and prevent accidental overwrites or merge conflicts across the 4 teammates, **direct pushes to the `main` branch are strictly prohibited**.

All development by team members and AI assistants must follow the **Feature Branch & Pull Request (PR)** model.

### 📌 Core Rules for Everyone (Members & AI Assistants)

1. **Never commit or push directly to `main`**:
   - Always create a new descriptive branch for each feature or bugfix (e.g., `feature/m1-astronaut-rig`, `feature/m2-alien-generator`, `feature/m3-arena-kepler`, `feature/m4-chrono-hud`, `fix/hud-font-fallback`).
2. **One Feature, One Branch**:
   - Keep branch changes focused strictly on your module's assigned tasks.
3. **Pull Request (PR) Requirement**:
   - Push your feature branch to GitHub and open a Pull Request targeting `main`.
4. **Clean Merge Condition**:
   - A PR may only be merged into `main` if:
     - ✅ **No merge conflicts** exist with `main`.
     - ✅ **All unit tests pass** (`python3 -m unittest discover -s tests`).
     - ✅ The code runs cleanly without breaking the PyOpenGL game loop.
5. **Mandate for AI Assistants**:
   - Any AI assistant executing changes must work within an isolated feature branch and prepare commits for PR review rather than pushing straight to `main`.

---

### 🚀 Standard Git Workflow (Step-by-Step)

#### 1. Fetch latest changes from `main`
```bash
git checkout main
git pull origin main
```

#### 2. Create and switch to your feature branch
```bash
# Branch naming convention: feature/m<module_number>-<feature_name>
git checkout -b feature/m1-astronaut-rig
```

#### 3. Make changes and verify locally
```bash
# Verify unit tests pass
python3 -m unittest discover -s tests

# Test the game loop
python -m src.main
```

#### 4. Stage and commit your changes
```bash
git add src/M1_player_camera/...
git commit -m "feat(M1): implement articulated astronaut rig with walking animation"
```

#### 5. Push branch to GitHub
```bash
git push -u origin feature/m1-astronaut-rig
```

#### 6. Open Pull Request on GitHub
- Go to the repository on GitHub: [heisenberg-611/Riftwalker--Paradox-Protocol-CSE423-Final-Project-](https://github.com/heisenberg-611/Riftwalker--Paradox-Protocol-CSE423-Final-Project-)
- Click **"Compare & pull request"**.
- Confirm base is `main` and compare is your feature branch.
- If **"Able to merge"** (no conflicts) and tests pass, merge the PR into `main`.

#### 7. Update your local `main` after merging
```bash
git checkout main
git pull origin main
```

---

### ⚠️ IMPORTANT NOTICE ABOUT `git push` FOR ALL MEMBERS & AI ASSISTANTS

> [!WARNING]
> **CRITICAL PUSH SAFETY NOTICES:**
> 1. **DO NOT run `git push origin main` directly.** Always push to your dedicated feature branch (`git push origin feature/<branch-name>`).
> 2. **NEVER use `git push --force` or `-f` on `main`.** Force pushing can overwrite and permanently delete your teammates' merged work.
> 3. **Resolve Conflicts Locally Before Merging:** If your PR has conflicts with `main`, switch to your branch locally, pull/merge latest `main` (`git pull origin main`), resolve conflicting files in your editor, commit the resolution, and push back to your branch.
> 4. **Run Unit Tests Before Pushing:** Always execute `python3 -m unittest discover -s tests` before pushing to ensure math, physics, and logic invariants remain 100% functional.

### 🤖 Mandatory Git Protocol for AI Assistants
If a team member instructs an AI assistant (e.g. Antigravity, Claude, Cursor, Copilot, ChatGPT) to handle code changes, commits, or git pushes:
1. **Active Branch Check:** The AI must run `git branch --show-current` before staging or committing.
2. **Auto-Branching:** If currently on `main`, the AI **MUST NOT commit to main**. It must immediately create and checkout a feature branch (`git checkout -b feature/mX-<task-name>`).
3. **Zero Force-Push:** The AI is strictly forbidden from running `git push --force` or `-f`.
4. **Pre-Push Validation:** The AI must execute `python3 -m unittest discover -s tests` and verify 0 failures before pushing.
5. **PR Handoff:** The AI must push to `origin feature/mX-...` and direct the user to open and merge the Pull Request on GitHub.

---

## 🤖 Team AI Onboarding Prompts (Zero-Context Starters)

When each team member opens an AI assistant session without prior context, they should copy and paste their module's starter prompt below. Every prompt includes binding instructions ensuring the AI adheres to the feature-branching and test verification rules.

### 👤 Member 1 (M1 — Player & Camera Systems)
```markdown
I am working on **Module M1 (Player & Camera Systems)** for the computer graphics game **Riftwalker: Paradox Protocol** built with **Python, PyOpenGL, and GLUT**.

### Project Context & Specifications:
- The project specification is strictly locked down in `PROJECT_SPEC.md` and `docs/architecture.md`. Treat `PROJECT_SPEC.md` as the single authoritative source of truth.
- Core technologies: Python 3, PyOpenGL, GLUT, pure Python vector/matrix math in `src/shared/math3d.py`, centralized inputs in `src/shared/input_manager.py`, and shared geometric collision tests in `src/shared/collision.py`.

### 🛡️ Mandatory Git & Push Safety Protocol for AI:
1. **Active Branch Check:** Run `git branch --show-current`. If currently on `main`, **DO NOT COMMIT TO MAIN**. Create and checkout a feature branch first (`git checkout -b feature/m1-<feature-name>`).
2. **Never Force-Push:** NEVER execute `git push --force` or `-f`.
3. **Pre-Push Validation:** Always run `python3 -m unittest discover -s tests` before pushing. If any test fails, resolve the failure first.
4. **Push & PR:** Push exclusively to `origin feature/m1-<feature-name>` and guide the user to open a Pull Request targeting `main`.

### My Ownership & Deliverables (`src/M1_player_camera/`):
1. `astronaut_rig.py`: Procedural hierarchical 3D astronaut model using OpenGL matrix stacks (`glPushMatrix`/`glPopMatrix`) with articulated limbs and sinusoidal walking animations.
2. `first_person_camera.py`: 1st-person FPS camera with pitch/yaw clamping and first-person viewmodel gun positioning.
3. `third_person_camera.py`: 3rd-person follow/orbit camera with smooth tracking and distance offset.
4. `player_movement.py`: WASD movement kinematics, arena boundary clamping via `src/shared/collision.py`, and orientation synchronization.
5. `player_weapon.py`: **Weapon Visual Presentation** (astronaut 3D weapon mesh attached to the character's right hand and first-person viewmodel presentation with firing recoil animation).
6. `player.py`: Player coordinator tying health, cameras, rig, movement, and viewmodel together.
7. `blink_teleport.py`: *(Optional Stretch Feature)* Short-range combat dash.

### Boundaries & Rules:
- M1 owns weapon *visuals & viewmodel*, while M2 owns *combat logic, hitscan raycasting, and damage*.
- Use `src/shared/collision.py` for spatial bounds checks. Do not build a separate collision system.
- Standard vertical gravity (+Y up, floor at Y=0) is the baseline; do not assume arbitrary gravity.
- No Inverse Kinematics (IK); use hierarchical forward trigonometry.

Please review `PROJECT_SPEC.md` (Sections 2, 7, 8, 9, 10, 27A) and `src/M1_player_camera/` before implementing or modifying M1 code.
```

---

### 👾 Member 2 (M2 — Enemies & Combat Systems)
```markdown
I am working on **Module M2 (Enemies & Combat Systems)** for the computer graphics game **Riftwalker: Paradox Protocol** built with **Python, PyOpenGL, and GLUT**.

### Project Context & Specifications:
- The project specification is strictly locked down in `PROJECT_SPEC.md` and `docs/architecture.md`. Treat `PROJECT_SPEC.md` as the single authoritative source of truth.
- Core technologies: Python 3, PyOpenGL, GLUT, vector/matrix math in `src/shared/math3d.py`, and shared geometric collision utilities in `src/shared/collision.py`.

### 🛡️ Mandatory Git & Push Safety Protocol for AI:
1. **Active Branch Check:** Run `git branch --show-current`. If currently on `main`, **DO NOT COMMIT TO MAIN**. Create and checkout a feature branch first (`git checkout -b feature/m2-<feature-name>`).
2. **Never Force-Push:** NEVER execute `git push --force` or `-f`.
3. **Pre-Push Validation:** Always run `python3 -m unittest discover -s tests` before pushing. If any test fails, resolve the failure first.
4. **Push & PR:** Push exclusively to `origin feature/m2-<feature-name>` and guide the user to open a Pull Request targeting `main`.

### My Ownership & Deliverables (`src/M2_enemies_combat/`):
1. `alien_generator.py`: Procedural articulated alien creature generator with segmented carapaces, glowing bio-luminescent nodes, and multi-jointed spider/insectoid legs.
2. `enemy_base.py`: Abstract enemy base class tracking HP, states (`IDLE`, `CHASE`, `ATTACK`, `DEAD`), bounding spheres, and Chrono Slow time scaling.
3. `melee_rift_stalker.py`: Fast melee rusher AI that closes distance and performs leaping/lunging attacks.
4. `ranged_rift_spitter.py`: Long-range projectile spitter AI that strafes and launches plasma balls at the player's position.
5. `rift_guardian_boss.py`: Multi-stage final boss encounter featuring rotating orbital shield plates, radial shockwaves, and phased combat.
6. `weapon_system.py`: **Combat Gameplay Logic** (firing rate timers, damage values, projectile pooling, and active projectile updates).
7. `raycast.py`: Precision 3D hitscan raycasting against enemy bounding spheres/AABBs using `src/shared/collision.py`.

### Boundaries & Rules:
- M2 owns *combat logic, hit detection, damage, and projectile physics*, while M1 owns the *weapon mesh & viewmodel rendering*.
- Use `src/shared/collision.py` for pure geometric tests (ray-sphere, sphere-sphere). M2 decides damage and death effects.
- Enemy updates and projectile movement must be scaled by `game_dt` (`dt * 0.30` during Chrono Slow).
- Scope is locked to exactly 2 enemy types and 1 boss. Do not create extra enemy variants or multiple bosses.

Please review `PROJECT_SPEC.md` (Sections 2, 10, 12, 13, 14, 15, 18, 27A) and `src/M2_enemies_combat/` before implementing or modifying M2 code.
```

---

### 🌌 Member 3 (M3 — World, Arenas & Teleportation)
```markdown
I am working on **Module M3 (World, Arenas & Teleportation)** for the computer graphics game **Riftwalker: Paradox Protocol** built with **Python, PyOpenGL, and GLUT**.

### Project Context & Specifications:
- The project specification is strictly locked down in `PROJECT_SPEC.md` and `docs/architecture.md`. Treat `PROJECT_SPEC.md` as the single authoritative source of truth.
- Core technologies: Python 3, PyOpenGL, GLUT, math in `src/shared/math3d.py`, and shared boundary clamping in `src/shared/collision.py`.

### 🛡️ Mandatory Git & Push Safety Protocol for AI:
1. **Active Branch Check:** Run `git branch --show-current`. If currently on `main`, **DO NOT COMMIT TO MAIN**. Create and checkout a feature branch first (`git checkout -b feature/m3-<feature-name>`).
2. **Never Force-Push:** NEVER execute `git push --force` or `-f`.
3. **Pre-Push Validation:** Always run `python3 -m unittest discover -s tests` before pushing. If any test fails, resolve the failure first.
4. **Push & PR:** Push exclusively to `origin feature/m3-<feature-name>` and guide the user to open a Pull Request targeting `main`.

### My Ownership & Deliverables (`src/M3_world_teleport/`):
1. `world.py`: World coordinator managing active arena switching, coordinate mapping, and teleportation triggers.
2. `arena_base.py`: Abstract arena base class holding boundaries, spawn points, and environment props.
3. `arena_01_kepler_relay.py`: Arena 1 environment — high-tech metallic relay station with industrial platforms, perimeter barriers, and server towers.
4. `arena_02_sundered_rift.py`: Arena 2 environment — floating cosmic asteroid wasteland with obsidian ground, floating hazard platforms, and glowing crystal spires.
5. `environment_generator.py`: Modular procedural geometry builder for crates, barricades, pillars, and crystal clusters.
6. `rift_beacon.py`: **Rift Beacon Platform (REQUIRED)** — interactive beacon platform featuring glowing base, spinning concentric torus rings, and activation radius detection ($R \le 3.5$).
7. `gravity_zone.py`: *(Optional Stretch Feature)* Predefined low-gravity / jump-pad zone.

### Boundaries & Rules:
- **Rift Beacon Teleportation is a REQUIRED core feature**: Linked pair ($\text{Arena 1 Beacon A} \leftrightarrow \text{Arena 2 Beacon B}$).
- Implemented as a clean scene state transition with coordinate reset, screen flash, and particles. **Do NOT implement optical portals or simulated wormholes.**
- Core movement model uses standard vertical gravity (+Y up). Do not implement arbitrary wall/ceiling gravity systems.
- Use `src/shared/collision.py` for arena boundary limits and obstacle bounding boxes.

Please review `PROJECT_SPEC.md` (Sections 2, 4, 5, 16, 17, 27A) and `src/M3_world_teleport/` before implementing or modifying M3 code.
```

---

### 🎨 Member 4 (M4 — Rendering, Chrono, HUD & Integration)
```markdown
I am working on **Module M4 (Rendering, Chrono, HUD & Integration)** for the computer graphics game **Riftwalker: Paradox Protocol** built with **Python, PyOpenGL, and GLUT**.

### Project Context & Specifications:
- The project specification is strictly locked down in `PROJECT_SPEC.md` and `docs/architecture.md`. Treat `PROJECT_SPEC.md` as the single authoritative source of truth.
- Core technologies: Python 3, PyOpenGL, GLUT, math in `src/shared/math3d.py`, and timing in `src/shared/game_time.py`.

### 🛡️ Mandatory Git & Push Safety Protocol for AI:
1. **Active Branch Check:** Run `git branch --show-current`. If currently on `main`, **DO NOT COMMIT TO MAIN**. Create and checkout a feature branch first (`git checkout -b feature/m4-<feature-name>`).
2. **Never Force-Push:** NEVER execute `git push --force` or `-f`.
3. **Pre-Push Validation:** Always run `python3 -m unittest discover -s tests` before pushing. If any test fails, resolve the failure first.
4. **Push & PR:** Push exclusively to `origin feature/m4-<feature-name>` and guide the user to open a Pull Request targeting `main`.

### My Ownership & Deliverables (`src/M4_rendering_gameplay/` and `src/main.py`):
1. `renderer.py`: Master OpenGL 3D and 2D render pass orchestrator (clearing buffers, setting projection, rendering world, enemies, player, lighting, particles, and HUD overlay).
2. `primitives.py`: Optimized procedural 3D drawing routines (cubes, cylinders, spheres, cones, torus rings).
3. `lighting.py`: Multi-source dynamic lighting (directional sunlight `GL_LIGHT0`, dynamic beacon/hazard point lights `GL_LIGHT1`).
4. `materials.py`: Specular, diffuse, and ambient material presets for suits, visors, metals, and alien carapaces.
5. `particles.py`: Particle systems (teleport vortex swirl, hit sparks, jet thrusters, blood/death bursts).
6. `effects.py`: Post-render visual filters (teleport cyan screen flash, Chrono Slow cool blue screen tint overlay).
7. `chrono_slow.py`: **Chrono Slow Manager** (charge meter 0-100%, 100% activation gate via key `Q`, 0% reset, 5-second fixed timer countdown, 30% speed scale `0.30`).
8. `hud.py`: **2D Orthographic HUD** (Suit Health bar, Chrono Charge/countdown bar, Score, Objective text prompts).
9. `crosshair.py`: Dynamic interactive center crosshair with hitmarker animation feedback.
10. `scoring.py`: Score manager tracking kills, combos, and letter rank evaluation ($S/A/B/C/D$).
11. `game_state.py`: Global game state machine (`PLAYING`, `TELEPORTING`, `GAME_OVER`, `VICTORY`).
12. `level_manager.py`: Enemy wave spawning and progression.
13. `src/main.py`: Main executable entry point and GLUT callback orchestration.

### Boundaries & Rules:
- **Chrono Slow is simple delta-time scaling** (`game_dt = real_dt * 0.30`), NOT full world rewind or state buffering.
- Player, camera, particles, and HUD update with unscaled `real_dt`; enemies, projectiles, and world physics update with scaled `game_dt`.
- Resolve PyOpenGL GLUT bitmap fonts lazily inside rendering methods to avoid C-pointer reference issues.

Please review `PROJECT_SPEC.md` (Sections 2, 6, 19, 20, 24, 25, 27A, 28) and `src/M4_rendering_gameplay/` before implementing or modifying M4 code.
```

