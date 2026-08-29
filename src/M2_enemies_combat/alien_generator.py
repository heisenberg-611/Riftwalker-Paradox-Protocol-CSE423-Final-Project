"""Procedural Alien Geometry Generator."""
import math
from OpenGL.GL import *
from OpenGL.GLUT import *


class AlienGenerator:
    """
    Generates procedural articulated alien geometry:
    Carapace / segmented abdomen + multi-jointed spider legs + mandibles + glowing eyes.
    """
    @staticmethod
    def draw_stalker(anim_time: float):
        glPushMatrix()
        # Abdomen / Carapace (Metallic Violet/Obsidian)
        glColor3f(0.35, 0.15, 0.45)
        glPushMatrix()
        glTranslatef(0.0, 0.8, 0.0)
        glScalef(0.7, 0.5, 1.1)
        glutSolidSphere(1.0, 12, 12)
        glPopMatrix()

        # Head & Glowing Eyes
        glPushMatrix()
        glTranslatef(0.0, 0.85, 0.9)
        glColor3f(0.25, 0.1, 0.35)
        glutSolidSphere(0.4, 10, 10)
        # 4 Bioluminescent Red/Pink Eyes
        glColor3f(1.0, 0.1, 0.3)
        for dx, dy in [(-0.15, 0.1), (0.15, 0.1), (-0.08, -0.05), (0.08, -0.05)]:
            glPushMatrix()
            glTranslatef(dx, dy, 0.32)
            glutSolidSphere(0.06, 6, 6)
            glPopMatrix()
        glPopMatrix()

        # 6 Articulated Crawling Legs
        glColor3f(0.2, 0.1, 0.25)
        for side in (-1, 1):
            for i, z_offset in enumerate([-0.4, 0.0, 0.4]):
                phase = anim_time * 6.0 + (i * 1.2) * side
                leg_rot = math.sin(phase) * 25.0

                glPushMatrix()
                glTranslatef(side * 0.5, 0.7, z_offset)
                glRotatef(side * 35.0, 0.0, 1.0, 0.0)
                glRotatef(leg_rot, 1.0, 0.0, 0.0)

                # Upper leg segment
                glPushMatrix()
                glRotatef(side * -30.0, 0.0, 0.0, 1.0)
                glTranslatef(side * 0.3, 0.1, 0.0)
                glScalef(0.6, 0.1, 0.1)
                glutSolidCube(1.0)
                glPopMatrix()

                # Lower leg segment
                glPushMatrix()
                glTranslatef(side * 0.6, -0.25, 0.0)
                glRotatef(side * 45.0, 0.0, 0.0, 1.0)
                glScalef(0.1, 0.7, 0.1)
                glutSolidCube(1.0)
                glPopMatrix()

                glPopMatrix()

        glPopMatrix()

    @staticmethod
    def draw_spitter(anim_time: float):
        glPushMatrix()
        # Bulbous Acid-Sac Abdomen (Toxic Bioluminescent Green/Cyan)
        pulse = 1.0 + 0.08 * math.sin(anim_time * 4.0)
        glColor3f(0.1, 0.75, 0.6)
        glPushMatrix()
        glTranslatef(0.0, 1.2, -0.4)
        glScalef(0.9 * pulse, 0.8 * pulse, 1.2 * pulse)
        glutSolidSphere(1.0, 12, 12)
        glPopMatrix()

        # Thorax & Spitter Cannon Head
        glColor3f(0.3, 0.35, 0.3)
        glPushMatrix()
        glTranslatef(0.0, 1.1, 0.6)
        glScalef(0.5, 0.5, 0.8)
        glutSolidCube(1.0)
        # Acid Cannon Muzzle
        glColor3f(0.0, 1.0, 0.5)
        glTranslatef(0.0, 0.0, 0.6)
        glutSolidTorus(0.08, 0.18, 8, 12)
        glPopMatrix()

        # 4 Tripod/Quad Legs
        glColor3f(0.2, 0.25, 0.2)
        for side in (-1, 1):
            for z_offset in [-0.2, 0.5]:
                glPushMatrix()
                glTranslatef(side * 0.6, 0.9, z_offset)
                glScalef(0.15, 1.1, 0.15)
                glutSolidCube(1.0)
                glPopMatrix()

        glPopMatrix()

    @staticmethod
    def draw_guardian_boss(anim_time: float):
        glPushMatrix()
        # Giant Central Core
        pulse = 1.0 + 0.05 * math.sin(anim_time * 2.0)
        glColor3f(0.8, 0.1, 0.2)
        glPushMatrix()
        glTranslatef(0.0, 3.5, 0.0)
        glScalef(1.8 * pulse, 2.2 * pulse, 1.8 * pulse)
        glutSolidSphere(1.0, 16, 16)
        glPopMatrix()

        # Rotating Shield Shards (Orbital Shielding)
        rot_shield = anim_time * 45.0
        glColor3f(0.2, 0.15, 0.3)
        for i in range(4):
            glPushMatrix()
            glTranslatef(0.0, 3.5, 0.0)
            glRotatef(rot_shield + i * 90.0, 0.0, 1.0, 0.0)
            glTranslatef(3.2, 0.0, 0.0)
            glScalef(0.4, 2.0, 1.0)
            glutSolidCube(1.0)
            glPopMatrix()

        glPopMatrix()
