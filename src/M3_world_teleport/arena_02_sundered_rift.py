"""Arena 2: Sundered Rift Floating Void Asteroid."""
from OpenGL.GL import *
from OpenGL.GLUT import *
from src.shared.constants import ARENA_01_KEPLER_RELAY, ARENA_02_SUNDERED_RIFT
from src.shared.math3d import Vector3
from src.M3_world_teleport.arena_base import ArenaBase
from src.M3_world_teleport.rift_beacon import RiftBeacon
from src.M3_world_teleport.rift_energy_pickup import RiftEnergyPickup
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
        # Collectible Rift Energy Crystals in Sundered Rift
        self.energy_pickups = [
            RiftEnergyPickup(Vector3(25.0, 0.0, 10.0)),
            RiftEnergyPickup(Vector3(-25.0, 0.0, 10.0)),
            RiftEnergyPickup(Vector3(0.0, 0.0, 30.0)),
            RiftEnergyPickup(Vector3(20.0, 0.0, 40.0)),
            RiftEnergyPickup(Vector3(-20.0, 0.0, 40.0)),
        ]

    def draw(self):
        # 1. Main Obsidian Island (Textured Rock)
        from src.M4_rendering_gameplay.materials import Materials
        glPushMatrix()
        Materials.bind_rock_material()
        glColor3f(0.85, 0.8, 0.9)
        glBegin(GL_POLYGON)
        glNormal3f(0.0, 1.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-45.0, 0.0, -55.0)
        glTexCoord2f(8.0, 0.0); glVertex3f(45.0, 0.0, -55.0)
        glTexCoord2f(10.0, 6.0); glVertex3f(60.0, 0.0, 20.0)
        glTexCoord2f(8.0, 10.0); glVertex3f(40.0, 0.0, 65.0)
        glTexCoord2f(2.0, 10.0); glVertex3f(-40.0, 0.0, 65.0)
        glTexCoord2f(0.0, 6.0); glVertex3f(-60.0, 0.0, 20.0)
        glEnd()
        Materials.unbind_all()

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

        # 4. Collectible Rift Energy Crystals
        for pickup in self.energy_pickups:
            pickup.draw()
