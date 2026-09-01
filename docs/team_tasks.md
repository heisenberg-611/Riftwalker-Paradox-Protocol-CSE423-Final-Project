# Team Work Breakdown & Task Allocation

## Team Member 1 (M1) — Player & Camera Systems
- **Directory**: `src/M1_player_camera/`
- **Assigned Modules**:
  - `player.py`: Player coordinator managing HP, position, orientation, cameras, and viewmodel
  - `astronaut_rig.py`: Procedural hierarchical astronaut rig with matrix stacks (`glPushMatrix`/`glPopMatrix`), articulated walking limbs, visor, and thruster pack
  - `player_movement.py`: WASD movement kinematics, velocity damping, and orientation synchronization
  - `first_person_camera.py`: 1st-person FPS camera with pitch/yaw clamping
  - `third_person_camera.py`: 3rd-person follow/orbit camera with spherical coordinate tracking
  - `player_weapon.py`: **Weapon Visual Presentation** (astronaut weapon 3D mesh & 1st-person laser rifle viewmodel with firing recoil and muzzle flash)
  - `blink_teleport.py`: *(Optional Stretch Feature)* Short-range evasive combat dash

---

## Team Member 2 (M2) — Enemies & Combat Systems
- **Directory**: `src/M2_enemies_combat/`
- **Visual Aesthetic**: Crystalline Void Horrors (Faceted obsidian shard carapaces, glowing cyan/purple rift fissure cores, rotating crystal shard rings)
- **Assigned Modules**:
  - `alien_generator.py`: Procedural Crystalline Void alien generator (hierarchical matrix stacks, floating shard rings, rift cores)
  - `enemy_base.py`: Base class for AI, pathing, states, hitboxes, and Chrono Slow time scaling
  - `melee_rift_stalker.py`: Aggressive melee shadow-hound with articulated scythe blades
  - `ranged_rift_spitter.py`: Floating dimensional crystal prism with dual orbital rotating shard rings launching plasma bolts
  - `rift_guardian_boss.py`: Final multi-phase boss with 4 rotating orbital shield obelisks (rapid spinning in Phase 2)
  - `weapon_system.py`: **Combat Gameplay Logic** (firing rate timers, damage application, projectile pooling, and active projectile physics)
  - `raycast.py`: Precision 3D hitscan raycasting detection using `src/shared/collision.py`

---

## Team Member 3 (M3) — World, Arenas & Teleportation
- **Directory**: `src/M3_world_teleport/`
- **Assigned Modules**:
  - `world.py`: World container managing active arenas and transition triggers
  - `arena_base.py`: Abstract arena layout container updating and drawing beacons/pickups
  - `arena_01_kepler_relay.py`: Industrial human relay station with metallic floor grid, security walls, pillars, crates, and tighter covered combat
  - `arena_02_sundered_rift.py`: Floating obsidian asteroid void with neon purple anomaly grid and crystal spires (open boss arena)
  - `environment_generator.py`: Procedural placement of modular props and obstacles
  - `rift_beacon.py`: **Rift Beacon Platform (REQUIRED)** — interactive beacon platform with animated spinning torus rings and proximity detection ($R \le 3.5$)
  - `rift_energy_pickup.py`: **Rift Energy Collectibles** — floating glowing crystal pickups restoring +25% Chrono Charge with 15s respawn timer
  - `gravity_zone.py`: *(Optional Stretch Feature)* Special low-gravity / jump-pad triggers

---

## Team Member 4 (M4) — Rendering, HUD, Effects & Game Integration
- **Directory**: `src/M4_rendering_gameplay/` and `src/main.py`
- **Assigned Modules**:
  - `renderer.py`: Master OpenGL rendering pipeline orchestrator (3D world, enemies, projectiles, 1P viewmodel, particles, screen effects, and 2D HUD)
  - `primitives.py`: Optimized basic geometry drawers (cube, cylinder, sphere, torus, octahedron)
  - `lighting.py`: Multi-source dynamic lighting (`GL_LIGHT0` directional sun, `GL_LIGHT1` dynamic beacon/projectile point lights)
  - `materials.py`: Material optical definitions (ambient, diffuse, specular, shininess)
  - `particles.py`: Particle systems for teleport vortex, hit sparks, collectible sparkle bursts, alien death shatter, and Chrono ripples
  - `effects.py`: Visual distortion filters (teleport cyan screen flash, Chrono Slow cool-blue screen tint and corner vignette overlay)
  - `chrono_slow.py`: **Chrono Slow Manager** (100% activation gate via `Q`, 0% reset, 5.0s countdown, 0.30 speed scale)
  - `hud.py`: **2D Orthographic HUD** (Suit Health bar, Chrono Charge/countdown bar, Boss Health bar with phase indicator, Score, Crosshair)
  - `crosshair.py`: Dynamic crosshair with hitmarker animation feedback
  - `scoring.py`: High score tracking, multipliers, and combo timer
  - `game_state.py`: Game loop state machine (`PLAYING`, `TELEPORTING`, `GAME_OVER`, `VICTORY`)
  - `level_manager.py`: Wave spawning, arena progression, and boss trigger
  - `src/main.py`: Entry point and GLUT loop coordination
