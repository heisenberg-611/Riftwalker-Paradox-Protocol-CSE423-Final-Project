"""Abstract Base Class for Arenas."""
from typing import List
from src.shared.math3d import Vector3
from src.M3_world_teleport.rift_beacon import RiftBeacon


class ArenaBase:
    def __init__(self, arena_id: str, half_extent: float):
        self.arena_id = arena_id
        self.half_extent = half_extent
        self.rift_beacons: List[RiftBeacon] = []

    def update(self, dt: float):
        for beacon in self.rift_beacons:
            beacon.update(dt)

    def draw(self):
        raise NotImplementedError("Subclasses must implement draw()")
