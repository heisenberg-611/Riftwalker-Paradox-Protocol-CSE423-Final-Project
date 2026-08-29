"""Chrono Slow Time Dilation Resource and Mechanics Manager."""
from src.shared.constants import (
    MAX_CHRONO_ENERGY,
    CHRONO_DRAIN_RATE,
    CHRONO_RECHARGE_RATE,
    CHRONO_SLOW_FACTOR
)


class ChronoSlowManager:
    def __init__(self):
        self.energy = MAX_CHRONO_ENERGY
        self.max_energy = MAX_CHRONO_ENERGY
        self.is_active = False
        self.slow_factor = CHRONO_SLOW_FACTOR

    def toggle(self) -> bool:
        if self.is_active:
            self.is_active = False
        else:
            if self.energy > 15.0:
                self.is_active = True
        return self.is_active

    def update(self, dt: float):
        if self.is_active:
            self.energy = max(0.0, self.energy - CHRONO_DRAIN_RATE * dt)
            if self.energy <= 0.0:
                self.is_active = False
        else:
            self.energy = min(self.max_energy, self.energy + CHRONO_RECHARGE_RATE * dt)

    @property
    def current_time_scale(self) -> float:
        return self.slow_factor if self.is_active else 1.0
