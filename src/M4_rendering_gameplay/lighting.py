"""Multi-Source Dynamic Lighting Setup."""
from OpenGL.GL import *
from src.shared.math3d import Vector3


class LightingSystem:
    @staticmethod
    def init_lighting():
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_SMOOTH)

        # Global Ambient Light (Vibrant space ambient)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.45, 0.45, 0.55, 1.0])

        # Light 0: Directional Sunlight / Key Light
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.35, 0.35, 0.45, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.8, 0.8, 0.9, 1.0])
        glLightfv(GL_LIGHT0, GL_POSITION, [50.0, 120.0, 40.0, 0.0])  # Directional (w=0)

    @staticmethod
    def update_point_lights(beacon_pos: Vector3, is_beacon_active: bool):
        # Light 1: Dynamic Point Light at Rift Beacon
        if is_beacon_active:
            glEnable(GL_LIGHT1)
            glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.2, 0.9, 1.0, 1.0])
            glLightfv(GL_LIGHT1, GL_SPECULAR, [0.4, 1.0, 1.0, 1.0])
            glLightfv(GL_LIGHT1, GL_POSITION, [beacon_pos.x, beacon_pos.y + 2.0, beacon_pos.z, 1.0])
            glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 1.0)
            glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.03)
            glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.003)
        else:
            glDisable(GL_LIGHT1)

