"""Melee Alien: Fast agile stalking predator."""
from src.shared.math3d import Vector3
from src.shared.constants import ENEMY_MELEE_RIFT_STALKER
from src.M2_enemies_combat.enemy_base import EnemyBase
from src.M2_enemies_combat.alien_generator import AlienGenerator


class MeleeRiftStalker(EnemyBase):
    def __init__(self, pos: Vector3):
        super().__init__(
            enemy_id=ENEMY_MELEE_RIFT_STALKER,
            pos=pos,
            hp=45.0,
            speed=7.5,
            radius=1.2
        )
        self.attack_damage = 15.0
        self.attack_cooldown = 1.0
        self.attack_timer = 0.0

    def update(self, player_pos: Vector3, dt: float):
        super().update(player_pos, dt)
        if self.is_dead:
            return

        self.attack_timer = max(0.0, self.attack_timer - dt)

        to_player = player_pos - self.position
        dist = to_player.length()

        # Move towards player if not in melee contact
        if dist > 1.8:
            move_dir = to_player.normalized()
            self.position = self.position + move_dir * (self.speed * dt)

    def render_model(self):
        AlienGenerator.draw_stalker(self.anim_time)
