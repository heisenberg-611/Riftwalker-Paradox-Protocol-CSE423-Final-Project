"""Third-Person Orbit/Follow Camera aligned with Crosshair Targeting."""
import math
from OpenGL.GLU import gluLookAt
from src.shared.constants import (
    TP_CAM_DISTANCE,
    TP_CAM_HEIGHT,
    TP_CAM_PITCH_MIN,
    TP_CAM_PITCH_MAX,
    MOUSE_SENSITIVITY
)
from src.shared.math3d import Vector3, clamp


class ThirdPersonCamera:
    def __init__(self, distance: float = TP_CAM_DISTANCE, height: float = TP_CAM_HEIGHT):
        self.distance = distance
        self.height = height
        self.yaw = 0.0
        self.pitch = 0.0
        self.shoulder_offset = 1.15  # Offset to the right of the astronaut

    def update_orientation(self, mouse_dx: float, mouse_dy: float, sensitivity: float = MOUSE_SENSITIVITY):
        self.yaw -= mouse_dx * sensitivity
        self.pitch -= mouse_dy * sensitivity
        self.pitch = clamp(self.pitch, TP_CAM_PITCH_MIN, TP_CAM_PITCH_MAX)

    def get_aim_direction(self) -> Vector3:
        rad_yaw = math.radians(self.yaw)
        rad_pitch = math.radians(self.pitch)
        return Vector3(
            math.sin(rad_yaw) * math.cos(rad_pitch),
            math.sin(rad_pitch),
            math.cos(rad_yaw) * math.cos(rad_pitch)
        ).normalized()

    def get_basis_vectors(self):
        forward = self.get_aim_direction()
        world_up = Vector3(0.0, 1.0, 0.0)
        right = world_up.cross(forward)
        if right.length_squared() < 1e-6:
            right = Vector3(1.0, 0.0, 0.0)
        else:
            right = right.normalized()
        up = forward.cross(right).normalized()
        return forward, right, up

    def get_cam_eye(self, player_pos: Vector3) -> Vector3:
        forward, right, up = self.get_basis_vectors()
        # Over-the-shoulder placement: elevated, shifted right, pulled back along forward
        head_pos = Vector3(player_pos.x, player_pos.y + self.height, player_pos.z)
        cam_pos = head_pos + (right * self.shoulder_offset) + (up * 0.2) - (forward * self.distance)
        cam_pos.y = max(0.5, cam_pos.y)
        return cam_pos

    def apply(self, player_pos: Vector3):
        forward, right, up = self.get_basis_vectors()
        eye = self.get_cam_eye(player_pos)
        # Look forward into the world along the crosshair aim vector
        target = eye + forward * 100.0

        gluLookAt(
            eye.x, eye.y, eye.z,
            target.x, target.y, target.z,
            0.0, 1.0, 0.0
        )




