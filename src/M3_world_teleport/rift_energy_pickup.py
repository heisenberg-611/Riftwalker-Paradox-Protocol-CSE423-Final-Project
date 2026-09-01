"""Rift Energy Collectible Pickup for Chrono Charge restoration."""
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from src.shared.math3d import Vector3
from src.shared.constants import CHRONO_CHARGE_PICKUP


class RiftEnergyPickup:
    """
    Floating glowing Rift Energy pickup crystal:
    - Provides instant Chrono Charge boost upon collection.
    - Features continuous vertical bobbing, dual-axis spinning, and a rotating halo ring.
    - Respawns after a cooldown period so arena traversal remains dynamic.
    """
    def __init__(self, position: Vector3, charge_amount: float = CHRONO_CHARGE_PICKUP):
        self.position = position
        self.radius = 1.4
        self.is_collected = False
        self.respawn_timer = 0.0
        self.respawn_delay = 15.0  # seconds
        self.charge_amount = charge_amount
        self.anim_time = 0.0

    def update(self, dt: float):
        self.anim_time += dt
        if self.is_collected:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0.0:
                self.is_collected = False

    def collect(self) -> float:
        """Collects the pickup, puts it on respawn cooldown, and returns charge gained."""
        if self.is_collected:
            return 0.0
        self.is_collected = True
        self.respawn_timer = self.respawn_delay
        return self.charge_amount

    def is_player_in_range(self, player_pos: Vector3, player_radius: float = 1.0) -> bool:
        """Checks sphere collision with player."""
        if self.is_collected:
            return False
        dist_sq = (self.position - player_pos).length_squared()
        combined_r = self.radius + player_radius
        return dist_sq <= (combined_r * combined_r)

    def draw(self):
        """Renders the glowing 3D crystal pickup in world space."""
        if self.is_collected:
            return

        glPushMatrix()
        hover_y = self.position.y + 1.2 + math.sin(self.anim_time * 3.5) * 0.25
        glTranslatef(self.position.x, hover_y, self.position.z)
        glRotatef(self.anim_time * 75.0, 0.0, 1.0, 0.0)
        glRotatef(20.0, 1.0, 0.0, 0.0)

        # 1. Pulsing Glowing Cyan Octahedron Core
        pulse = 1.0 + 0.12 * math.sin(self.anim_time * 6.0)
        glColor3f(0.0, 0.85 * pulse, 1.0)
        glPushMatrix()
        glScalef(0.45 * pulse, 0.7 * pulse, 0.45 * pulse)
        glutSolidOctahedron()
        glPopMatrix()

        # 2. Inner Magenta Energy Shards
        glColor3f(1.0, 0.2, 0.8)
        glPushMatrix()
        glRotatef(self.anim_time * -100.0, 0.0, 1.0, 0.0)
        glScalef(0.25, 0.4, 0.25)
        glutSolidCube(1.0)
        glPopMatrix()

        # 3. Orbiting Torus Energy Ring
        glColor4f(0.2, 0.8, 1.0, 0.75)
        glPushMatrix()
        glRotatef(self.anim_time * -120.0, 0.0, 0.0, 1.0)
        glutSolidTorus(0.04, 0.65, 8, 16)
        glPopMatrix()

        glPopMatrix()
