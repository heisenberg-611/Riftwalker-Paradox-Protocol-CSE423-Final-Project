"""Modular Environment Props & Obstacle Generators."""
from OpenGL.GL import *
from OpenGL.GLUT import *
from src.shared.math3d import Vector3


class EnvironmentGenerator:
    @staticmethod
    def draw_crate(pos: Vector3, size: float = 2.0):
        from src.M4_rendering_gameplay.materials import Materials
        from src.M4_rendering_gameplay.primitives import Primitives
        glPushMatrix()
        glTranslatef(pos.x, pos.y + size * 0.5, pos.z)
        Materials.bind_metal_wall_material()
        glColor3f(0.85, 0.85, 0.9)
        Primitives.draw_textured_cube(size)
        Materials.unbind_all()
        # Warning stripes / edges
        glColor3f(0.85, 0.65, 0.1)
        glutWireCube(size * 1.01)
        glPopMatrix()

    @staticmethod
    def draw_pillar(pos: Vector3, radius: float = 1.0, height: float = 6.0):
        from src.M4_rendering_gameplay.materials import Materials
        from src.M4_rendering_gameplay.primitives import Primitives
        glPushMatrix()
        glTranslatef(pos.x, pos.y, pos.z)
        Materials.bind_metal_wall_material()
        glColor3f(0.8, 0.85, 0.9)
        glPushMatrix()
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        Primitives.draw_textured_cylinder(radius, radius, height, 16, 1)
        glPopMatrix()
        Materials.unbind_all()

        # Glowing capacitor ring
        glColor3f(0.0, 0.7, 0.9)
        glPushMatrix()
        glTranslatef(0.0, height * 0.8, 0.0)
        glutSolidTorus(0.15, radius * 1.1, 8, 16)
        glPopMatrix()
        glPopMatrix()

    @staticmethod
    def draw_crystal_spire(pos: Vector3, height: float = 7.0):
        from src.M4_rendering_gameplay.materials import Materials
        from src.M4_rendering_gameplay.primitives import Primitives
        glPushMatrix()
        glTranslatef(pos.x, pos.y, pos.z)
        Materials.bind_crystal_material()
        glColor3f(0.9, 0.4, 1.0)  # Glowing Purple Void Crystal
        glPushMatrix()
        glTranslatef(0.0, height * 0.5, 0.0)
        glScalef(1.2, height * 0.5, 1.2)
        Primitives.draw_textured_octahedron(1.0)
        glPopMatrix()
        Materials.unbind_all()
        glPopMatrix()


