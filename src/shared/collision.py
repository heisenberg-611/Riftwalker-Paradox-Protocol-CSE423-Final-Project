"""Reusable Geometric Collision Utilities and Spatial Query Functions.

This module provides pure geometric and mathematical intersection tests.
Gameplay modules (M1 Player, M2 Combat, M3 World) consume these shared utilities
to determine physical contacts, ray intersections, and arena boundary limits,
while retaining ownership of their respective gameplay responses (damage, bounces,
teleport triggers, etc.).
"""
from typing import Optional, Tuple
from src.shared.math3d import Vector3, clamp, ray_intersects_sphere, ray_intersects_aabb


class CollisionGeometry:
    """Pure geometric intersection and spatial containment routines."""

    @staticmethod
    def check_sphere_sphere(pos_a: Vector3, rad_a: float, pos_b: Vector3, rad_b: float) -> bool:
        """Tests if two 3D bounding spheres overlap."""
        dist_sq = pos_a.distance_squared_to(pos_b)
        min_dist = rad_a + rad_b
        return dist_sq <= (min_dist * min_dist)

    @staticmethod
    def check_sphere_aabb(sphere_pos: Vector3, sphere_rad: float, box_min: Vector3, box_max: Vector3) -> bool:
        """Tests if a bounding sphere overlaps an Axis-Aligned Bounding Box (AABB)."""
        closest_point = Vector3(
            clamp(sphere_pos.x, box_min.x, box_max.x),
            clamp(sphere_pos.y, box_min.y, box_max.y),
            clamp(sphere_pos.z, box_min.z, box_max.z)
        )
        return sphere_pos.distance_squared_to(closest_point) <= (sphere_rad * sphere_rad)

    @staticmethod
    def clamp_to_arena_bounds(pos: Vector3, half_extent: float, margin: float = 1.5) -> Vector3:
        """Clamps a 3D position within square horizontal arena bounds."""
        bound = half_extent - margin
        return Vector3(
            clamp(pos.x, -bound, bound),
            pos.y,
            clamp(pos.z, -bound, bound)
        )

    @staticmethod
    def ray_intersects_sphere(
        ray_origin: Vector3,
        ray_dir: Vector3,
        sphere_center: Vector3,
        radius: float
    ) -> Optional[float]:
        """Wrapper for ray-sphere intersection distance test."""
        return ray_intersects_sphere(ray_origin, ray_dir, sphere_center, radius)

    @staticmethod
    def ray_intersects_aabb(
        ray_origin: Vector3,
        ray_dir: Vector3,
        box_min: Vector3,
        box_max: Vector3
    ) -> Optional[float]:
        """Wrapper for ray-AABB intersection distance test."""
        return ray_intersects_aabb(ray_origin, ray_dir, box_min, box_max)
