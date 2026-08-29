"""World Manager coordinating active Arena and Teleportation transitions."""
from typing import Dict, Optional
from src.shared.constants import ARENA_01_KEPLER_RELAY, ARENA_02_SUNDERED_RIFT
from src.shared.math3d import Vector3
from src.M3_world_teleport.arena_base import ArenaBase
from src.M3_world_teleport.arena_01_kepler_relay import ArenaKeplerRelay
from src.M3_world_teleport.arena_02_sundered_rift import ArenaSunderedRift


class World:
    def __init__(self):
        self.arenas: Dict[str, ArenaBase] = {
            ARENA_01_KEPLER_RELAY: ArenaKeplerRelay(),
            ARENA_02_SUNDERED_RIFT: ArenaSunderedRift(),
        }
        self.active_arena_id = ARENA_01_KEPLER_RELAY

    @property
    def current_arena(self) -> ArenaBase:
        return self.arenas[self.active_arena_id]

    def update(self, dt: float):
        self.current_arena.update(dt)

    def draw(self):
        self.current_arena.draw()

    def check_teleport_trigger(self, player_pos: Vector3) -> Optional[str]:
        """Returns destination arena ID if player activates a nearby beacon."""
        for beacon in self.current_arena.rift_beacons:
            if beacon.is_active and beacon.is_player_in_range(player_pos):
                return beacon.linked_arena_id
        return None

    def switch_arena(self, new_arena_id: str) -> Vector3:
        """Switches active arena and returns the destination spawn coordinate."""
        self.active_arena_id = new_arena_id
        if new_arena_id == ARENA_02_SUNDERED_RIFT:
            # Arrive at Sundered Rift entrance
            return Vector3(0.0, 0.0, -40.0)
        else:
            # Arrive back at Kepler Relay center
            return Vector3(0.0, 0.0, -10.0)
