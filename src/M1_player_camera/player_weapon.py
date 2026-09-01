"""Player Hitscan Weapon System and First-Person Viewmodel."""
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from src.shared.constants import PRIMARY_FIRE_COOLDOWN, PRIMARY_FIRE_DAMAGE, PRIMARY_FIRE_RANGE


class PlayerWeapon:
    def __init__(self):
        self.cooldown = PRIMARY_FIRE_COOLDOWN
        self.damage = PRIMARY_FIRE_DAMAGE
        self.range = PRIMARY_FIRE_RANGE
        self.time_since_last_shot = 999.0
        self.is_firing_effect_active = False

    def update(self, dt: float):
        self.time_since_last_shot += dt
        if self.time_since_last_shot > 0.08:
            self.is_firing_effect_active = False

    def can_fire(self) -> bool:
        return self.time_since_last_shot >= self.cooldown

    def trigger_shot(self) -> bool:
        if not self.can_fire():
            return False
        self.time_since_last_shot = 0.0
        self.is_firing_effect_active = True
        return True

    def get_fp_muzzle_world(
        self,
        camera_eye,
        camera_forward,
        camera_right,
        camera_up,
        offset_right: float = 0.35,
        offset_up: float = -0.28,
        offset_forward: float = 0.68
    ):
        """
        Converts the camera-space weapon viewmodel muzzle position into world coordinates.
        """
        return (
            camera_eye
            + camera_right * offset_right
            + camera_up * offset_up
            + camera_forward * offset_forward
        )

    def draw_viewmodel(self, width: int, height: int, is_moving: bool = False):

        """
        Renders the First-Person Sci-Fi Laser Rifle Viewmodel in the bottom-right foreground.
        Uses a dedicated camera projection so it never clips into arena walls.
        """
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        aspect = float(max(1, width)) / float(max(1, height))
        gluPerspective(52.0, aspect, 0.05, 50.0)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)

        # Dynamic firing recoil and idle bobbing
        recoil_z = -0.12 * max(0.0, 1.0 - (self.time_since_last_shot / 0.12)) if self.is_firing_effect_active else 0.0

        # Position weapon in bottom-right foreground
        glTranslatef(0.38, -0.32, -0.85 + recoil_z)
        glRotatef(-8.0, 0.0, 1.0, 0.0)
        glRotatef(4.0, 1.0, 0.0, 0.0)

        # 1. Main Rifle Body
        glColor3f(0.18, 0.20, 0.25)
        glPushMatrix()
        glScalef(0.12, 0.16, 0.75)
        glutSolidCube(1.0)
        glPopMatrix()

        # 2. Glowing Cyan Plasma Energy Rail
        glColor3f(0.0, 0.9, 1.0)
        glPushMatrix()
        glTranslatef(0.0, 0.09, -0.05)
        glScalef(0.05, 0.04, 0.6)
        glutSolidCube(1.0)
        glPopMatrix()

        # 3. Muzzle Barrel
        glColor3f(0.32, 0.35, 0.4)
        glPushMatrix()
        glTranslatef(0.0, 0.02, 0.42)
        glScalef(0.08, 0.08, 0.22)
        glutSolidCube(1.0)
        glPopMatrix()

        # 4. Muzzle Flash Flare on Fire
        if self.is_firing_effect_active:
            glDisable(GL_LIGHTING)
            glColor3f(0.2, 1.0, 1.0)
            glPushMatrix()
            glTranslatef(0.0, 0.02, 0.56)
            glutSolidSphere(0.08, 10, 10)
            glPopMatrix()
            glEnable(GL_LIGHTING)

        glEnable(GL_DEPTH_TEST)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
