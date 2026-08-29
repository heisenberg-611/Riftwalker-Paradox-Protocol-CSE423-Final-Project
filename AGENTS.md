# AGENTS.md — Mandatory AI Assistant Directives

This document provides binding constraints and protocols for all AI coding assistants operating on the **Riftwalker: Paradox Protocol** repository.

---

## 🛡️ 1. Mandatory Git Branching & Push Safety Protocol

Any AI assistant executing git commands, creating code, or collaborating with a team member MUST strictly obey the following rules:

### Rule 1: NEVER Commit or Push Directly to `main`
- Direct commits and direct pushes to the `main` branch are **strictly prohibited**.
- Before staging or committing any code, the AI must verify the active branch:
  ```bash
  git branch --show-current
  ```
- If the current branch is `main`, the AI **MUST** create and switch to a dedicated feature branch first:
  ```bash
  git checkout -b feature/m<module_number>-<descriptive-feature-name>
  ```

### Rule 2: NEVER Force Push
- The AI must **NEVER** propose or execute `git push --force` or `git push -f` under any circumstances.

### Rule 3: Mandatory Pre-Push Automated Test Verification
- Before pushing any branch to the remote repository, the AI **MUST** run the unit test suite and confirm 100% pass:
  ```bash
  python3 -m unittest discover -s tests
  ```
- If any test fails, the AI must fix the issue before pushing.

### Rule 4: Push to Feature Branch & Open PR
- Push exclusively to the feature branch:
  ```bash
  git push -u origin feature/m<module_number>-<feature-name>
  ```
- Instruct the user to open a Pull Request on GitHub targeting `main`.

---

## 🎯 2. Scope & Specification Discipline

1. **Authoritative Specification:** `PROJECT_SPEC.md` is the single source of truth. Do not invent out-of-scope features.
2. **Locked Baseline:**
   - 2 Arenas (Kepler Relay, Sundered Rift)
   - Linked Rift Beacon Teleportation (Required)
   - Dual Camera (1st-person & 3rd-person)
   - Procedural Astronaut & Alien Generator
   - Hitscan Combat & Projectiles
   - Chrono Slow (5-second 30% time dilation, activated only at 100% charge, resets to 0%)
   - 2D Orthographic HUD (Health, Chrono bar, Crosshair, Score, Objective)
   - 2 Enemy Types (Stalker, Spitter) + 1 Boss (Rift Guardian)
3. **Strictly Prohibited / Removed Systems:**
   - Do NOT implement full-world rewind or historical buffers.
   - Do NOT implement arbitrary wall/ceiling gravity everywhere (keep standard vertical gravity).
   - Do NOT implement Inverse Kinematics (use forward hierarchical joint trigonometry).
   - Do NOT implement multiple bosses, skill trees, or economy systems.
   - Do NOT implement physically simulated optical wormholes.

---

## 👥 3. Module Ownership Boundaries

| Module | Directory | Ownership & Deliverables |
|---|---|---|
| **M1** | `src/M1_player_camera/` | Astronaut rig, 1P/3P cameras, movement kinematics, weapon 3D mesh & viewmodel, Blink (stretch) |
| **M2** | `src/M2_enemies_combat/` | Alien generator, melee/ranged AI, boss, weapon gameplay logic, raycasting, damage |
| **M3** | `src/M3_world_teleport/` | Kepler Relay, Sundered Rift, environment generator, Rift Beacon platform (REQUIRED) |
| **M4** | `src/M4_rendering_gameplay/` | Master renderer, lighting, particles, effects, Chrono Slow manager, HUD overlay, game state |
| **Shared** | `src/shared/` | Constants, math3d, collision geometry (`src/shared/collision.py`), input manager, game time |
