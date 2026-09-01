"""Unit Tests for First-Time Cinematic Story Introduction System."""
import unittest
import os
import tempfile
from src.M4_rendering_gameplay.story_intro import StoryIntroManager
from src.M4_rendering_gameplay.game_state import GameState
from src.shared.constants import STATE_STORY, STATE_PLAYING


class TestStoryIntro(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_story_panel_content_and_structure(self):
        manager = StoryIntroManager(config_file=self.temp_file.name)
        self.assertEqual(len(manager.panels), 6)

        expected_headings = [
            "2089 — EARTH",
            "THE RIFTS",
            "THE RIFTBORN",
            "THE RIFT-CHRONO PROJECT",
            "KEPLER RELAY",
            "THE PARADOX"
        ]
        actual_headings = [p["heading"] for p in manager.panels]
        self.assertEqual(actual_headings, expected_headings)

        # Check key narrative sentences exist
        self.assertTrue(any("silence" in line for line in manager.panels[0]["lines"]))
        self.assertTrue(any("something came through" in line for line in manager.panels[1]["lines"]))
        self.assertTrue(any("fractures in space" in line for line in manager.panels[2]["lines"]))
        self.assertTrue(any("THE RIFT-CHRONO SUIT" in line for line in manager.panels[3]["lines"]))
        self.assertTrue(any("They found us" in line for line in manager.panels[4]["lines"]))
        self.assertTrue(any("coming from Earth" in line for line in manager.panels[5]["lines"]))

    def test_story_pagination_flow(self):
        manager = StoryIntroManager(config_file=self.temp_file.name)
        self.assertFalse(manager.is_story_seen())
        self.assertEqual(manager.current_panel_index, 0)

        # Advance through panels 0 -> 1 -> 2 -> 3 -> 4 -> 5
        for expected_index in range(1, 6):
            has_next = manager.next_panel()
            self.assertTrue(has_next)
            self.assertEqual(manager.current_panel_index, expected_index)

        # Reached final panel (index 5). Next advance should return False and mark story seen
        has_next = manager.next_panel()
        self.assertFalse(has_next)
        self.assertTrue(manager.is_story_seen())

    def test_story_skip_and_persistence(self):
        manager1 = StoryIntroManager(config_file=self.temp_file.name)
        self.assertFalse(manager1.is_story_seen())

        # Skip story
        manager1.skip_story()
        self.assertTrue(manager1.is_story_seen())

        # New instance pointing to same file should load story_seen = True
        manager2 = StoryIntroManager(config_file=self.temp_file.name)
        self.assertTrue(manager2.is_story_seen())

        # Reset story
        manager2.reset_story()
        self.assertFalse(manager2.is_story_seen())
        self.assertEqual(manager2.current_panel_index, 0)

    def test_game_state_story_integration(self):
        game_state = GameState(initial_state=STATE_STORY)
        self.assertEqual(game_state.current_state, STATE_STORY)

        game_state.current_state = STATE_PLAYING
        self.assertEqual(game_state.current_state, STATE_PLAYING)


if __name__ == '__main__':
    unittest.main()
