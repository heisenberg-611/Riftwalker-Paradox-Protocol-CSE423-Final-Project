"""Ranged Alien: Stationary/Kiting plasma acid spitter."""
from typing import Optional
from src.shared.math3d import Vector3
from src.shared.constants import ENEMY_RANGED_RIFT_SPITTER
from src.M2_enemies_combat.enemy_base import EnemyBase
from src.M2_enemies_combat.alien_generator import AlienGenerator
from src.M2_enemies_combat.weapon_system import Projectile


class RangedRiftSpitter(EnemyBase):
    def __init__(self, pos: Vector3):
        super().__init__(
            enemy_id=ENEMY_RANGED_RIFT_SPITTER,
            pos=pos,
            hp=60.0,
            speed=3.0,
            radius=1.4
        )
        self.shoot_cooldown = 2.2
        self.shoot_timer = 1.0

    def update_and_shoot(self, player_pos: Vector3, dt: float) -> Optional[Projectile]:
        super().update(player_pos, dt)
        if self.is_dead:
            return None

        self.shoot_timer -= dt

        # Maintain distance of around 15-20 units from player
        to_player = player_pos - self.position
        dist = to_player.length()
        if dist < 12.0:
            # Back up
            move_dir = -to_player.normalized()
            self.position = self.position + move_dir * (self.speed * dt)
        elif dist > 25.0:
            # Advance closer
            move_dir = to_player.normalized()
            self.position = self.position + move_dir * (self.speed * dt)

        # Fire projectile when ready
        if self.shoot_timer <= 0.0:
            self.shoot_timer = self.shoot_cooldown
            aim_dir = (player_pos + Vector3(0.0, 1.2, 0.0) - (self.position + Vector3(0.0, 1.0, 0.0))).normalized()
            return Projectile(
                origin=self.position + Vector3(0.0, 1.0, 0.0),
                direction=aim_dir,
                speed=18.0,
                damage=15.0,
                color=(0.0, 1.0, 0.5)
            )
        return None

    def render_model(self):
        AlienGenerator.draw_spitter(self.anim_time)
