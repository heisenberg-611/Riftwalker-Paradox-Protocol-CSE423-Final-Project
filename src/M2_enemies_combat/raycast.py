"""Authoritative Raycasting Hitscan Detection for Crosshair-Driven Aiming."""
import math
from typing import List, Optional
from src.shared.math3d import Vector3, ray_intersects_sphere
from src.M2_enemies_combat.enemy_base import EnemyBase


class AimResult:
    """
    Unified gameplay aim structure for both 1st-person and 3rd-person modes.
    Contains authoritative camera origin, aim direction, target impact/point, distance, and hit enemy.
    """
    __slots__ = ('origin', 'direction', 'hit_point', 'distance', 'hit_enemy')

    def __init__(
        self,
        origin: Vector3,
        direction: Vector3,
        hit_point: Vector3,
        distance: float,
        hit_enemy: Optional[EnemyBase] = None
    ):
        self.origin = origin
        self.direction = direction
        self.hit_point = hit_point
        self.distance = distance
        self.hit_enemy = hit_enemy


# Alias for backward compatibility if referenced
HitResult = AimResult


class RaycastSystem:
    @staticmethod
    def fire_ray(
        origin: Vector3,
        direction: Vector3,
        enemies: List[EnemyBase],
        max_range: float = 120.0
    ) -> AimResult:
        """
        Casts a ray from camera eye along crosshair direction against active enemies.
        Always returns a complete AimResult (with hit_enemy=None and max range hit_point if missed).
        """
        norm_dir = direction.normalized()
        closest_hit_enemy: Optional[EnemyBase] = None
        min_dist = max_range

        for enemy in enemies:
            if enemy.is_dead:
                continue
            effective_radius = enemy.radius * 1.35
            center_y = max(1.0, enemy.radius)
            dist = ray_intersects_sphere(
                ray_origin=origin,
                ray_dir=norm_dir,
                sphere_center=enemy.position + Vector3(0.0, center_y, 0.0),
                radius=effective_radius
            )
            if dist is not None and dist < min_dist:
                min_dist = dist
                closest_hit_enemy = enemy

        if closest_hit_enemy is not None:
            hit_pt = origin + norm_dir * min_dist
            return AimResult(
                origin=origin,
                direction=norm_dir,
                hit_point=hit_pt,
                distance=min_dist,
                hit_enemy=closest_hit_enemy
            )
        else:
            default_aim_point = origin + norm_dir * max_range
            return AimResult(
                origin=origin,
                direction=norm_dir,
                hit_point=default_aim_point,
                distance=max_range,
                hit_enemy=None
            )

