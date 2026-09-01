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


class LaserTracer:
    __slots__ = ('start_pos', 'end_pos', 'color', 'life', 'max_life', 'is_overcharged')

    def __init__(self, start_pos: Vector3, end_pos: Vector3, color: Tuple[float, float, float] = (0.0, 0.95, 1.0), life: float = 0.22, is_overcharged: bool = False):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color
        self.life = life
        self.max_life = life
        self.is_overcharged = is_overcharged


class ParticleSystem:
    def __init__(self):
        self.particles: List[Particle] = []
        self.tracers: List[LaserTracer] = []

    def spawn_laser_tracer(
        self,
        start_pos: Vector3,
        end_pos: Vector3,
        color: Tuple[float, float, float] = (0.0, 0.95, 1.0),
        is_overcharged: bool = False
    ):
        """Draws an intensely glowing neon laser tracer line from gun to target."""
        if is_overcharged:
            tracer_color = (1.0, 0.85, 0.25)
            self.tracers.append(LaserTracer(start_pos, end_pos, tracer_color, life=0.32, is_overcharged=True))
        else:
            self.tracers.append(LaserTracer(start_pos, end_pos, color, life=0.22, is_overcharged=False))

    def spawn_muzzle_flash(self, barrel_pos: Vector3, is_overcharged: bool = False):
        """Spawns bright sparks and flash burst at weapon muzzle."""
        count = 22 if is_overcharged else 10
        for _ in range(count):
            vel = Vector3(
                random.uniform(-4.5, 4.5),
                random.uniform(-4.5, 4.5),
                random.uniform(-4.5, 4.5)
            )
            if is_overcharged:
                color = random.choice([(1.0, 0.85, 0.2), (1.0, 0.3, 0.8), (1.0, 1.0, 1.0)])
            else:
                color = (0.3, 0.95, 1.0)
            self.particles.append(Particle(barrel_pos, vel, color, 0.14 if is_overcharged else 0.12, random.uniform(0.12, 0.25)))

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

        for t in self.tracers:
            t.life -= dt
        self.tracers = [t for t in self.tracers if t.life > 0.0]

    def draw(self):
        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)

        # 1. Render glowing 3D Laser Tracer Beams (Dual-pass glow and intense core)
        if self.tracers:
            for t in self.tracers:
                alpha = max(0.0, min(1.0, t.life / t.max_life))
                # Pass A: Outer glow beam
                outer_w = 11.0 if t.is_overcharged else 6.0
                glLineWidth(outer_w)
                glBegin(GL_LINES)
                glColor4f(t.color[0], t.color[1], t.color[2], alpha * 0.85)
                glVertex3f(t.start_pos.x, t.start_pos.y, t.start_pos.z)
                glVertex3f(t.end_pos.x, t.end_pos.y, t.end_pos.z)
                glEnd()

                # Pass B: Inner intense core
                inner_w = 4.5 if t.is_overcharged else 2.5
                glLineWidth(inner_w)
                glBegin(GL_LINES)
                if t.is_overcharged:
                    glColor4f(1.0, 1.0, 0.85, alpha)
                else:
                    glColor4f(0.85, 1.0, 1.0, alpha)
                glVertex3f(t.start_pos.x, t.start_pos.y, t.start_pos.z)
                glVertex3f(t.end_pos.x, t.end_pos.y, t.end_pos.z)
                glEnd()

        # 2. Render Point Particles
        glPointSize(5.0)
        glBegin(GL_POINTS)
        for p in self.particles:
            alpha = max(0.0, min(1.0, p.life / p.max_life))
            glColor4f(p.color[0], p.color[1], p.color[2], alpha)
            glVertex3f(p.pos.x, p.pos.y, p.pos.z)
        glEnd()

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)


