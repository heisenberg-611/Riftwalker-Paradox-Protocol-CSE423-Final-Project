"""Multi-Source Dynamic Lighting Setup."""
from OpenGL.GL import *
from src.shared.math3d import Vector3


class LightingSystem:
    @staticmethod
    def init_lighting():
        glEnable(GL_LIGHTING)
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_SMOOTH)

        # Global Ambient Light
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.25, 0.25, 0.3, 1.0])

        # Light 0: Directional Sunlight
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.15, 0.15, 0.2, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.85, 0.85, 0.9, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.6, 1.0])
        glLightfv(GL_LIGHT0, GL_POSITION, [50.0, 100.0, 30.0, 0.0])  # Directional (w=0)

    @staticmethod
    def update_point_lights(beacon_pos: Vector3, is_beacon_active: bool):
        # Light 1: Dynamic Point Light at Rift Beacon
        if is_beacon_active:
            glEnable(GL_LIGHT1)
            glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.0, 0.8, 1.0, 1.0])
            glLightfv(GL_LIGHT1, GL_SPECULAR, [0.2, 0.9, 1.0, 1.0])
            glLightfv(GL_LIGHT1, GL_POSITION, [beacon_pos.x, beacon_pos.y + 2.0, beacon_pos.z, 1.0])
            glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 1.0)
            glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.05)
            glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.005)
        else:
            glDisable(GL_LIGHT1)
