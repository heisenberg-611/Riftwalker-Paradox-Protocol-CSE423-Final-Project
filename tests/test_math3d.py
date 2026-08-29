"""Unit Tests for 3D Vector Math and Geometric Intersections."""
import unittest
import math
from src.shared.math3d import (
    Vector3,
    ray_intersects_sphere,
    ray_intersects_aabb,
    clamp,
    lerp
)


class TestMath3D(unittest.TestCase):
    def test_vector_addition_and_subtraction(self):
        v1 = Vector3(1.0, 2.0, 3.0)
        v2 = Vector3(4.0, 5.0, 6.0)
        self.assertEqual(v1 + v2, Vector3(5.0, 7.0, 9.0))
        self.assertEqual(v2 - v1, Vector3(3.0, 3.0, 3.0))

    def test_vector_normalization_and_length(self):
        v = Vector3(3.0, 4.0, 0.0)
        self.assertEqual(v.length(), 5.0)
        norm = v.normalized()
        self.assertAlmostEqual(norm.length(), 1.0)
        self.assertAlmostEqual(norm.x, 0.6)
        self.assertAlmostEqual(norm.y, 0.8)

    def test_vector_dot_and_cross_product(self):
        v1 = Vector3(1.0, 0.0, 0.0)
        v2 = Vector3(0.0, 1.0, 0.0)
        self.assertEqual(v1.dot(v2), 0.0)
        self.assertEqual(v1.cross(v2), Vector3(0.0, 0.0, 1.0))

    def test_ray_intersects_sphere(self):
        origin = Vector3(0.0, 0.0, 0.0)
        direction = Vector3(0.0, 0.0, 1.0)
        sphere_center = Vector3(0.0, 0.0, 10.0)
        radius = 2.0

        hit_dist = ray_intersects_sphere(origin, direction, sphere_center, radius)
        self.assertIsNotNone(hit_dist)
        self.assertAlmostEqual(hit_dist, 8.0)

        # Ray missing sphere
        miss_direction = Vector3(1.0, 0.0, 0.0)
        self.assertIsNone(ray_intersects_sphere(origin, miss_direction, sphere_center, radius))

    def test_ray_intersects_aabb(self):
        origin = Vector3(0.0, 0.0, -5.0)
        direction = Vector3(0.0, 0.0, 1.0)
        box_min = Vector3(-1.0, -1.0, 0.0)
        box_max = Vector3(1.0, 1.0, 2.0)

        hit_dist = ray_intersects_aabb(origin, direction, box_min, box_max)
        self.assertIsNotNone(hit_dist)
        self.assertAlmostEqual(hit_dist, 5.0)

    def test_clamp_and_lerp(self):
        self.assertEqual(clamp(15.0, 0.0, 10.0), 10.0)
        self.assertEqual(clamp(-5.0, 0.0, 10.0), 0.0)
        self.assertEqual(lerp(10.0, 20.0, 0.5), 15.0)


if __name__ == '__main__':
    unittest.main()
