"""Procedural Hierarchical Astronaut Rig with nested Matrix Transformations."""
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class AstronautRig:
    """
    Articulated Astronaut Model:
    Torso -> Head (Visor) -> Backpack (Thrusters) -> Left/Right Arms -> Left/Right Legs
    Uses nested glPushMatrix/glPopMatrix calls.
    """
    def __init__(self):
        self.walk_phase = 0.0
        self.quadric = gluNewQuadric()

    def draw(self, is_moving: bool = False, dt: float = 0.016, aim_pitch: float = 0.0):
        if is_moving:
            self.walk_phase += dt * 8.0
        else:
            self.walk_phase = 0.0

        leg_swing = math.sin(self.walk_phase) * 28.0
        arm_swing = -leg_swing

        from src.M4_rendering_gameplay.materials import Materials
        from src.M4_rendering_gameplay.primitives import Primitives

        glPushMatrix()
        # Scale to standard player height
        glScalef(1.2, 1.2, 1.2)

        # 1. Torso (Textured Hex-Weave Suit)
        Materials.bind_suit_material()
        glColor3f(0.95, 0.98, 1.0)
        glPushMatrix()
        glTranslatef(0.0, 1.4, 0.0)
        glScalef(0.6, 0.8, 0.4)
        Primitives.draw_textured_cube(1.0)
        glPopMatrix()

        # 2. Chest Armor Plate
        glColor3f(0.3, 0.4, 0.55)
        glPushMatrix()
        glTranslatef(0.0, 1.5, 0.22)
        glScalef(0.45, 0.4, 0.1)
        Primitives.draw_textured_cube(1.0)
        glPopMatrix()

        # 3. Backpack / Life Support & Thrusters
        glColor3f(0.35, 0.4, 0.48)
        glPushMatrix()
        glTranslatef(0.0, 1.45, -0.3)
        glScalef(0.5, 0.7, 0.25)
        Primitives.draw_textured_cube(1.0)
        # Thruster Nozzles
        glColor3f(0.1, 0.8, 1.0)  # Cyan glowing thruster nozzles
        glTranslatef(-0.15, -0.35, 0.0)
        glutSolidSphere(0.08, 10, 10)
        glTranslatef(0.3, 0.0, 0.0)
        glutSolidSphere(0.08, 10, 10)
        glPopMatrix()

        # 4. Helmet & Visor
        glColor3f(0.92, 0.95, 1.0)
        glPushMatrix()
        glTranslatef(0.0, 2.0, 0.0)
        Primitives.draw_textured_sphere(0.28, 16, 16)
        Materials.unbind_all()

        # Gold/Cyan Visor (Textured polarized horizon glare)
        Materials.bind_visor_material()
        glColor3f(0.2, 0.9, 1.0)
        glTranslatef(0.0, 0.02, 0.14)
        glScalef(0.22, 0.16, 0.18)
        Primitives.draw_textured_sphere(1.0, 14, 14)
        Materials.unbind_all()
        glPopMatrix()

        # 5. Left Arm
        Materials.bind_suit_material()
        glPushMatrix()
        glTranslatef(-0.42, 1.7, 0.0)
        glRotatef(arm_swing, 1.0, 0.0, 0.0)
        glColor3f(0.9, 0.92, 0.96)
        # Shoulder
        Primitives.draw_textured_sphere(0.12, 10, 10)
        # Upper arm
        glTranslatef(0.0, -0.25, 0.0)
        glPushMatrix()
        glScalef(0.15, 0.35, 0.15)
        Primitives.draw_textured_cube(1.0)
        glPopMatrix()
        # Forearm & Hand
        glTranslatef(0.0, -0.25, 0.0)
        glColor3f(0.3, 0.35, 0.42)
        Primitives.draw_textured_sphere(0.1, 8, 8)
        glPopMatrix()

        # 6. Right Arm & Weapon (Articulated with vertical aim pitch)
        glPushMatrix()
        glTranslatef(0.42, 1.7, 0.0)
        glRotatef(-arm_swing + aim_pitch, 1.0, 0.0, 0.0)
        glColor3f(0.9, 0.92, 0.96)
        # Shoulder
        Primitives.draw_textured_sphere(0.12, 10, 10)
        # Upper arm
        glTranslatef(0.0, -0.25, 0.0)
        glPushMatrix()
        glScalef(0.15, 0.35, 0.15)
        Primitives.draw_textured_cube(1.0)
        glPopMatrix()
        # Forearm
        glTranslatef(0.0, -0.25, 0.0)
        glColor3f(0.3, 0.35, 0.42)
        Primitives.draw_textured_sphere(0.1, 8, 8)
        Materials.unbind_all()

        # Weapon in right hand (Textured gunmetal alloy)
        Materials.bind_metal_wall_material()
        glColor3f(0.7, 0.75, 0.85)
        glTranslatef(0.0, 0.0, 0.2)
        glScalef(0.1, 0.12, 0.45)
        Primitives.draw_textured_cube(1.0)
        Materials.unbind_all()
        glPopMatrix()

        # 7. Left Leg
        Materials.bind_suit_material()
        glPushMatrix()
        glTranslatef(-0.2, 0.95, 0.0)
        glRotatef(leg_swing, 1.0, 0.0, 0.0)
        glColor3f(0.85, 0.88, 0.92)
        # Hip
        Primitives.draw_textured_sphere(0.12, 10, 10)
        # Thigh
        glTranslatef(0.0, -0.3, 0.0)
        glPushMatrix()
        glScalef(0.18, 0.45, 0.18)
        Primitives.draw_textured_cube(1.0)
        glPopMatrix()
        # Shin & Boot
        glTranslatef(0.0, -0.35, 0.0)
        glColor3f(0.3, 0.32, 0.38)
        glPushMatrix()
        glScalef(0.2, 0.35, 0.25)
        Primitives.draw_textured_cube(1.0)
        glPopMatrix()
        glPopMatrix()

        # 8. Right Leg
        glPushMatrix()
        glTranslatef(0.2, 0.95, 0.0)
        glRotatef(-leg_swing, 1.0, 0.0, 0.0)
        glColor3f(0.85, 0.88, 0.92)
        # Hip
        Primitives.draw_textured_sphere(0.12, 10, 10)
        # Thigh
        glTranslatef(0.0, -0.3, 0.0)
        glPushMatrix()
        glScalef(0.18, 0.45, 0.18)
        Primitives.draw_textured_cube(1.0)
        glPopMatrix()
        # Shin & Boot
        glTranslatef(0.0, -0.35, 0.0)
        glColor3f(0.3, 0.32, 0.38)
        glPushMatrix()
        glScalef(0.2, 0.35, 0.25)
        Primitives.draw_textured_cube(1.0)
        glPopMatrix()
        glPopMatrix()
        Materials.unbind_all()

        glPopMatrix()


    def get_tp_muzzle_world(self, player_pos, yaw: float, pitch: float = 0.0):
        """
        Calculates the world-space position of the rifle barrel muzzle in the astronaut's right hand.
        """
        rad_yaw = math.radians(yaw)
        cos_y = math.cos(rad_yaw)
        sin_y = math.sin(rad_yaw)

        # Local arm base position (scaled by 1.2)
        local_x = 0.42 * 1.2  # ~0.504
        local_y = 1.70 * 1.2  # ~2.04

        rad_pitch = math.radians(pitch)
        arm_len_y = -0.45 * math.cos(rad_pitch) + 0.35 * math.sin(rad_pitch)
        arm_len_z = 0.45 * math.cos(rad_pitch) + 0.35 * math.sin(rad_pitch)

        rel_y = local_y + arm_len_y
        rel_z = max(0.2, arm_len_z)

        from src.shared.math3d import Vector3
        world_x = player_pos.x + (local_x * cos_y + rel_z * sin_y)
        world_y = player_pos.y + rel_y
        world_z = player_pos.z + (-local_x * sin_y + rel_z * cos_y)

        return Vector3(world_x, world_y, world_z)

