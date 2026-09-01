"""Level Progression and Structured Wave Spawner."""
import random
from typing import List, Optional
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
    STATE_COMBAT = "COMBAT"
    STATE_INTERMISSION = "INTERMISSION"
    STATE_ARENA_CLEARED = "ARENA_CLEARED"

    def __init__(self):
        self.current_arena_id = ARENA_01_KEPLER_RELAY
        self.current_wave = 1
        self.max_waves = 3
        self.wave_state = self.STATE_COMBAT
        self.intermission_timer = 0.0
        self.intermission_duration = 3.0
        self.is_arena_cleared = False
        self.enemies_remaining = 0
        self.boss_spawned = False

    def start_arena(self, arena_id: str, beacon=None) -> List[EnemyBase]:
        """Initializes wave progression for the selected arena."""
        self.current_arena_id = arena_id
        self.current_wave = 1
        self.is_arena_cleared = False
        self.wave_state = self.STATE_COMBAT
        self.intermission_timer = 0.0
        self.boss_spawned = False

        if arena_id == ARENA_01_KEPLER_RELAY:
            self.max_waves = 3
            if beacon:
                beacon.is_active = False  # Locked until all waves are cleared
        elif arena_id == ARENA_02_SUNDERED_RIFT:
            self.max_waves = 4  # 3 normal waves + Boss wave
            if beacon:
                beacon.is_active = True

        return self._spawn_wave(self.current_arena_id, self.current_wave)

    def init_arena_enemies(self, arena_id: str) -> List[EnemyBase]:
        """Backward-compatible alias for start_arena."""
        return self.start_arena(arena_id)

    def _spawn_wave(self, arena_id: str, wave_num: int) -> List[EnemyBase]:
        """Spawns structured enemy formations based on arena and wave index."""
        enemies: List[EnemyBase] = []

        if arena_id == ARENA_01_KEPLER_RELAY:
            if wave_num == 1:
                # Wave 1: 3 Melee Stalkers
                enemies.append(MeleeRiftStalker(Vector3(-14.0, 0.0, 18.0)))
                enemies.append(MeleeRiftStalker(Vector3(14.0, 0.0, 18.0)))
                enemies.append(MeleeRiftStalker(Vector3(0.0, 0.0, 24.0)))
            elif wave_num == 2:
                # Wave 2: 2 Melee Stalkers + 2 Ranged Spitters
                enemies.append(MeleeRiftStalker(Vector3(-18.0, 0.0, 16.0)))
                enemies.append(MeleeRiftStalker(Vector3(18.0, 0.0, 16.0)))
                enemies.append(RangedRiftSpitter(Vector3(-12.0, 0.0, 28.0)))
                enemies.append(RangedRiftSpitter(Vector3(12.0, 0.0, 28.0)))
            elif wave_num == 3:
                # Wave 3: 3 Melee Stalkers + 2 Ranged Spitters
                enemies.append(MeleeRiftStalker(Vector3(-20.0, 0.0, 12.0)))
                enemies.append(MeleeRiftStalker(Vector3(0.0, 0.0, 22.0)))
                enemies.append(MeleeRiftStalker(Vector3(20.0, 0.0, 12.0)))
                enemies.append(RangedRiftSpitter(Vector3(-16.0, 0.0, 32.0)))
                enemies.append(RangedRiftSpitter(Vector3(16.0, 0.0, 32.0)))

        elif arena_id == ARENA_02_SUNDERED_RIFT:
            if wave_num == 1:
                # Wave 1: 3 Stalkers + 2 Spitters
                enemies.append(MeleeRiftStalker(Vector3(-18.0, 0.0, 5.0)))
                enemies.append(MeleeRiftStalker(Vector3(18.0, 0.0, 5.0)))
                enemies.append(MeleeRiftStalker(Vector3(0.0, 0.0, 15.0)))
                enemies.append(RangedRiftSpitter(Vector3(-22.0, 0.0, 25.0)))
                enemies.append(RangedRiftSpitter(Vector3(22.0, 0.0, 25.0)))
            elif wave_num == 2:
                # Wave 2: 4 Stalkers + 3 Spitters
                enemies.append(MeleeRiftStalker(Vector3(-22.0, 0.0, -5.0)))
                enemies.append(MeleeRiftStalker(Vector3(22.0, 0.0, -5.0)))
                enemies.append(MeleeRiftStalker(Vector3(-12.0, 0.0, 18.0)))
                enemies.append(MeleeRiftStalker(Vector3(12.0, 0.0, 18.0)))
                enemies.append(RangedRiftSpitter(Vector3(-20.0, 0.0, 32.0)))
                enemies.append(RangedRiftSpitter(Vector3(0.0, 0.0, 38.0)))
                enemies.append(RangedRiftSpitter(Vector3(20.0, 0.0, 32.0)))
            elif wave_num == 3:
                # Wave 3: 2 Stalkers + 4 Spitters
                enemies.append(MeleeRiftStalker(Vector3(-15.0, 0.0, 10.0)))
                enemies.append(MeleeRiftStalker(Vector3(15.0, 0.0, 10.0)))
                enemies.append(RangedRiftSpitter(Vector3(-28.0, 0.0, 20.0)))
                enemies.append(RangedRiftSpitter(Vector3(-10.0, 0.0, 38.0)))
                enemies.append(RangedRiftSpitter(Vector3(10.0, 0.0, 38.0)))
                enemies.append(RangedRiftSpitter(Vector3(28.0, 0.0, 20.0)))
            elif wave_num == 4:
                # Boss Encounter: Rift Guardian Boss + 2 Elite Stalker guards
                self.boss_spawned = True
                boss = RiftGuardianBoss(Vector3(0.0, 0.0, 35.0))
                enemies.append(boss)
                enemies.append(MeleeRiftStalker(Vector3(-22.0, 0.0, 15.0)))
                enemies.append(MeleeRiftStalker(Vector3(22.0, 0.0, 15.0)))

        self.enemies_remaining = len(enemies)
        return enemies

    def update(
        self,
        dt: float,
        enemies: List[EnemyBase],
        score_manager=None,
        beacon=None
    ) -> List[EnemyBase]:
        """
        Updates wave progression state, handles intermission timers,
        and spawns incoming enemy waves.
        """
        alive_enemies = [e for e in enemies if not e.is_dead]
        self.enemies_remaining = len(alive_enemies)

        if self.wave_state == self.STATE_COMBAT:
            if self.enemies_remaining == 0:
                if self.current_wave < self.max_waves:
                    # Completed wave -> enter intermission countdown
                    self.wave_state = self.STATE_INTERMISSION
                    self.intermission_timer = self.intermission_duration
                    if score_manager:
                        score_manager.add_score(300 * self.current_wave)
                else:
                    # Cleared all waves in this arena!
                    self.wave_state = self.STATE_ARENA_CLEARED
                    self.is_arena_cleared = True
                    if score_manager:
                        score_manager.add_score(1500)
                    if beacon:
                        beacon.is_active = True  # Unlock Rift Beacon for teleportation

        elif self.wave_state == self.STATE_INTERMISSION:
            self.intermission_timer -= dt
            if self.intermission_timer <= 0.0:
                self.current_wave += 1
                self.wave_state = self.STATE_COMBAT
                new_wave_enemies = self._spawn_wave(self.current_arena_id, self.current_wave)
                enemies.extend(new_wave_enemies)

        return enemies

    def get_objective_title(self) -> str:
        """Returns primary objective string for 2D HUD."""
        if self.is_arena_cleared:
            if self.current_arena_id == ARENA_01_KEPLER_RELAY:
                return "ARENA 1 CLEARED — RIFT BEACON ONLINE"
            else:
                return "SUNDERED RIFT CLEARED"

        if self.wave_state == self.STATE_INTERMISSION:
            next_w = self.current_wave + 1
            if self.current_arena_id == ARENA_02_SUNDERED_RIFT and next_w == 4:
                return f"WAVE {self.current_wave} CLEARED! BOSS BREACH IN {max(0.0, self.intermission_timer):.1f}s"
            return f"WAVE {self.current_wave} CLEARED! WAVE {next_w} IN {max(0.0, self.intermission_timer):.1f}s"

        if self.current_arena_id == ARENA_02_SUNDERED_RIFT and self.current_wave == 4:
            return "OBJECTIVE: DEFEAT THE RIFT GUARDIAN BOSS"

        return f"OBJECTIVE: CLEAR WAVE {self.current_wave}/{self.max_waves}"

    def get_objective_subtitle(self) -> str:
        """Returns secondary status / remaining enemy count string."""
        if self.is_arena_cleared:
            if self.current_arena_id == ARENA_01_KEPLER_RELAY:
                return "PROCEED TO CENTRAL PLATFORM & PRESS 'F' TO TELEPORT"
            else:
                return "DIMENSIONAL BREACH NEUTRALIZED"

        if self.wave_state == self.STATE_INTERMISSION:
            return "PREPARE FOR INCOMING ENEMY FORMATION"

        if self.current_arena_id == ARENA_02_SUNDERED_RIFT and self.current_wave == 4:
            return "DESTROY ROTATING SHIELDS & EXPOSE CORE"

        return f"ENEMIES REMAINING: {self.enemies_remaining}"
