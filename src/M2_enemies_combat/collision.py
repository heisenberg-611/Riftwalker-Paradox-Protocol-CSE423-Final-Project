"""Spatial Collision Detection and Boundary Resolution."""
from typing import List, Optional
from src.shared.math3d import Vector3, clamp
from src.shared.collision import CollisionGeometry, CylinderObstacle, BoxObstacle, Obstacle


class CollisionSystem:
    @staticmethod
    def check_sphere_sphere(pos_a: Vector3, rad_a: float, pos_b: Vector3, rad_b: float) -> bool:
        return CollisionGeometry.check_sphere_sphere(pos_a, rad_a, pos_b, rad_b)

    @staticmethod
    def check_sphere_aabb(sphere_pos: Vector3, sphere_rad: float, box_min: Vector3, box_max: Vector3) -> bool:
        return CollisionGeometry.check_sphere_aabb(sphere_pos, sphere_rad, box_min, box_max)

    @staticmethod
    def resolve_obstacles(pos: Vector3, entity_radius: float, obstacles: List[Obstacle], passes: int = 2) -> Vector3:
        return CollisionGeometry.resolve_obstacles(pos, entity_radius, obstacles, passes)

    @staticmethod
    def clamp_to_arena_bounds(pos: Vector3, half_extent: float, margin: float = 1.5) -> Vector3:
        """Keep position within square arena bounds."""
        return CollisionGeometry.clamp_to_arena_bounds(pos, half_extent, margin)

