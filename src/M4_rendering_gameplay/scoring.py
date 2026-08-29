"""Scoring, Multiplier, and Kill Feed Tracker."""
from src.shared.constants import (
    ENEMY_MELEE_RIFT_STALKER,
    ENEMY_RANGED_RIFT_SPITTER,
    BOSS_RIFT_GUARDIAN
)


class ScoreManager:
    def __init__(self):
        self.score = 0
        self.combo = 1
        self.combo_timer = 0.0

    def add_kill(self, enemy_id: str):
        points = 100
        if enemy_id == ENEMY_MELEE_RIFT_STALKER:
            points = 150
        elif enemy_id == ENEMY_RANGED_RIFT_SPITTER:
            points = 250
        elif enemy_id == BOSS_RIFT_GUARDIAN:
            points = 2000

        self.score += points * self.combo
        self.combo = min(8, self.combo + 1)
        self.combo_timer = 4.0

    def update(self, dt: float):
        if self.combo_timer > 0.0:
            self.combo_timer -= dt
            if self.combo_timer <= 0.0:
                self.combo = 1
