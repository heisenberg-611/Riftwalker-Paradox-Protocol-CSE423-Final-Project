"""First-Person Perspective Camera."""
import math
from OpenGL.GLU import gluLookAt
from src.shared.math3d import Vector3, clamp


class FirstPersonCamera:
    def __init__(self):
        self.pitch = 0.0
        self.yaw = 0.0
        self.eye_height = 2.1

    def update_orientation(self, mouse_dx: float, mouse_dy: float, sensitivity: float = 0.2):
        self.yaw -= mouse_dx * sensitivity
        self.pitch -= mouse_dy * sensitivity
        self.pitch = clamp(self.pitch, -85.0, 85.0)

    def apply(self, player_pos: Vector3):
        rad_yaw = math.radians(self.yaw)
        rad_pitch = math.radians(self.pitch)

        forward = Vector3(
            math.sin(rad_yaw) * math.cos(rad_pitch),
            math.sin(rad_pitch),
            math.cos(rad_yaw) * math.cos(rad_pitch)
        )

        eye = Vector3(player_pos.x, player_pos.y + self.eye_height, player_pos.z)
        target = eye + forward

        gluLookAt(
            eye.x, eye.y, eye.z,
            target.x, target.y, target.z,
            0.0, 1.0, 0.0
        )
