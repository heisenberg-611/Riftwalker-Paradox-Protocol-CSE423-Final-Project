"""Spatial Collision Detection and Boundary Resolution."""
from src.shared.math3d import Vector3, clamp


class CollisionSystem:
    @staticmethod
    def check_sphere_sphere(pos_a: Vector3, rad_a: float, pos_b: Vector3, rad_b: float) -> bool:
        dist_sq = pos_a.distance_squared_to(pos_b)
        min_dist = rad_a + rad_b
        return dist_sq <= (min_dist * min_dist)

    @staticmethod
    def clamp_to_arena_bounds(pos: Vector3, half_extent: float) -> Vector3:
        """Keep position within square arena bounds."""
        margin = 1.5
        bound = half_extent - margin
        return Vector3(
            clamp(pos.x, -bound, bound),
            pos.y,
            clamp(pos.z, -bound, bound)
        )
