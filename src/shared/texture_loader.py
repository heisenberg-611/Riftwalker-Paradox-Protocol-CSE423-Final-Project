"""Reusable OpenGL Texture Loader and Texture Management System using Pillow/PIL."""
import os
import math
import random
from typing import Dict, Optional, Tuple
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image, ImageDraw


# Base Assets Directory
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "assets", "textures")


class TextureManager:
    """
    Centralized Texture Manager with caching, automatic directory resolution,
    and procedural fallback generation.
    """
    _textures: Dict[str, int] = {}
    _initialized: bool = False

    @classmethod
    def get_texture_dir(cls, category: str = "") -> str:
        base = ASSETS_DIR
        if category:
            base = os.path.join(base, category)
        os.makedirs(base, exist_ok=True)
        return base

    @classmethod
    def generate_all_disk_textures(cls):
        """Generates all required PNG texture files on disk using Pillow without requiring OpenGL."""
        categories = {
            "environment": [
                "kepler_metal_wall.png", "kepler_floor_panel.png", "kepler_warning_panel.png",
                "kepler_pipe_metal.png", "sundered_rock.png", "sundered_crystal.png", "alien_structure.png"
            ],
            "characters": [
                "astronaut_suit.png", "astronaut_visor.png",
                "rift_stalker_body.png", "rift_spitter_body.png", "rift_guardian_core.png"
            ],
            "weapons": ["plasma_rifle.png"],
            "rift": ["rift_energy.png", "beacon_runes.png"],
            "background": ["space_background.png"]
        }
        for cat, filenames in categories.items():
            cat_dir = cls.get_texture_dir(cat)
            for fname in filenames:
                path = os.path.join(cat_dir, fname)
                if not os.path.exists(path):
                    img = cls._generate_fallback_image(path)
                    img.save(path, format="PNG")

    @classmethod
    def load_texture(
        cls,
        filepath: str,
        wrap_s: int = GL_REPEAT,
        wrap_t: int = GL_REPEAT,
        min_filter: int = GL_LINEAR_MIPMAP_LINEAR,
        mag_filter: int = GL_LINEAR
    ) -> int:
        """
        Loads an image from filepath into an OpenGL 2D texture with mipmapping.
        Returns the OpenGL texture ID. Results are cached by filepath.
        """
        if filepath in cls._textures:
            return cls._textures[filepath]

        if not os.path.exists(filepath):
            # If image file does not exist on disk, generate procedural fallback and save
            img = cls._generate_fallback_image(filepath)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            img.save(filepath, format="PNG")
        else:
            try:
                img = Image.open(filepath).convert("RGBA")
            except Exception:
                img = cls._generate_fallback_image(filepath)

        width, height = img.size
        # OpenGL expects flipped vertical coordinates (Y=0 at bottom)
        img_flipped = img.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = img_flipped.tobytes("raw", "RGBA", 0, -1)

        try:
            tex_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, tex_id)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap_s)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap_t)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, min_filter)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, mag_filter)

            # Build Mipmaps for optimal texture filtering at various distances
            try:
                gluBuild2DMipmaps(
                    GL_TEXTURE_2D,
                    GL_RGBA,
                    width,
                    height,
                    GL_RGBA,
                    GL_UNSIGNED_BYTE,
                    img_data
                )
            except Exception:
                glTexImage2D(
                    GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,
                    GL_RGBA, GL_UNSIGNED_BYTE, img_data
                )

            glBindTexture(GL_TEXTURE_2D, 0)
        except Exception:
            # Fallback texture ID if running in headless test without active GL context
            tex_id = len(cls._textures) + 1

        cls._textures[filepath] = tex_id
        return tex_id


    @classmethod
    def bind(cls, texture_id: int):
        """Enables texturing and binds the specified texture ID."""
        if texture_id > 0:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    @classmethod
    def unbind(cls):
        """Unbinds the active 2D texture and disables GL_TEXTURE_2D."""
        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)

    @classmethod
    def get(cls, key: str) -> int:
        """
        Retrieves a loaded texture ID by short key (e.g. 'kepler_metal_wall')
        or file path. Automatically resolves paths if needed.
        """
        if key in cls._textures:
            return cls._textures[key]

        # Search matching file in texture subdirectories
        for cat in ("environment", "characters", "weapons", "rift", "background", ""):
            candidate = os.path.join(ASSETS_DIR, cat, f"{key}.png" if not key.endswith(".png") else key)
            if os.path.exists(candidate) or cls._is_known_key(key):
                tex_id = cls.load_texture(candidate)
                cls._textures[key] = tex_id
                return tex_id

        # Fallback to direct path
        tex_id = cls.load_texture(key)
        cls._textures[key] = tex_id
        return tex_id

    @classmethod
    def _is_known_key(cls, key: str) -> bool:
        known = {
            "kepler_metal_wall", "kepler_floor_panel", "kepler_warning_panel", "kepler_pipe_metal",
            "sundered_rock", "sundered_crystal", "alien_structure",
            "astronaut_suit", "astronaut_visor",
            "rift_stalker_body", "rift_spitter_body", "rift_guardian_core",
            "plasma_rifle", "rift_energy", "beacon_runes", "space_background"
        }
        clean_key = key.replace(".png", "")
        return clean_key in known

    @classmethod
    def _generate_fallback_image(cls, filepath: str) -> Image.Image:
        """
        Procedurally generates high-detail seamless, tileable 512x512 sci-fi textures with PIL.
        """
        size = (512, 512)
        basename = os.path.basename(filepath).replace(".png", "").lower()
        img = Image.new("RGBA", size, (20, 24, 30, 255))
        draw = ImageDraw.Draw(img)

        # 1. Kepler Metal Wall (Brushed dark titanium plates with rivets & seam lines)
        if "metal_wall" in basename or "alien_structure" in basename:
            for y in range(0, 512, 128):
                for x in range(0, 512, 128):
                    # Plate background
                    shade = 45 + (x + y) % 25
                    draw.rectangle([x + 2, y + 2, x + 126, y + 126], fill=(shade, shade + 5, shade + 12, 255), outline=(25, 30, 38, 255), width=2)
                    # Rivets in corners
                    for rx, ry in [(x + 8, y + 8), (x + 120, y + 8), (x + 8, y + 120), (x + 120, y + 120)]:
                        draw.ellipse([rx - 2, ry - 2, rx + 2, ry + 2], fill=(85, 95, 110, 255))
                    # Fine brushed metal lines
                    for ly in range(y + 15, y + 115, 16):
                        draw.line([x + 10, ly, x + 118, ly], fill=(shade + 10, shade + 15, shade + 22, 255), width=1)

        # 2. Kepler Floor Panel (Industrial steel grid tiles)
        elif "floor_panel" in basename:
            for y in range(0, 512, 64):
                for x in range(0, 512, 64):
                    base_c = 35 + (x * 3 + y * 7) % 20
                    draw.rectangle([x + 1, y + 1, x + 63, y + 63], fill=(base_c, base_c + 3, base_c + 6, 255), outline=(18, 20, 25, 255), width=2)
                    # Cross grip pattern
                    draw.line([x + 8, y + 8, x + 56, y + 56], fill=(base_c + 15, base_c + 18, base_c + 24, 255), width=2)
                    draw.line([x + 56, y + 8, x + 8, y + 56], fill=(base_c + 15, base_c + 18, base_c + 24, 255), width=2)

        # 3. Kepler Warning Panel (Hazard yellow and black diagonal stripes)
        elif "warning" in basename:
            draw.rectangle([0, 0, 512, 512], fill=(220, 180, 20, 255))
            stripe_w = 48
            for i in range(-512, 1024, stripe_w * 2):
                points = [(i, 0), (i + stripe_w, 0), (i + stripe_w + 512, 512), (i + 512, 512)]
                draw.polygon(points, fill=(25, 25, 30, 255))

        # 4. Kepler Pipe Metal (Cylindrical brushed chrome / dark alloy)
        elif "pipe" in basename:
            for x in range(512):
                ratio = math.sin(x * math.pi / 256.0) ** 2
                val = int(35 + 120 * ratio)
                draw.line([x, 0, x, 512], fill=(val, val + 5, val + 15, 255))
            for y in range(0, 512, 64):
                draw.line([0, y, 512, y], fill=(15, 18, 22, 255), width=3)
                draw.line([0, y + 2, 512, y + 2], fill=(80, 90, 105, 255), width=1)

        # 5. Sundered Rock (Cracked dark volcanic basalt with rift energy veins)
        elif "sundered_rock" in basename or "rock" in basename:
            draw.rectangle([0, 0, 512, 512], fill=(25, 20, 30, 255))
            for _ in range(120):
                rx, ry = random.randint(0, 500), random.randint(0, 500)
                rw, rh = random.randint(10, 45), random.randint(10, 45)
                shade = random.randint(30, 55)
                draw.ellipse([rx, ry, rx + rw, ry + rh], fill=(shade, shade - 5, shade + 8, 255))
            # Glowing purple rift fissures
            for _ in range(8):
                x1, y1 = random.randint(0, 512), random.randint(0, 512)
                for _ in range(4):
                    x2 = (x1 + random.randint(-80, 80)) % 512
                    y2 = (y1 + random.randint(40, 120)) % 512
                    draw.line([x1, y1, x2, y2], fill=(180, 40, 240, 220), width=3)
                    draw.line([x1, y1, x2, y2], fill=(240, 120, 255, 255), width=1)
                    x1, y1 = x2, y2

        # 6. Sundered Crystal (Luminous violet & cyan multifaceted crystalline grid)
        elif "crystal" in basename:
            draw.rectangle([0, 0, 512, 512], fill=(30, 10, 45, 255))
            for y in range(0, 512, 64):
                for x in range(0, 512, 64):
                    poly = [(x + 32, y), (x + 64, y + 32), (x + 32, y + 64), (x, y + 32)]
                    c_val = (x * 4 + y * 6) % 100
                    draw.polygon(poly, fill=(120 + c_val, 30 + c_val // 2, 210 + c_val // 3, 240), outline=(200, 100, 255, 255), width=2)
                    draw.line([x, y + 32, x + 64, y + 32], fill=(255, 180, 255, 255), width=1)

        # 7. Astronaut Suit Fabric (High-tech synthetic hex weave armor)
        elif "astronaut_suit" in basename or "suit" in basename:
            draw.rectangle([0, 0, 512, 512], fill=(210, 215, 225, 255))
            for y in range(0, 512, 16):
                for x in range(0, 512, 16):
                    draw.rectangle([x, y, x + 14, y + 14], fill=(195, 202, 212, 255), outline=(170, 178, 190, 255), width=1)
            # Subtle cyan tech seams
            for x in range(0, 512, 128):
                draw.line([x, 0, x, 512], fill=(0, 180, 220, 255), width=2)

        # 8. Astronaut Visor (Reflective Gold & Cyan polarized metallic sheen)
        elif "visor" in basename:
            for y in range(512):
                t = y / 512.0
                r = int(240 * (1.0 - t * 0.5))
                g = int(190 * (1.0 - t * 0.3) + 80 * t)
                b = int(40 * (1.0 - t) + 240 * t)
                draw.line([0, y, 512, y], fill=(r, g, b, 255))

        # 9. Alien Carapace / Stalker / Spitter Body (Obsidian segmented scales)
        elif "stalker" in basename or "spitter" in basename or "guardian" in basename or "alien" in basename:
            draw.rectangle([0, 0, 512, 512], fill=(18, 14, 22, 255))
            for y in range(0, 512, 32):
                for x in range(0, 512, 32):
                    offset = 16 if (y // 32) % 2 == 1 else 0
                    px = (x + offset) % 512
                    draw.polygon([(px + 16, y), (px + 32, y + 16), (px + 16, y + 32), (px, y + 16)], fill=(32, 24, 40, 255), outline=(60, 40, 75, 255), width=1)
            # Glowing rift core fissure
            for y in range(0, 512, 4):
                f_x = int(256 + 40 * math.sin(y * 0.05))
                draw.line([f_x - 3, y, f_x + 3, y], fill=(0, 220, 255, 255), width=2)

        # 10. Plasma Rifle Body (Carbon fiber and glowing power rail)
        elif "rifle" in basename or "weapon" in basename:
            draw.rectangle([0, 0, 512, 512], fill=(30, 32, 38, 255))
            for y in range(0, 512, 8):
                for x in range(0, 512, 8):
                    draw.rectangle([x, y, x + 6, y + 6], fill=(42, 45, 54, 255))
            # Glowing power conductor rail
            draw.rectangle([64, 236, 448, 276], fill=(0, 210, 255, 255), outline=(180, 240, 255, 255), width=3)

        # 11. Rift Energy / Beacon Runes (Glowing cyan & violet runic nexus)
        elif "energy" in basename or "beacon" in basename or "runes" in basename:
            draw.rectangle([0, 0, 512, 512], fill=(10, 25, 40, 255))
            for r in range(40, 240, 35):
                draw.ellipse([256 - r, 256 - r, 256 + r, 256 + r], outline=(0, 220, 255, 220), width=3)
            for a in range(0, 360, 45):
                rad = math.radians(a)
                x2 = int(256 + 220 * math.cos(rad))
                y2 = int(256 + 220 * math.sin(rad))
                draw.line([256, 256, x2, y2], fill=(160, 80, 255, 200), width=2)

        # 12. Space Background (Deep cosmic starfield nebula)
        elif "space" in basename or "background" in basename:
            draw.rectangle([0, 0, 512, 512], fill=(4, 6, 12, 255))
            for _ in range(350):
                sx, sy = random.randint(0, 511), random.randint(0, 511)
                brightness = random.randint(140, 255)
                star_color = random.choice([
                    (brightness, brightness, brightness, 255),
                    (brightness - 30, brightness - 10, brightness, 255),
                    (brightness, brightness - 20, brightness - 40, 255),
                    (brightness - 40, brightness, brightness, 255)
                ])
                draw.point([sx, sy], fill=star_color)
                if random.random() < 0.08:
                    draw.rectangle([sx - 1, sy - 1, sx + 1, sy + 1], fill=star_color)

        return img

    @classmethod
    def init_all_textures(cls):
        """
        Pre-loads and initializes all required textures across categories.
        """
        if cls._initialized:
            return

        categories = {
            "environment": [
                "kepler_metal_wall.png", "kepler_floor_panel.png", "kepler_warning_panel.png",
                "kepler_pipe_metal.png", "sundered_rock.png", "sundered_crystal.png", "alien_structure.png"
            ],
            "characters": [
                "astronaut_suit.png", "astronaut_visor.png",
                "rift_stalker_body.png", "rift_spitter_body.png", "rift_guardian_core.png"
            ],
            "weapons": ["plasma_rifle.png"],
            "rift": ["rift_energy.png", "beacon_runes.png"],
            "background": ["space_background.png"]
        }

        for cat, filenames in categories.items():
            cat_dir = cls.get_texture_dir(cat)
            for fname in filenames:
                path = os.path.join(cat_dir, fname)
                cls.load_texture(path)
                # Register short key without extension
                short_key = fname.replace(".png", "")
                cls._textures[short_key] = cls._textures[path]

        cls._initialized = True


# Global Module API Convenience Functions
def load_texture(path: str, **kwargs) -> int:
    return TextureManager.load_texture(path, **kwargs)


def bind_texture(texture_id: int):
    TextureManager.bind(texture_id)


def unbind_texture():
    TextureManager.unbind()


def get_texture(name_or_key: str) -> int:
    return TextureManager.get(name_or_key)


def init_textures():
    TextureManager.init_all_textures()
