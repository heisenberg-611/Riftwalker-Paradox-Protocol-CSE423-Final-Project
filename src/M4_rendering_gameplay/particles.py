"""Particle Emitters for Teleportation Vortex, Jet Thrusters, and Hit Impacts."""
import random
from typing import List, Tuple
from OpenGL.GL import *
from OpenGL.GLUT import *
from src.shared.math3d import Vector3


class Particle:
    __slots__ = ('pos', 'vel', 'color', 'size', 'life', 'max_life')

    def __init__(self, pos: Vector3, vel: Vector3, color: Tuple[float, float, float], size: float, life: float):
        self.pos = pos
        self.vel = vel
        self.color = color
        self.size = size
        self.life = life
        self.max_life = life


class ParticleSystem:
    def __init__(self):
        self.particles: List[Particle] = []

    def spawn_teleport_vortex(self, center: Vector3, count: int = 25):
        for _ in range(count):
            offset = Vector3(
                random.uniform(-1.5, 1.5),
                random.uniform(0.2, 3.5),
                random.uniform(-1.5, 1.5)
            )
            vel = Vector3(
                -offset.z * 2.0 + random.uniform(-0.5, 0.5),
                random.uniform(0.5, 2.0),
                offset.x * 2.0 + random.uniform(-0.5, 0.5)
            )
            color = (0.0, random.uniform(0.7, 1.0), 1.0)
            self.particles.append(Particle(center + offset, vel, color, random.uniform(0.08, 0.18), 1.2))

    def spawn_hit_sparks(self, hit_point: Vector3, count: int = 12):
        for _ in range(count):
            vel = Vector3(
                random.uniform(-3.0, 3.0),
                random.uniform(1.0, 4.0),
                random.uniform(-3.0, 3.0)
            )
            color = (1.0, random.uniform(0.4, 0.9), 0.1)
            self.particles.append(Particle(hit_point, vel, color, 0.08, random.uniform(0.3, 0.6)))

    def update(self, dt: float):
        for p in self.particles:
            p.pos = p.pos + p.vel * dt
            p.life -= dt
        self.particles = [p for p in self.particles if p.life > 0.0]

    def draw(self):
        glDisable(GL_LIGHTING)
        glPointSize(4.0)
        glBegin(GL_POINTS)
        for p in self.particles:
            alpha = p.life / p.max_life
            glColor3f(p.color[0] * alpha, p.color[1] * alpha, p.color[2] * alpha)
            glVertex3f(p.pos.x, p.pos.y, p.pos.z)
        glEnd()
        glEnable(GL_LIGHTING)
