"""Game State Machine."""
from src.shared.constants import (
    STATE_MENU,
    STATE_PLAYING,
    STATE_TELEPORTING,
    STATE_GAME_OVER,
    STATE_VICTORY
)


class GameState:
    def __init__(self):
        self.current_state = STATE_PLAYING
        self.teleport_timer = 0.0

    def start_teleport(self, duration: float = 1.8):
        self.current_state = STATE_TELEPORTING
        self.teleport_timer = duration

    def update_teleport(self, dt: float) -> bool:
        """Returns True when teleport sequence completes."""
        if self.current_state == STATE_TELEPORTING:
            self.teleport_timer -= dt
            if self.teleport_timer <= 0.0:
                self.current_state = STATE_PLAYING
                return True
        return False

    def trigger_game_over(self):
        self.current_state = STATE_GAME_OVER

    def trigger_victory(self):
        self.current_state = STATE_VICTORY

    def restart(self):
        self.current_state = STATE_PLAYING
        self.teleport_timer = 0.0
