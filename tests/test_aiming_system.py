"""Unit tests for Unified Crosshair-Driven Aiming and Visual Laser System."""
import unittest
import math
from src.shared.math3d import Vector3
from src.M1_player_camera.first_person_camera import FirstPersonCamera
from src.M1_player_camera.third_person_camera import ThirdPersonCamera
from src.M1_player_camera.player_weapon import PlayerWeapon
from src.M1_player_camera.astronaut_rig import AstronautRig
from src.M1_player_camera.player import Player
from src.M2_enemies_combat.raycast import RaycastSystem, AimResult
from src.M2_enemies_combat.melee_rift_stalker import MeleeRiftStalker
from src.M2_enemies_combat.ranged_rift_spitter import RangedRiftSpitter


class TestAimingSystem(unittest.TestCase):

    def setUp(self):
        self.player = Player(start_pos=Vector3(0.0, 0.0, 0.0))
        self.weapon = PlayerWeapon()
        self.rig = AstronautRig()

    def test_first_person_aim_origin_is_camera_eye(self):
        """FP gameplay ray origin must be camera eye, not the gun muzzle."""
        cam_eye = self.player.fp_cam.get_cam_eye(self.player.position)
        self.assertAlmostEqual(cam_eye.x, 0.0)
        self.assertAlmostEqual(cam_eye.y, 2.1)
        self.assertAlmostEqual(cam_eye.z, 0.0)

    def test_third_person_aim_origin_is_camera_eye(self):
        """TP gameplay ray origin must be camera eye behind/above the player over the right shoulder."""
        self.player.tp_cam.yaw = 0.0
        self.player.tp_cam.pitch = 0.0
        cam_eye = self.player.tp_cam.get_cam_eye(self.player.position)
        # In third-person at yaw=0, pitch=0, eye is over right shoulder: (shoulder_offset, height + 0.2, -distance)
        self.assertAlmostEqual(cam_eye.x, self.player.tp_cam.shoulder_offset, places=2)
        self.assertAlmostEqual(cam_eye.y, self.player.tp_cam.height + 0.2, places=2)
        self.assertAlmostEqual(cam_eye.z, -self.player.tp_cam.distance, places=2)




    def test_first_person_muzzle_world_basis(self):
        """FP viewmodel muzzle position must transform correctly into world space using camera basis."""
        cam_eye = self.player.fp_cam.get_cam_eye(self.player.position)
        fwd, right, up = self.player.fp_cam.get_basis_vectors()

        muzzle_world = self.weapon.get_fp_muzzle_world(
            cam_eye, fwd, right, up,
            offset_right=0.35, offset_up=-0.28, offset_forward=0.68
        )

        # Muzzle should be offset to the right, slightly down, and forward from eye
        self.assertAlmostEqual(muzzle_world.x, 0.35, places=2)
        self.assertAlmostEqual(muzzle_world.y, 2.1 - 0.28, places=2)
        self.assertAlmostEqual(muzzle_world.z, 0.68, places=2)

    def test_third_person_muzzle_world(self):
        """TP muzzle position must originate from astronaut right hand."""
        muzzle_tp = self.rig.get_tp_muzzle_world(self.player.position, yaw=0.0, pitch=0.0)
        self.assertGreater(muzzle_tp.x, 0.3)  # On the right side
        self.assertGreater(muzzle_tp.y, 1.0)  # At weapon height
        self.assertGreater(muzzle_tp.z, 0.2)  # In front of player body

    def test_aim_result_structure_and_miss_hit_point(self):
        """When no enemy is hit, raycast returns AimResult pointing to max range."""
        cam_eye = self.player.fp_cam.get_cam_eye(self.player.position)
        fwd = self.player.fp_cam.get_aim_direction()
        enemies = []

        result = RaycastSystem.fire_ray(cam_eye, fwd, enemies, max_range=100.0)
        self.assertIsInstance(result, AimResult)
        self.assertIsNone(result.hit_enemy)
        self.assertAlmostEqual(result.distance, 100.0)
        self.assertAlmostEqual(result.hit_point.z, 100.0, places=2)

    def test_hit_detection_close_and_distant_enemy(self):
        """Raycast must hit enemies accurately at both close (5u) and far (40u) ranges."""
        cam_eye = self.player.fp_cam.get_cam_eye(self.player.position)
        fwd = Vector3(0.0, 0.0, 1.0)

        # Close enemy at (0, 0, 8)
        stalker = MeleeRiftStalker(Vector3(0.0, 0.0, 8.0))
        result_close = RaycastSystem.fire_ray(cam_eye, fwd, [stalker], max_range=120.0)
        self.assertIsNotNone(result_close.hit_enemy)
        self.assertEqual(result_close.hit_enemy, stalker)

        # Distant enemy at (0, 0, 45)
        spitter = RangedRiftSpitter(Vector3(0.0, 0.0, 45.0))
        result_far = RaycastSystem.fire_ray(cam_eye, fwd, [spitter], max_range=120.0)
        self.assertIsNotNone(result_far.hit_enemy)
        self.assertEqual(result_far.hit_enemy, spitter)

    def test_camera_switching_preserves_orientation(self):
        """Pressing V to toggle camera must keep yaw and pitch perfectly synchronized without snapping."""
        self.player.tp_cam.yaw = 135.0
        self.player.tp_cam.pitch = 22.5

        # Switch to first person
        self.player.toggle_camera()
        self.assertTrue(self.player.is_first_person)
        self.assertAlmostEqual(self.player.fp_cam.yaw, 135.0)
        self.assertAlmostEqual(self.player.fp_cam.pitch, 22.5)

        # Rotate while in first person
        self.player.fp_cam.yaw = 270.0
        self.player.fp_cam.pitch = -15.0

        # Switch back to third person
        self.player.toggle_camera()
        self.assertFalse(self.player.is_first_person)
        self.assertAlmostEqual(self.player.tp_cam.yaw, 270.0)
        self.assertAlmostEqual(self.player.tp_cam.pitch, -15.0)


if __name__ == '__main__':
    unittest.main()
