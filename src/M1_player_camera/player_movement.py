"""Player Kinematics, WASD Movement, and Velocity Calculation."""
import math
from src.shared.math3d import Vector3
from src.shared.constants import PLAYER_MOVE_SPEED


class PlayerMovement:
    def __init__(self, move_speed: float = PLAYER_MOVE_SPEED):
        self.move_speed = move_speed
        self.velocity = Vector3(0.0, 0.0, 0.0)

    def compute_movement(
        self,
        forward_input: float,
        strafe_input: float,
        yaw_deg: float,
        dt: float
    ) -> Vector3:
        if abs(forward_input) < 1e-4 and abs(strafe_input) < 1e-4:
            self.velocity = Vector3(0.0, 0.0, 0.0)
            return Vector3(0.0, 0.0, 0.0)

        rad_yaw = math.radians(yaw_deg)
        fwd = Vector3(math.sin(rad_yaw), 0.0, math.cos(rad_yaw)).normalized()
        right = Vector3(-math.cos(rad_yaw), 0.0, math.sin(rad_yaw)).normalized()

        move_dir = (fwd * forward_input + right * strafe_input).normalized()
        self.velocity = move_dir * self.move_speed
        return self.velocity * dt
