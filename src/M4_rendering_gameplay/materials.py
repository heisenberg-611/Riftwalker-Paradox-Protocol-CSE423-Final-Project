"""Preset Optical Materials and Color Properties."""
from OpenGL.GL import *


class Materials:
    @staticmethod
    def set_suit_material():
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.4, 0.4, 0.45, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.75, 0.75, 0.8, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.6, 0.6, 0.7, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 40.0)

    @staticmethod
    def set_visor_material():
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.1, 0.6, 0.8, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.0, 0.8, 1.0, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 100.0)

    @staticmethod
    def set_alien_carapace():
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.1, 0.25, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.4, 0.2, 0.5, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.8, 0.4, 0.9, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 60.0)

    @staticmethod
    def set_beacon_energy():
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.8, 1.0, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.0, 0.9, 1.0, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 80.0)
