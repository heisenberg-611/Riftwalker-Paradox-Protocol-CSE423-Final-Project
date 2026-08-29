# Riftwalker: Paradox Protocol

**Project Type:** Computer Graphics / OpenGL Course Project  
**Course Context:** CG423  
**Project Goal:** Build a manageable but visually impressive sci-fi third-person/first-person OpenGL game that demonstrates computer-graphics techniques more strongly than complex game-engine infrastructure.

> **Important:** This document is the project's single source of truth. Any developer or AI assistant joining the project should read this file first. When the supplied course OpenGL starter/template is provided later, this document should be updated only where the starter project's actual constraints or APIs require changes.

---

## 1. Project Summary

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

## 2. Final Scope — Locked Baseline

### 2.1 Keep These Features

| Feature | Priority | Notes |
|---|---:|---|
| Procedural astronaut model | Critical | Hierarchical transformations |
| Procedural alien model | Critical | Reusable procedural creature generator |
| First-person camera | High | Precision combat mode |
| Third-person camera | High | Default exploration/combat view |
| Two arenas | Critical | Main game spaces |
| Rift teleportation | Critical | Teleport between linked arena beacons |
| Chrono Slow | High | Simple time manipulation mechanic |
| Basic shooting | Critical | Hitscan weapon |
| Basic collision | Critical | Player/world + projectile/enemy interactions |
| Two enemy types | High | Melee + ranged |
| One boss | High | Final encounter |
| Lighting | Critical | Main graphics demonstration |
| Particle effects | High | Rift, weapon, jet/energy, death effects |
| Hierarchical animation | High | Astronaut and selected enemy articulation |
| Gravity system | Medium | Keep mostly conventional; one controlled special gravity section at most |
| HUD | Medium | HP, Chrono Charge, score, crosshair |
| Score/rank | Medium | Simple scoring only |

### 2.2 Explicitly Cut From the Baseline

Do **not** implement these unless the project is already fully complete:

- Full 6-DOF zero-G flight
- Full-world rewind
- Temporal Echo simulation of the whole world
- Four separate environments
- Multiple complex gravity directions
- Two-bone IK
- Persistent upgrade economy
- Skill tree
- Rift currency system
- Multiple bosses
- Complex save-state restoration
- Large-scale LOD framework
- Advanced physics engine
- Online/multiplayer systems
- Procedural infinite levels

These features are outside the core CG423 objective and can destabilize the schedule.

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

# 5. Teleportation System

Teleportation is a major feature and should remain simple internally.

## 5.1 Design

A **Rift Beacon** is a spatial anchor with a linked destination beacon.

```text
Rift Beacon A
      │
      │ spatial link
      ▼
Rift Beacon B
```

Stepping into / activating Beacon A moves the player to Beacon B.

## 5.2 Teleport Sequence

1. Player enters activation radius.
2. Beacon starts visual charge.
3. Short control lockout.
4. Screen flash / distortion.
5. Player position and orientation are changed.
6. Destination arena becomes active.
7. Player appears at the destination beacon.
8. Rift particles continue briefly.

## 5.3 Teleport Data Model

Conceptually:

```python
RiftBeacon:
    id
    position
    rotation
    linked_beacon_id
    activation_radius
    active
```

The implementation may differ after the course OpenGL starter code is supplied.

## 5.4 Important Constraint

Teleportation should **not** require simulated wormhole physics.

The visual effect creates the illusion; internally it is a controlled transform/state transition.

---

# 6. Chrono Slow System

Chrono Slow is the simplified time-travel/time-manipulation feature.

## 6.1 Behavior

When active:

- Player movement remains normal.
- Enemy movement uses reduced delta time.
- Enemy animations slow down.
- Enemy projectiles move more slowly.
- Visual effect indicates temporal distortion.

Example target factor:

```text
PLAYER TIME SCALE = 1.0
ENEMY TIME SCALE  = 0.3
```

The exact value should be exposed as a configurable constant.

## 6.2 Resource

Use one simple **Chrono Charge** meter.

```text
MAX_CHRONO_CHARGE
       ↓
Activate Chrono Slow
       ↓
Charge drains
       ↓
Ability ends at zero
       ↓
Charge regenerates
```

No rewind buffer is required.

## 6.3 Visual Treatment

While Chrono Slow is active:

- slight screen desaturation
- blue/cool tint
- enemy motion trails / afterimages
- subtle Rift particles
- HUD meter animation

These should be implemented using techniques compatible with the supplied OpenGL starter framework.

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

## 10.1 Primary Weapon

Use one basic energy pistol/rifle.

### Shooting

Use a hitscan ray.

```text
Aim Origin + Aim Direction
            ↓
       Ray Intersection
            ↓
         Hit Enemy
```

No need for a large arsenal.

## 10.2 Aim Abstraction

Both camera modes should expose a common aim interface.

Conceptually:

```python
AimResult:
    origin
    direction
    hit
    hit_position
    target
```

This prevents weapon logic from depending on a specific camera mode.

---

# 11. Blink Teleport

Separate this from the large Rift Beacon teleport system.

## 11.1 Blink

Short-range directional teleport for combat.

Concept:

```text
P_new = P + normalize(aim_direction) * blink_range
```

Apply collision checks before accepting the new position.

## 11.2 Visual Effect

- ghost silhouette at source
- bright particle burst
- destination particle burst
- short screen flash

Blink shares no complicated physics with the Rift Beacon system.

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

# 18. Collision

Keep collision primitive and understandable.

## Player

Approximate with a capsule/cylinder or bounding volume.

## Enemies

Approximate with spheres/capsules.

## Weapon

Use ray intersection.

## Teleport

Before teleporting the player, verify destination is valid and not inside blocked geometry when practical.

Do not implement a general physics engine.

---

# 19. HUD

Keep the HUD simple.

### Required

```text
HP:        [██████████]
CHRONO:    [███████░░░]
SCORE:     012500

               +

[Optional] RIFT BEACON READY
```

### First-person and third-person

The same HUD can be reused in both modes.

The crosshair stays centered.

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

Use a directory structure that is understandable to both humans and AI assistants.

Recommended baseline:

```text
riftwalker-paradox-protocol/
│
├── README.md
├── PROJECT_SPEC.md
├── CHANGELOG.md
├── TODO.md
├── requirements.txt                 # Only if required by the supplied starter framework
│
├── src/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── app.py
│   │   ├── input_manager.py
│   │   ├── game_time.py
│   │   ├── math3d.py
│   │   └── constants.py
│   │
│   ├── camera/
│   │   ├── camera.py
│   │   ├── first_person_camera.py
│   │   └── third_person_camera.py
│   │
│   ├── player/
│   │   ├── player.py
│   │   ├── player_movement.py
│   │   ├── astronaut_rig.py
│   │   ├── player_weapon.py
│   │   ├── blink_teleport.py
│   │   └── chrono_slow.py
│   │
│   ├── enemies/
│   │   ├── enemy_base.py
│   │   ├── melee_alien.py
│   │   ├── ranged_alien.py
│   │   ├── alien_generator.py
│   │   └── rift_guardian_boss.py
│   │
│   ├── world/
│   │   ├── world.py
│   │   ├── arena_base.py
│   │   ├── arena_01_kepler_relay.py
│   │   ├── arena_02_sundered_rift.py
│   │   ├── environment_generator.py
│   │   ├── gravity_zone.py
│   │   └── rift_beacon.py
│   │
│   ├── combat/
│   │   ├── weapon_system.py
│   │   ├── raycast.py
│   │   ├── projectile.py
│   │   └── collision.py
│   │
│   ├── rendering/
│   │   ├── renderer.py
│   │   ├── lighting.py
│   │   ├── materials.py
│   │   ├── particles.py
│   │   ├── primitives.py
│   │   └── effects.py
│   │
│   ├── ui/
│   │   ├── hud.py
│   │   ├── crosshair.py
│   │   └── score_display.py
│   │
│   └── gameplay/
│       ├── game_state.py
│       ├── scoring.py
│       └── level_manager.py
│
├── scenes/
│   ├── arena_01_kepler_relay/
│   │   ├── scene_notes.md
│   │   ├── layout_notes.md
│   │   └── spawn_points.md
│   │
│   └── arena_02_sundered_rift/
│       ├── scene_notes.md
│       ├── layout_notes.md
│       └── spawn_points.md
│
├── assets/
│   ├── concept_art/
│   │   ├── characters/
│   │   ├── environments/
│   │   ├── enemies/
│   │   └── effects/
│   │
│   ├── textures/
│   ├── reference_images/
│   └── generated_images/
│
├── docs/
│   ├── graphics_techniques.md
│   ├── controls.md
│   ├── architecture.md
│   ├── team_tasks.md
│   └── implementation_notes.md
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

> **Starter-code integration rule:** When the CG423 OpenGL file is supplied, first inspect its existing file names and architecture. Do not blindly rename or rewrite the starter project. This directory proposal is a target architecture, not a requirement to fight the starter template.

---

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

# 28. Development Phases

## Phase 0 — Starter Template Integration

**Goal:** Understand the supplied CG423 OpenGL code before adding project features.

Tasks:

- identify main loop
- identify rendering entry point
- identify input system
- identify camera code
- identify matrix stack usage
- identify primitive drawing utilities
- identify lighting setup
- identify current collision/input helpers

**Deliverable:** update this project specification with the actual starter architecture.

---

## Phase 1 — Graphics Foundation

Build:

- primitive drawing helpers
- transformation helpers
- camera
- lighting
- procedural astronaut

**Deliverable:** astronaut visible and controllable in a blank test scene.

---

## Phase 2 — First Arena

Build:

- Kepler Relay geometry
- lighting
- player movement
- third-person camera
- first-person camera

**Deliverable:** walkable playable test arena.

---

## Phase 3 — Combat

Build:

- weapon
- raycast
- collision
- melee alien
- ranged alien
- enemy health

**Deliverable:** basic combat loop.

---

## Phase 4 — Rift Teleportation

Build:

- Rift Beacon geometry
- beacon animation
- teleport logic
- screen flash
- destination spawn handling

**Deliverable:** working teleport from Arena 1 to Arena 2.

---

## Phase 5 — Second Arena

Build:

- Sundered Rift geometry
- alien lighting
- particles
- enemy placements
- return beacon

**Deliverable:** two connected arenas.

---

## Phase 6 — Chrono Slow

Build:

- Chrono Charge
- enemy time scale
- projectile slow
- visual distortion
- HUD meter

**Deliverable:** stable time-slow mechanic.

---

## Phase 7 — Boss

Build:

- Rift Guardian model
- boss health
- two simple phases
- boss attacks
- defeat effect

**Deliverable:** complete combat encounter.

---

## Phase 8 — Presentation / Polish

Add:

- particle polish
- camera polish
- lighting polish
- HUD polish
- score/rank
- sound only if allowed and time remains
- screenshots/video for presentation

**Deliverable:** final demo build.

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

## Chrono

- player remains normal speed
- enemy movement slows
- enemy projectile speed slows
- charge drains and regenerates
- activation/deactivation is stable

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

**Status:** Simplified

Do not implement full rewind/world reversal. Represent time manipulation through **Chrono Slow**.

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

---

# 39. AI Assistant Quick Context

When giving this document to another AI assistant, the following compact context can be used:

> We are building a CG423 Computer Graphics OpenGL project called **Riftwalker: Paradox Protocol**. It is a manageable sci-fi combat game targeting approximately 60% graphics and 40% gameplay. The player is an astronaut who can move, shoot, Blink, use Chrono Slow, and switch between first-person and third-person cameras. The game has exactly two baseline arenas: **Kepler Relay** and **Sundered Rift**. Rift Beacons teleport the player between the two arenas. Chrono Slow is the simplified time-manipulation feature; there is no world rewind. There are two normal enemies (melee and ranged) and one boss (Rift Guardian). The graphics priorities are procedural/hierarchical astronaut modeling, procedural alien generation, lighting, particles, camera transformations, and simple collision/raycasting. Avoid scope creep such as 6-DOF flight, multiple gravity systems, IK, upgrade trees, multiple bosses, or full temporal simulation. The supplied CG423 OpenGL starter code is authoritative and must be integrated rather than unnecessarily replaced.

---

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
