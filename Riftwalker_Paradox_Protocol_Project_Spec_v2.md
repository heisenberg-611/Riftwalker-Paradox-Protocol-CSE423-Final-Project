# 1. Project Summary# Riftwalker: Paradox Protocol — CG423 Master Project Specification

**Document status:** Updated after reviewing the semester OpenGL templates and Assignment 3  
**Purpose:** Single source of truth for students, teammates, and AI assistants  
**Course:** Computer Graphics 423 (CG423)  
**Target:** A polished PyOpenGL/GLUT graphics-focused game that is substantially larger than Assignment 3 while remaining manageable for a 4-person student team.

> **IMPORTANT:** The official course starter/OpenGL code supplied by the course is authoritative. This specification describes the target project architecture and feature scope. After the team finalizes the starter framework, the project must be mapped onto its actual functions/files rather than unnecessarily replacing them.

---

## 0. Why This Project Is Larger Than Assignment 3

The supplied Assignment 3 is already a useful foundation. It demonstrates a working 3D game loop with PyOpenGL/GLUT, primitive-based player/enemy rendering, keyboard and mouse callbacks, first-person/third-person camera state, bullets, enemy movement, collisions, life, score, restart/game-over state, and frame-based animation. The Assignment 3 code uses primitive composition for the astronaut and enemy, updates bullets/enemies in an idle callback, and switches camera behavior through `first_person` state. 

The final Riftwalker project should **reuse that mental model** but expand it substantially in graphics depth and game-system breadth.

The intended final project is roughly **3–4× the feature breadth of Assignment 3**, but not 3–4× the code complexity in every subsystem.

### Assignment 3 baseline

Existing baseline concepts we can build on:

- PyOpenGL `GL`, `GLUT`, and `GLU`
- `gluPerspective()` + `gluLookAt()` camera setup
- `glPushMatrix()` / `glPopMatrix()` hierarchical primitive composition
- cubes, cylinders, spheres
- keyboard input
- special-key input
- mouse input
- animation through time / `dt`
- player state
- enemy list
- bullet list
- enemy pursuit
- bullet/enemy collision
- player/enemy collision
- first-person camera flag
- life
- score
- missed bullets
- restart/game-over state

The course examples also establish the simpler 2D/interactive callback style: OpenGL projection setup, display callbacks, idle animation, keyboard listeners, special-key listeners, and mouse listeners.

### Final-project expansion

Riftwalker adds:

1. **Two complete arenas**
2. **Rift Beacon teleportation between arenas**
3. **Blink teleport for combat**
4. **Procedural astronaut with hierarchy**
5. **Reusable procedural alien generator**
6. **Two distinct enemy behaviors**
7. **One multi-phase boss**
8. **First-person and third-person cameras**
9. **Chrono Slow**
10. **Lighting system / scene lighting variation**
11. **Particle/effect system**
12. **Modular procedural environment construction**
13. **Improved collision and ray-based aiming**
14. **HUD with multiple live game values**
15. **Score/rank and complete-game flow**
16. **Optional restrained gravity-zone showcase**
17. **A polished teleport visual transition**

This is intentionally much more than Assignment 3 while remaining centered on CG techniques rather than a giant game engine.

---



### 1.1 High Concept

**Riftwalker: Paradox Protocol** is a small sci-fi combat game in which an astronaut uses an experimental Rift-Chrono suit to fight alien creatures across two arenas. The suit provides two signature abilities:

1. **Rift Teleportation** — teleport between linked Rift Beacons and move between the two arenas.
2. **Chrono Slow** — temporarily slow enemies and enemy projectiles while the player continues at normal speed.

The game supports both **third-person** and **first-person** camera modes.

The game is deliberately scoped for a Computer Graphics course. The priority is approximately:

- **60% graphics / visual systems**
- **40% gameplay / supporting systems**

The project should look technically ambitious while keeping gameplay architecture simple enough for a student team to finish reliably.

---

## 2. FINAL SCOPE LOCK

> **IMPORTANT ARCHITECTURE RULE:** Do not redesign the project around stretch features. Core systems must work using the simpler baseline architecture first. Any AI assistant working on this repository must treat `PROJECT_SPEC.md` as the authoritative scope document and must not introduce removed features unless explicitly requested.

### 2.1 Scope Categorization

#### REQUIRED (Core Baseline Scope):
* **2 Arenas:** Arena 1 (*Kepler Relay*) and Arena 2 (*Sundered Rift*).
* **Linked Rift Beacon Teleportation:** Spatial teleportation between the two arenas via linked beacons (Arena 1 Beacon A $\leftrightarrow$ Arena 2 Beacon B).
* **Dual Camera System:** Dedicated First-Person and Third-Person camera modes with synchronized aiming.
* **Procedural Astronaut Model:** Multi-joint hierarchical modeling with nested transformation matrices.
* **Procedural Alien Models:** Reusable multi-legged/segmented procedural alien generator.
* **Hierarchical Modeling & Animation:** Walking animations, articulated limbs, weapon aiming.
* **Lighting System:** Directional sunlight (`GL_LIGHT0`) and dynamic localized point lights (`GL_LIGHT1` on beacons).
* **Particle Effects:** Teleport vortex swirl, hit sparks, thruster plumes, and death effects.
* **Shooting & Combat:** Hitscan primary weapon with raycast hit detection and projectile system.
* **Collision Detection:** Reusable geometric tests defined in `src/shared/collision.py` (sphere-sphere, ray-box, bounds clamping).
* **2 Enemy Types:** Melee Rift Stalker (rusher) + Ranged Rift Spitter (projectile shooter).
* **1 Boss Encounter:** Multi-phase Rift Guardian with rotating orbital shields and radial attacks.
* **Chrono Slow with Charge Bar:** 5-second 30% enemy time dilation powered by a combat-filled Chrono Charge bar (available only at 100%, resets to 0%).
* **2D HUD:** 2D orthographic overlay displaying Health, Chrono Charge/countdown bar, Score, Objective prompts, and Crosshair.
* **Score & Rank:** Kill scores, multipliers, combo timer, and rank assessment.
* **Basic Level Progression:** Start Menu $\rightarrow$ Arena 1 $\rightarrow$ Beacon Teleport $\rightarrow$ Arena 2 $\rightarrow$ Boss Fight $\rightarrow$ Victory / Game Over $\rightarrow$ Restart.

#### OPTIONAL / STRETCH (Only After MVP Completion):
* **Blink Teleport:** Short-range combat dash/teleport. Must NOT be required for the core project, demo, or grading.
* **One Special Gravity/Wall-Walking Section:** Single predefined low-gravity / jump-pad zone. Core movement remains standard vertical gravity.
* **Additional Visual Polish:** Extra post-processing screen filters, audio effects, destructible debris.

#### REMOVED / DO NOT IMPLEMENT:
* **Full-World Rewind:** No historical state recording buffers or world reversal.
* **Temporal Echo/Past/Future Level System:** No past/future time-clone mechanics.
* **Full 6-DOF Zero-G Flight:** No arbitrary free-floating 6-axis flight mechanics.
* **Arbitrary Gravity Everywhere:** Camera, movement, and collision architecture must NOT depend on arbitrary-gravity support.
* **Inverse Kinematics (IK):** Use forward hierarchical trigonometric joint posing instead.
* **Upgrade Economy / Persistent Currency:** No skill trees, shop systems, or persistent currency.
* **Multiple Bosses:** Scope is strictly locked to exactly one boss (Rift Guardian).
* **Complex Temporal Simulation:** Simple delta-time scaling only.
* **Physically Simulated Wormholes / Real-Time Portals:** Teleportation is a clean transform/scene transition, not optical portal physics.

---

# 3. Game Design

## 3.1 Player Fantasy

The player is an astronaut equipped with a classified **Rift-Chrono Suit**. The suit manipulates spatial position and local time through unstable experimental technology.

The game should communicate this through visuals rather than lengthy narrative systems:

- glowing Rift energy
- short teleport flash
- temporal distortion during Chrono Slow
- futuristic astronaut silhouette
- alien bio-luminescence
- strong lighting contrast

---

## 3.2 Core Gameplay Loop

```text
Start Game
    ↓
Arena 1
    ↓
Fight Aliens
    ↓
Use Blink / Weapon / Chrono Slow
    ↓
Reach Rift Beacon
    ↓
Teleport
    ↓
Arena 2
    ↓
Fight Harder Aliens
    ↓
Boss
    ↓
Final Score / Rank
```

The game should be finishable in a short session and should not require a large amount of progression content.

---

# 4. Arenas

## 4.1 Arena 1 — Kepler Relay

### Theme

A human communications/research station damaged by the first alien breach.

### Visual Identity

- metallic corridors
- modular wall panels
- industrial floors
- cool technical lights
- emergency lights
- cables / vents / structural frames
- occasional broken panels

### Gameplay

- introductory arena
- conventional gravity
- smaller combat areas
- teaches shooting
- teaches teleportation
- introduces Chrono Slow

### Enemies

- melee alien
- ranged alien

### Rift Beacon

One destination beacon should clearly communicate that it connects to Arena 2.

---

## 4.2 Arena 2 — Sundered Rift

### Theme

An alien rift chamber surrounding the source of the spatial anomaly.

### Visual Identity

- large open combat space
- alien architecture
- glowing rift structures
- darker environment
- stronger contrast
- volumetric-looking particles simulated with simple transparent sprites/geometry
- stronger Rift color effects

### Gameplay

- larger combat arena
- more enemy density
- more aggressive ranged enemies
- final boss encounter

### Rift Beacon

The beacon links back to Arena 1 for the teleportation demonstration and provides a natural gameplay anchor.

---

# 5. Rift Beacon Teleportation System — REQUIRED

Spatial teleportation between the two arenas is a **mandatory core feature** of the game and demo.

## 5.1 Design & Linked Beacon Pair

The game defines one bidirectional linked beacon pair:
$$\text{Arena 1: Kepler Relay Beacon A} \longleftrightarrow \text{Arena 2: Sundered Rift Beacon B}$$

```text
Kepler Relay (Arena 1)                          Sundered Rift (Arena 2)
  [Beacon A Platform]                             [Beacon B Platform]
          │                                               │
          └─── Spatial Arena State Transition (Key 'F') ──┘
```

Interacting with / activating Beacon A seamlessly transports the player to Beacon B in Arena 2 (and vice-versa for the return trip).

## 5.2 Teleport Sequence & Execution Pipeline

The teleport sequence is executed as a clean scene/arena state transition:
1. **Trigger Detection:** Player enters the beacon activation radius ($R \le 3.5$) and presses interact (`F`).
2. **Visual Charge:** Beacon rotating torus rings accelerate with intensified cyan point-light emission.
3. **Control Lockout:** Brief input control lockout (approx. 1.8 seconds) to prevent input glitches.
4. **Visual Transition:** Cyan screen flash overlay quad (`GL_BLEND`) and radial vortex particle emitter burst.
5. **Coordinate & State Reset:** Active arena swaps, player coordinates and camera orientation are safely reset to the destination beacon platform spawn offset.
6. **Arrival:** Destination arena geometry renders active, and lingering particle dissipation effects conclude the transition.

## 5.3 Data Model & Constraints

```python
class RiftBeacon:
    beacon_id: str             # e.g., "BEACON_KEPLER_MAIN"
    position: Vector3          # 3D world coordinate
    linked_arena_id: str       # e.g., "ARENA_02_SUNDERED_RIFT"
    activation_radius: float   # 3.5 units
    is_active: bool            # True
```

### Critical Scope Constraints:
* **No Wormhole Physics / Non-Euclidean Portals:** We are **NOT** implementing physically simulated wormholes, stencils, render-to-texture portals, or optical warping.
* **State Transition:** The visual particles and screen flash create the sci-fi illusion, while internally it is an atomic, predictable transform/state transition.
* **Mandatory Status:** Rift Beacon teleportation remains mandatory and grading-critical even if optional features (like Blink) are omitted.

---

# 6. Chrono Slow System

Chrono Slow is the signature time-manipulation feature of the Rift-Chrono suit.

> **Architecture Clarification:** Chrono Slow is strictly a **gameplay delta-time scaling mechanic** (`game_dt = unscaled_dt * CHRONO_SLOW_FACTOR`), **NOT a full world rewind, state buffer, or temporal physics simulation**. Player input, camera systems, and HUD animations operate at full real-time speed (`1.0`), while enemy AI, pathing, animations, and enemy projectiles advance at scaled simulation speed (`0.30`).

## 6.1 Behavior & Speed Factors

When Chrono Slow is active:

- **Player Time Scale:** `1.0` (100% normal speed — full responsiveness in WASD movement, camera look, weapon aiming, and shooting).
- **Enemy Time Scale:** `0.30` (Enemies move, turn, and play attack animations at approximately 30% of normal speed).
- **Enemy Projectiles:** `0.30` (Enemy plasma/acid projectiles travel at 30% speed, allowing the player to dodge effectively).
- **Duration:** Fixed duration of approximately **5 seconds** (`CHRONO_SLOW_DURATION = 5.0`).
- **Visual Presentation:** Cool blue/cyan screen tint overlay and radial distortion particle ripples.

Configurable baseline constants:

```python
CHRONO_SLOW_FACTOR = 0.30       # Enemies and projectiles run at 30% speed
CHRONO_SLOW_DURATION = 5.0      # Active slow duration in seconds
MAX_CHRONO_CHARGE = 100.0       # 100% charge required for activation
```

## 6.2 Chrono Charge Bar & Gameplay Loop

Chrono Slow is governed by an active gameplay-driven **Chrono Charge Bar** on the HUD.

### Rules & Mechanics:
1. **Fills from Gameplay Actions:** The charge bar starts at 0% and does **not** passively auto-regenerate over time. The player must earn charge through active combat:
   - Defeating a Melee Rift Stalker: `+25% Charge`
   - Defeating a Ranged Rift Spitter: `+35% Charge`
   - Damaging the Boss (Rift Guardian) milestone: `+20% Charge`
   - Collecting Rift Energy pickups: `+25% Charge`
2. **100% Activation Requirement:** Chrono Slow **can ONLY be activated when the charge reaches 100%** (`MAX_CHRONO_CHARGE`).
3. **Full Charge Consumption & Reset:** Activating the ability (pressing `Q`) immediately consumes the entire charge and resets the meter to **0%**.
4. **5-Second Countdown:** During the 5-second active window, a timer countdown is displayed on the HUD. Once the 5 seconds expire, world simulation returns to normal speed (`1.0`), and the player must earn charge again through gameplay actions.

```text
Defeat Enemies / Collect Rift Energy
                ↓
    Chrono Charge Bar Fills (0% → 100%)
                ↓
    [100% FULL] → Press 'Q' to Activate
                ↓
    Meter Resets to 0% (Full Consumption)
                ↓
    5-Second Chrono Slow Active (30% Enemy Speed)
                ↓
    Time Returns to Normal Speed (100%)
```

## 6.3 Visual Treatment

While Chrono Slow is active:

- Subtle cool blue/cyan screen tint (`GL_BLEND` transparent quad overlay).
- Enemy motion trails and slowed procedural limb animations.
- Radial particle pulse emitted upon activation.
- Distinct pulsing **"100% READY"** HUD indicator transitioning to a 5.0s active countdown bar.

---

# 7. Player

## 7.1 Controls

Recommended baseline controls:

| Input | Action |
|---|---|
| W | Move forward |
| S | Move backward |
| A | Move left |
| D | Move right |
| Mouse | Look / aim |
| Left Mouse | Fire |
| Space | Jump, if supported by starter framework |
| Shift | Blink / short teleport |
| Q | Chrono Slow |
| V | Toggle first-person / third-person |
| Esc | Pause / quit according to starter framework |

Actual key names may change after the course starter code is provided.

---

## 7.2 Player Representation

The astronaut should be built procedurally from primitive geometry.

### Recommended hierarchy

```text
Astronaut
├── Torso
├── Helmet
│   └── Visor
├── LeftArm
│   ├── UpperArm
│   ├── Forearm
│   └── Hand
├── RightArm
│   ├── UpperArm
│   ├── Forearm
│   └── Hand
├── LeftLeg
│   ├── UpperLeg
│   └── LowerLeg
└── RightLeg
    ├── UpperLeg
    └── LowerLeg
```

Use local coordinate systems and nested transformations.

### Geometry Guidance

- torso: scaled cylinder/capsule-like primitive
- helmet: sphere or UV-style primitive
- visor: flattened transparent/dark primitive or simple material treatment
- limbs: cylinders/capsules
- joints: spheres
- backpack: boxes/cylinders
- weapon: small procedural collection of boxes/cylinders

Do not spend time creating production-quality mesh assets. The point is procedural/hierarchical modeling.

---

# 8. Astronaut Animation

Keep the animation lightweight.

### Required

- walking animation
- idle animation
- shooting pose
- hit reaction, if practical

### Optional

- sprint animation
- teleport reaction
- Chrono activation pose

Do **not** require IK for the baseline.

The weapon arm can use direct rotation toward the aim direction or a simple pose-based approach.

---

# 9. Camera System

Two camera modes share the same underlying player orientation/aim concept.

## 9.1 Third Person

Recommended default.

Characteristics:

- orbital camera behind player
- mouse-controlled yaw/pitch
- adjustable camera distance
- collision avoidance is optional/simple
- shows full astronaut model

## 9.2 First Person

Characteristics:

- camera located near helmet/eye position
- centered aiming
- simplified weapon/viewmodel rendered near camera
- does not render the astronaut head in front of the camera

## 9.3 View Switching

Press `V` to toggle.

Switching cameras must preserve the current view direction so the camera does not visibly snap.

## 9.4 Orientation Rule

Avoid hardcoding world +Z as the camera's only 'up' direction if the final gravity feature allows special gravity.

Preferred conceptual relationship:

```text
Player Orientation
       ↓
   Camera Basis
       ↓
    Aim Ray
```

This keeps the camera, astronaut and weapon coherent.

---

# 10. Aiming and Weapons

## 10.1 Weapon Architecture & Responsibility Split

To ensure clean modularity between graphics presentation and combat math:

* **M1 (Player & Camera) Responsibility:**
  * Astronaut weapon 3D mesh attached to the character's right hand.
  * First-person weapon viewmodel positioning and recoil animation presentation.
  * Camera forward aiming vector calculation.
* **M2 (Enemies & Combat) Responsibility:**
  * Weapon gameplay logic, firing rates, and cooldown timers.
  * Raycast hit detection against enemy bounding volumes.
  * Damage application, projectile pooling, and combat state changes.

## 10.2 Shooting & Aim Abstraction

Shooting is implemented as an accurate 3D hitscan ray from the camera viewpoint:

```text
Aim Origin + Aim Direction (from M1 Camera)
                 ↓
      Raycast Intersection (M2 Math)
                 ↓
   Enemy Hit Detection & Damage Applied
                 ↓
  Hitmarker / Spark Feedback (M4 Renderer)
```

Both first-person and third-person camera modes expose a unified aim vector:

```python
class AimResult:
    origin: Vector3
    direction: Vector3
    hit_enemy: Optional[EnemyBase]
    hit_point: Vector3
    distance: float
```

---

# 11. Blink Teleport — OPTIONAL / STRETCH

> **SCOPE CLARIFICATION:** Blink is an **OPTIONAL / STRETCH** feature. It is **NOT** required for the core project baseline, final demo, or grading-critical delivery. **Rift Beacon teleportation (Section 5) remains mandatory even if Blink is never implemented.**

## 11.1 Blink Behavior (If Implemented)

Short-range evasive directional combat dash:

```text
P_new = P + normalize(forward_aim_direction) * BLINK_DISTANCE
```

* **Constraints:** Must use `src/shared/collision.py` to clamp within arena boundaries and prevent clipping into obstacles.
* **Cooldown & Cost:** Cooldown timer (e.g. 3.0s) and energy cost.

## 11.2 Visual Effect

- Temporary ghost silhouette at origin.
- Quick spark / vortex particle burst.
- Subtle FOV kick or brief screen flash.
- No physics simulation or portal rendering required.

---

# 12. Enemy Design

Only two normal enemy types are required.

## 12.1 Melee Alien — Rift Stalker

Behavior:

1. Detect player.
2. Move toward player.
3. Stop within attack range.
4. Perform simple melee attack.
5. Repeat.

Visual:

- curved spine
- multiple simple limbs
- glowing eyes/bioluminescent nodes
- asymmetrical or slightly insectoid silhouette

## 12.2 Ranged Alien — Rift Spitter

Behavior:

1. Detect player.
2. Maintain distance.
3. Aim toward approximate player position.
4. Fire projectile.
5. Reposition if too close.

Projectile behavior can be simple linear motion.

No advanced pathfinding is required.

---

# 13. Boss — Rift Guardian

One boss only.

## 13.1 Concept

Large alien entity surrounding a Rift core.

### Geometry

Reuse the procedural alien generation approach from normal enemies, but:

- larger scale
- more limbs
- glowing central core
- larger silhouette
- distinctive ring/particle effects

## 13.2 Simple Boss Phases

### Phase 1

- basic melee/ranged attacks
- core exposed

### Phase 2

Triggered at approximately 50% HP:

- faster attacks
- more projectiles
- stronger particle effects
- core partially shielded

No complicated state machine is necessary.

---

# 14. Procedural Alien Generator

This is one of the major graphics-focused components.

## 14.1 Core Idea

Create an alien around a sampled spine curve.

```text
Spine Curve
    ↓
Sample Points
    ↓
Local Frames
    ↓
Cross Sections
    ↓
Body Surface
    ↓
Add Limbs
    ↓
Add Glowing Nodes
```

## 14.2 Parameters

A reusable alien generator should expose values such as:

```text
spine_length
spine_curve_strength
body_radius
limb_count
limb_length
limb_thickness
head_size
glow_node_count
body_scale
```

Different enemies should primarily be parameter variations of the same generator.

## 14.3 Graphics Goal

Demonstrate that procedural geometry can produce multiple visually different creatures without manually modeling every one.

---

# 15. Environment Construction

## 15.1 General Principle

Do not build giant custom worlds.

Use modular procedural pieces.

### Arena 1 Modules

```text
corridor_straight
corridor_corner
room_small
room_large
door_frame
wall_panel
floor_panel
ceiling_panel
beacon_platform
```

### Arena 2 Modules

```text
rift_floor
alien_wall
alien_column
rift_arch
crystal_or_energy_node
boss_platform
beacon_platform
```

The exact naming can be changed to match the existing starter code.

---

# 16. Lighting

Lighting is a major CG423 showcase component.

## 16.1 Arena 1

Use a human-industrial lighting style:

- cool environment fill
- localized bright key lights
- emergency warning lights
- stronger shadows where supported

## 16.2 Arena 2

Use a more dramatic alien lighting style:

- strong Rift key light
- darker surroundings
- high contrast
- glowing emissive-looking geometry
- particle lighting approximation if true dynamic lighting is too expensive

## 16.3 Rule

Prefer a small number of visually meaningful lights over a large number of lights.

---

# 17. Particles / Effects

Particle systems are one of the easiest ways to make the project look significantly more advanced.

## Required Effects

### Rift Beacon

- rotating energy ring
- small orbiting particles
- vertical energy stream

### Blink

- source burst
- destination burst
- ghost trail

### Weapon

- muzzle flash
- impact flash

### Alien Death

- particle burst
- colored energy/ichor particles

### Chrono Slow

- subtle trails
- slow-moving particles
- screen/HUD effect

### Boss

- Rift energy around core
- attack effects
- defeat explosion

Particles should use simple billboarded quads, sprites, points, or other mechanisms supported by the course framework.

---

# 18. Collision System & Shared Utilities

Collision is kept strictly primitive, robust, and geometrically well-defined.

## 18.1 Architecture: Centralized in `src/shared/collision.py`

To prevent fragmented or incompatible collision implementations across the team:

* **Shared Module (`src/shared/collision.py`):** Contains pure **geometric intersection tests** (sphere-sphere, sphere-AABB, ray-sphere, ray-AABB, point containment, and arena boundary clamping).
* **Gameplay Modules Own the Collision Consequences:**
  * **M1 (Player):** Calls shared boundary/obstacle clamping after movement and Blink. Decides player health reduction on damage.
  * **M2 (Combat):** Calls shared ray-sphere / ray-AABB tests for hitscan shots, and sphere-sphere tests for projectiles. Decides enemy damage, knockback, and death.
  * **M3 (World):** Provides arena extents and obstacle bounds to the shared checkers. Handles beacon radius containment triggers.

## 18.2 Bounding Volume Representations

* **Player:** Bounding sphere of radius $R = 1.0$ (centered at player chest/waist).
* **Melee Alien (Rift Stalker):** Bounding sphere of radius $R = 1.2$.
* **Ranged Alien (Rift Spitter):** Bounding sphere of radius $R = 1.4$.
* **Boss (Rift Guardian):** Bounding sphere of radius $R = 3.0$ with rotating shield sub-bounds.
* **Arena Boundaries:** Clamped horizontal extents ($[-X_{\text{bound}}, +X_{\text{bound}}], [-Z_{\text{bound}}, +Z_{\text{bound}}]$) at floor level $Y = 0$.

> **Constraint:** Do not implement a continuous physics simulation engine. Simple geometric intersection tests are authoritative and sufficient.

---

# 19. HUD

Keep the HUD clean, responsive, and informative in both 1st-person and 3rd-person camera modes.

### Required Elements

```text
SUIT INTEGRITY:  [██████████] 100 / 100
CHRONO CHARGE:   [███████░░░] 70%  [READY AT 100% - DEFEAT ENEMIES]
                 (During 5s Slow: [██████░░░░] 3.2s REMAINING)
SCORE:           012500

                       + (Centered Crosshair with Hit Feedback)

>> PRESS 'F' TO RIFT TELEPORT << (When in Beacon Radius)
```

### Chrono Charge Bar Specification
- **Charge State (< 100%):** Renders progress bar from 0% to 100% filled via combat kills and energy pickups. Status text displays percentage and reminds player to defeat enemies.
- **Ready State (= 100%):** Turns glowing bright cyan with animated status text: `[100% READY - PRESS 'Q']`.
- **Active State (Chrono Slow Active):** The 100% charge is consumed; the bar displays a 5.0-second countdown bar with `[CHRONO SLOW ACTIVE: X.Xs REMAINING]`.
- **Post-Effect:** Resets to 0% once the 5 seconds conclude.

### First-person and third-person
The same 2D orthographic overlay (`glOrtho`) is reused across both camera modes. The crosshair remains locked at center screen.

---

# 20. Scoring

Use simple scoring.

## Suggested Formula

```text
Enemy Kill       = +100
Boss Damage      = +50 per damage milestone, if useful
Boss Defeated    = +1000
Arena Completed  = +500
Time Bonus       = optional
```

The final score can map to a rank:

```text
S = excellent
A = very good
B = good
C = completed
D = poor
```

Exact thresholds should be tuned during playtesting.

No upgrade tree or persistent currency is required.

---

# 21. Directory Structure

The directory is intentionally organized so a teammate or AI can immediately see **who owns what**. `M1`–`M4` are team ownership labels, not programming-language requirements.

```text
riftwalker_paradox_protocol/
│
├── README.md
├── PROJECT_SPEC.md
├── CHANGELOG.md
├── TODO.md
├── requirements.txt
│
├── src/
│   ├── main.py                         # M4 — integration entry point
│   │
│   ├── M1_player_camera/
│   │   ├── player.py                   # M1 — player entity coordinator
│   │   ├── astronaut_rig.py            # M1 — hierarchical articulated rig
│   │   ├── player_movement.py          # M1 — WASD movement kinematics
│   │   ├── first_person_camera.py      # M1 — 1st-person FPS camera
│   │   ├── third_person_camera.py      # M1 — 3rd-person follow camera
│   │   ├── player_weapon.py            # M1 — weapon 3D mesh & viewmodel presentation
│   │   └── blink_teleport.py           # M1 — (optional stretch) combat dash
│   │
│   ├── M2_enemies_combat/
│   │   ├── enemy_base.py               # M2 — abstract enemy base
│   │   ├── alien_generator.py          # M2 — procedural alien generator
│   │   ├── melee_rift_stalker.py       # M2 — melee rusher AI
│   │   ├── ranged_rift_spitter.py      # M2 — ranged spitter AI
│   │   ├── rift_guardian_boss.py       # M2 — final boss encounter
│   │   ├── weapon_system.py            # M2 — weapon firing logic & projectiles
│   │   └── raycast.py                  # M2 — raycast hit detection & damage
│   │
│   ├── M3_world_teleport/
│   │   ├── world.py                    # M3 — arena container & state transitions
│   │   ├── arena_base.py               # M3 — abstract arena class
│   │   ├── arena_01_kepler_relay.py    # M3 — Arena 1 Kepler Relay geometry
│   │   ├── arena_02_sundered_rift.py   # M3 — Arena 2 Sundered Rift geometry
│   │   ├── environment_generator.py    # M3 — procedural obstacles/crates/pillars
│   │   ├── rift_beacon.py              # M3 — interactive Rift Beacon platform
│   │   └── gravity_zone.py             # M3 — (optional stretch) special gravity zone
│   │
│   ├── M4_rendering_gameplay/
│   │   ├── renderer.py                 # M4 — master 3D/2D render pipeline
│   │   ├── primitives.py               # M4 — procedural geometry helpers
│   │   ├── lighting.py                 # M4 — directional sunlight & point lights
│   │   ├── materials.py                # M4 — material optical properties
│   │   ├── particles.py                # M4 — vortex, sparks, thruster particles
│   │   ├── effects.py                  # M4 — screen flash & color filters
│   │   ├── chrono_slow.py              # M4 — Chrono Slow manager & countdown
│   │   ├── hud.py                      # M4 — 2D HUD (Health, Chrono bar, Score)
│   │   ├── crosshair.py                # M4 — dynamic crosshair & hitmarkers
│   │   ├── scoring.py                  # M4 — score tracking & multipliers
│   │   ├── game_state.py               # M4 — game state machine
│   │   └── level_manager.py            # M4 — wave spawner & progression
│   │
│   └── shared/
│       ├── constants.py                # Global constants, IDs, speeds, keys
│       ├── math3d.py                   # Vector3, Matrix4, linear algebra
│       ├── collision.py                # Shared geometric collision & raycast utilities
│       ├── input_manager.py            # Centralized keyboard & mouse input state
│       └── game_time.py                # Real-time dt vs. Chrono Slow scaled dt
│
├── scenes/
│   ├── arena_01_kepler_relay/
│   │   ├── scene_notes.md
│   │   ├── layout_notes.md
│   │   ├── spawn_points.md
│   │   └── object_list.md
│   │
│   └── arena_02_sundered_rift/
│       ├── scene_notes.md
│       ├── layout_notes.md
│       ├── spawn_points.md
│       └── object_list.md
│
├── assets/
│   ├── concept_art/
│   │   ├── characters/
│   │   ├── environments/
│   │   ├── enemies/
│   │   ├── teleport/
│   │   └── effects/
│   ├── reference_images/
│   └── generated_images/
│
├── docs/
│   ├── graphics_techniques.md
│   ├── controls.md
│   ├── architecture.md
│   ├── team_tasks.md
│   ├── implementation_notes.md
│   └── integration_audit.md
│
├── tests/
│   ├── test_math3d.py
│   ├── test_collision.py
│   └── test_gameplay_logic.py
│
└── screenshots/
    ├── development/
    └── final/
```

### Ownership rule

- **M1** owns player/camera work.
- **M2** owns aliens/combat.
- **M3** owns arenas/world/teleportation.
- **M4** owns rendering, Chrono Slow, HUD, score, and final integration.
- `shared/` is common infrastructure; changes there must be communicated to everyone.
- `main.py` should stay small and mostly wire systems together.

If the official starter code is monolithic, do **not** force an immediate split into dozens of files. The team may initially keep a smaller number of files while preserving the M1/M2/M3/M4 ownership boundaries in comments and documentation. Refactoring into the target tree can happen after the game works.

# 22. Naming Convention

The project should use names that are self-explanatory when seen out of context.

## Files

Use lowercase `snake_case`.

Good:

```text
rift_beacon.py
first_person_camera.py
alien_generator.py
arena_02_sundered_rift.py
```

Avoid:

```text
rb.py
cam2.py
thing.py
testnew.py
final_final.py
```

## Classes

Use PascalCase.

```python
class RiftBeacon:
class FirstPersonCamera:
class AlienGenerator:
```

## Functions

Use descriptive `snake_case`.

```python
update_player()
spawn_enemy()
activate_rift_beacon()
apply_chrono_slow()
```

## Constants

Use uppercase with underscores.

```python
MAX_PLAYER_HP
CHRONO_SLOW_FACTOR
BLINK_RANGE
TELEPORT_CONTROL_LOCK_TIME
```

## Scene IDs

Use fixed readable IDs:

```text
ARENA_01_KEPLER_RELAY
ARENA_02_SUNDERED_RIFT
```

## Enemy IDs

```text
ENEMY_MELEE_RIFT_STALKER
ENEMY_RANGED_RIFT_SPITTER
BOSS_RIFT_GUARDIAN
```

---

# 23. AI Assistant Context Rules

Any AI assistant working on this project should follow these rules.

## Rule 1 — Read the project specification first

Before editing code, understand:

- current architecture
- current scope
- assigned system
- existing APIs
- OpenGL starter constraints

## Rule 2 — Do not introduce scope creep

Do not spontaneously add:

- new levels
- new enemy classes
- complicated physics
- inventory systems
- save systems
- procedural world generation beyond the required arenas
- multiplayer

unless explicitly requested.

## Rule 3 — Reuse existing infrastructure

When the course starter code already provides:

- camera functions
- primitive drawing
- keyboard input
- mouse input
- lighting
- display lists
- texture loading
- matrix helpers

prefer adapting those systems rather than duplicating them.

## Rule 4 — Keep modules single-purpose

A module called `rift_beacon.py` should manage Rift Beacon logic, not the entire game loop.

## Rule 5 — Do not silently change APIs

If another module already depends on a function or class, preserve its public interface unless the change is intentional and documented.

## Rule 6 — Prefer simple graphics-compatible mathematics

Use understandable vector, matrix, interpolation, ray intersection, and transformation logic rather than unnecessary frameworks.

## Rule 7 — Document non-obvious math

Any non-trivial graphics equation should include a small comment explaining:

- what it computes
- what each variable means
- why the equation is needed

## Rule 8 — Check course constraints before adding libraries

The supplied CG423 OpenGL environment is authoritative.

Do not add external packages simply because they make a feature easier unless the course rules permit them.

---

# 24. Scene Creation Prompts

These prompts are intended for generating concept/reference images. They are **visual references**, not textures or final 3D assets unless explicitly converted later.

When generating images for this project, preserve the same visual language across all scenes.

## 24.1 Global Visual Direction

Use this base context with scene prompts:

> Stylized-realistic sci-fi computer graphics concept art for a university OpenGL game project, clean readable shapes, modular geometric architecture, strong cinematic lighting, moderate detail, practical game-environment design, no text, no logos, no UI, designed so a student can reconstruct the scene procedurally from primitive geometry.

## 24.2 Arena 1 Prompt

> Create a wide game-environment concept image for **Kepler Relay**, a damaged human communications station. Show modular metallic corridors opening into a medium-sized combat room, industrial wall panels, structural beams, vents, cables, floor panels, a clearly visible glowing Rift Beacon, cool artificial overhead lighting, a few emergency red lights, subtle smoke/particles, clean navigable combat space, practical low-to-medium geometric complexity, cinematic perspective, no characters, no UI, no text. The environment must look realistically buildable from boxes, cylinders, planes, and simple procedural modules in OpenGL.

## 24.3 Arena 2 Prompt

> Create a wide game-environment concept image for **Sundered Rift**, an alien Rift chamber. Show a large open combat arena with an angular alien floor, towering organic-mechanical structures, glowing Rift energy veins, a prominent circular Rift Beacon, darker surroundings, dramatic cyan/blue/purple energy lighting, floating particles, a central platform suitable for a boss battle, readable paths and open movement space, moderate geometric complexity, cinematic perspective, no characters, no UI, no text. The environment must be practical to recreate with procedural primitives in OpenGL.

## 24.4 Rift Beacon Prompt

> Design a standalone **Rift Beacon** for the game Riftwalker: Paradox Protocol. A futuristic circular teleportation platform with a thick glowing ring, central spatial distortion, rotating energy bands, small orbiting particles, simple mechanical base, strong emissive-looking energy, sci-fi but geometrically practical, front three-quarter view, clean silhouette, dark neutral background, no text, no UI. Make the design easy to reproduce using torus/ring geometry, cylinders, quads, particles, and simple transformations in OpenGL.

---

# 24A. Scene/Asset Creation Workflow for AI-Generated References

When a new scene or major game element needs visual design, use this procedure.

### A. Create the prompt in `docs/` first

Before generating the image, write a small note containing:

```text
Asset/Scene Name:
Purpose:
Arena:
Approximate dimensions:
Main primitives:
Color/material direction:
Lighting:
Gameplay requirements:
Things that must NOT be included:
```

### B. Generate one concept image

Store the approved image in:

```text
assets/generated_images/
```

Use a clear filename such as:

```text
arena_01_kepler_relay_concept_v01.png
rift_beacon_concept_v02.png
rift_guardian_concept_v01.png
```

### C. Convert the image into implementation notes

The image is not the implementation.

The team should extract:
- primitive shapes
- approximate dimensions
- object positions
- repeated structures
- lighting locations
- particle locations
- gameplay blockers/spawn points

and record these in the corresponding scene folder.

### D. Build from primitives

The final OpenGL scene should remain compatible with the course's primitive/hierarchical modeling style.

### E. Never let generated art silently expand scope

If the generated concept contains dozens of details, choose only the details that matter visually and can be built reliably.

# 25. Character / Object Reference Prompts

## 25.1 Astronaut Prompt

> Design a procedural-friendly sci-fi astronaut for the university OpenGL game **Riftwalker: Paradox Protocol**. Full-body humanoid astronaut wearing a compact experimental Rift-Chrono suit, spherical helmet, dark visor, segmented torso, cylindrical arms and legs, small backpack, compact energy weapon. The body must be composed visually from spheres, cylinders, boxes, and simple capsule-like primitives. Clear articulated joints, readable silhouette, practical proportions, front three-quarter view, neutral background, no text, no UI.

## 25.2 Melee Alien Prompt

> Design a procedural alien enemy called **Rift Stalker** for a university OpenGL graphics project. Build its visual form around a curved central spine, multiple articulated clawed limbs, simple spherical glowing biological nodes, an aggressive but readable silhouette, slightly asymmetric creature anatomy, dark organic body with luminous accents, front three-quarter view, neutral background, no text, no UI. The design must be reconstructable from curves, cylinders, spheres, and repeated transformed limb segments.

## 25.3 Ranged Alien Prompt

> Design a procedural alien enemy called **Rift Spitter** for a university OpenGL project. Creature with a curved spine, fewer but longer limbs, a distinctive glowing mouth/core for ranged attacks, spherical biological nodes, angular organic silhouette, dark body with luminous Rift energy, front three-quarter view, neutral background, no text, no UI. The design should be practical to generate by changing parameters of a reusable procedural creature function.

## 25.4 Boss Prompt

> Design the **Rift Guardian** boss for Riftwalker: Paradox Protocol. A large procedural alien built from a sweeping central spine, many articulated limbs, a massive glowing Rift core, symmetrical energy rings, threatening silhouette, readable weak point at the center, dark alien material with strong luminous accents, standing on a circular Rift platform, cinematic three-quarter view, neutral dark background, no text, no UI. The design must remain practical to approximate with procedural OpenGL primitives.

---

# 26. Effects Reference Prompts

## 26.1 Blink Effect Prompt

> Create a game VFX concept for a short-range astronaut Blink teleport. Show a bright source burst, translucent ghost silhouette where the astronaut started, a sharp spatial streak connecting source and destination, particles expanding outward at both ends, clean sci-fi energy, dark background, centered composition, no UI, no text. Design it so it can be approximated with transparent quads, particles, rings, and simple animated geometry in OpenGL.

## 26.2 Chrono Slow Prompt

> Create a visual-effect concept for **Chrono Slow** in a sci-fi OpenGL game. Show a normal astronaut moving clearly while alien enemies and projectiles appear slowed, subtle ghost trails behind enemies, cool blue temporal distortion, thin circular energy ripples, restrained screen-space feel, cinematic but practical VFX, no UI, no text.

## 26.3 Teleport Transition Prompt

> Create a cinematic gameplay frame showing an astronaut stepping into a glowing Rift Beacon during teleportation. Circular energy ring, spatial distortion, swirling particles, brief white-blue flash, destination-like depth visible through the portal, futuristic space-station environment, readable silhouette, practical game VFX aesthetic, no UI, no text.

---

# 27. Scene Documentation Format

Each arena should have a small `scene_notes.md` describing the scene in a fixed format.

Example:

```markdown
# Arena 01 — Kepler Relay

## Purpose
Introductory combat arena and teleportation tutorial.

## Visual Theme
Industrial human space station.

## Main Geometry
- Corridor modules
- Combat room
- Maintenance room
- Beacon platform

## Lighting
- Cool key
- Neutral fill
- Emergency red accents

## Gameplay Objects
- Player spawn
- Melee enemy spawns
- Ranged enemy spawns
- Rift Beacon
- Arena completion trigger

## Exit Condition
Defeat required enemies and activate the Rift Beacon.

## Graphics Techniques Demonstrated
- Hierarchical modeling
- Primitive composition
- Lighting
- Particle system
- Camera transformations
```

---

# 27A. Four-Member Work Breakdown

Use these labels everywhere in the repository so ownership is obvious.

## M1 — Player & Camera

**Primary responsibility:** astronaut model, movement kinematics, camera systems, weapon visual presentation, and optional Blink.

### Folder
`src/M1_player_camera/`

### Main deliverables
- `player.py` — player entity coordinator and health state
- `astronaut_rig.py` — procedural hierarchical articulated mesh
- `player_movement.py` — WASD movement kinematics and velocity damping
- `first_person_camera.py` — 1st-person FPS camera with viewmodel offset
- `third_person_camera.py` — 3rd-person follow/orbit camera
- `player_weapon.py` — **Weapon Visual Presentation** (astronaut weapon 3D mesh & 1st-person viewmodel presentation)
- `blink_teleport.py` — *(Optional Stretch)* short-range combat dash

### Graphics focus
- hierarchical modeling & matrix stacks (`glPushMatrix`/`glPopMatrix`)
- local transformations & articulated walking animation
- camera/view transformations (`gluLookAt`, `gluPerspective`)
- first-person viewmodel presentation
- procedural astronaut proportions

### Dependencies
M1 consumes:
- `src/shared/math3d.py`, `src/shared/collision.py`, `src/shared/input_manager.py`
- M2 combat hit results
- M3 world collision / beacon destination info
- M4 effects & HUD hooks

---

## M2 — Enemies & Combat

**Primary responsibility:** alien generator, enemy AI, combat gameplay logic, raycasting, hitboxes, projectiles, and boss encounter.

### Folder
`src/M2_enemies_combat/`

### Main deliverables
- `alien_generator.py` — procedural articulated alien generator
- `enemy_base.py` — abstract base enemy class
- `melee_rift_stalker.py` — fast melee rusher AI
- `ranged_rift_spitter.py` — long-range projectile spitter AI
- `rift_guardian_boss.py` — multi-stage boss with rotating orbital shields
- `weapon_system.py` — **Weapon Gameplay Logic** (firing rate, damage, cooldowns, projectile pooling)
- `raycast.py` — precision hitscan raycasting & hitbox intersection math

### Graphics focus
- procedural alien geometry (segmented carapaces, multi-jointed spider legs)
- articulated limb animations
- projectile trajectories and muzzle points
- boss visual hierarchy & rotating shields
- hit/death effects hooks

### Dependencies
M2 consumes:
- `src/shared/collision.py` for geometric tests
- M1 aim vector / player position
- M3 arena bounds & spawn points
- M4 Chrono Slow time scale (`0.30`) & particle hooks

---

## M3 — World, Arenas & Teleportation

**Primary responsibility:** two arenas, environment props, Rift Beacons, and arena-to-arena teleportation state transitions.

### Folder
`src/M3_world_teleport/`

### Main deliverables
- `world.py` — world manager & arena state switcher
- `arena_base.py` — abstract arena container
- `arena_01_kepler_relay.py` — industrial relay station geometry
- `arena_02_sundered_rift.py` — floating asteroid void geometry
- `environment_generator.py` — modular pillars, crates, crystal spires
- `rift_beacon.py` — **Rift Beacon Model & Trigger** (spinning torus rings & glow)
- `gravity_zone.py` — *(Optional Stretch)* special low-gravity jump pad

### Graphics focus
- modular environment construction
- spatial layout & transformation-heavy scene composition
- Rift Beacon geometry and spinning torus animation
- arena-specific lighting hooks
- scene transition effects

### Dependencies
M3 consumes:
- `src/shared/collision.py` for arena boundary extents
- M1 player coordinates
- M2 enemy spawn states
- M4 rendering & particle effects

---

## M4 — Rendering, Chrono, HUD & Integration

**Primary responsibility:** graphics pipeline, lighting, particle systems, Chrono Slow time dilation, 2D HUD, scoring, and full game-loop coordination.

### Folder
`src/M4_rendering_gameplay/`

### Main deliverables
- `renderer.py` — master OpenGL 3D & 2D render pass coordinator
- `primitives.py` — optimized procedural geometry helpers (cubes, cylinders, spheres, toruses)
- `lighting.py` — directional sunlight (`GL_LIGHT0`) & beacon point lights (`GL_LIGHT1`)
- `materials.py` — optical material presets (suit, visor, alien carapace)
- `particles.py` — particle systems (teleport vortex, hit sparks, thrusters)
- `effects.py` — screen flash & visual distortion filters
- `chrono_slow.py` — **Chrono Slow Manager** (100% activation gate, 0% reset, 5s countdown, 0.30 scale)
- `hud.py` — **2D Orthographic HUD** (Health bar, Chrono Charge/countdown bar, Score, Objective text)
- `crosshair.py` — dynamic crosshair with hitmarker feedback
- `scoring.py` — score tracking, kill feed, and combo multipliers
- `game_state.py` — game state machine (`PLAYING`, `TELEPORTING`, `GAME_OVER`, `VICTORY`)
- `level_manager.py` — wave spawning and arena progression

### Graphics focus
- lighting setup & point-light attenuation
- material specular/diffuse properties
- particle systems & alpha blending
- teleport visual vortex transition
- Chrono Slow cool blue screen tint overlay
- 2D orthographic projection matrix switching (`glOrtho`)

### Integration responsibility
M4 coordinates:
- `src/main.py` entry point and GLUT callbacks
- game start / restart flow
- arena transition triggers
- victory / game-over state evaluation
- delta-time distribution (unscaled `real_dt` vs. scaled `game_dt`)

---

## Shared-code Rule (`src/shared/`)

`src/shared/` contains common infrastructure:
- `constants.py`: authoritative constants
- `math3d.py`: Vector3, Matrix4, linear algebra
- `collision.py`: pure geometric tests (sphere-sphere, ray-box, bounds clamping)
- `input_manager.py`: centralized keyboard and mouse state tracking
- `game_time.py`: real-time vs. Chrono Slow scaled delta-time calculation

Nobody should modify `src/shared/` casually. For any shared change:
```text
1. Explain the reason.
2. Identify affected modules.
3. Make the smallest compatible change.
4. Test M1 + M2 + M3 + M4 together.
```

# 28. Implementation Priority & Development Phases

The project follows a strict **9-phase implementation priority order**. Do not attempt stretch features or secondary polish until earlier phases are stable and tested.

```text
Phase 1: Starter-Code Integration + Core Rendering
                    ↓
Phase 2: Player + Camera + Astronaut
                    ↓
Phase 3: Arena 1 + Arena 2
                    ↓
Phase 4: Enemies + Combat + Collision
                    ↓
Phase 5: Rift Beacon Teleportation
                    ↓
Phase 6: Chrono Slow + Charge System
                    ↓
Phase 7: Boss + Scoring + HUD
                    ↓
Phase 8: Particles + Lighting + Visual Polish
                    ↓
Phase 9: Optional Stretch Features (Blink, Gravity Zone)
```

---

## Phase 1 — Starter-Code Integration & Core Rendering
- Audit course starter template and Assignment 3 callbacks.
- Establish OpenGL matrix stack discipline (`glPushMatrix`/`glPopMatrix`).
- Build procedural primitives helper (`primitives.py`) and master render loop (`renderer.py`).
- **Deliverable:** Working graphics sandbox rendering basic geometry at 60 FPS.

---

## Phase 2 — Player, Camera & Procedural Astronaut
- Build articulated hierarchical astronaut model (`astronaut_rig.py`).
- Implement 3rd-person orbit camera and 1st-person FPS camera (`camera.py`).
- Implement WASD movement kinematics and orientation tracking.
- Build astronaut weapon mesh attachment and 1st-person viewmodel presentation.
- **Deliverable:** Controllable astronaut moving smoothly in dual camera modes.

---

## Phase 3 — Arena 1 & Arena 2 Environments
- Construct Arena 1: Kepler Relay metallic platform, walls, and modular props.
- Construct Arena 2: Sundered Rift floating obsidian asteroid and crystal spires.
- Integrate shared collision geometry (`src/shared/collision.py`) for boundary limits.
- **Deliverable:** Both arenas fully constructed and walkable.

---

## Phase 4 — Enemies, Combat & Collision
- Build procedural alien generator (`alien_generator.py`).
- Implement Melee Rift Stalker (rush AI) and Ranged Rift Spitter (plasma projectile AI).
- Implement hitscan raycasting, hitbox detection, damage application, and projectile pooling.
- **Deliverable:** Playable combat loop with responsive enemy engagement and damage.

---

## Phase 5 — Rift Beacon Teleportation (REQUIRED)
- Construct animated Rift Beacon model with spinning concentric torus rings.
- Implement bidirectional beacon link ($\text{Arena 1 Beacon A} \leftrightarrow \text{Arena 2 Beacon B}$).
- Coordinate screen flash, control lockout, coordinate reset, and scene transition.
- **Deliverable:** Mandatory spatial teleportation between Kepler Relay and Sundered Rift.

---

## Phase 6 — Chrono Slow & Charge System (REQUIRED)
- Implement combat-driven Chrono Charge accumulator (earned from kills and pickups).
- Implement 100% activation requirement (`Q` key) with immediate 0% reset.
- Implement 5-second fixed active timer countdown.
- Apply 30% speed scaling (`0.30`) to enemies and projectiles while player runs at 100% speed.
- Apply cool blue screen tint overlay and radial particle pulse.
- **Deliverable:** Locked-down 5-second time dilation mechanic without world rewind.

---

## Phase 7 — Boss Encounter, Scoring & HUD
- Construct Rift Guardian boss model with rotating orbital shields and radial attacks.
- Implement 2D orthographic HUD overlay (Suit Health bar, Chrono Charge/countdown bar, Score, Objective text).
- Implement score manager, combo multipliers, and full game state machine (`PLAYING` $\rightarrow$ `VICTORY` / `GAME_OVER`).
- **Deliverable:** Complete, end-to-end playable game loop.

---

## Phase 8 — Particles, Dynamic Lighting & Visual Polish
- Implement multi-source dynamic lighting (directional sunlight `GL_LIGHT0`, beacon point lights `GL_LIGHT1`).
- Configure specular/diffuse material properties for suits, visors, and alien carapaces.
- Implement particle emitters (teleport vortex, hit sparks, jetpack thrusters).
- **Deliverable:** Polished, visually impressive presentation meeting all CG423 criteria.

---

## Phase 9 — Optional Stretch Features (Post-MVP Only)
- *Optional:* Short-range Blink combat dash (`blink_teleport.py`).
- *Optional:* Predefined low-gravity / jump-pad zone (`gravity_zone.py`).
- *Optional:* Additional post-processing filters and sound effects.
- **Rule:** Only proceed to Phase 9 if Phases 1–8 are 100% complete and fully verified.

---

# 29. Recommended Team Split

Assuming a four-person team:

## Member 1 — Player + Camera

Owns:

- astronaut rig
- player movement
- first-person camera
- third-person camera
- input
- weapon aiming
- Blink

## Member 2 — Enemies + Combat

Owns:

- procedural alien generator
- melee enemy
- ranged enemy
- boss
- enemy collision
- enemy health/attacks

## Member 3 — World + Teleportation

Owns:

- Arena 1
- Arena 2
- modular environment generation
- Rift Beacon
- teleport transitions
- optional simple gravity zone

## Member 4 — Rendering + Gameplay Presentation

Owns:

- lighting
- particles
- materials
- HUD
- score/rank
- effects
- integration testing

### Shared Responsibility

All members should participate in:

- integration
- debugging
- final optimization
- demo preparation
- documentation

No subsystem is considered finished until it works with the rest of the project.

---

# 30. Integration Rules

To avoid merge/integration chaos:

1. Each feature should have a single owning module.
2. Avoid editing the same large file unnecessarily.
3. Every major feature should have a small test scene or test function when possible.
4. Do not hardcode data that belongs in configuration/constants.
5. Keep arena-specific values in arena files where practical.
6. Use readable names for all objects and IDs.
7. After integrating a feature, run the full game before starting another major feature.

---

# 31. Minimum Viable Product

The project is considered functionally complete when all of the following work:

```text
[ ] Game launches
[ ] Player can move
[ ] Third-person camera works
[ ] First-person camera works
[ ] Astronaut is procedurally rendered
[ ] Weapon fires
[ ] Hitscan collision works
[ ] Melee alien works
[ ] Ranged alien works
[ ] Arena 1 works
[ ] Rift Beacon works
[ ] Teleportation to Arena 2 works
[ ] Arena 2 works
[ ] Chrono Slow works
[ ] Boss works
[ ] Player can win
[ ] Score appears
```

Anything beyond this is polish.

---

# 32. Stretch Features — Only After MVP

These are optional and must not delay the minimum viable project:

1. Simple special gravity wall section.
2. Better teleport portal rendering.
3. Additional enemy animation.
4. More elaborate boss particles.
5. Environmental destruction props.
6. Simple audio.
7. Simple post-processing-style visual overlays if supported.
8. More advanced astronaut animation.

Only implement these after all MVP items are stable.

---

# 33. Testing Checklist

## Player

- movement does not drift unexpectedly
- camera does not flip
- first/third-person switch preserves orientation
- player cannot teleport into invalid geometry
- Blink respects collision

## Weapon

- ray points in correct direction
- enemies take damage correctly
- first-person and third-person aim consistently

## Enemies

- enemies detect player
- enemies can attack
- enemies can die
- ranged projectiles interact with player

## Chrono Slow

- player remains responsive at 100% normal speed
- enemy movement slows to ~30% normal speed
- enemy projectile velocity drops to ~30% speed
- charge bar correctly fills exclusively from defeating enemies and picking up Rift energy
- activation is blocked when charge is below 100%
- activating consumes 100% charge, immediately resets bar to 0%, and triggers 5-second duration
- HUD displays remaining active duration countdown
- ability automatically ends after 5.0 seconds and returns world simulation to 100% speed
- confirmed to be delta-time scaling without complex world rewind buffers

## Teleport

- source beacon activates
- destination is correct
- player appears safely
- camera remains stable
- effects reset correctly

## Arenas

- no major holes or unreachable geometry
- player spawns at correct location
- enemies spawn correctly
- beacon links are correct

## Boss

- health decreases
- phase transition works
- boss can be defeated
- game finishes after victory

---

# 34. Graphics Techniques to Emphasize in the Final Report

The final report/presentation should explicitly connect implemented features to computer-graphics concepts.

Recommended topics:

### Transformations

- translation
- rotation
- scaling
- hierarchical model transforms

### Camera

- view transformation
- first-person camera
- orbital camera
- local coordinate frames

### Procedural Modeling

- spine sampling
- cross-sections
- repeated limb placement
- parameterized geometry

### Lighting

- light placement
- material response
- contrast between arenas

### Animation

- hierarchical joint rotation
- time-based transformations

### Collision / Geometry

- ray intersection
- bounding volume tests

### Particle Systems

- position updates
- velocity
- lifetime
- transparency

### Spatial Transformation

- teleportation as a controlled coordinate transformation

### Temporal Transformation

- different delta-time scales for player and enemies

---

# 35. Performance Principles

Because the project is for a course, optimize only where it is understandable and necessary.

Prefer:

- reusing generated geometry
- keeping enemy counts moderate
- limiting particle counts
- reusing primitive geometry
- avoiding unnecessary per-frame allocations
- using the starter framework's existing batching/display-list/mesh utilities when available

Do not spend large amounts of time building advanced optimization systems unless performance actually becomes a problem.

---

# 35A. Exact Making Procedure

This is the recommended order for building the project. Do not build everything simultaneously.

## Step 1 — Freeze the starter baseline

Run the supplied OpenGL starter and Assignment 3.

Record:
- window size
- callbacks
- camera implementation
- primitive helpers
- current global state
- time/update mechanism
- limitations imposed by the course

Create `docs/integration_audit.md`.

**Do not add game features yet.**

---

## Step 2 — Create the project skeleton

Create:

```text
src/M1_player_camera/
src/M2_enemies_combat/
src/M3_world_teleport/
src/M4_rendering_gameplay/
src/shared/
scenes/
assets/
docs/
tests/
```

Copy only the minimum starter code needed to launch the project.

---

## Step 3 — Build a graphics sandbox

Before building the final arenas, create a temporary test scene containing:

- floor
- cubes
- cylinders
- spheres
- astronaut
- one alien
- one light
- camera
- HUD text

This becomes the team's graphics debugging environment.

---

## Step 4 — Build the astronaut first

M1 creates:

1. torso
2. helmet
3. visor
4. arms
5. legs
6. backpack
7. weapon
8. basic idle/walk pose

Each body part uses nested matrix transforms.

Success condition:

> The astronaut can be rendered correctly from multiple camera angles without matrix-state corruption.

---

## Step 5 — Build both cameras

Implement third-person first.

Then add first-person.

The two cameras should use a common player orientation/aim concept.

Success condition:

> Pressing the view toggle changes camera mode without breaking player direction or weapon aiming.

---

## Step 6 — Build Arena 1

Use simple procedural modules first.

Do not decorate heavily.

Build:
- floor
- walls
- two or three rooms
- corridor
- player spawn
- enemy spawn points
- Rift Beacon

Success condition:

> Player can move through the arena and return to the beacon.

---

## Step 7 — Build combat

M2 adds:

- melee enemy
- ranged enemy
- weapon
- raycast/hit detection
- enemy HP
- player HP
- death

Success condition:

> A complete fight is playable inside Arena 1.

---

## Step 8 — Build Arena 2

Reuse world-building utilities from M3.

Give Arena 2:
- distinct geometry
- distinct lighting
- larger combat area
- boss platform
- destination beacon

Success condition:

> Arena 1 and Arena 2 can exist as separate scene states and render correctly.

---

## Step 9 — Add Rift Beacon teleportation

Add:

- activation range
- linked destination
- player position transfer
- orientation transfer
- transition lockout
- particles
- flash/distortion

Success condition:

> Player can visibly teleport from Arena 1 to Arena 2 and arrive correctly.

---

## Step 10 — Add Blink

Blink is a short-distance combat teleport and should remain separate from the arena teleport.

Success condition:

> Player can use Blink without breaking collisions, camera, or arena boundaries.

---

## Step 11 — Add Chrono Slow

Start with the decoupled delta-time simulation logic:

```python
unscaled_dt = real_dt                  # 1.0 for Player, Camera, HUD
game_dt = unscaled_dt * 0.30 if chrono_active else unscaled_dt  # 0.30 for Enemies/Projectiles
```

Then integrate:
- Gameplay charge accumulator (0% to 100% charged from kills and Rift energy)
- 100% activation gate (key `Q`) with immediate 0% reset
- 5.0-second active countdown timer
- Slowed projectile translation and enemy limb animation
- Cool blue screen tint overlay and activation particle pulse
- 2D HUD charge bar and remaining time countdown

Success condition:

> Player remains 100% responsive while enemies and projectiles visibly slow to 30% for exactly 5 seconds, after which time returns to normal.

---

## Step 12 — Add the procedural alien generator

M2 builds one generator with adjustable parameters.

Then create:
- Rift Stalker
- Rift Spitter
- Rift Guardian

Success condition:

> The three enemy designs visibly derive from a shared procedural strategy.

---

## Step 13 — Add lighting and particles

M4 now makes the scenes look finished.

Prioritize:
1. Rift Beacon
2. weapon fire
3. enemy death
4. Blink
5. Chrono Slow
6. boss defeat

---

## Step 14 — Add boss encounter

Keep boss logic simple.

Two phases are enough.

Success condition:

> Player can defeat the boss and reach a clear victory state.

---

## Step 15 — Add HUD, score and rank

Only after gameplay is stable.

---

## Step 16 — Polish

Use remaining time for:
- lighting balance
- particle timing
- camera feel
- animation timing
- visual consistency
- bug fixes

Do not add a new major mechanic during the last polish stage.

# 36. Future OpenGL Starter File Integration

When the supplied CG423 OpenGL file arrives, the next task is **not** to start coding gameplay immediately.

First create an **Integration Audit** containing:

```text
1. Existing file tree
2. Entry point
3. Window/context initialization
4. Main loop
5. Keyboard input
6. Mouse input
7. Camera implementation
8. Projection setup
9. Lighting setup
10. Primitive/model helpers
11. Matrix stack usage
12. Texture handling
13. Collision helpers, if any
14. Existing animation/game state logic
15. Course-specific restrictions
```

Then map the starter code into this document.

Example:

```text
STARTER FUNCTION: setupCamera()
        ↓
USED BY: camera/camera.py

STARTER FUNCTION: keyboardListener()
        ↓
USED BY: core/input_manager.py

STARTER FUNCTION: drawSphere()
        ↓
USED BY: rendering/primitives.py
```

Do not replace working starter functionality without a reason.

---

# 37. Change Management

Update this file whenever one of these changes occurs:

- project scope changes
- file architecture changes
- a major mechanic is removed or added
- starter OpenGL constraints are discovered
- team ownership changes
- scene design changes materially

Minor implementation details do not need to be added here.

Use `CHANGELOG.md` for smaller project-level changes.

---

# 38. Current Project Decision Log

## Decision 01 — Two Arenas

**Status:** Approved

Use two main arenas so teleportation is meaningful and demonstrable.

## Decision 02 — Teleportation

**Status:** Approved

Teleportation remains a headline mechanic.

## Decision 03 — Time Travel

**Status:** Locked Baseline — Chrono Slow

Do not implement full rewind/world reversal or state-history buffers. Represent time manipulation through **Chrono Slow**:
- Active combat charge (0% to 100% filled from kills and Rift energy).
- 100% activation gate with immediate 0% reset.
- 5-second fixed duration.
- 30% enemy and projectile speed scale (`0.30`) with 100% normal player responsiveness (`1.0`).
- Handled under M4 ownership via simple delta-time scaling.

## Decision 04 — Cameras

**Status:** Approved

Support both first-person and third-person modes.

## Decision 05 — Scope Ratio

**Status:** Approved

Target approximately **60% graphics / 40% gameplay**.

## Decision 06 — Gravity

**Status:** Simplified

Keep conventional gravity as the baseline. A small special gravity section may be added only after MVP completion.

## Decision 07 — IK

**Status:** Removed from baseline

Use simpler hierarchical arm posing instead.

# 39. AI Assistant Quick Context & Scope Enforcement Rules

> **AUTHORITATIVE MANDATE FOR AI ASSISTANTS:** Any AI assistant working on this repository must treat `PROJECT_SPEC.md` as the authoritative single source of truth and scope boundary.
> 1. **Scope Boundary:** AI assistants must **NOT** introduce or generate code for removed/out-of-scope features (e.g. world rewind buffers, complex 6-DOF physics, IK, arbitrary gravity, upgrade trees, multiple bosses) unless the user explicitly requests them.
> 2. **Branch Protection & PR Policy:** Direct pushes to `main` are prohibited. All code and asset modifications must be developed within isolated feature branches (`feature/m<module_num>-<feature_name>`) and submitted via Pull Requests targeting `main` only after ensuring all unit tests pass (`python3 -m unittest discover -s tests`).

When giving this document to another AI assistant, the following compact context can be used:

> We are building a CG423 Computer Graphics OpenGL project called **Riftwalker: Paradox Protocol**. It is a manageable sci-fi combat game targeting approximately 60% graphics and 40% gameplay. The player is an astronaut who can move, shoot, use Chrono Slow (5s duration at 30% enemy speed, activated only at 100% combat charge), and switch between first-person and third-person cameras. The game has exactly two baseline arenas: **Kepler Relay** and **Sundered Rift**. Linked Rift Beacons teleport the player between the two arenas as a clean scene state transition. Chrono Slow is a simple delta-time scaling mechanic without world rewind. There are two normal enemies (melee and ranged) and one boss (Rift Guardian). Collision is centralized in `src/shared/collision.py`. Blink and Gravity zones are optional stretch features. The graphics priorities are procedural/hierarchical astronaut modeling, procedural alien generation, lighting, particles, camera transformations, and raycast shooting. Avoid scope creep such as 6-DOF flight, arbitrary gravity systems, IK, upgrade trees, multiple bosses, or full temporal simulation. NEVER push directly to `main`; always use isolated feature branches (`feature/mX-...`) and Pull Requests. The supplied CG423 OpenGL starter code is authoritative and must be integrated rather than unnecessarily replaced.

---

# 39A. Final Feature Matrix

| Area | Assignment 3 Baseline | Riftwalker Final |
|---|---|---|
| Player | Primitive astronaut | Detailed hierarchical astronaut + animation |
| Camera | Basic first/third-person state | Dedicated first/third-person systems |
| Enemy | One simple pursuer | Procedural melee + ranged + boss |
| Combat | Bullet movement/collision | Raycast weapon + enemy/projectile combat |
| World | Flat square arena + walls | Two distinct modular arenas |
| Teleportation | None | Blink + Rift Beacon arena teleport |
| Time | Frame-based update | Chrono Slow with independent enemy time scale |
| Graphics | Primitive composition | Procedural models + lighting + particles + effects |
| HUD | Life/score/missed bullets | HP + Chrono + score + objective/state + crosshair |
| Game flow | Restart/game over | Arena 1 → teleport → Arena 2 → boss → victory/rank |
| Scene variety | One arena | Two visually different arenas |
| Boss | None | One final multi-phase boss |
| Presentation | Functional | Designed visual identity + VFX polish |

This is the intended reason the final project qualifies as a substantial expansion rather than a small modification of Assignment 3.

# 40. Final Principle

The project should feel **larger than it is**.

Achieve this through:

- strong visual design
- procedural modeling
- lighting contrast
- particle effects
- smooth camera transitions
- a convincing Rift teleport sequence
- a polished Chrono Slow effect
- readable enemy silhouettes
- a strong final boss

Do **not** achieve perceived scale by adding many systems.

The safest formula for this project is:

```text
Small number of systems
        +
High visual quality
        +
Clear graphics techniques
        +
Strong integration
        =
Strong CG423 project
```

---

**Document Status:** Baseline project specification  
**Next Required Input:** The official CG423 OpenGL starter/source file  
**Next Step After Starter File:** Perform the Integration Audit and map the real starter architecture onto this specification.
