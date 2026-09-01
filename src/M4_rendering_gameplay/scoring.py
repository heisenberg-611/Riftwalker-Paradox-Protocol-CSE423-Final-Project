"""Scoring, Multiplier, and Kill Feed Tracker."""
from src.shared.constants import (
    ENEMY_MELEE_RIFT_STALKER,
    ENEMY_RANGED_RIFT_SPITTER,
    BOSS_RIFT_GUARDIAN
)


class ScoreManager:
    COMBO_MAX_DURATION = 3.5

    def __init__(self):
        self.score = 0
        self.combo = 1
        self.combo_timer = 0.0

    def add_score(self, amount: int):
        """Add arbitrary score (e.g. from picking up Rift Energy crystals or clearing waves)."""
        self.score += max(0, int(amount))

    def add_kill(self, enemy_id: str):
        """Awards points scaled by active combo multiplier and advances combo tier."""
        points = 100
        if enemy_id == ENEMY_MELEE_RIFT_STALKER:
            points = 150
        elif enemy_id == ENEMY_RANGED_RIFT_SPITTER:
            points = 250
        elif enemy_id == BOSS_RIFT_GUARDIAN:
            points = 2000

        self.score += points * self.combo
        self.combo = min(4, self.combo + 1)
        self.combo_timer = self.COMBO_MAX_DURATION

    def take_damage_penalty(self):
        """Taking damage drops the active combo multiplier by 1 step."""
        if self.combo > 1:
            self.combo -= 1
            self.combo_timer = min(self.combo_timer, 2.0)

    def update(self, dt: float):
        if self.combo_timer > 0.0:
            self.combo_timer -= dt
            if self.combo_timer <= 0.0:
                self.combo = 1
                self.combo_timer = 0.0

    @property
    def combo_ratio(self) -> float:
        """Returns 0.0 to 1.0 fraction of remaining combo window."""
        return max(0.0, min(1.0, self.combo_timer / self.COMBO_MAX_DURATION))
