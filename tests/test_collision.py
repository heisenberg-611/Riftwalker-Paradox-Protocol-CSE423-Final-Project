"""Unit Tests for Spatial Collision and Bounds."""
import unittest
from src.shared.math3d import Vector3
from src.M2_enemies_combat.collision import CollisionSystem


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


if __name__ == '__main__':
    unittest.main()
