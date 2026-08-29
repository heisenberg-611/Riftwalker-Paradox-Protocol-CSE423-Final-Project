# Project TODO & Milestones

## Phase 0: Project Baseline & Skeleton Setup

- [x] Create project repository structure and `.gitignore`
- [x] Create specification and documentation templates (`docs/`, `scenes/`)
- [x] Create core shared libraries (`constants.py`, `math3d.py`, `input_manager.py`, `game_time.py`)
- [x] Implement baseline graphics test sandbox in `main.py`
- [x] Set up unit tests for `math3d` and core logic
- [x] Create shared collision utilities (`collision.py`)

## Phase 1: M1 — Player & Camera Systems

- [ ] Implement procedural hierarchical astronaut model (`astronaut_rig.py`)
- [ ] Implement third-person camera with smooth follow and orbit
- [ ] Implement first-person precision camera with viewmodel offset
- [ ] Implement player movement (WASD) and collision bounds
- [ ] Implement player health/death state
- [ ] [STRETCH] Implement Blink teleportation mechanic

## Phase 2: M2 — Enemies & Combat

- [ ] Implement procedural alien creature generator (`alien_generator.py`)
- [ ] Implement Melee Rift Stalker AI and state machine
- [ ] Implement Ranged Rift Spitter AI and projectile behavior
- [ ] Implement Boss: Rift Guardian hierarchy and attack patterns
- [ ] Implement hitscan weapon system
- [ ] Implement raycasting and hitbox detection
- [ ] Implement damage/death handling

## Phase 3: M3 — World, Arenas & Teleportation

- [ ] Build Arena 1: Kepler Relay layout and modular props
- [ ] Build Arena 2: Sundered Rift layout and hazard props
- [ ] Implement animated Rift Beacon models
- [ ] Implement Rift Beacon visual effects
- [ ] Implement Arena-to-Arena teleportation state machine
- [ ] Implement player spawn/coordinate mapping for both arenas
- [ ] Implement basic level/arena state management

## Phase 4: M4 — Rendering, Effects, HUD & Final Integration

- [ ] Implement dynamic lighting (directional light + beacon/enemy/muzzle lighting where supported)
- [ ] Implement particle systems
    - [ ] Rift Beacon vortex
    - [ ] Teleport flash
    - [ ] Muzzle flash
    - [ ] Bullet impact
    - [ ] Alien death
    - [ ] Environmental sparks
- [ ] Implement Chrono Charge accumulation
- [ ] Implement Chrono Slow activation at 100% charge
- [ ] Implement ~5-second Chrono Slow duration
- [ ] Scale enemies/projectiles to ~0.3x time during Chrono Slow
- [ ] Reset Chrono Charge after activation
- [ ] Implement simple Chrono Slow visual feedback
- [ ] Implement 2D OpenGL HUD overlay
    - [ ] Health
    - [ ] Chrono Charge bar
    - [ ] Crosshair
    - [ ] Score
    - [ ] Objective
- [ ] Implement scoring and rank system
- [ ] Integrate full game loop
    - [ ] Start Screen
    - [ ] Arena 1
    - [ ] Rift Beacon teleport
    - [ ] Arena 2
    - [ ] Boss
    - [ ] Victory
    - [ ] Game Over
    - [ ] Restart