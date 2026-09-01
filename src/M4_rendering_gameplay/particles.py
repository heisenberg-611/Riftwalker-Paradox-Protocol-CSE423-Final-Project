"""Particle Emitters for Teleportation Vortex, Jet Thrusters, and Hit Impacts."""
import random
from typing import List, Tuple
from OpenGL.GL import *
from OpenGL.GLUT import *
from src.shared.math3d import Vector3
import math


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
                random.uniform(-4.0, 4.0),
                random.uniform(1.0, 5.0),
                random.uniform(-4.0, 4.0)
            )
            color = (1.0, random.uniform(0.5, 0.95), 0.1)
            self.particles.append(Particle(hit_point, vel, color, 0.08, random.uniform(0.3, 0.6)))

    def spawn_pickup_burst(self, center: Vector3, count: int = 18):
        """Cyan and Magenta energy sparkle burst on collecting Rift Energy."""
        for _ in range(count):
            vel = Vector3(
                random.uniform(-2.5, 2.5),
                random.uniform(2.0, 6.5),
                random.uniform(-2.5, 2.5)
            )
            color = (
                random.choice([0.0, 0.9]),
                random.uniform(0.8, 1.0),
                1.0
            )
            self.particles.append(Particle(center + Vector3(0.0, 1.0, 0.0), vel, color, 0.12, random.uniform(0.5, 0.9)))

    def spawn_death_burst(self, center: Vector3, count: int = 24):
        """Obsidian shards & glowing violet rift energy burst when alien dies."""
        for _ in range(count):
            vel = Vector3(
                random.uniform(-5.0, 5.0),
                random.uniform(1.5, 6.0),
                random.uniform(-5.0, 5.0)
            )
            color = (
                random.uniform(0.4, 0.9),
                random.uniform(0.0, 0.3),
                random.uniform(0.7, 1.0)
            )
            self.particles.append(Particle(center + Vector3(0.0, 1.0, 0.0), vel, color, 0.15, random.uniform(0.6, 1.1)))

    def spawn_chrono_ripple(self, center: Vector3, count: int = 28):
        """Radial expanding time distortion wave on Chrono Slow activation."""
        for i in range(count):
            angle = (3.14159 * 2.0 / count) * i
            vel = Vector3(
                math.cos(angle) * random.uniform(6.0, 10.0),
                random.uniform(0.2, 1.5),
                math.sin(angle) * random.uniform(6.0, 10.0)
            )
            color = (0.0, random.uniform(0.7, 1.0), 1.0)
            self.particles.append(Particle(center + Vector3(0.0, 0.8, 0.0), vel, color, 0.14, random.uniform(0.5, 0.8)))

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
