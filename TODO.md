# Project TODO & Milestones

## Phase 0: Project Baseline & Skeleton Setup
- [x] Create project repository structure and `.gitignore`
- [x] Create specification and documentation templates (`docs/`, `scenes/`)
- [x] Create core shared libraries (`constants.py`, `math3d.py`, `input_manager.py`, `game_time.py`)
- [x] Implement baseline graphics test sandbox in `main.py`
- [x] Set up unit tests for `math3d` and core logic

## Phase 1: M1 — Player & Camera Systems
- [ ] Implement procedural hierarchical astronaut model (`astronaut_rig.py`)
- [ ] Implement third-person camera with smooth follow and orbit
- [ ] Implement first-person precision camera with viewmodel offset
- [ ] Implement player movement (WASD) and collision bounds
- [ ] Implement Blink teleportation mechanic

## Phase 2: M2 — Enemies & Combat
- [ ] Implement procedural alien creature generator (`alien_generator.py`)
- [ ] Implement Melee Rift Stalker AI and state machine
- [ ] Implement Ranged Rift Spitter AI and projectile trajectory
- [ ] Implement Boss: Rift Guardian multi-part hierarchy and attack patterns
- [ ] Implement hitscan weapon system, raycasting, and hitbox detection

## Phase 3: M3 — World, Arenas & Teleportation
- [ ] Build Arena 1: Kepler Relay layout and modular props
- [ ] Build Arena 2: Sundered Rift floating terrain and hazard props
- [ ] Implement animated Rift Beacon models with glow effects
- [ ] Implement Arena-to-Arena teleportation state machine and coordinate mapping

## Phase 4: M4 — Rendering, Effects, HUD & Final Integration
- [ ] Implement dynamic multi-source lighting (Sun, Beacon Pointlights, Muzzle flashes)
- [ ] Implement particle effect systems (Rift vortex, bullet impacts, jet thrusters, sparks)
- [ ] Implement Chrono Slow time-dilation shader/visual distortion filter
- [ ] Implement 2D OpenGL HUD overlay (Health, Chrono Charge bar, Crosshair, Score, Objective)
- [ ] Integrate full game loop (Start Screen -> Arena 1 -> Teleport -> Arena 2 Boss -> Victory/GameOver)
