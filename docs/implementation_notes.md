# Implementation Notes & Guidelines

## 1. OpenGL Matrix Discipline
- Every drawing routine modifying matrix state (`glTranslate`, `glRotate`, `glScale`) must wrap its operations in `glPushMatrix()` and `glPopMatrix()`.
- Never leave dangling matrix state after a rendering function exits.

## 2. Fixed Timestep & Chrono Slow Scaling
- Time is managed through `game_time.py`.
- Two distinct delta-time values are provided each frame:
  - `unscaled_dt`: Real-time delta (used for player inputs, camera motion, HUD animations).
  - `game_dt = unscaled_dt * chrono_factor`: Time-scaled delta (used for enemies, projectiles, hazards, and boss animations).
- During Chrono Slow, `chrono_factor = 0.25` (enemies and bullets slow down to 25% speed, while player moves at 100% speed).

## 3. 2D HUD Rendering Protocol
To draw 2D HUD elements cleanly on top of the 3D scene:
```python
def begin_2d(width, height):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)

def end_2d():
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
```

## 4. Hierarchical Astronaut Articulation
The astronaut body hierarchy:
```text
Torso (Origin)
├── Helmet
│   └── Visor (Specular cyan)
├── Backpack (Thrusters with particle emitters)
├── Left Upper Arm
│   └── Left Forearm & Hand
├── Right Upper Arm
│   └── Right Forearm & Hand
│       └── Weapon Model (Muzzle Flash anchor)
├── Left Thigh
│   └── Left Shin & Boot
└── Right Thigh
    └── Right Shin & Boot
```
Each limb joint receives a rotational offset modulated by `sin(time * speed)`.
