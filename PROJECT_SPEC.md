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

1. **Two complete arenas with distinct tactical profiles** (Kepler Relay & Sundered Rift)
2. **Structured Wave-Based Combat** (3 escalating waves per arena with defined clear conditions)
3. **Tactical Arena Hazards** (Moving laser barriers, electrified floors, closing bulkheads, rotating energy beams, rift damage zones)
4. **Linked Rift Beacon Teleportation** (Tactical repositioning and escape mechanism; unlocked upon arena wave clearance)
5. **Dynamic Combo Scoring System** (`COMBO x1` to `x4` multiplier with decay window)
6. **Procedural astronaut with hierarchy**
7. **Reusable procedural alien generator**
8. **Two distinct, aggressive enemy behaviors** (Zig-zagging lunging Stalker, strafing projectile Spitter)
9. **One multi-phase boss** (Rift Guardian with rotating shield obelisks)
10. **First-person and third-person cameras** (with synchronized crosshair aiming)
11. **Chrono Slow strategic time dilation** (100% combat charge gate, 5s duration, 30% enemy speed scaling)
12. **Lighting system / scene lighting variation**
13. **Particle/effect system** (Vortex swirls, hit sparks, tracers, death bursts)
14. **Modular procedural environment construction**
15. **Centralized 3D collision resolution and ray-based aiming**
16. **2D Orthographic HUD with live wave objectives, combo meter, cooldown bar, and boss status**
17. **Score/rank and complete-game flow**
18. **Optional restrained gravity-zone showcase**
19. **A polished teleport visual transition**

This is intentionally much more challenging and engaging than Assignment 3 while remaining centered on CG techniques (60% graphics / 40% gameplay) rather than a giant game engine.

---

### 1.1 High Concept

**Riftwalker: Paradox Protocol** is a fast-paced sci-fi combat arena game in which an astronaut uses an experimental Rift-Chrono suit to survive waves of aggressive alien invaders and navigate hazardous environments across two interconnected arenas. The suit provides two signature abilities:

1. **Rift Teleportation** — tactical teleportation between linked Rift Beacons to transition between arenas and escape overwhelming swarms once arena waves are cleared.
2. **Chrono Slow** — a strategic 5-second 30% time dilation ability earned through combat kills to survive intense enemy encounters and dodge hazardous traps.

The game supports both **third-person** and **first-person** camera modes.

The game is deliberately scoped for a Computer Graphics course. The priority is approximately:

- **60% graphics / visual systems**
- **40% gameplay / supporting systems**

The project delivers intense, engaging combat and challenging hazards while keeping the architecture simple and robust for a 4-person student team.

---

## 2. FINAL SCOPE LOCK

> **IMPORTANT ARCHITECTURE RULE:** Do not redesign the project around stretch features. Core systems must work using the simpler baseline architecture first. Any AI assistant working on this repository must treat `PROJECT_SPEC.md` as the authoritative scope document and must not introduce removed features unless explicitly requested.

### 2.1 Scope Categorization

#### REQUIRED (Core Baseline Scope):
* **2 Arenas:** Arena 1 (*Kepler Relay*) and Arena 2 (*Sundered Rift*) with distinct combat layouts and tactical characteristics.
* **Wave-Based Combat (NEW REQUIRED):** Structured combat waves (3 waves per arena) with defined completion conditions. Rift Beacons remain locked until arena waves are cleared.
* **Tactical Arena Hazards (NEW REQUIRED):** Dynamic environmental traps forcing player movement:
  - *Kepler Relay:* Moving laser barrier, electrified floor zone, temporary closing/opening bulkhead doors.
  - *Sundered Rift:* Rift energy damage zone, rotating energy beam, unstable/falling platform area.
* **Tactical Rift Beacon Teleportation (NEW REQUIRED):** Spatial teleportation between arenas via linked beacons (Arena 1 Beacon A $\leftrightarrow$ Arena 2 Beacon B) serving as arena transition and tactical repositioning.
* **Combo Scoring System (NEW REQUIRED):** Dynamic kill-chain multiplier (`COMBO x1` to `x4`) rewarding rapid consecutive kills with configurable time decay.
* **Dual Camera System:** Dedicated First-Person and Third-Person (over-the-shoulder) camera modes with synchronized crosshair aiming.
* **Procedural Astronaut Model:** Multi-joint hierarchical modeling with nested transformation matrices.
* **Procedural Alien Models:** Reusable multi-legged/segmented procedural alien generator.
* **Hierarchical Modeling & Animation:** Walking animations, articulated limbs, weapon aiming.
* **Lighting System:** Directional sunlight (`GL_LIGHT0`) and dynamic localized point lights (`GL_LIGHT1` on beacons/hazards).
* **Particle Effects:** Teleport vortex swirl, hit sparks, dual-pass laser tracers, thruster plumes, and death effects.
* **Shooting & Combat:** Hitscan primary weapon with raycast hit detection, visual muzzle alignment, and projectile system.
* **Collision Detection & Obstacle Resolution:** Reusable geometric tests and sliding push-out physics defined in `src/shared/collision.py` (cylinder pillars, AABB crates, hazard triggers, boundary clamping).
* **2 Dangerous Enemy Types:** Melee Rift Stalker (fast pursuit, zig-zag pathing, melee lunge) + Ranged Rift Spitter (strafing standoff AI, projectile volley).
* **1 Boss Encounter:** Multi-phase Rift Guardian with rotating orbital shield obelisks and radial energy shockwaves.
* **Chrono Slow with Charge Bar:** 5-second 30% enemy time dilation powered by a combat-filled Chrono Charge bar (available only at 100%, resets to 0%).
* **2D Orthographic HUD:** Overlay displaying Health, Chrono Charge/countdown bar, Weapon Cooldown bar, live Wave Objectives, Remaining Enemies counter, Combo Multiplier meter, Boss Health Bar with Phase indicator, and Crosshair.
* **Score & Rank:** Kill scores, combo multipliers, hazard penalties, and final rank assessment (S/A/B/C/D).
* **Structured Level Progression:** Start Menu / Story Intro $\rightarrow$ Arena 1 (Waves 1–3) $\rightarrow$ Beacon Unlock $\rightarrow$ Teleportation $\rightarrow$ Arena 2 (Waves 1–3) $\rightarrow$ Boss Fight (Phases 1 & 2) $\rightarrow$ Victory / Game Over $\rightarrow$ Restart.

#### OPTIONAL / STRETCH (Only After MVP Completion):
* **Blink Teleport:** Short-range combat dash/teleport (`E` key). Must NOT be required for the core project, demo, or grading.
* **One Special Gravity/Wall-Walking Section:** Single predefined low-gravity / jump-pad zone. Core movement remains standard vertical gravity.
* **Additional Visual Polish:** Extra post-processing screen filters, audio effects, destructible debris.

#### REMOVED / DO NOT IMPLEMENT:
* **Full-World Rewind:** No historical state recording buffers or world reversal.
* **Temporal Echo/Past/Future Level System:** No past/future time-clone mechanics.
* **Full 6-DOF Zero-G Flight:** No arbitrary free-floating 6-axis flight mechanics.
* **Arbitrary Gravity Everywhere:** Camera, movement, and collision architecture must NOT depend on arbitrary-gravity support.
* **Inverse Kinematics (IK):** Use forward hierarchical trigonometric joint posing instead.
* **Upgrade Economy / Persistent Currency / Skill Trees:** No inventory, equipment shops, or character stats.
* **Multiple Bosses:** Scope is strictly locked to exactly one boss (Rift Guardian).
* **Complex Physics Simulation:** Simple geometric trigger checks and obstacle sliding only; no rigid-body dynamics engine.
* **Physically Simulated Wormholes / Real-Time Portals:** Teleportation is a clean transform/scene transition, not optical portal physics.

---

# 3. Game Design

## 3.1 Player Fantasy

The player is an elite astronaut equipped with an experimental **Rift-Chrono Combat Suit**. Trapped behind enemy lines in an active spatial breach, the player must outmaneuver swarms of crystalline void predators, evade hazardous station traps, and leverage time manipulation and teleportation to eliminate the Rift Guardian boss.

Visual storytelling cues:
- Glowing cyan/violet Rift energy conduits and hazard indicators
- Instantaneous screen flash and vortex swirl during teleportation
- Cool-blue chromatic overlay and slowed audio/motion during Chrono Slow
- Detailed astronaut rig with articulated arms tracking weapon aim
- Bioluminescent crystalline alien silhouettes and glowing weak-point cores
- High-contrast sci-fi industrial and cosmic void lighting

---

## 3.2 Master Gameplay Loop

```text
Start / Story Intro
        ↓
Arena 1: Kepler Relay
        ↓
     Wave 1 (3 Stalkers)
        ↓
     Wave 2 (2 Stalkers + 2 Spitters + Hazards)
        ↓
     Wave 3 (3 Stalkers + 2 Spitters + Active Hazards)
        ↓
Arena 1 Cleared → Rift Beacon Unlocked & Online
        ↓
Rift Teleport (Press 'F' at Beacon)
        ↓
Arena 2: Sundered Rift
        ↓
     Wave 1 (3 Stalkers + 2 Spitters)
        ↓
     Wave 2 (4 Stalkers + 3 Spitters + Void Hazards)
        ↓
     Wave 3 (2 Stalkers + 4 Spitters + Rotating Beams)
        ↓
Arena 2 Waves Cleared → Boss Breach
        ↓
Rift Guardian Boss Encounter
        ↓
     Phase 1 (Rotating Orbital Shield Obelisks)
        ↓
     Phase 2 (HP ≤ 50% - Rapid Rotation & Radial Shockwaves)
        ↓
Victory Screen & Final Rank Evaluation (S/A/B/C/D)
```

### In-Wave Tactical Micro-Loop

```text
Move & Strafe (WASD)
        ↓
Evade Hazards (Laser barriers, electrified zones, energy beams)
        ↓
Aim & Fire Laser Rifle (Crosshair-aligned raycast)
        ↓
Maintain Distance / Dodge Stalker Lunges & Spitter Projectiles
        ↓
Earn Chrono Charge & Build Combo Multiplier (Quick consecutive kills)
        ↓
Activate Chrono Slow (At 100% Charge) to survive lethal swarms
        ↓
Clear Wave → Transition to Next Wave or Unlock Rift Beacon
```

---

# 4. Arenas & Tactical Hazards

## 4.1 Arena 1 — Kepler Relay

### Theme & Tactical Profile
A damaged industrial space station communications outpost.
- **Combat Characteristics:** Smaller interior spaces, tight corridors, extensive structural cover (pillars, crates).
- **Tactical Advantage:** Excellent cover for breaking line-of-sight against ranged Spitters.
- **Tactical Danger:** High risk in close quarters against fast melee Stalkers.
- **Bounds:** Rectangular metallic deck ($[-28, +28] \times [-28, +28]$).

### Wave Structure (Kepler Relay)
* **Wave 1 — Initial Breach:** 3 Melee Rift Stalkers. (Teaches movement, hip-fire aiming, and melee evasion).
* **Wave 2 — Combined Assault:** 2 Rift Stalkers + 2 Rift Spitters. (Introduces ranged projectile dodging and cover usage).
* **Wave 3 — Station Overrun:** 3 Rift Stalkers + 2 Rift Spitters with active hazards. (Demands combo building and Chrono Slow usage).

### Tactical Arena Hazards (Kepler Relay — REQUIRED)
1. **Moving Laser Barrier:**
   - *Visual:* Neon-red horizontal laser beam oscillating between two structural pillars.
   - *Logic:* Moves back and forth along an axis ($Z$ or $X$). AABB/line trigger check.
   - *Effect:* Deals 15 damage and applies a brief 0.5s movement slow if touched. Cooldown: 1.0s.
2. **Electrified Floor Zone:**
   - *Visual:* Pulsing yellow-orange warning grid on floor panel section.
   - *Logic:* Activates periodically (3.0s active, 3.0s safe). Bounding box trigger.
   - *Effect:* Deals 8 damage per tick while standing inside the active electrified grid.
3. **Closing/Opening Security Bulkhead Door:**
   - *Visual:* Heavy metal door frame that periodically opens and closes across a corridor choke point.
   - *Logic:* Cyclic vertical motion. Solid AABB collision when closed, passable when open.
   - *Effect:* Blocks player and enemy movement/sightlines, dynamically altering escape routes.

---

## 4.2 Arena 2 — Sundered Rift

### Theme & Tactical Profile
A shattered cosmic asteroid plateau suspended over a dimensional abyss.
- **Combat Characteristics:** Vast open arena with towering floating crystal spires and long sightlines.
- **Tactical Advantage:** Wide maneuvering room, clear visibility, easy to track enemy positions.
- **Tactical Danger:** Sparse cover makes the player vulnerable to crossfire from multiple ranged Spitters.
- **Bounds:** Cosmic obsidian plateau ($[-35, +35] \times [-35, +35]$).

### Wave Structure (Sundered Rift)
* **Wave 1 — Void Vanguard:** 3 Rift Stalkers + 2 Rift Spitters. (Introduces open-field kite tactics).
* **Wave 2 — Swarm Surge:** 4 Rift Stalkers + 3 Rift Spitters + active void hazards. (High-density swarm requiring Chrono Slow).
* **Wave 3 — Elite Cadre:** 2 Rift Stalkers + 4 Rift Spitters + rotating energy beams. (Heavy ranged projectile barrages).
* **Boss Encounter — Rift Guardian:** Multi-phase boss fight with rotating orbital shields and radial shockwaves.

### Tactical Arena Hazards (Sundered Rift — REQUIRED)
1. **Rift Energy Damage Zone:**
   - *Visual:* Swirling pool of violet void particles and dark energy crackles on the arena floor.
   - *Logic:* Static circular trigger zone ($R = 4.0$).
   - *Effect:* Deals 12 damage per second and rapidly drains suit integrity if traversed.
2. **Rotating Energy Beam:**
   - *Visual:* High-intensity cyan laser beam radiating from a central spire and sweeping 360° across the arena.
   - *Logic:* Continuous angular rotation (`angle += rotation_speed * dt`). Radial ray-cylinder collision test.
   - *Effect:* Deals 20 damage and knocks the player back. Encourages timed movement and jump/dash timing.
3. **Unstable Platform Area:**
   - *Visual:* Floating obsidian rock slab with glowing stress fractures.
   - *Logic:* Steps onto platform $\rightarrow$ 1.5s warning flash $\rightarrow$ platform collapses/disables collision for 3.0s before respawning.
   - *Effect:* Forces player to stay mobile and avoid cornering themselves on unstable ground.

---

## 4.3 Hazard Architecture & Collision Logic

Hazards are designed to be **mechanically lightweight and computationally robust**:

```text
Player position (x, y, z) + radius
        ↓
Check against Hazard Trigger Volumes (AABB / Sphere / Radial Ray)
        ↓
Is Hazard currently in Active State?
   ├─ No  → Ignore
   └─ Yes → Apply damage to Player HP + Spawn Hazard Sparks + Trigger brief invulnerability cooldown (0.8s)
```

> **Constraint:** Hazards use simple geometric intersection tests in `src/shared/collision.py` or arena classes. No continuous rigid-body physics engine is required.

---

# 5. Rift Beacon Teleportation System — REQUIRED

Spatial teleportation between the two arenas is a **mandatory core feature** of the game and demo.

## 5.1 Tactical Beacon Design & Lock State

The game defines one bidirectional linked beacon pair:
$$\text{Arena 1: Kepler Relay Beacon A} \longleftrightarrow \text{Arena 2: Sundered Rift Beacon B}$$

```text
Kepler Relay (Arena 1)                          Sundered Rift (Arena 2)
  [Beacon A Platform]                             [Beacon B Platform]
          │                                               │
          └─── Spatial Arena State Transition (Key 'F') ──┘
```

### Tactical Gameplay Rules:
1. **Wave Lockout:** While active waves are spawning or enemies remain alive, the Rift Beacon is **LOCKED** (rings rotate slowly in amber standby mode, HUD indicates beacon offline).
2. **Wave Clear Unlock:** Upon defeating the final enemy of Wave 3 in an arena, the Beacon **ACTIVATES** (rings spin rapidly with bright cyan energy glow, HUD displays `ARENA CLEARED - RIFT BEACON ONLINE - PRESS 'F' TO TELEPORT`).
3. **Tactical Repositioning:** Once unlocked, the beacon serves as a spatial conduit between arenas, allowing the player to transition between environments or strategically reposition.

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
    is_unlocked: bool          # Set to True once arena waves are cleared
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

# 12. Enemy Design (Crystalline Void Horrors)

The dimensional invaders are designed as **Crystalline Void Horrors** — otherworldly entities composed of floating obsidian shards, sharp geometric facets, and glowing cyan/violet rift fissure nodes rather than generic earthly bugs. Only two normal enemy types are required, each featuring dangerous tactical combat behaviors.

## 12.1 Melee Alien — Rift Stalker

A swift, predatory quadrupedal horror that closes the gap aggressively:

**Tactical Behaviors & Combat AI:**
1. **Aggressive Pursuit:** Moves at high velocity ($6.5\text{–}8.5\text{ units/sec}$) directly tracking player position.
2. **Sinusoidal Zig-Zag Evasion:** Alternates lateral velocity perpendicular to line of sight while charging, making straight hitscan shots harder to land.
3. **Melee Lunge Burst:** When closing into short range ($R \le 4.5\text{ units}$), accelerates forward in a rapid lunging leap with slashing scythe animations.
4. **Slash Strike & Cooldown:** Deals 20 damage on contact ($R \le 1.8$), then pauses briefly (0.8s attack cooldown) before resuming pursuit.

**Visual Aesthetic (M2 Deliverable):**
- Sharp angular obsidian carapace plates.
- Glowing cyan/purple rift energy core visible through rib fissures.
- Articulated crystalline bladed front limbs with animated lunging transformations.
- Menacing multi-eyed bioluminescent cluster.

---

## 12.2 Ranged Alien — Rift Spitter

A hovering dimensional prism monolith that controls space through ranged projectile barrages:

**Tactical Behaviors & Combat AI:**
1. **Standoff Range Regulation:** Actively maintains a safe engagement distance ($15.0 \le R \le 22.0\text{ units}$) from the player.
2. **Perpendicular Strafing:** Constantly strafes clockwise/counter-clockwise around the player to avoid incoming fire.
3. **Repositioning:** If the player charges into close quarters ($R < 10.0$), the Spitter immediately retreats backwards to re-establish standoff range.
4. **Targeted Projectile Volley:** Charges its core (accelerating shard ring spin) and fires high-velocity plasma bolts directly toward the player's predicted position.
5. **Wave Speed Scaling:** Projectile travel speed increases moderately in later waves ($14\text{ u/s}$ in Wave 2 $\rightarrow$ $18\text{ u/s}$ in Wave 3), making Chrono Slow essential for dodging.

**Visual Aesthetic (M2 Deliverable):**
- Floating dimensional crystal prism/monolith.
- Orbital rotating shard rings (`glRotatef`) that spin faster during attack windup.
- Glowing pulsing plasma eye/emitter.
- No ground legs (pure hovering dimensional entity).

---

# 13. Boss — Rift Guardian

One final boss encounter only.

## 13.1 Design & Phase Mechanics

The **Rift Guardian** is a colossal dimensional nexus entity:
- **Phase 1:** Core protected by 4 rotating orbital shield obelisks. Direct shots to shields deal reduced damage. Fires alternating plasma bursts.
- **Phase 2 (HP $\le 50\%$):** Shield plates expand and rotate rapidly, unleashing radial shockwave bursts and aggressive arena-wide energy discharges.

**Visual Aesthetic (M2 Deliverable):**
- Massive pulsating central obsidian polyhedron core.
- Floating independent orbiting shield obelisks with distinct transformation hierarchies.
- Dynamic point-light emission and glowing dimensional runes.

---

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

# 19. HUD & Objective Communication

Keep the HUD clean, responsive, and informative in both 1st-person and 3rd-person camera modes.

### 2D Orthographic HUD Layout

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ SCORE: 014500  [COMBO x3 ■■■■░░ (2.1s)]           CAMERA: 3rd Person [V] │
│                                                                          │
│                 RIFT GUARDIAN [PHASE 1]: 850/1000                        │
│                 [████████████████████░░░░░░]                             │
│                                                                          │
│                                                                          │
│                       OBJECTIVE: Clear Wave 2                            │
│                         ENEMIES REMAINING: 3                             │
│                                                                          │
│                                  +                                       │
│                                                                          │
│                 >> PRESS 'F' TO RIFT TELEPORT <<                         │
│                                                                          │
│ SUIT INTEGRITY:  [██████████] 85 / 100                                   │
│ CHRONO CHARGE:   [███████░░░] 70%  [READY AT 100% - DEFEAT ENEMIES]      │
│                  (Active: [██████░░░░] 3.2s REMAINING)                   │
│ LASER RIFLE:     [██████████] READY [CLICK / SPACE]                      │
└──────────────────────────────────────────────────────────────────────────┘
```

### HUD Components & State Feedback

1. **Suit Integrity (Bottom Left):**
   - Green-to-red horizontal health bar ($0\text{--}100\text{ HP}$).
   - Status text: `SUIT INTEGRITY: [HP]/100`.

2. **Chrono Charge Bar (Bottom Left):**
   - **Charging (< 100%):** Cyan-blue bar filling from kills and pickups with percentage read-out.
   - **Ready (= 100%):** Glowing cyan bar with pulsing text: `CHRONO CHARGE: [100% READY - PRESS 'Q']`.
   - **Active (5s Duration):** Cyan countdown bar with `CHRONO SLOW: X.Xs REMAINING`.
   - **Post-Slow:** Automatically resets to 0%.

3. **Laser Rifle Cycling Cooldown Bar (Bottom Left):**
   - Renders real-time weapon cycling state ($0.0\text{--}1.0$).
   - Bright cyan `[READY - CLICK / SPACE]` when ready to fire; amber fill bar `RIFLE CYCLING: XX%` during cooldown.

4. **Live Wave Objectives & Status Banners (Center / Upper-Center):**
   - Active Wave: `OBJECTIVE: Clear Wave X` and `ENEMIES REMAINING: N`.
   - Wave Transition: `WAVE CLEARED - NEXT WAVE IN 2.0s`.
   - Arena Clearance: `ARENA CLEARED - RIFT BEACON ONLINE - PRESS 'F' TO TELEPORT`.

5. **Combo Multiplier Meter (Top Left):**
   - Displays current multiplier badge: `COMBO x1`, `COMBO x2`, `COMBO x3`, `COMBO x4`.
   - Includes horizontal decaying timer bar indicating remaining window before reset.

6. **Boss Health Bar & Phase Indicator (Top Center):**
   - Active during the Rift Guardian boss fight.
   - Renders health bar with phase text: `RIFT GUARDIAN [PHASE 1 / PHASE 2]: [HP]/[MaxHP]`.

7. **Crosshair & Hitmarkers (Center Screen):**
   - Centered 2D crosshair with dynamic red hitmarker flares on successful hits.

8. **End-Game Overlay:**
   - `GAME OVER` with red banner and `Press 'R' to Restart Mission`.
   - `MISSION ACCOMPLISHED!` with green victory banner and final rank evaluation.

---

# 20. Scoring & Combo Multiplier System — REQUIRED

The scoring system actively rewards aggressive, fast-paced play through a **time-sensitive combo chain**.

## 20.1 Score Calculation Formula

$$\text{Total Score} = \sum (\text{Base Kill Score} \times \text{Combo Multiplier}) + \text{Bonuses} - \text{Hazard Penalties}$$

### Base Score Values:
* **Melee Rift Stalker Kill:** $+100\text{ pts}$
* **Ranged Rift Spitter Kill:** $+150\text{ pts}$
* **Wave Clearance Bonus:** $+300\text{ pts}$ (Wave 1), $+500\text{ pts}$ (Wave 2), $+800\text{ pts}$ (Wave 3)
* **Boss Phase 1 Milestone:** $+500\text{ pts}$
* **Boss Defeated:** $+2000\text{ pts}$
* **Arena Completion Bonus:** $+1000\text{ pts}$

## 20.2 Combo Multiplier Mechanics

```text
Kill Enemy 1 (COMBO x1)
       │ (Kill within 3.5s window)
       ▼
Kill Enemy 2 (COMBO x2)
       │ (Kill within 3.5s window)
       ▼
Kill Enemy 3 (COMBO x3)
       │ (Kill within 3.5s window)
       ▼
Kill Enemy 4+ (COMBO x4 — Maximum Multiplier)
```

* **Combo Window Duration:** $3.5\text{ seconds}$ (`COMBO_TIMEOUT = 3.5`).
* **Multiplier Scaling:**
  - 1 kill: $\times 1$
  - 2 consecutive kills: $\times 2$
  - 3 consecutive kills: $\times 3$
  - 4+ consecutive kills: $\times 4$ (Max cap)
* **Decay Rule:** If no enemy is killed within the 3.5-second window, the combo timer expires and multiplier resets to $\times 1$.
* **Damage Penalty:** Taking damage from enemy attacks or arena hazards reduces the active combo multiplier by 1 step.

## 20.3 Performance Ranks

The final end-game score maps directly to an operational performance rank:

* **Rank S (Elite Riftwalker):** $\ge 12,000\text{ pts}$ (Fast clears, sustained $\times 3/\times 4$ combos, minimal hazard hits)
* **Rank A (Senior Operative):** $9,000\text{ -- }11,999\text{ pts}$
* **Rank B (Field Agent):** $6,500\text{ -- }8,999\text{ pts}$
* **Rank C (Survivor):** $4,000\text{ -- }6,499\text{ pts}$
* **Rank D (Compromised):** $< 4,000\text{ pts}$

> **Constraint:** No persistent currency, skill trees, or RPG stat upgrades are required. Scoring is purely performance-based and resets each run.

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
├── assets/
│   └── textures/
│       ├── environment/
│       │   ├── kepler_metal_wall.png
│       │   ├── kepler_floor_panel.png
│       │   ├── kepler_warning_panel.png
│       │   ├── kepler_pipe_metal.png
│       │   ├── sundered_rock.png
│       │   ├── sundered_crystal.png
│       │   └── alien_structure.png
│       ├── characters/
│       │   ├── astronaut_suit.png
│       │   ├── astronaut_visor.png
│       │   ├── rift_stalker_body.png
│       │   ├── rift_spitter_body.png
│       │   └── rift_guardian_core.png
│       ├── weapons/
│       │   └── plasma_rifle.png
│       ├── rift/
│       │   ├── rift_energy.png
│       │   └── beacon_runes.png
│       └── background/
│           └── space_background.png
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
│   │   ├── primitives.py               # M4 — procedural & textured geometry helpers
│   │   ├── lighting.py                 # M4 — directional sunlight & point lights
│   │   ├── materials.py                # M4 — material optical & texture properties
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
│       ├── texture_loader.py           # Shared PIL/OpenGL texture loader & caching manager
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

These prompts are intended for generating concept/reference images. They are **visual references and texture-ready assets** conforming strictly to standard OpenGL-compatible image formats.

When generating images for this project, preserve the same visual language across all scenes.

## 24.0 Image Format & OpenGL Compatibility Standards

All reference, concept, and potential texture images MUST adhere to the following OpenGL-compliant specifications:
* **Image Format:** Standard lossless **PNG (`.png`)** with 24-bit RGB or 32-bit RGBA color channels.
* **OpenGL Texture Pipeline:** Decodable via Python Pillow/PIL into raw byte arrays for `glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)`.
* **Aspect Ratios:**
  - **Environment / Arena Scenes:** `16:9` widescreen (`1920x1080` or `1280x720`).
  - **Characters / Aliens / Beacons / Props:** `1:1` square (`1024x1024` or `512x512`).
  - **Effects / VFX Frames:** `16:9` widescreen.
* **Storage Location:** `assets/generated_images/<filename>.png`.

## 24.1 Global Visual Direction

Use this base context with scene prompts:

> Stylized-realistic sci-fi computer graphics concept art for a university OpenGL game project, clean readable shapes, modular geometric architecture, strong cinematic lighting, moderate detail, practical game-environment design, no text, no logos, no UI, designed so a student can reconstruct the scene procedurally from primitive geometry.

## 24.2 Arena 1 Prompt (Kepler Relay)
* **Format:** `PNG (.png)` | **Aspect Ratio:** `16:9` | **Target:** `assets/generated_images/arena_01_kepler_relay_concept_v01.png`

> Create a wide game-environment concept image in PNG format for **Kepler Relay**, a damaged human communications station. Show modular metallic corridors opening into a medium-sized combat room, industrial wall panels, structural beams, vents, cables, floor panels, a clearly visible glowing Rift Beacon, cool artificial overhead lighting, a few emergency red lights, subtle smoke/particles, clean navigable combat space, practical low-to-medium geometric complexity, cinematic perspective, no characters, no UI, no text. The environment must look realistically buildable from boxes, cylinders, planes, and simple procedural modules in OpenGL.

## 24.3 Arena 2 Prompt (Sundered Rift)
* **Format:** `PNG (.png)` | **Aspect Ratio:** `16:9` | **Target:** `assets/generated_images/arena_02_sundered_rift_concept_v01.png`

> Create a wide game-environment concept image in PNG format for **Sundered Rift**, an alien Rift chamber. Show a large open combat arena with an angular alien floor, towering organic-mechanical structures, glowing Rift energy veins, a prominent circular Rift Beacon, darker surroundings, dramatic cyan/blue/purple energy lighting, floating particles, a central platform suitable for a boss battle, readable paths and open movement space, moderate geometric complexity, cinematic perspective, no characters, no UI, no text. The environment must be practical to recreate with procedural primitives in OpenGL.

## 24.4 Rift Beacon Prompt
* **Format:** `PNG (.png)` | **Aspect Ratio:** `1:1` | **Target:** `assets/generated_images/rift_beacon_concept_v01.png`

> Design a standalone **Rift Beacon** in PNG format for the game Riftwalker: Paradox Protocol. A futuristic circular teleportation platform with a thick glowing ring, central spatial distortion, rotating energy bands, small orbiting particles, simple mechanical base, strong emissive-looking energy, sci-fi but geometrically practical, front three-quarter view, clean silhouette, dark neutral background, no text, no UI. Make the design easy to reproduce using torus/ring geometry, cylinders, quads, particles, and simple transformations in OpenGL.

---

# 24A. Scene/Asset Creation Workflow for AI-Generated References

When a new scene or major game element needs visual design, use this procedure.

### A. Create the prompt in `docs/` first

Before generating the image, write a small note containing:

```text
Asset/Scene Name:
Purpose:
Arena:
Target Format: PNG (.png)
Aspect Ratio: 16:9 or 1:1
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
arena_02_sundered_rift_concept_v01.png
rift_beacon_concept_v01.png
rift_stalker_concept_v01.png
rift_spitter_concept_v01.png
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

All character and object concept images are generated in standard **PNG (`.png`) format with 1:1 square aspect ratio** to allow direct inspection and optional OpenGL 2D billboard/texture mapping.

## 25.1 Astronaut Prompt
* **Format:** `PNG (.png)` | **Aspect Ratio:** `1:1` | **Target:** `assets/generated_images/astronaut_concept_v01.png`

> Design a procedural-friendly sci-fi astronaut in PNG format for the university OpenGL game **Riftwalker: Paradox Protocol**. Full-body humanoid astronaut wearing a compact experimental Rift-Chrono suit, spherical helmet, dark visor, segmented torso, cylindrical arms and legs, small backpack, compact energy weapon. The body must be composed visually from spheres, cylinders, boxes, and simple capsule-like primitives. Clear articulated joints, readable silhouette, practical proportions, front three-quarter view, neutral background, no text, no UI.

## 25.2 Melee Alien Prompt (Rift Stalker — Crystalline Void)
* **Format:** `PNG (.png)` | **Aspect Ratio:** `1:1` | **Target:** `assets/generated_images/rift_stalker_concept_v01.png`

> Design a procedural Crystalline Void alien enemy called **Rift Stalker** in PNG format for a university OpenGL graphics project. Aggressive predatory quadrupedal silhouette constructed visually from sharp geometric obsidian shards, faceted angular carapace plates, glowing cyan and violet rift energy fissures pulsing through its core, and articulated crystalline bladed front limbs. Low-slung predatory stance, faceted geometry easily constructable with cubes, cones, and polyhedra, front three-quarter view, neutral dark sci-fi background, no text, no UI.

## 25.3 Ranged Alien Prompt (Rift Spitter — Floating Prism)
* **Format:** `PNG (.png)` | **Aspect Ratio:** `1:1` | **Target:** `assets/generated_images/rift_spitter_concept_v01.png`

> Design a procedural Crystalline Void alien enemy called **Rift Spitter** in PNG format for a university OpenGL project. Hovering dimensional entity composed of a floating central crystal monolith / prism surrounded by concentric orbital rotating shard rings and floating polyhedral fragments. Pulsating bioluminescent plasma eye charging a cyan energy bolt, no ground legs (pure floating/hovering entity), clean geometric faceted silhouette practical to build with OpenGL matrix transformations and rotation stacks, front three-quarter view, neutral dark background, no text, no UI.

## 25.4 Boss Prompt (Rift Guardian — Dimensional Nexus)
* **Format:** `PNG (.png)` | **Aspect Ratio:** `1:1` | **Target:** `assets/generated_images/rift_guardian_concept_v01.png`

> Design the **Rift Guardian** boss in PNG format for Riftwalker: Paradox Protocol. A colossal dimensional nexus entity featuring a massive pulsating central obsidian polyhedron core surrounded by four independent floating orbiting shield obelisks/plates. Symmetrical geometric rift energy rings, cyan and purple energetic lightning arcing between crystal facets, menacing floating silhouette, readable central weak point core, hovering above a circular glowing Rift Beacon platform, cinematic three-quarter view, neutral dark void background, no text, no UI.

---

# 26. Effects Reference Prompts

All visual effects references are generated in standard **PNG (`.png`) format with 16:9 widescreen aspect ratio**.

## 26.1 Blink Effect Prompt
* **Format:** `PNG (.png)` | **Aspect Ratio:** `16:9` | **Target:** `assets/generated_images/vfx_blink_concept_v01.png`

> Create a game VFX concept in PNG format for a short-range astronaut Blink teleport. Show a bright source burst, translucent ghost silhouette where the astronaut started, a sharp spatial streak connecting source and destination, particles expanding outward at both ends, clean sci-fi energy, dark background, centered composition, no UI, no text. Design it so it can be approximated with transparent quads, particles, rings, and simple animated geometry in OpenGL.

## 26.2 Chrono Slow Prompt
* **Format:** `PNG (.png)` | **Aspect Ratio:** `16:9` | **Target:** `assets/generated_images/vfx_chrono_slow_concept_v01.png`

> Create a visual-effect concept in PNG format for **Chrono Slow** in a sci-fi OpenGL game. Show a normal astronaut moving clearly while alien enemies and projectiles appear slowed, subtle ghost trails behind enemies, cool blue temporal distortion, thin circular energy ripples, restrained screen-space feel, cinematic but practical VFX, no UI, no text.

## 26.3 Teleport Transition Prompt
* **Format:** `PNG (.png)` | **Aspect Ratio:** `16:9` | **Target:** `assets/generated_images/vfx_teleport_transition_concept_v01.png`

> Create a cinematic gameplay frame in PNG format showing an astronaut stepping into a glowing Rift Beacon during teleportation. Circular energy ring, spatial distortion, swirling particles, brief white-blue flash, destination-like depth visible through the portal, futuristic space-station environment, readable silhouette, practical game VFX aesthetic, no UI, no text.

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
- `arena_01_kepler_relay.py` — industrial relay station geometry (covered combat space)
- `arena_02_sundered_rift.py` — floating asteroid void geometry (open boss arena)
- `environment_generator.py` — modular pillars, crates, crystal spires
- `rift_beacon.py` — **Rift Beacon Model & Trigger** (spinning torus rings & glow)
- `rift_energy_pickup.py` — **Rift Energy Collectibles** (floating glowing crystal pickups restoring +25% Chrono Charge)
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

**Primary responsibility:** graphics pipeline, texture mapping, dynamic lighting, particle systems, Chrono Slow time dilation, 2D HUD, scoring, and full game-loop coordination.

### Folder
`src/M4_rendering_gameplay/`

### Main deliverables
- `renderer.py` — master OpenGL 3D & 2D render pass coordinator
- `primitives.py` — optimized procedural & UV-mapped geometry helpers (textured cubes, cylinders, spheres, planes)
- `lighting.py` — directional sunlight (`GL_LIGHT0`) & beacon point lights (`GL_LIGHT1`)
- `materials.py` — optical material presets & texture binding integration
- `particles.py` — particle systems (teleport vortex, hit sparks, thrusters, laser beams)
- `effects.py` — screen flash & visual distortion filters
- `chrono_slow.py` — **Chrono Slow Manager** (100% activation gate, 0% reset, 5s countdown, 0.30 scale)
- `hud.py` — **2D Orthographic HUD** (Health bar, Chrono Charge/countdown bar, Score, Objective text)
- `crosshair.py` — dynamic crosshair with hitmarker feedback
- `scoring.py` — score tracking, kill feed, and combo multipliers
- `game_state.py` — game state machine (`PLAYING`, `TELEPORTING`, `GAME_OVER`, `VICTORY`)
- `level_manager.py` — wave spawning and arena progression

### Graphics focus & CG423 Procedural Pipeline
Texture mapping is a required graphics feature added to improve visual realism while preserving the project's procedural-modeling requirement. No external 3D models or game engines are used.
```text
Primitive Geometry → Hierarchical / Procedural Modeling → Texture Mapping → Lighting → Particles / Effects → Final Scene
```
- **Texture Mapping & UV Coordinates:** Reusable PIL loader (`src/shared/texture_loader.py`), 512x512 tileable PBR-style textures, clean binding/unbinding lifecycle.
- **Dynamic Lighting:** Multi-source lighting setup & quadratic point-light attenuation.
- **Material Properties:** Specular/diffuse/ambient optical properties and surface texture modulation.
- **Particle Systems:** Additive alpha blending, glowing laser tracers, and teleport vortices.
- **2D Orthographic HUD:** Matrix switching (`glOrtho`) with health, chrono, and crosshair overlays.

### Integration responsibility
M4 coordinates:
- `src/main.py` entry point and GLUT callbacks
- texture resource pre-loading (`init_textures()`)
- game start / restart flow
- arena transition triggers
- victory / game-over state evaluation
- delta-time distribution (unscaled `real_dt` vs. scaled `game_dt`)

---

## 27B. The 12 Major Team Features (3 per Member)

| Member / Module | Feature 1 | Feature 2 | Feature 3 |
|---|---|---|---|
| **M1: Player & Camera** | **Procedural Hierarchical Astronaut Rig** (`glPushMatrix`/`glPopMatrix`, suit, visor, thruster pack, articulated walking limbs) | **Dual Camera System** (`V` hotkey, 1st-person FPS & 3rd-person orbital TPS view matrix preservation) | **Player Movement & 1P Blaster Viewmodel** (WASD kinematics, velocity damping, foreground 3D rifle viewmodel with firing recoil) |
| **M2: Enemies & Combat** | **Procedural Crystalline Void Alien Generator** (Obsidian carapaces, glowing rift cores, articulated scythes & rotating shard rings) | **Enemy AI & Hitscan Combat** (Melee Stalker pursuit, Ranged Spitter kiting, 3D raycast laser fire & projectile collisions) | **Rift Guardian Boss Encounter** (Pulsating nexus core, 4 rotating orbital shield obelisks, Phase 1 vs Phase 2 rapid spinning) |
| **M3: World & Teleportation** | **Kepler Relay Arena** (Industrial space station, metallic floor grid, security walls, pillars, crates, tighter covered combat) | **Sundered Rift Arena** (Floating obsidian asteroid void, neon purple anomaly grid, crystal spires, open boss battleground) | **Tactical Rift Beacon Teleportation & Pickups** (Linked interactive beacons with vortex transitions + glowing collectible Rift Energy crystals) |
| **M4: Rendering & Gameplay** | **Multi-Source Dynamic Lighting** (`GL_LIGHT0` directional sun + `GL_LIGHT1` dynamic beacon/projectile point light attenuation) | **Texture Mapping & Materials** (Reusable PIL texture loader, 512x512 tileable PBR-style textures, UV coordinate mapping across procedural geometry, optical material presets) | **Particle/VFX + Chrono/HUD Presentation** (Teleport vortex, hit sparks, collectible sparkle bursts, alien death shatter, 5s 30% time dilation, cool-blue screen overlay, 2D HUD loop, score & crosshair) |


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

## Decision 08 — Wave-Based Combat Progression

**Status:** Approved — REQUIRED Baseline

Replace flat continuous enemy spawning with structured 3-wave encounters per arena. Rift Beacons remain locked until all waves are cleared.

## Decision 09 — Tactical Arena Hazards

**Status:** Approved — REQUIRED Baseline

Add lightweight geometric hazards (moving laser barriers, electrified floors, closing doors, rotating energy beams, rift damage zones) to force active player movement and spatial awareness.

## Decision 10 — Combo Scoring System

**Status:** Approved — REQUIRED Baseline

Incorporate time-decaying combo multipliers (`COMBO x1` to `x4`) to reward aggressive play and high accuracy.

---

# 39. AI Assistant Quick Context & Scope Enforcement Rules

> **AUTHORITATIVE MANDATE FOR AI ASSISTANTS:** Any AI assistant working on this repository must treat `PROJECT_SPEC.md` as the authoritative single source of truth and scope boundary.
> 1. **Scope Boundary:** AI assistants must **NOT** introduce or generate code for removed/out-of-scope features (e.g. world rewind buffers, complex 6-DOF physics, IK, arbitrary gravity, upgrade trees, multiple bosses) unless the user explicitly requests them.
> 2. **Branch Protection & PR Policy:** Direct pushes to `main` are prohibited. All code and asset modifications must be developed within isolated feature branches (`feature/m<module_num>-<feature_name>`) and submitted via Pull Requests targeting `main` only after ensuring all unit tests pass (`python3 -m unittest discover -s tests`).

When giving this document to another AI assistant, the following compact context can be used:

> We are building a CG423 Computer Graphics OpenGL project called **Riftwalker: Paradox Protocol**. It is a manageable sci-fi combat game targeting approximately 60% graphics and 40% gameplay. The player is an astronaut who can move, shoot, use Chrono Slow (5s duration at 30% enemy speed, activated only at 100% combat charge), and switch between first-person and third-person cameras. The game has exactly two baseline arenas: **Kepler Relay** (tight cover, moving lasers, electrified floors) and **Sundered Rift** (open plateau, rotating beams, rift zones). Linked Rift Beacons teleport the player between the two arenas once 3 structured combat waves per arena are cleared. Chrono Slow is a simple delta-time scaling mechanic without world rewind. Combat features combo multipliers (`COMBO x1` to `x4`), two aggressive enemies (zig-zagging Stalkers and strafing Spitters), and one multi-phase boss (Rift Guardian). Collision is centralized in `src/shared/collision.py`. Blink and Gravity zones are optional stretch features. Avoid scope creep such as 6-DOF flight, arbitrary gravity systems, IK, upgrade trees, multiple bosses, or full temporal simulation. NEVER push directly to `main`; always use isolated feature branches (`feature/mX-...`) and Pull Requests.

---

# 39A. Final Feature Matrix

| Area | Assignment 3 Baseline | Riftwalker Final |
|---|---|---|
| Player | Primitive astronaut | Detailed hierarchical astronaut + articulated arms + weapon aim |
| Camera | Basic first/third-person state | Dedicated 1P viewmodel + 3P OTS camera with synced crosshair |
| Enemy | One simple pursuer | Zig-zagging melee Stalkers + strafing ranged Spitters + multi-phase boss |
| Combat & Waves | Continuous respawn / bullets | 3 structured combat waves per arena + hitscan raycast + projectiles |
| Arena Hazards | None | Moving laser barriers, electrified floors, rotating energy beams, rift zones |
| World | Flat square arena + walls | Two distinct modular arenas with unique tactical cover & sightline profiles |
| Teleportation | None | Wave-unlocked tactical Rift Beacon teleportation between arenas + Blink |
| Time | Frame-based update | Strategic Chrono Slow (5s, 30% enemy speed, 100% combat charge gate) |
| Graphics | Primitive composition | Procedural models + multi-source lighting + particles + laser tracers |
| HUD | Life/score/missed bullets | HP + Chrono bar + cooldown bar + live wave objectives + combo meter + boss bar |
| Scoring | Flat kill score | Base kill score × dynamic combo multiplier (`x1` to `x4`) + performance ranks |
| Game flow | Restart/game over | Story Intro → Arena 1 (Waves 1–3) → Beacon → Arena 2 (Waves 1–3) → Boss → Victory |

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
