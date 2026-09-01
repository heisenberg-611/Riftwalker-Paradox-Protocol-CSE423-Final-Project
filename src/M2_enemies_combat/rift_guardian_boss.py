"""Boss Encounter: The Rift Guardian."""
import math
from typing import List
from src.shared.math3d import Vector3
from src.shared.constants import BOSS_RIFT_GUARDIAN
from src.M2_enemies_combat.enemy_base import EnemyBase
from src.M2_enemies_combat.alien_generator import AlienGenerator
from src.M2_enemies_combat.weapon_system import Projectile


class RiftGuardianBoss(EnemyBase):
    def __init__(self, pos: Vector3):
        super().__init__(
            enemy_id=BOSS_RIFT_GUARDIAN,
            pos=pos,
            hp=350.0,
            speed=2.0,
            radius=3.0
        )
        self.attack_timer = 2.0
        self.burst_cooldown = 3.5
        self.phase = 1

    def update_and_attack(self, player_pos: Vector3, dt: float) -> List[Projectile]:
        super().update(player_pos, dt)
        projectiles: List[Projectile] = []
        if self.is_dead:
            return projectiles

        # Check phase transition
        if self.hp < 175.0:
            self.phase = 2

        self.attack_timer -= dt
        if self.attack_timer <= 0.0:
            self.attack_timer = self.burst_cooldown if self.phase == 1 else self.burst_cooldown * 0.6
            # Spawn radial projectile burst
            num_bolts = 6 if self.phase == 1 else 10
            for i in range(num_bolts):
                angle = (math.pi * 2 / num_bolts) * i + self.anim_time
                dir_vec = Vector3(math.sin(angle), 0.0, math.cos(angle)).normalized()
                projectiles.append(
                    Projectile(
                        origin=self.position + Vector3(0.0, 3.5, 0.0),
                        direction=dir_vec,
                        speed=14.0,
                        damage=20.0,
                        color=(1.0, 0.1, 0.3)
                    )
                )

        return projectiles

    def render_model(self):
        AlienGenerator.draw_guardian_boss(self.anim_time, phase=self.phase)
