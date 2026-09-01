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

    def get_cooldown_ratio(self) -> float:
        """Returns 0.0 (just fired) to 1.0 (ready to fire)."""
        return min(1.0, self.time_since_last_shot / self.cooldown)


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
        offset_right: float = 0.26,
        offset_up: float = -0.20,
        offset_forward: float = 0.50
    ):
        """
        Converts the camera-space weapon viewmodel muzzle position into world coordinates.
        Aligned directly with the 1P blaster rifle muzzle on screen.
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
        Uses an isolated camera projection so it never clips into arena walls or alters world matrices.
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

        from src.M4_rendering_gameplay.materials import Materials
        from src.M4_rendering_gameplay.primitives import Primitives

        try:
            # Dynamic firing recoil and idle bobbing
            recoil_z = -0.09 * max(0.0, 1.0 - (self.time_since_last_shot / 0.10)) if self.is_firing_effect_active else 0.0

            # Position weapon in bottom-right foreground
            glTranslatef(0.30, -0.24, -0.66 + recoil_z)
            glRotatef(-6.0, 0.0, 1.0, 0.0)
            glRotatef(2.0, 1.0, 0.0, 0.0)

            # 1. Main Rifle Receiver Chassis (Textured gunmetal alloy)
            Materials.bind_metal_wall_material()
            glColor3f(0.85, 0.90, 0.95)
            glPushMatrix()
            glScalef(0.10, 0.14, 0.60)
            Primitives.draw_textured_cube(1.0)
            glPopMatrix()
            Materials.unbind_all()

            # 2. Glowing Cyan Plasma Energy Rail (along upper receiver)
            glColor3f(0.0, 0.95, 1.0)
            glPushMatrix()
            glTranslatef(0.0, 0.08, -0.02)
            glScalef(0.045, 0.035, 0.46)
            Primitives.draw_textured_cube(1.0)
            glPopMatrix()

            # 3. Holographic Sight on Top with glowing lens
            glColor3f(0.2, 0.25, 0.35)
            glPushMatrix()
            glTranslatef(0.0, 0.115, -0.15)
            glScalef(0.05, 0.05, 0.12)
            Primitives.draw_textured_cube(1.0)
            # Glowing reticle
            glColor3f(0.0, 1.0, 0.9)
            glTranslatef(0.0, 0.0, 0.06)
            glutSolidSphere(0.02, 6, 6)
            glPopMatrix()

            # 4. Stepped Barrel with Heat Shroud
            Materials.bind_metal_wall_material()
            glColor3f(0.70, 0.75, 0.82)
            glPushMatrix()
            glTranslatef(0.0, 0.015, 0.38)
            glScalef(0.065, 0.065, 0.22)
            Primitives.draw_textured_cube(1.0)
            glPopMatrix()
            Materials.unbind_all()

            # 5. Flared Muzzle Brake with Glowing Core Tip
            glColor3f(0.3, 0.35, 0.45)
            glPushMatrix()
            glTranslatef(0.0, 0.015, 0.50)
            glScalef(0.08, 0.08, 0.06)
            Primitives.draw_textured_cube(1.0)
            # Glowing cyan emitter tip
            glColor3f(0.0, 1.0, 1.0)
            glTranslatef(0.0, 0.0, 0.03)
            glutSolidSphere(0.03, 8, 8)
            glPopMatrix()

            # 6. Lower Magazine / Power Pack
            glColor3f(0.2, 0.22, 0.28)
            glPushMatrix()
            glTranslatef(0.0, -0.10, -0.05)
            glRotatef(12.0, 1.0, 0.0, 0.0)
            glScalef(0.065, 0.12, 0.12)
            Primitives.draw_textured_cube(1.0)
            glPopMatrix()

            # 7. Muzzle Flash Flare on Fire
            if self.is_firing_effect_active:
                glDisable(GL_LIGHTING)
                glColor4f(0.4, 1.0, 1.0, 0.9)
                glPushMatrix()
                glTranslatef(0.0, 0.015, 0.56)
                glutSolidSphere(0.085, 10, 10)
                glColor4f(0.0, 0.85, 1.0, 0.6)
                glutSolidTorus(0.018, 0.10, 8, 16)
                glPopMatrix()
                glEnable(GL_LIGHTING)

        finally:
            glEnable(GL_DEPTH_TEST)
            glMatrixMode(GL_MODELVIEW)
            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)




