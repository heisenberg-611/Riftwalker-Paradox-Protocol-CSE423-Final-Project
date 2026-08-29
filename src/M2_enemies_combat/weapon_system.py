"""Weapon System, Projectile Manager, and Tracers."""
from typing import List, Tuple
from OpenGL.GL import *
from OpenGL.GLUT import *
from src.shared.math3d import Vector3


class Projectile:
    def __init__(
        self,
        origin: Vector3,
        direction: Vector3,
        speed: float = 20.0,
        damage: float = 15.0,
        color: Tuple[float, float, float] = (1.0, 0.2, 0.2),
        radius: float = 0.35,
        lifetime: float = 6.0
    ):
        self.position = origin
        self.direction = direction.normalized()
        self.speed = speed
        self.damage = damage
        self.color = color
        self.radius = radius
        self.lifetime = lifetime
        self.is_alive = True

    def update(self, dt: float):
        self.lifetime -= dt
        if self.lifetime <= 0.0:
            self.is_alive = False
            return
        self.position = self.position + self.direction * (self.speed * dt)

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glColor3f(*self.color)
        glutSolidSphere(self.radius, 8, 8)
        glPopMatrix()


class WeaponSystem:
    def __init__(self):
        self.enemy_projectiles: List[Projectile] = []

    def add_projectile(self, proj: Projectile):
        self.enemy_projectiles.append(proj)

    def add_projectiles(self, projs: List[Projectile]):
        self.enemy_projectiles.extend(projs)

    def update(self, dt: float):
        for p in self.enemy_projectiles:
            p.update(dt)
        self.enemy_projectiles = [p for p in self.enemy_projectiles if p.is_alive]

    def draw(self):
        for p in self.enemy_projectiles:
            p.draw()
