"""Arena 2: Sundered Rift Floating Void Asteroid."""
from OpenGL.GL import *
from OpenGL.GLUT import *
from src.shared.constants import ARENA_01_KEPLER_RELAY, ARENA_02_SUNDERED_RIFT
from src.shared.math3d import Vector3
from src.M3_world_teleport.arena_base import ArenaBase
from src.M3_world_teleport.rift_beacon import RiftBeacon
from src.M3_world_teleport.environment_generator import EnvironmentGenerator


class ArenaSunderedRift(ArenaBase):
    def __init__(self):
        super().__init__(arena_id=ARENA_02_SUNDERED_RIFT, half_extent=70.0)
        # Arrival Beacon linking back to Kepler Relay
        self.rift_beacons.append(
            RiftBeacon("BEACON_SUNDERED_RETURN", Vector3(0.0, 0.0, -45.0), ARENA_01_KEPLER_RELAY)
        )
        self.crystal_spires = [
            Vector3(35.0, 0.0, 20.0),
            Vector3(-35.0, 0.0, 20.0),
            Vector3(20.0, 0.0, 45.0),
            Vector3(-20.0, 0.0, 45.0),
            Vector3(0.0, 0.0, 55.0),
        ]

    def draw(self):
        # 1. Main Obsidian Island
        glPushMatrix()
        glColor3f(0.12, 0.08, 0.16)
        glBegin(GL_POLYGON)
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(-45.0, 0.0, -55.0)
        glVertex3f(45.0, 0.0, -55.0)
        glVertex3f(60.0, 0.0, 20.0)
        glVertex3f(40.0, 0.0, 65.0)
        glVertex3f(-40.0, 0.0, 65.0)
        glVertex3f(-60.0, 0.0, 20.0)
        glEnd()

        # Neon Purple Anomaly Grid
        glColor3f(0.6, 0.1, 0.7)
        glBegin(GL_LINE_LOOP)
        glVertex3f(-45.0, 0.02, -55.0)
        glVertex3f(45.0, 0.02, -55.0)
        glVertex3f(60.0, 0.02, 20.0)
        glVertex3f(40.0, 0.02, 65.0)
        glVertex3f(-40.0, 0.02, 65.0)
        glVertex3f(-60.0, 0.02, 20.0)
        glEnd()
        glPopMatrix()

        # 2. Floating Void Crystal Spires
        for spire in self.crystal_spires:
            EnvironmentGenerator.draw_crystal_spire(spire)

        # 3. Rift Beacons
        for beacon in self.rift_beacons:
            beacon.draw()
