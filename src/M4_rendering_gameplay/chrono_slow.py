"""Chrono Slow Time Dilation Resource and Mechanics Manager."""
from src.shared.constants import (
    MAX_CHRONO_CHARGE,
    CHRONO_SLOW_DURATION,
    CHRONO_SLOW_FACTOR
)


class ChronoSlowManager:
    """
    Manages the locked-down Chrono Slow gameplay mechanic:
    - Charge bar starts at 0% and fills strictly from gameplay actions (defeating enemies, energy pickups).
    - Can only be activated when charge reaches 100%.
    - Activating consumes the full 100% charge and resets the meter to 0%.
    - Runs for a fixed duration of ~5.0 seconds.
    - During the effect, enemy AI and projectiles run at 30% speed (slow_factor = 0.30).
    - Pure delta-time scaling without world rewind buffers.
    """
    def __init__(self):
        self.charge = 0.0
        self.max_charge = MAX_CHRONO_CHARGE
        self.is_active = False
        self.duration = CHRONO_SLOW_DURATION
        self.active_time_remaining = 0.0
        self.slow_factor = CHRONO_SLOW_FACTOR

    def add_charge(self, amount: float):
        """Adds charge from gameplay actions (enemy defeat / energy pickups)."""
        if not self.is_active:
            self.charge = min(self.max_charge, self.charge + amount)

    def can_activate(self) -> bool:
        """Chrono Slow can ONLY be activated when the charge bar reaches 100%."""
        return (not self.is_active) and (self.charge >= self.max_charge)

    def activate(self) -> bool:
        """
        Attempts to activate Chrono Slow.
        Consumes full 100% charge and resets to 0% if successful.
        """
        if self.can_activate():
            self.is_active = True
            self.charge = 0.0  # Full consumption & reset
            self.active_time_remaining = self.duration
            return True
        return False

    def update(self, dt: float):
        """Updates active timer countdown (uses unscaled real dt)."""
        if self.is_active:
            self.active_time_remaining -= dt
            if self.active_time_remaining <= 0.0:
                self.is_active = False
                self.active_time_remaining = 0.0

    @property
    def current_time_scale(self) -> float:
        """Simulation factor for enemies and projectiles (0.30 while active, 1.0 normally)."""
        return self.slow_factor if self.is_active else 1.0

    @property
    def charge_percentage(self) -> float:
        return (self.charge / self.max_charge) * 100.0
