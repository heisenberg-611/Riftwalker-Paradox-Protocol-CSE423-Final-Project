"""Raycasting Hitscan Detection."""
import math
from typing import List, Optional
from src.shared.math3d import Vector3, ray_intersects_sphere
from src.M2_enemies_combat.enemy_base import EnemyBase


class HitResult:
    def __init__(self, hit_enemy: Optional[EnemyBase], distance: float, hit_point: Vector3):
        self.hit_enemy = hit_enemy
        self.distance = distance
        self.hit_point = hit_point


class RaycastSystem:
    @staticmethod
    def fire_ray(
        origin: Vector3,
        direction: Vector3,
        enemies: List[EnemyBase],
        max_range: float = 120.0
    ) -> Optional[HitResult]:
        closest_hit: Optional[HitResult] = None
        min_dist = max_range

        norm_dir = direction.normalized()

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
                hit_point = origin + norm_dir * dist
                closest_hit = HitResult(
                    hit_enemy=enemy,
                    distance=dist,
                    hit_point=hit_point
                )


        return closest_hit
