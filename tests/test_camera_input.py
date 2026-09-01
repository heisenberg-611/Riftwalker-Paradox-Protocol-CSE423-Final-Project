"""Unit Tests for Mouse Input Tracking, Camera Pitch/Yaw Controls, and Score Manager."""
import unittest
import math
from src.shared.math3d import Vector3
from src.shared.input_manager import InputManager
from src.M1_player_camera.first_person_camera import FirstPersonCamera
from src.M1_player_camera.third_person_camera import ThirdPersonCamera
from src.M4_rendering_gameplay.scoring import ScoreManager
from src.shared.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    MOUSE_SENSITIVITY,
    FP_CAM_PITCH_MIN,
    FP_CAM_PITCH_MAX,
    TP_CAM_PITCH_MIN,
    TP_CAM_PITCH_MAX
)


class TestCameraInput(unittest.TestCase):
    def test_input_manager_initial_state_and_resizing(self):
        input_mgr = InputManager(width=1024, height=768)
        self.assertEqual(input_mgr.center_x, 512)
        self.assertEqual(input_mgr.center_y, 384)
        self.assertTrue(input_mgr.first_mouse)

        # First mouse event should set baseline and zero delta
        input_mgr.on_mouse_motion(500, 380)
        self.assertFalse(input_mgr.first_mouse)
        self.assertEqual(input_mgr.mouse_delta, (0.0, 0.0))

        # Subsequent movement produces expected relative delta (510 - 500 = 10, 390 - 380 = 10)
        input_mgr.on_mouse_motion(510, 390)
        self.assertEqual(input_mgr.mouse_delta, (10.0, 10.0))

        # Large jump (e.g. from window re-entry) is filtered out safely
        input_mgr.on_mouse_motion(900, 390)  # dx = 390 (> 100)
        self.assertEqual(input_mgr.mouse_delta, (0.0, 0.0))

        # Subsequent normal movement works smoothly again
        input_mgr.on_mouse_motion(905, 392)
        self.assertEqual(input_mgr.mouse_delta, (5.0, 2.0))

        # Window resizing
        input_mgr.set_window_size(1920, 1080)
        self.assertEqual(input_mgr.center_x, 960)
        self.assertEqual(input_mgr.center_y, 540)
        self.assertTrue(input_mgr.first_mouse)



    def test_first_person_camera_orientation(self):
        cam = FirstPersonCamera()
        self.assertEqual(cam.yaw, 0.0)
        self.assertEqual(cam.pitch, 0.0)

        # Move mouse right (dx = 10, dy = 0)
        cam.update_orientation(mouse_dx=10.0, mouse_dy=0.0, sensitivity=0.1)
        self.assertAlmostEqual(cam.yaw, -1.0)
        self.assertEqual(cam.pitch, 0.0)

        # Move mouse up (dx = 0, dy = -20) -> looking up increases pitch
        cam.update_orientation(mouse_dx=0.0, mouse_dy=-20.0, sensitivity=0.1)
        self.assertAlmostEqual(cam.pitch, 2.0)

        # Test pitch clamping limits
        cam.update_orientation(mouse_dx=0.0, mouse_dy=-2000.0, sensitivity=0.1)
        self.assertEqual(cam.pitch, FP_CAM_PITCH_MAX)

        cam.update_orientation(mouse_dx=0.0, mouse_dy=4000.0, sensitivity=0.1)
        self.assertEqual(cam.pitch, FP_CAM_PITCH_MIN)

    def test_third_person_camera_orientation_and_alignment(self):
        tp_cam = ThirdPersonCamera()
        self.assertEqual(tp_cam.yaw, 0.0)
        self.assertEqual(tp_cam.pitch, 0.0)

        # Move mouse right (dx = 10, dy = 0)
        tp_cam.update_orientation(mouse_dx=10.0, mouse_dy=0.0, sensitivity=0.1)
        self.assertAlmostEqual(tp_cam.yaw, -1.0)

        # Move mouse up (dx = 0, dy = -20)
        tp_cam.update_orientation(mouse_dx=0.0, mouse_dy=-20.0, sensitivity=0.1)
        self.assertAlmostEqual(tp_cam.pitch, 2.0)

        # Pitch clamping
        tp_cam.update_orientation(mouse_dx=0.0, mouse_dy=-2000.0, sensitivity=0.1)
        self.assertEqual(tp_cam.pitch, TP_CAM_PITCH_MAX)

        tp_cam.update_orientation(mouse_dx=0.0, mouse_dy=4000.0, sensitivity=0.1)
        self.assertEqual(tp_cam.pitch, TP_CAM_PITCH_MIN)

    def test_score_manager_add_score(self):
        score_mgr = ScoreManager()
        self.assertEqual(score_mgr.score, 0)

        score_mgr.add_score(150)
        self.assertEqual(score_mgr.score, 150)

        score_mgr.add_score(250)
        self.assertEqual(score_mgr.score, 400)


if __name__ == '__main__':
    unittest.main()
