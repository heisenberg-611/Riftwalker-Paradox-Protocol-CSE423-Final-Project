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

    def update_orientation(self, mouse_dx: float, mouse_dy: float, sensitivity: float = MOUSE_SENSITIVITY):
        self.yaw -= mouse_dx * sensitivity
        self.pitch -= mouse_dy * sensitivity
        self.pitch = clamp(self.pitch, TP_CAM_PITCH_MIN, TP_CAM_PITCH_MAX)

    def apply(self, player_pos: Vector3):
        rad_yaw = math.radians(self.yaw)
        rad_pitch = math.radians(self.pitch)

        # Forward look direction vector (identical to first-person and raycast aim)
        forward = Vector3(
            math.sin(rad_yaw) * math.cos(rad_pitch),
            math.sin(rad_pitch),
            math.cos(rad_yaw) * math.cos(rad_pitch)
        )

        # Target point on player (upper torso / head)
        target = Vector3(player_pos.x, player_pos.y + self.height, player_pos.z)

        # Calculate camera eye position along reverse look direction
        cam_x = target.x - forward.x * self.distance
        cam_y = max(0.4, target.y - forward.y * self.distance)  # Prevent floor clipping
        cam_z = target.z - forward.z * self.distance

        gluLookAt(
            cam_x, cam_y, cam_z,
            target.x, target.y, target.z,
            0.0, 1.0, 0.0
        )

