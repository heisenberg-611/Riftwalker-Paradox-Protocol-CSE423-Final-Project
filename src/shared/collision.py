import math
from typing import List, Optional, Tuple, Union
from src.shared.math3d import Vector3, clamp, ray_intersects_sphere, ray_intersects_aabb


class CylinderObstacle:
    """Cylindrical physical collision obstacle (pillars, spires, beacon pedestals)."""
    __slots__ = ('position', 'radius', 'height')

    def __init__(self, position: Vector3, radius: float, height: float = 10.0):
        self.position = position
        self.radius = radius
        self.height = height


class BoxObstacle:
    """Axis-Aligned Bounding Box (AABB) collision obstacle (crates, barricades)."""
    __slots__ = ('min_point', 'max_point')

    def __init__(self, min_point: Vector3, max_point: Vector3):
        self.min_point = min_point
        self.max_point = max_point

    @classmethod
    def from_center_cube(cls, center: Vector3, size: float) -> 'BoxObstacle':
        half = size * 0.5
        return cls(
            min_point=Vector3(center.x - half, center.y, center.z - half),
            max_point=Vector3(center.x + half, center.y + size, center.z + half)
        )

    @classmethod
    def from_center_extents(cls, center: Vector3, size_x: float, size_y: float, size_z: float) -> 'BoxObstacle':
        hx = size_x * 0.5
        hz = size_z * 0.5
        return cls(
            min_point=Vector3(center.x - hx, center.y, center.z - hz),
            max_point=Vector3(center.x + hx, center.y + size_y, center.z + hz)
        )


Obstacle = Union[CylinderObstacle, BoxObstacle]


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
    def resolve_circle_cylinder(
        pos: Vector3,
        entity_radius: float,
        obs_pos: Vector3,
        obs_radius: float
    ) -> Vector3:
        """
        Resolves horizontal (XZ) collision between a circular entity and cylindrical obstacle.
        Pushes entity smoothly outwards along the contact normal.
        """
        dx = pos.x - obs_pos.x
        dz = pos.z - obs_pos.z
        dist_sq = dx * dx + dz * dz
        min_dist = entity_radius + obs_radius

        if dist_sq < min_dist * min_dist:
            dist = math.sqrt(dist_sq)
            if dist > 1e-5:
                push = min_dist - dist
                return Vector3(pos.x + (dx / dist) * push, pos.y, pos.z + (dz / dist) * push)
            else:
                # Entity is exactly at cylinder center; push along arbitrary positive X axis
                return Vector3(pos.x + min_dist, pos.y, pos.z)
        return pos

    @staticmethod
    def resolve_circle_aabb(
        pos: Vector3,
        entity_radius: float,
        box_min: Vector3,
        box_max: Vector3
    ) -> Vector3:
        """
        Resolves horizontal (XZ) collision between a circular entity and an AABB box obstacle.
        Handles both external boundary contacts and internal penetration smoothly.
        """
        # Closest point on the box in 2D XZ
        cx = clamp(pos.x, box_min.x, box_max.x)
        cz = clamp(pos.z, box_min.z, box_max.z)

        dx = pos.x - cx
        dz = pos.z - cz
        dist_sq = dx * dx + dz * dz

        if dist_sq < entity_radius * entity_radius:
            dist = math.sqrt(dist_sq)
            if dist > 1e-5:
                # Entity center is outside or on the border of the box
                push = entity_radius - dist
                return Vector3(pos.x + (dx / dist) * push, pos.y, pos.z + (dz / dist) * push)
            else:
                # Entity center is INSIDE the box; push out along the minimum penetration axis
                pen_left = pos.x - box_min.x
                pen_right = box_max.x - pos.x
                pen_back = pos.z - box_min.z
                pen_front = box_max.z - pos.z

                min_pen = min(pen_left, pen_right, pen_back, pen_front)
                if min_pen == pen_left:
                    return Vector3(box_min.x - entity_radius, pos.y, pos.z)
                elif min_pen == pen_right:
                    return Vector3(box_max.x + entity_radius, pos.y, pos.z)
                elif min_pen == pen_back:
                    return Vector3(pos.x, pos.y, box_min.z - entity_radius)
                else:
                    return Vector3(pos.x, pos.y, box_max.z + entity_radius)
        return pos

    @staticmethod
    def resolve_obstacles(
        pos: Vector3,
        entity_radius: float,
        obstacles: List[Obstacle],
        passes: int = 2
    ) -> Vector3:
        """
        Iteratively resolves collisions against all active obstacles in the arena.
        Multi-pass relaxation ensures smooth sliding around sharp corners and clusters.
        """
        resolved_pos = pos
        for _ in range(passes):
            for obs in obstacles:
                if isinstance(obs, CylinderObstacle):
                    resolved_pos = CollisionGeometry.resolve_circle_cylinder(
                        resolved_pos, entity_radius, obs.position, obs.radius
                    )
                elif isinstance(obs, BoxObstacle):
                    resolved_pos = CollisionGeometry.resolve_circle_aabb(
                        resolved_pos, entity_radius, obs.min_point, obs.max_point
                    )
        return resolved_pos

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

