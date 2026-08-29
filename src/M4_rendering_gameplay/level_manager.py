"""Level Progression and Wave Spawner."""
import random
from typing import List
from src.shared.constants import (
    ARENA_01_KEPLER_RELAY,
    ARENA_02_SUNDERED_RIFT
)
from src.shared.math3d import Vector3
from src.M2_enemies_combat.enemy_base import EnemyBase
from src.M2_enemies_combat.melee_rift_stalker import MeleeRiftStalker
from src.M2_enemies_combat.ranged_rift_spitter import RangedRiftSpitter
from src.M2_enemies_combat.rift_guardian_boss import RiftGuardianBoss


class LevelManager:
    def __init__(self):
        self.current_arena_id = ARENA_01_KEPLER_RELAY
        self.spawn_timer = 0.0
        self.boss_spawned = False

    def init_arena_enemies(self, arena_id: str) -> List[EnemyBase]:
        self.current_arena_id = arena_id
        enemies: List[EnemyBase] = []

        if arena_id == ARENA_01_KEPLER_RELAY:
            self.boss_spawned = False
            # Initial Kepler Relay wave
            for _ in range(4):
                pos = Vector3(random.uniform(-35.0, 35.0), 0.0, random.uniform(15.0, 45.0))
                enemies.append(MeleeRiftStalker(pos))
            for _ in range(2):
                pos = Vector3(random.uniform(-30.0, 30.0), 0.0, random.uniform(30.0, 45.0))
                enemies.append(RangedRiftSpitter(pos))

        elif arena_id == ARENA_02_SUNDERED_RIFT:
            # Boss encounter wave
            self.boss_spawned = True
            boss = RiftGuardianBoss(Vector3(0.0, 0.0, 35.0))
            enemies.append(boss)
            enemies.append(MeleeRiftStalker(Vector3(-25.0, 0.0, 15.0)))
            enemies.append(MeleeRiftStalker(Vector3(25.0, 0.0, 15.0)))

        return enemies
