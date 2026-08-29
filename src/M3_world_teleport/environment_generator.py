"""Modular Environment Props & Obstacle Generators."""
from OpenGL.GL import *
from OpenGL.GLUT import *
from src.shared.math3d import Vector3


class EnvironmentGenerator:
    @staticmethod
    def draw_crate(pos: Vector3, size: float = 2.0):
        glPushMatrix()
        glTranslatef(pos.x, pos.y + size * 0.5, pos.z)
        glColor3f(0.35, 0.38, 0.42)
        glScalef(size, size, size)
        glutSolidCube(1.0)
        # Warning stripes / edges
        glColor3f(0.85, 0.65, 0.1)
        glutWireCube(1.01)
        glPopMatrix()

    @staticmethod
    def draw_pillar(pos: Vector3, radius: float = 1.0, height: float = 6.0):
        glPushMatrix()
        glTranslatef(pos.x, pos.y, pos.z)
        glColor3f(0.25, 0.28, 0.32)
        glPushMatrix()
        glTranslatef(0.0, height * 0.5, 0.0)
        glScalef(radius * 2, height, radius * 2)
        glutSolidCube(1.0)
        glPopMatrix()
        # Glowing capacitor ring
        glColor3f(0.0, 0.7, 0.9)
        glTranslatef(0.0, height * 0.8, 0.0)
        glutSolidTorus(0.15, radius * 1.1, 8, 16)
        glPopMatrix()

    @staticmethod
    def draw_crystal_spire(pos: Vector3, height: float = 7.0):
        glPushMatrix()
        glTranslatef(pos.x, pos.y, pos.z)
        glColor3f(0.7, 0.1, 0.85)  # Glowing Purple Void Crystal
        glPushMatrix()
        glTranslatef(0.0, height * 0.5, 0.0)
        glScalef(1.2, height, 1.2)
        glutSolidOctahedron()
        glPopMatrix()
        glPopMatrix()
