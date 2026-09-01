"""Unit Tests for Spatial Collision and Bounds."""
import unittest
from src.shared.math3d import Vector3
from src.shared.collision import CollisionGeometry, CylinderObstacle, BoxObstacle
from src.M2_enemies_combat.collision import CollisionSystem
from src.M3_world_teleport.arena_01_kepler_relay import ArenaKeplerRelay
from src.M3_world_teleport.arena_02_sundered_rift import ArenaSunderedRift


class TestCollision(unittest.TestCase):
    def test_sphere_sphere_collision(self):
        p1 = Vector3(0.0, 0.0, 0.0)
        p2 = Vector3(1.5, 0.0, 0.0)
        # Radii 1.0 + 1.0 = 2.0 > 1.5 distance -> Colliding
        self.assertTrue(CollisionSystem.check_sphere_sphere(p1, 1.0, p2, 1.0))

        p3 = Vector3(5.0, 0.0, 0.0)
        # Radii 1.0 + 1.0 = 2.0 < 5.0 distance -> Not Colliding
        self.assertFalse(CollisionSystem.check_sphere_sphere(p1, 1.0, p3, 1.0))

    def test_clamp_to_arena_bounds(self):
        out_of_bounds = Vector3(100.0, 0.0, -100.0)
        clamped = CollisionSystem.clamp_to_arena_bounds(out_of_bounds, half_extent=50.0)
        self.assertLessEqual(clamped.x, 48.5)
        self.assertGreaterEqual(clamped.z, -48.5)

    def test_resolve_circle_cylinder_collision(self):
        # Cylinder at (10, 0, 10) with radius 2.0. Entity radius 1.0 (min_dist = 3.0)
        cyl_pos = Vector3(10.0, 0.0, 10.0)
        obs_radius = 2.0
        entity_radius = 1.0

        # Case 1: Outside and safe
        outside_pos = Vector3(10.0, 0.0, 15.0)
        res_outside = CollisionGeometry.resolve_circle_cylinder(outside_pos, entity_radius, cyl_pos, obs_radius)
        self.assertAlmostEqual(res_outside.x, 10.0)
        self.assertAlmostEqual(res_outside.z, 15.0)

        # Case 2: Overlapping along +Z (at 10, 0, 11.5 -> distance 1.5 < 3.0)
        overlap_pos = Vector3(10.0, 0.0, 11.5)
        res_overlap = CollisionGeometry.resolve_circle_cylinder(overlap_pos, entity_radius, cyl_pos, obs_radius)
        self.assertAlmostEqual(res_overlap.x, 10.0)
        self.assertAlmostEqual(res_overlap.z, 13.0)  # Pushed to 10 + 3.0 = 13.0

        # Case 3: Exactly at center
        center_pos = Vector3(10.0, 0.0, 10.0)
        res_center = CollisionGeometry.resolve_circle_cylinder(center_pos, entity_radius, cyl_pos, obs_radius)
        dist_to_center = (res_center - cyl_pos).length()
        self.assertAlmostEqual(dist_to_center, 3.0)

    def test_resolve_circle_aabb_collision(self):
        # Box from (0, 0, 0) to (2, 2, 2)
        box_min = Vector3(0.0, 0.0, 0.0)
        box_max = Vector3(2.0, 2.0, 2.0)
        entity_radius = 1.0

        # Case 1: Safe outside
        outside_pos = Vector3(5.0, 0.0, 1.0)
        res = CollisionGeometry.resolve_circle_aabb(outside_pos, entity_radius, box_min, box_max)
        self.assertAlmostEqual(res.x, 5.0)

        # Case 2: Penetrating from right (+X side at x = 2.4, should push to x = 3.0)
        overlap_pos = Vector3(2.4, 0.0, 1.0)
        res = CollisionGeometry.resolve_circle_aabb(overlap_pos, entity_radius, box_min, box_max)
        self.assertAlmostEqual(res.x, 3.0)
        self.assertAlmostEqual(res.z, 1.0)

        # Case 3: Inside box at (0.5, 0.0, 1.0) -> closest face is left (x=0), should push to x = -1.0
        inside_pos = Vector3(0.5, 0.0, 1.0)
        res = CollisionGeometry.resolve_circle_aabb(inside_pos, entity_radius, box_min, box_max)
        self.assertAlmostEqual(res.x, -1.0)

    def test_kepler_relay_obstacle_resolution(self):
        kepler = ArenaKeplerRelay()
        self.assertGreater(len(kepler.get_obstacles()), 0)

        # Pillar is at (25, 0, 25) with radius 1.2
        # Player moves into (25.0, 0.0, 25.5) with radius 1.0 (min_dist = 2.2)
        test_pos = Vector3(25.0, 0.0, 25.5)
        resolved = kepler.resolve_collision(test_pos, radius=1.0)
        dist_to_pillar = (resolved - Vector3(25.0, 0.0, 25.0)).length()
        self.assertGreaterEqual(dist_to_pillar, 2.19)

        # Crate is at (15.0, 0.0, 8.0) size 2.0 (box x: [14, 16], z: [7, 9])
        # Player at (15.0, 0.0, 8.0) inside crate
        resolved_crate = kepler.resolve_collision(Vector3(15.0, 0.0, 8.0), radius=1.0)
        # Resolved position should not overlap box [14, 16] x [7, 9] with radius 1.0
        cx = max(14.0, min(resolved_crate.x, 16.0))
        cz = max(7.0, min(resolved_crate.z, 9.0))
        dist_sq = (resolved_crate.x - cx) ** 2 + (resolved_crate.z - cz) ** 2
        self.assertGreaterEqual(dist_sq, 0.99)

    def test_sundered_rift_obstacle_resolution(self):
        sundered = ArenaSunderedRift()
        self.assertGreater(len(sundered.get_obstacles()), 0)

        # Crystal spire at (35.0, 0.0, 20.0) with radius 1.3
        test_pos = Vector3(35.0, 0.0, 20.5)
        resolved = sundered.resolve_collision(test_pos, radius=1.0)
        dist_to_spire = (resolved - Vector3(35.0, 0.0, 20.0)).length()
        self.assertGreaterEqual(dist_to_spire, 2.29)


if __name__ == '__main__':
    unittest.main()

