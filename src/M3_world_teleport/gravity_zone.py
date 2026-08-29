"""Gravity Zones and Jump-pad triggers."""
from src.shared.math3d import Vector3


class GravityZone:
    def __init__(self, pos: Vector3, radius: float = 5.0, gravity_factor: float = 0.4):
        self.position = pos
        self.radius = radius
        self.gravity_factor = gravity_factor

    def contains(self, player_pos: Vector3) -> bool:
        return self.position.distance_to(player_pos) <= self.radius
