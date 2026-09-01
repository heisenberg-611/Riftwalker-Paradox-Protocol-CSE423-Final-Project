"""Rift Beacon Interactive Teleportation Pillar."""
from OpenGL.GL import *
from OpenGL.GLUT import *
from src.shared.math3d import Vector3
from src.shared.constants import TELEPORT_ACTIVATION_RADIUS


class RiftBeacon:
    def __init__(self, beacon_id: str, pos: Vector3, linked_arena_id: str):
        self.beacon_id = beacon_id
        self.position = pos
        self.linked_arena_id = linked_arena_id
        self.activation_radius = TELEPORT_ACTIVATION_RADIUS
        self.is_active = True
        self.rotation_angle = 0.0

    def update(self, dt: float):
        self.rotation_angle += dt * 60.0

    def is_player_in_range(self, player_pos: Vector3) -> bool:
        return self.position.distance_to(player_pos) <= self.activation_radius

    def draw(self):
        from src.M4_rendering_gameplay.materials import Materials
        from src.M4_rendering_gameplay.primitives import Primitives
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)

        # 1. Base Pedestal (Textured with Beacon Runes)
        Materials.bind_beacon_material()
        glColor3f(0.85, 0.95, 1.0)
        glPushMatrix()
        glTranslatef(0.0, 0.2, 0.0)
        glScalef(2.2, 0.4, 2.2)
        Primitives.draw_textured_cube(1.0)
        glPopMatrix()

        # 2. Central Core Column
        glPushMatrix()
        glTranslatef(0.0, 1.8, 0.0)
        glScalef(0.5, 3.2, 0.5)
        Primitives.draw_textured_cube(1.0)
        glPopMatrix()
        Materials.unbind_all()


        # 3. Rotating Dual Concentric Torus Rings (Cyan when active, Amber when locked)
        if self.is_active:
            glColor3f(0.0, 0.90, 1.0)
        else:
            glColor3f(0.85, 0.45, 0.1)

        glPushMatrix()
        glTranslatef(0.0, 2.2, 0.0)
        glRotatef(self.rotation_angle, 0.0, 1.0, 0.0)
        glRotatef(30.0, 1.0, 0.0, 0.0)
        glutSolidTorus(0.08, 1.2, 12, 24)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.0, 2.2, 0.0)
        glRotatef(-self.rotation_angle * 1.5, 0.0, 1.0, 0.0)
        glRotatef(-30.0, 1.0, 0.0, 0.0)
        glutSolidTorus(0.06, 0.85, 12, 24)
        glPopMatrix()

        # 4. Floating Pulsing Energy Orb in center
        if self.is_active:
            glColor3f(0.2, 0.95, 1.0)
        else:
            glColor3f(1.0, 0.55, 0.1)

        glPushMatrix()
        glTranslatef(0.0, 2.2, 0.0)
        glutSolidSphere(0.35, 14, 14)
        glPopMatrix()

        glPopMatrix()
