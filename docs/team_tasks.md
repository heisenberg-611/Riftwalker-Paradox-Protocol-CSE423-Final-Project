# Team Work Breakdown & Task Allocation

## Team Member 1 (M1) — Player & Camera Systems
- **Directory**: `src/M1_player_camera/`
- **Assigned Modules**:
  - `player.py`: Player state (HP, Chrono, position, speed, orientation)
  - `astronaut_rig.py`: Procedural hierarchical astronaut rig with limbs, visor, backpack
  - `player_movement.py`: WASD movement, direction calculation, acceleration
  - `first_person_camera.py`: FPS eye camera with viewmodel offset
  - `third_person_camera.py`: 3rd person follow/orbit camera with pitch clamping
  - `player_weapon.py`: Primary hitscan weapon handling
  - `blink_teleport.py`: Short-range evasive blink dash

---

## Team Member 2 (M2) — Enemies & Combat Systems
- **Directory**: `src/M2_enemies_combat/`
- **Assigned Modules**:
  - `alien_generator.py`: Procedural alien geometry generator (carapaces, legs, heads)
  - `enemy_base.py`: Base class for AI, pathing, states, and hitboxes
  - `melee_rift_stalker.py`: Aggressive melee rushing alien
  - `ranged_rift_spitter.py`: Ranged acid/plasma projectile shooter
  - `rift_guardian_boss.py`: Final multi-stage boss with rotating energy shields
  - `weapon_system.py`: Bullet pools, firing logic, muzzle positions
  - `raycast.py`: Raycasting algorithm for precision hitscan detection
  - `collision.py`: Bounding sphere and AABB collision resolution

---

## Team Member 3 (M3) — World, Arenas & Teleportation
- **Directory**: `src/M3_world_teleport/`
- **Assigned Modules**:
  - `world.py`: World container managing active arenas and transition triggers
  - `arena_base.py`: Abstract arena layout container
  - `arena_01_kepler_relay.py`: Industrial sci-fi arena with walkways, pillars, console props
  - `arena_02_sundered_rift.py`: Asteroid void arena with floating rock platforms
  - `environment_generator.py`: Procedural placement of modular props and obstacles
  - `rift_beacon.py`: Interactive Rift Beacon with animated spinning torus rings
  - `gravity_zone.py`: Low-gravity and jump-pad triggers

---

## Team Member 4 (M4) — Rendering, HUD, Effects & Game Integration
- **Directory**: `src/M4_rendering_gameplay/`
- **Assigned Modules**:
  - `renderer.py`: Master OpenGL rendering pipeline orchestrator
  - `primitives.py`: Optimized basic geometry drawers (cube, cylinder, sphere, torus)
  - `lighting.py`: Multi-source dynamic lighting configuration
  - `materials.py`: Material optical definitions (ambient, diffuse, specular, shininess)
  - `particles.py`: Particle systems for sparks, smoke, teleport vortex, thrusters
  - `effects.py`: Visual distortion filters (teleport flash, Chrono slow blue tint)
  - `chrono_slow.py`: Time dilation manager and resource consumption
  - `hud.py`: 2D Orthographic overlay rendering (Health bar, Chrono gauge, Ammo, Score)
  - `crosshair.py`: Dynamic crosshair with hit-marker feedback
  - `scoring.py`: High score tracking, multipliers, combo timer
  - `game_state.py`: Game loop state machine (Menu, Playing, Teleporting, Game Over, Win)
  - `level_manager.py`: Wave spawning, arena progression, boss trigger
  - `src/main.py`: Entry point and GLUT loop coordination
