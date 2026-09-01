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

    @staticmethod
    def bind_suit_material():
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.6, 0.6, 0.65, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.95, 0.95, 1.0, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.5, 0.5, 0.6, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 40.0)
        from src.shared.texture_loader import TextureManager
        TextureManager.bind(TextureManager.get("astronaut_suit"))

    @staticmethod
    def bind_visor_material():
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.3, 0.8, 1.0, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.4, 0.9, 1.0, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 100.0)
        from src.shared.texture_loader import TextureManager
        TextureManager.bind(TextureManager.get("astronaut_visor"))

    @staticmethod
    def bind_metal_wall_material():
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.65, 0.70, 0.75, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.6, 0.6, 0.7, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 32.0)
        from src.shared.texture_loader import TextureManager
        TextureManager.bind(TextureManager.get("kepler_metal_wall"))

    @staticmethod
    def bind_floor_panel_material():
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.70, 0.75, 0.80, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.5, 0.5, 0.6, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 24.0)
        from src.shared.texture_loader import TextureManager
        TextureManager.bind(TextureManager.get("kepler_floor_panel"))

    @staticmethod
    def bind_rock_material():
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.6, 0.5, 0.7, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.4, 0.3, 0.5, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 16.0)
        from src.shared.texture_loader import TextureManager
        TextureManager.bind(TextureManager.get("sundered_rock"))

    @staticmethod
    def bind_crystal_material():
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.5, 0.3, 0.7, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1.0, 0.5, 1.0, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 0.9, 1.0, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 96.0)
        from src.shared.texture_loader import TextureManager
        TextureManager.bind(TextureManager.get("sundered_crystal"))

    @staticmethod
    def bind_alien_carapace():
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.5, 0.4, 0.6, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.9, 0.8, 1.0, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.8, 0.5, 0.9, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 60.0)
        from src.shared.texture_loader import TextureManager
        TextureManager.bind(TextureManager.get("rift_stalker_body"))

    @staticmethod
    def bind_beacon_material():
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.6, 0.9, 1.0, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.8, 1.0, 1.0, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 80.0)
        from src.shared.texture_loader import TextureManager
        TextureManager.bind(TextureManager.get("beacon_runes"))


    @staticmethod
    def unbind_all():
        from src.shared.texture_loader import TextureManager
        TextureManager.unbind()


