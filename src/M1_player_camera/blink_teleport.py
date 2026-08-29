"""Player Short-Range Blink Teleport (Evasive Combat Dash)."""
import math
from src.shared.math3d import Vector3
from src.shared.constants import BLINK_DISTANCE, BLINK_COOLDOWN, BLINK_ENERGY_COST


class BlinkTeleport:
    def __init__(self):
        self.cooldown = BLINK_COOLDOWN
        self.cooldown_timer = 0.0
        self.distance = BLINK_DISTANCE
        self.energy_cost = BLINK_ENERGY_COST

    def update(self, dt: float):
        if self.cooldown_timer > 0.0:
            self.cooldown_timer = max(0.0, self.cooldown_timer - dt)

    def is_ready(self) -> bool:
        return self.cooldown_timer <= 0.0

    def execute_blink(self, player_pos: Vector3, yaw_deg: float) -> Vector3:
        """Computes new player position forward along current yaw angle."""
        self.cooldown_timer = self.cooldown
        rad = math.radians(yaw_deg)
        forward = Vector3(math.sin(rad), 0.0, math.cos(rad)).normalized()
        return player_pos + forward * self.distance
