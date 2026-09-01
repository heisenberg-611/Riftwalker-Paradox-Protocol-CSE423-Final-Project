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

        # Weapon in right hand (Detailed Sci-Fi Laser Rifle)
        glPushMatrix()
        glTranslatef(0.0, -0.02, 0.12)

        # 1. Main Rifle Receiver Chassis (Textured gunmetal alloy)
        Materials.bind_metal_wall_material()
        glColor3f(0.75, 0.80, 0.88)
        glPushMatrix()
        glTranslatef(0.0, 0.0, 0.18)
        glScalef(0.09, 0.13, 0.44)
        Primitives.draw_textured_cube(1.0)
        glPopMatrix()

        # 2. Glowing Cyan Plasma Energy Rail (along upper receiver)
        Materials.unbind_all()
        glColor3f(0.0, 0.95, 1.0)
        glPushMatrix()
        glTranslatef(0.0, 0.07, 0.16)
        glScalef(0.045, 0.035, 0.34)
        Primitives.draw_textured_cube(1.0)
        glPopMatrix()

        # 3. Optical Holographic Sight (Raised top scope with glowing lens)
        glColor3f(0.2, 0.25, 0.32)
        glPushMatrix()
        glTranslatef(0.0, 0.105, 0.02)
        glScalef(0.055, 0.055, 0.14)
        Primitives.draw_textured_cube(1.0)
        # Glowing reticle lens
        glColor3f(0.1, 1.0, 0.9)
        glTranslatef(0.0, 0.0, 0.07)
        glutSolidSphere(0.025, 6, 6)
        glPopMatrix()

        # 4. Extended Stepped Barrel & Cylindrical Heat Shroud
        Materials.bind_metal_wall_material()
        glColor3f(0.65, 0.70, 0.78)
        glPushMatrix()
        glTranslatef(0.0, 0.015, 0.46)
        glScalef(0.065, 0.065, 0.26)
        Primitives.draw_textured_cube(1.0)
        glPopMatrix()

        # 5. Flared Muzzle Brake with Glowing Cyan Emitter
        Materials.unbind_all()
        glColor3f(0.25, 0.30, 0.40)
        glPushMatrix()
        glTranslatef(0.0, 0.015, 0.62)
        glScalef(0.08, 0.08, 0.08)
        Primitives.draw_textured_cube(1.0)
        # Glowing cyan laser emitter tip
        glColor3f(0.0, 1.0, 1.0)
        glTranslatef(0.0, 0.0, 0.04)
        glutSolidSphere(0.035, 8, 8)
        glPopMatrix()

        # 6. Lower Magazine / Battery Power Cell (Angled)
        glColor3f(0.2, 0.22, 0.28)
        glPushMatrix()
        glTranslatef(0.0, -0.10, 0.10)
        glRotatef(15.0, 1.0, 0.0, 0.0)
        glScalef(0.07, 0.12, 0.12)
        Primitives.draw_textured_cube(1.0)
        # Power charge level indicator
        glColor3f(0.0, 0.9, 1.0)
        glTranslatef(0.035, 0.0, 0.0)
        glScalef(0.015, 0.07, 0.05)
        Primitives.draw_textured_cube(1.0)
        glPopMatrix()

        glPopMatrix()  # End of weapon in right hand
        glPopMatrix()  # End of right arm

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
        scale = 1.2
        local_x = 0.42 * scale  # ~0.504
        local_y = 1.70 * scale  # ~2.04

        rad_pitch = math.radians(pitch)
        cos_p = math.cos(rad_pitch)
        sin_p = math.sin(rad_pitch)

        # Hand offset from shoulder joint in pitch-rotated arm frame
        arm_len = 0.50 * scale
        hand_rel_y = -arm_len * cos_p + 0.12 * sin_p
        hand_rel_z = arm_len * sin_p + 0.12 * cos_p

        # Gun barrel extends forward from hand along aim pitch
        gun_len = 0.66 * scale
        gun_rel_y = gun_len * sin_p
        gun_rel_z = gun_len * cos_p

        total_rel_y = local_y + hand_rel_y + gun_rel_y
        total_rel_z = hand_rel_z + gun_rel_z

        from src.shared.math3d import Vector3
        world_x = player_pos.x + (local_x * cos_y + total_rel_z * sin_y)
        world_y = player_pos.y + total_rel_y
        world_z = player_pos.z + (-local_x * sin_y + total_rel_z * cos_y)

        return Vector3(world_x, world_y, world_z)


