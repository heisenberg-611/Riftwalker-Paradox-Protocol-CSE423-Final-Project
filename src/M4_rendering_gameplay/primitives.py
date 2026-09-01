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
            gluQuadricTexture(cls._quadric, GL_TRUE)
        return cls._quadric

    @classmethod
    def draw_cube(cls, size: float = 1.0):
        glutSolidCube(size)

    @classmethod
    def draw_textured_cube(cls, size: float = 1.0, u_repeat: float = 1.0, v_repeat: float = 1.0):
        """Renders a 3D cube with explicit UV texture coordinates and surface normals."""
        h = size * 0.5
        glBegin(GL_QUADS)
        # Front Face (Z+)
        glNormal3f(0.0, 0.0, 1.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-h, -h,  h)
        glTexCoord2f(u_repeat, 0.0); glVertex3f( h, -h,  h)
        glTexCoord2f(u_repeat, v_repeat); glVertex3f( h,  h,  h)
        glTexCoord2f(0.0, v_repeat); glVertex3f(-h,  h,  h)

        # Back Face (Z-)
        glNormal3f(0.0, 0.0, -1.0)
        glTexCoord2f(u_repeat, 0.0); glVertex3f(-h, -h, -h)
        glTexCoord2f(u_repeat, v_repeat); glVertex3f(-h,  h, -h)
        glTexCoord2f(0.0, v_repeat); glVertex3f( h,  h, -h)
        glTexCoord2f(0.0, 0.0); glVertex3f( h, -h, -h)

        # Top Face (Y+)
        glNormal3f(0.0, 1.0, 0.0)
        glTexCoord2f(0.0, v_repeat); glVertex3f(-h,  h, -h)
        glTexCoord2f(0.0, 0.0); glVertex3f(-h,  h,  h)
        glTexCoord2f(u_repeat, 0.0); glVertex3f( h,  h,  h)
        glTexCoord2f(u_repeat, v_repeat); glVertex3f( h,  h, -h)

        # Bottom Face (Y-)
        glNormal3f(0.0, -1.0, 0.0)
        glTexCoord2f(u_repeat, v_repeat); glVertex3f(-h, -h, -h)
        glTexCoord2f(0.0, v_repeat); glVertex3f( h, -h, -h)
        glTexCoord2f(0.0, 0.0); glVertex3f( h, -h,  h)
        glTexCoord2f(u_repeat, 0.0); glVertex3f(-h, -h,  h)

        # Right Face (X+)
        glNormal3f(1.0, 0.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f( h, -h, -h)
        glTexCoord2f(u_repeat, 0.0); glVertex3f( h,  h, -h)
        glTexCoord2f(u_repeat, v_repeat); glVertex3f( h,  h,  h)
        glTexCoord2f(0.0, v_repeat); glVertex3f( h, -h,  h)

        # Left Face (X-)
        glNormal3f(-1.0, 0.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-h, -h, -h)
        glTexCoord2f(u_repeat, 0.0); glVertex3f(-h, -h,  h)
        glTexCoord2f(u_repeat, v_repeat); glVertex3f(-h,  h,  h)
        glTexCoord2f(0.0, v_repeat); glVertex3f(-h,  h, -h)
        glEnd()

    @classmethod
    def draw_textured_plane(cls, size_x: float, size_z: float, u_repeat: float = 1.0, v_repeat: float = 1.0):
        """Renders a flat horizontal plane with repeating UV texture coordinates."""
        hx = size_x * 0.5
        hz = size_z * 0.5
        glBegin(GL_QUADS)
        glNormal3f(0.0, 1.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-hx, 0.0, -hz)
        glTexCoord2f(0.0, v_repeat); glVertex3f(-hx, 0.0,  hz)
        glTexCoord2f(u_repeat, v_repeat); glVertex3f( hx, 0.0,  hz)
        glTexCoord2f(u_repeat, 0.0); glVertex3f( hx, 0.0, -hz)
        glEnd()

    @classmethod
    def draw_sphere(cls, radius: float = 1.0, slices: int = 16, stacks: int = 16):
        glutSolidSphere(radius, slices, stacks)

    @classmethod
    def draw_textured_sphere(cls, radius: float = 1.0, slices: int = 16, stacks: int = 16):
        q = cls.get_quadric()
        gluSphere(q, radius, slices, stacks)

    @classmethod
    def draw_cylinder(cls, base_rad: float, top_rad: float, height: float, slices: int = 16, stacks: int = 1):
        q = cls.get_quadric()
        gluCylinder(q, base_rad, top_rad, height, slices, stacks)

    @classmethod
    def draw_textured_cylinder(cls, base_rad: float, top_rad: float, height: float, slices: int = 16, stacks: int = 1):
        q = cls.get_quadric()
        gluCylinder(q, base_rad, top_rad, height, slices, stacks)

    @classmethod
    def draw_torus(cls, inner_radius: float, outer_radius: float, nsides: int = 12, rings: int = 24):
        glutSolidTorus(inner_radius, outer_radius, nsides, rings)


