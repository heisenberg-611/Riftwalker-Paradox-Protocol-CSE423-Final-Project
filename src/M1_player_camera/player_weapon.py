"""Player Hitscan Weapon System."""
from src.shared.constants import PRIMARY_FIRE_COOLDOWN, PRIMARY_FIRE_DAMAGE, PRIMARY_FIRE_RANGE
from src.shared.math3d import Vector3


class PlayerWeapon:
    def __init__(self):
        self.cooldown = PRIMARY_FIRE_COOLDOWN
        self.damage = PRIMARY_FIRE_DAMAGE
        self.range = PRIMARY_FIRE_RANGE
        self.time_since_last_shot = 999.0
        self.is_firing_effect_active = False

    def update(self, dt: float):
        self.time_since_last_shot += dt
        if self.time_since_last_shot > 0.08:
            self.is_firing_effect_active = False

    def can_fire(self) -> bool:
        return self.time_since_last_shot >= self.cooldown

    def trigger_shot(self) -> bool:
        if not self.can_fire():
            return False
        self.time_since_last_shot = 0.0
        self.is_firing_effect_active = True
        return True
