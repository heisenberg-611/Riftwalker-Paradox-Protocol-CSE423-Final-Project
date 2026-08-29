# Integration Audit: Assignment 3 & Starter Baseline

## Purpose
This document records the baseline mechanics and constraints inherited from the CG423 OpenGL course foundations (such as Assignment 3) to ensure seamless compatibility with starter code requirements.

## 1. Window & Callback Setup
- Window dimensions: Default `1024x768` (resizable via `reshapeListener`).
- Display mode: `GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH`.
- Callbacks:
  - `glutDisplayFunc(display)`: Main render pass.
  - `glutIdleFunc(idle)`: Main game update loop triggering `glutPostRedisplay()`.
  - `glutKeyboardFunc(keyboard_down)` / `glutKeyboardUpFunc(keyboard_up)`: Key state tracking.
  - `glutSpecialFunc(special_key)`: Arrow keys / Function keys.
  - `glutPassiveMotionFunc(mouse_motion)` / `glutMotionFunc(mouse_motion)`: Mouse look aiming.
  - `glutMouseFunc(mouse_button)`: Left/Right click shooting and interaction.

## 2. Coordinate System & Units
- Right-handed Cartesian 3D coordinates:
  - $+X$: Right
  - $+Y$: Up (Vertical axis)
  - $+Z$: Forward / Backward (Player depth)
- Floor is located at $Y = 0$.

## 3. Scope Upgrades from Assignment 3 Baseline
1. **Procedural Hierarchical Astronaut**: Upgrade from static primitives to fully articulated multi-joint rig with walking animation.
2. **Procedural Multi-Legged Aliens**: Upgrade from basic geometric enemies to multi-variant procedural alien generator.
3. **Dual-Arena World with Teleportation**: Upgrade from single flat arena to two distinct themed environments connected by animated Rift Beacons.
4. **Chrono Slow Time Dilation**: Distinct real-time vs. simulated-time delta scaling for bullet-time effects.
5. **Dynamic Lighting & Particle Systems**: Multi-source light attenuation, thruster trails, teleport vortexes, spark bursts.
