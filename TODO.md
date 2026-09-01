# Project TODO & Milestones

## Phase 0: Project Baseline & Skeleton Setup

- [x] Create project repository structure and `.gitignore`
- [x] Create specification and documentation templates (`docs/`, `scenes/`)
- [x] Create core shared libraries (`constants.py`, `math3d.py`, `input_manager.py`, `game_time.py`)
- [x] Implement baseline graphics test sandbox in `main.py`
- [x] Set up unit tests for `math3d` and core logic
- [x] Create shared collision utilities (`collision.py`)

## Phase 1: M1 — Player & Camera Systems

- [x] Implement procedural hierarchical astronaut model (`astronaut_rig.py`)
- [x] Implement third-person camera with smooth follow and orbit
- [x] Implement first-person precision camera with viewmodel offset
- [x] Implement player movement (WASD) and collision bounds
- [x] Implement player health/death state
- [x] [STRETCH] Implement Blink teleportation mechanic
- [x] Implement foreground 3D blaster viewmodel with firing recoil and muzzle flare (`player_weapon.py`)
- [x] Implement continuous keyboard camera rotation (Arrow Keys `←`, `→`, `↑`, `↓`) and Fullscreen mode (`F11`)

## Phase 2: M2 — Enemies & Combat

- [x] Implement procedural alien creature generator (`alien_generator.py`)
- [x] Implement Melee Rift Stalker AI and state machine
- [x] Implement Ranged Rift Spitter AI and projectile behavior
- [x] Implement Boss: Rift Guardian hierarchy and attack patterns
- [x] Implement Rift Guardian Phase 1 vs Phase 2 rotating orbital shield obelisks
- [x] Implement hitscan weapon system
- [x] Implement raycasting and hitbox detection
- [x] Implement damage/death handling

## Phase 3: M3 — World, Arenas & Teleportation

- [x] Build Arena 1: Kepler Relay layout and modular props
- [x] Build Arena 2: Sundered Rift layout and hazard props
- [x] Implement animated Rift Beacon models
- [x] Implement Rift Beacon visual effects
- [x] Implement collectible glowing Rift Energy crystals (`energy_pickup.py`)
- [x] Implement Arena-to-Arena teleportation state machine
- [x] Implement player spawn/coordinate mapping for both arenas
- [x] Implement basic level/arena state management

## Phase 4: M4 — Rendering, Effects, HUD & Final Integration

- [x] Implement dynamic lighting (directional light + beacon/enemy/muzzle lighting where supported)
- [x] Implement Texture Mapping & Material System (`texture_loader.py`, `materials.py`)
    - [x] Reusable PIL texture loader with mipmapping and caching
    - [x] High-detail 512x512 tileable PBR-style PNG textures (`environment`, `characters`, `weapons`, `rift`, `background`)
    - [x] UV texture coordinate mapping across procedural 3D geometric primitives (`primitives.py`)
    - [x] Texture-to-material binding presets for Kepler Relay, Sundered Rift, astronaut suit, alien carapaces, and rift beacons
- [x] Implement particle systems

    - [x] Rift Beacon vortex
    - [x] Teleport flash
    - [x] Muzzle flash
    - [x] Bullet impact
    - [x] Alien death
    - [x] Environmental sparks
    - [x] Collectible crystal pickup burst
    - [x] Chrono Slow ripple waves
- [x] Implement Chrono Charge accumulation
- [x] Implement Chrono Slow activation at 100% charge
- [x] Implement ~5-second Chrono Slow duration
- [x] Scale enemies/projectiles to ~0.3x time during Chrono Slow
- [x] Reset Chrono Charge after activation
- [x] Implement simple Chrono Slow visual feedback
- [x] Implement 2D OpenGL HUD overlay
    - [x] Health
    - [x] Chrono Charge bar
    - [x] Crosshair
    - [x] Score
    - [x] Objective
    - [x] Camera Mode indicator
    - [x] Boss HP and Phase status
- [x] Implement scoring and rank system
- [x] Integrate full game loop
    - [x] Start Screen & First-Time 6-Panel Cinematic Story Introduction (`story_intro.py`)
    - [x] Arena 1
    - [x] Rift Beacon teleport
    - [x] Arena 2
    - [x] Boss
    - [x] Victory (with full camera & world freeze)
    - [x] Game Over (with full camera & world freeze)
    - [x] Restart