# Computer Graphics Techniques to Emphasize in CSE423

This project highlights key computer graphics principles covered in CG423:

## 1. Hierarchical Modeling & Matrix Stacks
- **Astronaut Character**: Articulated character model consisting of 10+ sub-meshes (torso, backpack, head, helmet visor, upper/lower arms, hands, weapon, thighs, shins, boots).
- Utilizes nested `glPushMatrix()` / `glPopMatrix()`, `glTranslate()`, `glRotate()`, and `glScale()` transformations.
- Articulated walking and weapon-aiming animations driven by sinusoidal limb angle functions.

## 2. Procedural Mesh Generation
- **Alien Creature Generator**: Dynamic generation of alien bodies with segmented carapaces, multi-jointed spider/insectoid legs, mandibles, and glowing bioluminescent organ sacs.
- Modular primitive assembly (spheres, cylinders, cones, toruses, prisms) without external heavy asset files.

## 3. Dual Camera Projections & Transformations
- **Third-Person Camera**: Spherical coordinate-to-Cartesian orbit tracking with smooth interpolation and pitch clamping.
- **First-Person Camera**: Direct eye-point placement, weapon viewmodel offset, and synchronization with crosshair aiming vectors.
- Transitioning with proper `gluLookAt` and `gluPerspective` matrix configurations.

## 4. Multi-Source Dynamic Lighting & Material Properties
- **Directional Sunlight (`GL_LIGHT0`)**: Ambient and diffuse simulation of alien planetary sunlight.
- **Dynamic Point Lights (`GL_LIGHT1`, `GL_LIGHT2`, `GL_LIGHT3`)**:
  - Pulsing cyan/violet light from active Rift Beacons with quadratic distance attenuation.
  - Brief high-intensity yellow/white muzzle flashes upon weapon discharge.
  - Bioluminescent pulsing glow around alien boss weakpoints.
- **Material Presets**: Configured `glMaterialfv` ambient, diffuse, specular, and shininess values for metallic armor, polished glass visors, and organic alien chrysalis.

## 5. Particle Systems
- Emitters with randomized velocity distributions, life timers, alpha fading, and gravity modifiers:
  - **Rift Portal Swirl**: Orbiting vortex particles.
  - **Laser/Muzzle Flash**: Bright expanding spark billow.
  - **Blood / Damage Splatter**: Directional splatter on projectile impacts.
  - **Jetpack Thrusters**: Continuous trailing exhaust plume.

## 6. Raycasting & Spatial Collision
- Hitscan ray-sphere and ray-AABB intersection calculations in 3D world space.
- Bounding sphere & box player-world obstacle resolution.

## 7. 2D Orthographic Overlay (HUD)
- Matrix mode switching (`GL_PROJECTION` -> `glOrtho` and back to `gluPerspective`).
- Depth buffer masking (`glDisable(GL_DEPTH_TEST)`) for crisp HUD rendering of health bars, crosshairs, chrono energy gauges, and score counters.
