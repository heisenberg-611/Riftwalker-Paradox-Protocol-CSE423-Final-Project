# Architecture & System Design

## 1. Modular Hierarchy

The codebase is split into 4 core functional modules (`M1` to `M4`) and one `shared` library to ensure clear ownership for team members:

```text
src/
├── main.py                     # Entry point (initializes GLUT, sets callbacks, runs mainloop)
│
├── shared/                     # Shared immutable data types & utilities
│   ├── constants.py            # Global constants (physics, keys, camera, speeds, IDs)
│   ├── math3d.py               # Vector3, Matrix4, transformations, ray-box/sphere intersections
│   ├── input_manager.py        # Centralized keyboard and mouse state tracking
│   └── game_time.py            # Delta time, Chrono time scaling, FPS regulation
│
├── M1_player_camera/           # [M1] Player Character & View Systems
│   ├── player.py               # Player entity state (HP, energy, position, orientation)
│   ├── astronaut_rig.py        # Procedural hierarchical astronaut mesh & matrix transformations
│   ├── player_movement.py      # Kinematics, WASD movement, velocity damping
│   ├── first_person_camera.py  # 1st-person FPS camera with viewmodel offset
│   ├── third_person_camera.py  # 3rd-person follow/orbit camera
│   ├── player_weapon.py        # Weapon state, cooldowns, muzzle points
│   └── blink_teleport.py       # Instant short-range combat blink dash
│
├── M2_enemies_combat/          # [M2] Alien AI & Combat Systems
│   ├── enemy_base.py           # Abstract base enemy class
│   ├── alien_generator.py      # Procedural multi-legged / segmented alien model builder
│   ├── melee_rift_stalker.py   # Fast melee rusher AI
│   ├── ranged_rift_spitter.py  # Long-range acid/energy projectile spitter AI
│   ├── rift_guardian_boss.py   # Multi-stage boss with articulated shield & energy beams
│   ├── weapon_system.py        # Projectile pool, hitscan trace dispatcher
│   ├── raycast.py              # Raycast shooting against axis-aligned & oriented bounding boxes
│   └── collision.py            # Spatial collision checks (sphere-sphere, AABB-AABB, ray-plane)
│
├── M3_world_teleport/          # [M3] Arenas, Environment & Teleportation
│   ├── world.py                # Active world manager, arena switching
│   ├── arena_base.py           # Base arena layout and boundary container
│   ├── arena_01_kepler_relay.py# Kepler Relay environment (sci-fi structures, towers, ramps)
│   ├── arena_02_sundered_rift.py# Sundered Rift environment (floating void platforms, ruins)
│   ├── environment_generator.py# Procedural obstacles, crates, pillars, debris
│   ├── rift_beacon.py          # Interactive Rift Beacon entity with rotating portal rings
│   └── gravity_zone.py         # Specialized low-G / jump pad triggers
│
└── M4_rendering_gameplay/      # [M4] Graphics Pipeline, Effects, HUD & Game State
    ├── renderer.py             # Main render pass orchestrator (3D world -> Lighting -> HUD)
    ├── primitives.py           # Optimized procedural primitives (cubes, cylinders, spheres, cones)
    ├── lighting.py             # Multi-light setup (GL_LIGHT0 directional sun, GL_LIGHT1-3 pointlights)
    ├── materials.py            # Specular/diffuse/ambient material presets
    ├── particles.py            # GPU/CPU particle emitter (vortex, sparks, smoke, blood)
    ├── effects.py              # Visual distortion effects (teleport flash, Chrono slow tint)
    ├── chrono_slow.py          # Chrono Slow time dilation manager
    ├── hud.py                  # 2D Orthographic HUD (Health bar, energy, crosshair, score)
    ├── crosshair.py            # Dynamic interactive crosshair
    ├── scoring.py              # Score tracker, combo multipliers, kill feed
    ├── game_state.py           # State machine (MENU, PLAYING, TELEPORTING, GAMEOVER, VICTORY)
    └── level_manager.py        # Level progression & wave spawning
```
