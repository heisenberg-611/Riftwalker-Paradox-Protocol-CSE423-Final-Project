"""Third-Person Orbit/Follow Camera."""
import math
from OpenGL.GLU import gluLookAt
from src.shared.constants import TP_CAM_DISTANCE, TP_CAM_HEIGHT, TP_CAM_PITCH_MIN, TP_CAM_PITCH_MAX
from src.shared.math3d import Vector3, clamp


class ThirdPersonCamera:
    def __init__(self, distance: float = TP_CAM_DISTANCE, height: float = TP_CAM_HEIGHT):
        self.distance = distance
        self.height = height
        self.yaw = 0.0
        self.pitch = 15.0

    def update_orientation(self, mouse_dx: float, mouse_dy: float, sensitivity: float = 0.2):
        self.yaw -= mouse_dx * sensitivity
        self.pitch -= mouse_dy * sensitivity
        self.pitch = clamp(self.pitch, TP_CAM_PITCH_MIN, TP_CAM_PITCH_MAX)

    def apply(self, player_pos: Vector3):
        rad_yaw = math.radians(self.yaw)
        rad_pitch = math.radians(self.pitch)

        target = Vector3(player_pos.x, player_pos.y + self.height * 0.5, player_pos.z)

        # Calculate camera eye position in orbit behind player
        cam_x = player_pos.x - math.sin(rad_yaw) * math.cos(rad_pitch) * self.distance
        cam_y = player_pos.y + self.height + math.sin(rad_pitch) * self.distance
        cam_z = player_pos.z - math.cos(rad_yaw) * math.cos(rad_pitch) * self.distance

        gluLookAt(
            cam_x, cam_y, cam_z,
            target.x, target.y, target.z,
            0.0, 1.0, 0.0
        )
