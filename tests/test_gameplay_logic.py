"""Unit Tests for Core Gameplay Logic, Chrono Slow, Scoring, and Teleportation."""
import unittest
from src.shared.math3d import Vector3
from src.M4_rendering_gameplay.chrono_slow import ChronoSlowManager
from src.M4_rendering_gameplay.scoring import ScoreManager
from src.M4_rendering_gameplay.game_state import GameState
from src.M3_world_teleport.world import World
from src.shared.constants import (
    ARENA_01_KEPLER_RELAY,
    ARENA_02_SUNDERED_RIFT,
    STATE_PLAYING,
    STATE_TELEPORTING,
    STATE_GAME_OVER,
    STATE_VICTORY,
    BOSS_RIFT_GUARDIAN
)


class TestGameplayLogic(unittest.TestCase):
    def test_chrono_slow_resource_management(self):
        chrono = ChronoSlowManager()
        self.assertFalse(chrono.is_active)
        self.assertEqual(chrono.current_time_scale, 1.0)

        # Activate Chrono Slow
        chrono.toggle()
        self.assertTrue(chrono.is_active)
        self.assertEqual(chrono.current_time_scale, 0.25)

        # Drain energy
        chrono.update(dt=2.0)  # Drains 40 energy
        self.assertAlmostEqual(chrono.energy, 60.0)

    def test_scoring_multipliers(self):
        score_mgr = ScoreManager()
        self.assertEqual(score_mgr.score, 0)
        self.assertEqual(score_mgr.combo, 1)

        score_mgr.add_kill("ENEMY_MELEE_RIFT_STALKER")
        self.assertEqual(score_mgr.score, 150)
        self.assertEqual(score_mgr.combo, 2)

        score_mgr.add_kill(BOSS_RIFT_GUARDIAN)
        self.assertEqual(score_mgr.score, 150 + 2000 * 2)

    def test_world_teleportation_trigger(self):
        world = World()
        self.assertEqual(world.active_arena_id, ARENA_01_KEPLER_RELAY)

        # Center beacon is at (0, 0, 0)
        player_near_beacon = Vector3(0.5, 0.0, 0.5)
        dest = world.check_teleport_trigger(player_near_beacon)
        self.assertEqual(dest, ARENA_02_SUNDERED_RIFT)

        # Player far from beacon
        player_far = Vector3(30.0, 0.0, 30.0)
        self.assertIsNone(world.check_teleport_trigger(player_far))

    def test_game_state_transitions(self):
        state = GameState()
        self.assertEqual(state.current_state, STATE_PLAYING)

        state.start_teleport(duration=1.0)
        self.assertEqual(state.current_state, STATE_TELEPORTING)

        completed = state.update_teleport(0.5)
        self.assertFalse(completed)
        self.assertEqual(state.current_state, STATE_TELEPORTING)

        completed = state.update_teleport(0.6)
        self.assertTrue(completed)
        self.assertEqual(state.current_state, STATE_PLAYING)

        state.trigger_game_over()
        self.assertEqual(state.current_state, STATE_GAME_OVER)


if __name__ == '__main__':
    unittest.main()
