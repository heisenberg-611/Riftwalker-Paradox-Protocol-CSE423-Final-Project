from typing import List
from src.shared.math3d import Vector3
from src.shared.collision import CollisionGeometry, Obstacle
from src.M3_world_teleport.rift_beacon import RiftBeacon
from src.M3_world_teleport.rift_energy_pickup import RiftEnergyPickup


class ArenaBase:
    def __init__(self, arena_id: str, half_extent: float):
        self.arena_id = arena_id
        self.half_extent = half_extent
        self.rift_beacons: List[RiftBeacon] = []
        self.energy_pickups: List[RiftEnergyPickup] = []
        self.obstacles: List[Obstacle] = []

    def get_obstacles(self) -> List[Obstacle]:
        return self.obstacles

    def resolve_collision(self, pos: Vector3, radius: float) -> Vector3:
        """Resolves horizontal collision against all obstacles in this arena."""
        return CollisionGeometry.resolve_obstacles(pos, radius, self.obstacles)

    def update(self, dt: float):
        for beacon in self.rift_beacons:
            beacon.update(dt)
        for pickup in self.energy_pickups:
            pickup.update(dt)

    def draw(self):
        raise NotImplementedError("Subclasses must implement draw()")

