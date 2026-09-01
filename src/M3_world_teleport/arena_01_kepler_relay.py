"""Arena 1: Kepler Relay Outpost."""
from OpenGL.GL import *
from OpenGL.GLUT import *
from src.shared.constants import ARENA_01_KEPLER_RELAY, ARENA_02_SUNDERED_RIFT
from src.shared.math3d import Vector3
from src.M3_world_teleport.arena_base import ArenaBase
from src.M3_world_teleport.rift_beacon import RiftBeacon
from src.M3_world_teleport.rift_energy_pickup import RiftEnergyPickup
from src.M3_world_teleport.environment_generator import EnvironmentGenerator


class ArenaKeplerRelay(ArenaBase):
    def __init__(self):
        super().__init__(arena_id=ARENA_01_KEPLER_RELAY, half_extent=55.0)
        # Center Rift Beacon linking to Arena 2
        self.rift_beacons.append(
            RiftBeacon("BEACON_KEPLER_MAIN", Vector3(0.0, 0.0, 0.0), ARENA_02_SUNDERED_RIFT)
        )
        self.pillars = [
            Vector3(25.0, 0.0, 25.0),
            Vector3(-25.0, 0.0, 25.0),
            Vector3(25.0, 0.0, -25.0),
            Vector3(-25.0, 0.0, -25.0),
        ]
        self.crates = [
            Vector3(15.0, 0.0, 8.0),
            Vector3(-18.0, 0.0, 12.0),
            Vector3(10.0, 0.0, -20.0),
            Vector3(-14.0, 0.0, -15.0),
        ]
        # Collectible Rift Energy Crystals
        self.energy_pickups = [
            RiftEnergyPickup(Vector3(18.0, 0.0, 18.0)),
            RiftEnergyPickup(Vector3(-18.0, 0.0, 18.0)),
            RiftEnergyPickup(Vector3(18.0, 0.0, -18.0)),
            RiftEnergyPickup(Vector3(-18.0, 0.0, -18.0)),
        ]

    def draw(self):
        # 1. Floor Grid / Textured Metallic Platform
        glPushMatrix()
        from src.M4_rendering_gameplay.materials import Materials
        from src.M4_rendering_gameplay.primitives import Primitives
        Materials.bind_floor_panel_material()
        glColor3f(1.0, 1.0, 1.0)
        Primitives.draw_textured_plane(self.half_extent * 2, self.half_extent * 2, u_repeat=12.0, v_repeat=12.0)
        Materials.unbind_all()
        glPopMatrix()


        # 2. Outer Perimeter Barrier Walls (Textured)
        Materials.bind_metal_wall_material()
        glColor3f(0.8, 0.85, 0.9)
        wall_h = 6.0
        glPushMatrix()
        # North wall
        glTranslatef(0.0, wall_h * 0.5, self.half_extent)
        glScalef(self.half_extent * 2, wall_h, 1.5)
        Primitives.draw_textured_cube(1.0, u_repeat=8.0, v_repeat=1.0)
        glPopMatrix()

        glPushMatrix()
        # South wall
        glTranslatef(0.0, wall_h * 0.5, -self.half_extent)
        glScalef(self.half_extent * 2, wall_h, 1.5)
        Primitives.draw_textured_cube(1.0, u_repeat=8.0, v_repeat=1.0)
        glPopMatrix()

        glPushMatrix()
        # East wall
        glTranslatef(self.half_extent, wall_h * 0.5, 0.0)
        glScalef(1.5, wall_h, self.half_extent * 2)
        Primitives.draw_textured_cube(1.0, u_repeat=8.0, v_repeat=1.0)
        glPopMatrix()

        glPushMatrix()
        # West wall
        glTranslatef(-self.half_extent, wall_h * 0.5, 0.0)
        glScalef(1.5, wall_h, self.half_extent * 2)
        Primitives.draw_textured_cube(1.0, u_repeat=8.0, v_repeat=1.0)
        glPopMatrix()
        Materials.unbind_all()


        # 3. Modular Obstacles
        for p in self.pillars:
            EnvironmentGenerator.draw_pillar(p)
        for c in self.crates:
            EnvironmentGenerator.draw_crate(c)

        # 4. Rift Beacons
        for beacon in self.rift_beacons:
            beacon.draw()

        # 5. Collectible Rift Energy Pickups
        for pickup in self.energy_pickups:
            pickup.draw()
