"""Procedural 3D Geometric Primitive Helpers."""
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class Primitives:
    _quadric = None

    @classmethod
    def get_quadric(cls):
        if cls._quadric is None:
            cls._quadric = gluNewQuadric()
            gluQuadricNormals(cls._quadric, GLU_SMOOTH)
        return cls._quadric

    @classmethod
    def draw_cube(cls, size: float = 1.0):
        glutSolidCube(size)

    @classmethod
    def draw_sphere(cls, radius: float = 1.0, slices: int = 16, stacks: int = 16):
        glutSolidSphere(radius, slices, stacks)

    @classmethod
    def draw_cylinder(cls, base_rad: float, top_rad: float, height: float, slices: int = 16, stacks: int = 1):
        q = cls.get_quadric()
        gluCylinder(q, base_rad, top_rad, height, slices, stacks)

    @classmethod
    def draw_torus(cls, inner_radius: float, outer_radius: float, nsides: int = 12, rings: int = 24):
        glutSolidTorus(inner_radius, outer_radius, nsides, rings)
