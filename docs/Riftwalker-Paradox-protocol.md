# 🌌 Riftwalker: Paradox Protocol
> **CSE423 Computer Graphics & Multimedia Laboratory — Final Project Brief**  
> *A 3D Sci-Fi Dimensional Combat & Procedural Graphics Game*

---

## 📌 Executive Summary

**Riftwalker: Paradox Protocol** is a real-time 3D sci-fi action game built from scratch using **Python 3, PyOpenGL, and GLUT**, without the use of external commercial game engines (e.g., Unity, Unreal). 

The game balances **60% Advanced Computer Graphics techniques** (hierarchical matrix transformations, multi-source lighting, particle systems, 3D raycasting, dual-camera projections, 2D orthographic HUD overlay) with **40% Core Gameplay dynamics** (tactical spatial arena teleportation, temporal time dilation, hitscan combat, collectible energy crystals, wave survival, and a multi-phase boss encounter).

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                 CORE GAMEPLAY LOOP                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  [Arena 1: Kepler Relay] ──(Kills + Rift Pickups → 100% Chrono)──> [Linked Rift Beacon] │
│      (Tighter / Covered)                                                    │           │
│                                                                    (Tactical Teleport)  │
│                                                                             ▼           │
│  [Victory / Mission Complete] <──(Defeat Phase 1 & 2 Boss)─── [Arena 2: Sundered Rift]  │
│                                                                  (Open Void Arena)      │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎨 Key Computer Graphics Techniques Demonstrated

The project demonstrates fundamental and advanced principles of the CSE423 curriculum:

| CG Technique | Implementation & Mathematical Foundation in Game |
|---|---|
| **Hierarchical 3D Modeling** | Nested matrix stacks (`glPushMatrix` / `glPopMatrix`) composing articulated characters (astronaut suit, limb swing animations, thruster pack) and faceted *Crystalline Void* aliens from basic geometric primitives (cubes, cylinders, spheres, cones, octahedrons, torus rings). |
| **Dual-Camera Coordinate Systems** | Seamless switching between **First-Person (FPS)** eye-level view (with dedicated 3D blaster viewmodel) and **Third-Person (TPS)** orbit/follow camera using `gluLookAt`, spherical coordinates ($\theta, \phi$), and trigonometric vector calculations. |
| **3D Vector Raycasting** | Pure Python ray-sphere and ray-AABB geometric intersection queries for instant hitscan laser weapon targeting and crosshair aim. |
| **Multi-Source Dynamic Lighting** | OpenGL fixed-function pipeline with ambient, diffuse, and specular components (`GL_LIGHT0` directional planetary sunlight, `GL_LIGHT1` dynamic point-light on glowing Rift Beacons and plasma projectiles). |
| **Particle Simulation Systems** | Real-time procedural particle emitters calculating gravity, velocity, fade lifetime, and color gradients for teleport vortex swirls, laser hit sparks, crystal pickup sparkles, alien death bursts, and Chrono ripples. |
| **2D Orthographic HUD Overlay** | Dynamic viewport matrix switching (`glMatrixMode(GL_PROJECTION)`, `glOrtho`) for rendering 2D health bars, Chrono charge gauges, Boss health bar, score counters, dynamic crosshairs, and objective prompts. |
| **Screen-Space Visual Filters** | Post-scene render overlays simulating optical effects (cyan screen flash during teleportation, cool-blue temporal tint and corner vignette during Chrono Slow). |

---

## 🎮 Core Gameplay Mechanics

### 1. Dual-Arena Progression & Tactical Spatial Teleportation
* **Arena 1 — Kepler Relay:** Tighter industrial human relay station with metallic floor grid, perimeter security walls, server pillars, crates, and covered combat areas.
* **Arena 2 — Sundered Rift:** Open floating obsidian asteroid void surrounded by a neon purple anomaly grid and floating dimensional crystal spires.
* **Linked Rift Beacon Teleportation (REQUIRED):** Interactive circular teleportation gates with animated rotating torus rings linking both arenas. Stepping on the platform ($R \le 3.5$) and pressing **`F`** initiates an atomic scene state transition with player coordinate resets, particle vortex swirls, and a screen flash. Teleportation can be used tactically during combat to reposition or retreat.

### 2. Chrono Slow (Time Dilation Engine)
* **Mechanic:** A combat-charged time manipulation ability.
* **Charge Dynamics:** Starts at 0% and fills from defeating enemies (+25% Stalker, +35% Spitter, +10% Boss hit) and collecting **Rift Energy Pickups** (+25%).
* **Activation Gate:** Can **only** be activated when the charge reaches **100%**.
* **Consumption:** Pressing **`Q`** consumes the entire charge and immediately resets the meter to **0%**.
* **Effect:** Triggers **5.0 seconds of 30% time dilation** (`game_dt = real_dt * 0.30`). Enemies and enemy plasma projectiles move at 30% speed, while the player moves, aims, and fires at 100% normal speed.
* **Visual Presentation:** Cool-blue temporal screen tint with corner vignette accents and expanding radial Chrono ripple particles.

### 3. Collectible Rift Energy Pickups
* **Visual:** Floating, spinning glowing cyan/magenta crystal octahedrons surrounded by rotating halo rings placed throughout both arenas.
* **Collection:** Walking into a pickup awards **+25% Chrono Charge**, +150 score, and spawns sparkling upward particle bursts.
* **Respawn:** Automatically respawns after a 15-second cooldown.

### 4. Combat System & Procedural Crystalline Void Enemies
* **Player Weapon & 1P Viewmodel:** High-precision hitscan laser rifle. In First-Person mode, renders a 3D blaster rifle in the bottom-right foreground with firing recoil, glowing cyan energy rails, and muzzle flare.
* **Rift Stalker (Melee):** Fast predatory quadrupedal shadow-hound composed of faceted obsidian carapace shards, a pulsing cyan rift fissure core, and articulated scythe blades that swing during pursuit.
* **Rift Spitter (Ranged):** Hovering dimensional crystal prism with dual counter-rotating orbital shard rings and a pulsating plasma eye that charges and fires projectiles.
* **Rift Guardian (Boss):** Colossal floating obsidian nexus core with 4 independent orbiting shield obelisks. Transitions to **Phase 2** at $\le 50\%$ HP where shields expand and rotate at 2.7x speed with radiating shockwave rings.

---

## 👥 The 12 Major Team Features (3 per Member)

| Member / Module | Feature 1 | Feature 2 | Feature 3 |
|---|---|---|---|
| **M1: Player & Camera** | **Procedural Hierarchical Astronaut Rig** (`glPushMatrix`/`glPopMatrix`, suit, visor, thruster pack, articulated walking limbs) | **Dual Camera System** (`V` hotkey, 1st-person FPS & 3rd-person orbital TPS view matrix preservation) | **Player Movement & 1P Blaster Viewmodel** (WASD kinematics, velocity damping, foreground 3D rifle viewmodel with firing recoil) |
| **M2: Enemies & Combat** | **Procedural Crystalline Void Alien Generator** (Obsidian carapaces, glowing rift cores, articulated scythes & rotating shard rings) | **Enemy AI & Hitscan Combat** (Melee Stalker pursuit, Ranged Spitter kiting, 3D raycast laser fire & projectile collisions) | **Rift Guardian Boss Encounter** (Pulsating nexus core, 4 rotating orbital shield obelisks, Phase 1 vs Phase 2 rapid spinning) |
| **M3: World & Teleportation** | **Kepler Relay Arena** (Industrial space station, metallic floor grid, security walls, pillars, crates, tighter covered combat) | **Sundered Rift Arena** (Floating obsidian asteroid void, neon purple anomaly grid, crystal spires, open boss battleground) | **Tactical Rift Beacon Teleportation & Pickups** (Linked interactive beacons with vortex transitions + glowing collectible Rift Energy crystals) |
| **M4: Rendering & Gameplay** | **Multi-Source Dynamic Lighting** (`GL_LIGHT0` directional sun + `GL_LIGHT1` dynamic beacon/projectile point light attenuation) | **Procedural Particle & VFX System** (Teleport vortex, hit sparks, collectible sparkle bursts, alien death shatter, Chrono ripples) | **Chrono Slow Dilation & 2D HUD Loop** (100% gate, 0% reset, 5s 30% time dilation, cool-blue screen overlay, health/chrono/boss bars, score & crosshair) |

---

## ⌨️ Controls & Keybindings

| Key / Input | Action |
|---|---|
| **`W`, `A`, `S`, `D`** | Move Forward / Strafe Left / Move Backward / Strafe Right |
| **Mouse Movement** | Look / Aim (Pitch & Yaw Precision Aim) |
| **Arrow Keys (`←`, `→`, `↑`, `↓`)** | Continuous Smooth Camera Turn & Pitch |
| **Left Click** / **`Space`** | Fire Hitscan Laser Rifle (with Muzzle Flare & Recoil) |
| **`V`** / **`C`** | Toggle First-Person (FPS with Viewmodel) / Third-Person (TPS Rig) |
| **`Q`** | Activate Chrono Slow (Requires 100% Charge) |
| **`F`** | Interact / Activate Rift Beacon Teleportation |
| **`E`** | Evasive Combat Blink Dash |
| **`F11`** | Toggle Fullscreen Mode (Fit Display) |
| **`R`** | Restart Mission (Game Over / Victory screen) |
| **`Esc`** | Exit Game |


---
