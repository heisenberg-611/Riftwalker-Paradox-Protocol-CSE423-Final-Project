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
        Procedurally generates high-contrast, vivid 512x512 sci-fi textures with PIL.
        """
        size = (512, 512)
        basename = os.path.basename(filepath).replace(".png", "").lower()
        img = Image.new("RGBA", size, (35, 40, 50, 255))
        draw = ImageDraw.Draw(img)

        # 1. Kepler Metal Wall (Heavy sci-fi bulkhead panels with bright rivets, seams & blue LED strips)
        if "metal_wall" in basename or "alien_structure" in basename:
            draw.rectangle([0, 0, 512, 512], fill=(140, 150, 165, 255))
            for y in range(0, 512, 128):
                for x in range(0, 512, 128):
                    # Plate Body
                    draw.rectangle([x + 3, y + 3, x + 125, y + 125], fill=(160, 170, 185, 255), outline=(30, 35, 45, 255), width=3)
                    # Plate Inner Inset
                    draw.rectangle([x + 14, y + 14, x + 114, y + 114], fill=(145, 155, 170, 255), outline=(90, 100, 115, 255), width=1)
                    # Corner Bolted Rivets
                    for rx, ry in [(x + 8, y + 8), (x + 120, y + 8), (x + 8, y + 120), (x + 120, y + 120)]:
                        draw.ellipse([rx - 3, ry - 3, rx + 3, ry + 3], fill=(225, 235, 250, 255), outline=(30, 35, 45, 255), width=1)
                    # Air Vent Grille in center of panel
                    for vy in range(y + 35, y + 95, 8):
                        draw.line([x + 25, vy, x + 103, vy], fill=(30, 35, 45, 255), width=2)
                        draw.line([x + 25, vy + 2, x + 103, vy + 2], fill=(200, 215, 235, 255), width=1)
                    # Glowing Cyan Indicator LED
                    draw.ellipse([x + 60, y + 105, x + 68, y + 113], fill=(0, 230, 255, 255), outline=(180, 255, 255, 255), width=1)

        # 2. Kepler Floor Panel (High-contrast industrial steel plates with cyan power conduits)
        elif "floor_panel" in basename:
            draw.rectangle([0, 0, 512, 512], fill=(40, 45, 55, 255))
            for y in range(0, 512, 64):
                for x in range(0, 512, 64):
                    # Plate Tile
                    draw.rectangle([x + 2, y + 2, x + 62, y + 62], fill=(135, 145, 160, 255), outline=(25, 30, 38, 255), width=2)
                    # Inner Plate Highlight
                    draw.rectangle([x + 6, y + 6, x + 58, y + 58], fill=(150, 160, 175, 255), outline=(180, 190, 205, 255), width=1)
                    # Diamond-tread / Cross-grip pattern
                    draw.line([x + 12, y + 12, x + 52, y + 52], fill=(195, 205, 220, 255), width=2)
                    draw.line([x + 52, y + 12, x + 12, y + 52], fill=(195, 205, 220, 255), width=2)
                    draw.line([x + 12, y + 12, x + 52, y + 52], fill=(70, 75, 85, 255), width=1)
                    # Corner Screws
                    for sx, sy in [(x + 5, y + 5), (x + 59, y + 5), (x + 5, y + 59), (x + 59, y + 59)]:
                        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(220, 230, 245, 255))
            # Glowing Electric Cyan Conduit Grid Lines
            for pos in range(0, 512, 128):
                draw.line([0, pos, 512, pos], fill=(0, 220, 255, 255), width=3)
                draw.line([0, pos, 512, pos], fill=(180, 255, 255, 255), width=1)
                draw.line([pos, 0, pos, 512], fill=(0, 220, 255, 255), width=3)
                draw.line([pos, 0, pos, 512], fill=(180, 255, 255, 255), width=1)

        # 3. Kepler Warning Panel (Vivid Hazard yellow & black diagonal caution stripes)
        elif "warning" in basename:
            draw.rectangle([0, 0, 512, 512], fill=(255, 215, 0, 255))
            stripe_w = 48
            for i in range(-512, 1024, stripe_w * 2):
                points = [(i, 0), (i + stripe_w, 0), (i + stripe_w + 512, 512), (i + 512, 512)]
                draw.polygon(points, fill=(20, 20, 25, 255))
            # Outer border frame with rivets
            draw.rectangle([4, 4, 508, 508], outline=(15, 15, 20, 255), width=8)
            for p in range(20, 512, 64):
                draw.ellipse([p - 4, 8, p + 4, 16], fill=(220, 220, 230, 255))
                draw.ellipse([p - 4, 496, p + 4, 504], fill=(220, 220, 230, 255))

        # 4. Kepler Pipe Metal (Polished cylindrical chrome alloy with specular highlights)
        elif "pipe" in basename:
            for x in range(512):
                ratio = math.sin(x * math.pi / 256.0) ** 2
                val = int(80 + 170 * ratio)
                draw.line([x, 0, x, 512], fill=(val, min(255, val + 10), min(255, val + 25), 255))
            for y in range(0, 512, 64):
                draw.line([0, y, 512, y], fill=(20, 25, 35, 255), width=4)
                draw.line([0, y + 2, 512, y + 2], fill=(230, 240, 255, 255), width=2)

        # 5. Sundered Rock (Cracked dark volcanic obsidian with glowing neon purple/magenta rift magma)
        elif "sundered_rock" in basename or "rock" in basename:
            draw.rectangle([0, 0, 512, 512], fill=(45, 35, 55, 255))
            for _ in range(150):
                rx, ry = random.randint(0, 500), random.randint(0, 500)
                rw, rh = random.randint(15, 65), random.randint(15, 65)
                shade = random.randint(60, 100)
                draw.ellipse([rx, ry, rx + rw, ry + rh], fill=(shade, shade - 10, shade + 15, 255), outline=(30, 20, 40, 255), width=1)
            # Radiant Glowing Purple/Magenta Rift Energy Fissures
            for _ in range(12):
                x1, y1 = random.randint(0, 512), random.randint(0, 512)
                for _ in range(5):
                    x2 = (x1 + random.randint(-90, 90)) % 512
                    y2 = (y1 + random.randint(50, 130)) % 512
                    # Outer glow
                    draw.line([x1, y1, x2, y2], fill=(160, 20, 240, 200), width=6)
                    # Intense neon core
                    draw.line([x1, y1, x2, y2], fill=(255, 60, 230, 255), width=3)
                    draw.line([x1, y1, x2, y2], fill=(255, 230, 255, 255), width=1)
                    x1, y1 = x2, y2

        # 6. Sundered Crystal (Luminous violet & electric cyan multifaceted crystalline grid)
        elif "crystal" in basename:
            draw.rectangle([0, 0, 512, 512], fill=(50, 20, 75, 255))
            for y in range(0, 512, 64):
                for x in range(0, 512, 64):
                    poly = [(x + 32, y), (x + 64, y + 32), (x + 32, y + 64), (x, y + 32)]
                    c_val = (x * 4 + y * 6) % 90
                    draw.polygon(poly, fill=(150 + c_val, 40 + c_val // 2, 230 + c_val // 4, 255), outline=(230, 140, 255, 255), width=3)
                    draw.line([x, y + 32, x + 64, y + 32], fill=(0, 240, 255, 255), width=2)
                    draw.line([x + 32, y, x + 32, y + 64], fill=(255, 220, 255, 255), width=1)

        # 7. Astronaut Suit Fabric (High-tech white composite hex weave armor with cyan/orange accents)
        elif "astronaut_suit" in basename or "suit" in basename:
            draw.rectangle([0, 0, 512, 512], fill=(230, 235, 245, 255))
            for y in range(0, 512, 16):
                for x in range(0, 512, 16):
                    draw.rectangle([x, y, x + 14, y + 14], fill=(215, 222, 235, 255), outline=(175, 185, 200, 255), width=1)
            # Tech armor panel insets
            for pos in range(0, 512, 128):
                draw.rectangle([pos + 10, pos + 10, pos + 118, pos + 118], outline=(60, 90, 130, 255), width=2)
                # Orange shoulder hazard patch
                draw.rectangle([pos + 20, pos + 20, pos + 40, pos + 40], fill=(255, 120, 20, 255))
            # Glowing cyan bio-monitor telemetry lines
            for x in range(0, 512, 128):
                draw.line([x, 0, x, 512], fill=(0, 210, 255, 255), width=3)
                draw.line([x, 0, x, 512], fill=(200, 255, 255, 255), width=1)

        # 8. Astronaut Visor (Iridescent Gold & Cyan polarized metallic horizon reflection)
        elif "visor" in basename:
            for y in range(512):
                t = y / 512.0
                r = int(255 * (1.0 - t * 0.45))
                g = int(210 * (1.0 - t * 0.25) + 80 * t)
                b = int(50 * (1.0 - t) + 250 * t)
                draw.line([0, y, 512, y], fill=(r, g, b, 255))
            # Horizon reflection glare flare
            draw.line([0, 256, 512, 256], fill=(255, 255, 255, 240), width=4)
            draw.line([0, 254, 512, 254], fill=(200, 240, 255, 200), width=2)
            draw.line([0, 258, 512, 258], fill=(255, 230, 150, 200), width=2)

        # 9. Alien Carapace / Stalker / Spitter Body (Faceted obsidian with bright cyan rift fissures)
        elif "stalker" in basename or "spitter" in basename or "guardian" in basename or "alien" in basename:
            draw.rectangle([0, 0, 512, 512], fill=(30, 20, 42, 255))
            for y in range(0, 512, 32):
                for x in range(0, 512, 32):
                    offset = 16 if (y // 32) % 2 == 1 else 0
                    px = (x + offset) % 512
                    draw.polygon([(px + 16, y), (px + 32, y + 16), (px + 16, y + 32), (px, y + 16)], fill=(55, 38, 70, 255), outline=(100, 65, 125, 255), width=2)
            # Glowing electric cyan bio-vein fissure
            for y in range(0, 512, 4):
                f_x = int(256 + 48 * math.sin(y * 0.05))
                draw.line([f_x - 4, y, f_x + 4, y], fill=(0, 230, 255, 255), width=3)
                draw.line([f_x - 1, y, f_x + 1, y], fill=(220, 255, 255, 255), width=1)

        # 10. Plasma Rifle Body (Carbon fiber and glowing cyan energy rail)
        elif "rifle" in basename or "weapon" in basename:
            draw.rectangle([0, 0, 512, 512], fill=(50, 55, 68, 255))
            for y in range(0, 512, 8):
                for x in range(0, 512, 8):
                    draw.rectangle([x, y, x + 6, y + 6], fill=(70, 78, 92, 255), outline=(30, 35, 45, 255), width=1)
            # Glowing power conductor rail
            draw.rectangle([48, 230, 464, 282], fill=(0, 225, 255, 255), outline=(220, 255, 255, 255), width=4)

        # 11. Rift Energy / Beacon Runes (Glowing cyan & violet runic nexus)
        elif "energy" in basename or "beacon" in basename or "runes" in basename:
            draw.rectangle([0, 0, 512, 512], fill=(15, 35, 55, 255))
            for r in range(40, 240, 35):
                draw.ellipse([256 - r, 256 - r, 256 + r, 256 + r], outline=(0, 240, 255, 255), width=4)
            for a in range(0, 360, 30):
                rad = math.radians(a)
                x2 = int(256 + 220 * math.cos(rad))
                y2 = int(256 + 220 * math.sin(rad))
                draw.line([256, 256, x2, y2], fill=(190, 90, 255, 240), width=3)
                draw.ellipse([x2 - 5, y2 - 5, x2 + 5, y2 + 5], fill=(0, 255, 255, 255))

        # 12. Space Background (Deep cosmic starfield nebula)
        elif "space" in basename or "background" in basename:
            draw.rectangle([0, 0, 512, 512], fill=(10, 12, 25, 255))
            # Nebula cloud wisps
            for _ in range(60):
                nx, ny = random.randint(0, 512), random.randint(0, 512)
                nr = random.randint(40, 150)
                n_col = random.choice([
                    (120, 30, 180, 40),
                    (0, 140, 200, 35),
                    (180, 50, 120, 30)
                ])
                draw.ellipse([nx - nr, ny - nr, nx + nr, ny + nr], fill=n_col)
            for _ in range(450):
                sx, sy = random.randint(0, 511), random.randint(0, 511)
                brightness = random.randint(180, 255)
                star_color = random.choice([
                    (brightness, brightness, brightness, 255),
                    (brightness - 20, brightness, brightness, 255),
                    (brightness, brightness - 10, brightness - 40, 255),
                    (200, 230, 255, 255)
                ])
                draw.point([sx, sy], fill=star_color)
                if random.random() < 0.12:
                    draw.rectangle([sx - 1, sy - 1, sx + 1, sy + 1], fill=star_color)

        return img


    @classmethod
    def generate_all_disk_textures(cls, force: bool = True):
        """Generates all 16 procedural textures and writes high-res PNGs to assets/textures/."""
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
            os.makedirs(cat_dir, exist_ok=True)
            for fname in filenames:
                path = os.path.join(cat_dir, fname)
                if force or not os.path.exists(path):
                    img = cls._generate_fallback_image(path)
                    img.save(path, format="PNG")

    @classmethod
    def init_all_textures(cls):
        """
        Pre-loads and initializes all required textures across categories.
        """
        if cls._initialized:
            return

        # Ensure disk textures are up-to-date with latest vivid designs
        cls.generate_all_disk_textures(force=True)

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
