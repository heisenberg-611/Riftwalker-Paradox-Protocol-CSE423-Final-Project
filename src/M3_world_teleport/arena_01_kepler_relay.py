"""Arena 1: Kepler Relay Outpost."""
from OpenGL.GL import *
from OpenGL.GLUT import *
from src.shared.constants import ARENA_01_KEPLER_RELAY, ARENA_02_SUNDERED_RIFT
from src.shared.math3d import Vector3
from src.M3_world_teleport.arena_base import ArenaBase
from src.M3_world_teleport.rift_beacon import RiftBeacon
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

    def draw(self):
        # 1. Floor Grid / Metallic Platform
        glPushMatrix()
        glColor3f(0.18, 0.22, 0.26)
        glBegin(GL_QUADS)
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(-self.half_extent, 0.0, -self.half_extent)
        glVertex3f(-self.half_extent, 0.0, self.half_extent)
        glVertex3f(self.half_extent, 0.0, self.half_extent)
        glVertex3f(self.half_extent, 0.0, -self.half_extent)
        glEnd()

        # Floor grid lines
        glColor3f(0.0, 0.5, 0.7)
        glBegin(GL_LINES)
        step = 5.0
        x = -self.half_extent
        while x <= self.half_extent:
            glVertex3f(x, 0.02, -self.half_extent)
            glVertex3f(x, 0.02, self.half_extent)
            x += step
        z = -self.half_extent
        while z <= self.half_extent:
            glVertex3f(-self.half_extent, 0.02, z)
            glVertex3f(self.half_extent, 0.02, z)
            z += step
        glEnd()
        glPopMatrix()

        # 2. Outer Perimeter Barrier Walls
        glColor3f(0.25, 0.28, 0.32)
        wall_h = 6.0
        glPushMatrix()
        # North wall
        glTranslatef(0.0, wall_h * 0.5, self.half_extent)
        glScalef(self.half_extent * 2, wall_h, 1.5)
        glutSolidCube(1.0)
        glPopMatrix()

        glPushMatrix()
        # South wall
        glTranslatef(0.0, wall_h * 0.5, -self.half_extent)
        glScalef(self.half_extent * 2, wall_h, 1.5)
        glutSolidCube(1.0)
        glPopMatrix()

        glPushMatrix()
        # East wall
        glTranslatef(self.half_extent, wall_h * 0.5, 0.0)
        glScalef(1.5, wall_h, self.half_extent * 2)
        glutSolidCube(1.0)
        glPopMatrix()

        glPushMatrix()
        # West wall
        glTranslatef(-self.half_extent, wall_h * 0.5, 0.0)
        glScalef(1.5, wall_h, self.half_extent * 2)
        glutSolidCube(1.0)
        glPopMatrix()

        # 3. Modular Obstacles
        for p in self.pillars:
            EnvironmentGenerator.draw_pillar(p)
        for c in self.crates:
            EnvironmentGenerator.draw_crate(c)

        # 4. Rift Beacons
        for beacon in self.rift_beacons:
            beacon.draw()
