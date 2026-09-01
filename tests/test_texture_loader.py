"""Unit Tests for Texture Loader, TextureManager, and Material Texture Pipeline."""
import os
import unittest
from PIL import Image
from src.shared.texture_loader import TextureManager, load_texture, bind_texture, unbind_texture, get_texture
from src.M4_rendering_gameplay.materials import Materials
from src.M4_rendering_gameplay.primitives import Primitives


class TestTextureLoader(unittest.TestCase):
    def setUp(self):
        TextureManager.generate_all_disk_textures()

    def test_texture_directories_exist(self):
        """All texture category directories must exist on disk."""
        categories = ["environment", "characters", "weapons", "rift", "background"]
        for cat in categories:
            cat_dir = TextureManager.get_texture_dir(cat)
            self.assertTrue(os.path.isdir(cat_dir), f"Directory missing: {cat_dir}")

    def test_required_texture_files_generated(self):
        """All baseline required PNG texture assets must exist and be valid 512x512 RGBA PNGs."""
        expected_textures = [
            ("environment", "kepler_metal_wall.png"),
            ("environment", "kepler_floor_panel.png"),
            ("environment", "kepler_warning_panel.png"),
            ("environment", "kepler_pipe_metal.png"),
            ("environment", "sundered_rock.png"),
            ("environment", "sundered_crystal.png"),
            ("environment", "alien_structure.png"),
            ("characters", "astronaut_suit.png"),
            ("characters", "astronaut_visor.png"),
            ("characters", "rift_stalker_body.png"),
            ("characters", "rift_spitter_body.png"),
            ("characters", "rift_guardian_core.png"),
            ("weapons", "plasma_rifle.png"),
            ("rift", "rift_energy.png"),
            ("rift", "beacon_runes.png"),
            ("background", "space_background.png")
        ]

        for cat, filename in expected_textures:
            filepath = os.path.join(TextureManager.get_texture_dir(cat), filename)
            self.assertTrue(os.path.isfile(filepath), f"Texture file missing: {filepath}")
            with Image.open(filepath) as img:
                self.assertEqual(img.size, (512, 512), f"Invalid dimensions for {filename}")
                self.assertEqual(img.mode, "RGBA", f"Invalid mode for {filename}")

    def test_texture_caching(self):
        """Loading the same texture multiple times must return the identical cached ID."""
        cat_dir = TextureManager.get_texture_dir("environment")
        path = os.path.join(cat_dir, "kepler_metal_wall.png")
        id1 = TextureManager.load_texture(path)
        id2 = TextureManager.load_texture(path)
        self.assertEqual(id1, id2)

    def test_get_by_short_key(self):
        """Texture lookup by short key must resolve correctly."""
        tex_wall = TextureManager.get("kepler_metal_wall")
        self.assertIsNotNone(tex_wall)
        tex_suit = TextureManager.get("astronaut_suit")
        self.assertIsNotNone(tex_suit)
        tex_rock = TextureManager.get("sundered_rock")
        self.assertIsNotNone(tex_rock)

    def test_materials_texture_binding_api(self):
        """Materials helper functions must execute cleanly."""
        try:
            Materials.bind_suit_material()
            Materials.unbind_all()
            Materials.bind_metal_wall_material()
            Materials.unbind_all()
            Materials.bind_floor_panel_material()
            Materials.unbind_all()
            Materials.bind_rock_material()
            Materials.unbind_all()
            Materials.bind_crystal_material()
            Materials.unbind_all()
            Materials.bind_alien_carapace()
            Materials.unbind_all()
            Materials.bind_beacon_material()
            Materials.unbind_all()
        except Exception as e:
            self.fail(f"Material texture binding raised unexpected exception: {e}")


if __name__ == '__main__':
    unittest.main()
