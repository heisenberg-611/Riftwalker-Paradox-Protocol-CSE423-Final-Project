"""2D Orthographic HUD Overlay with robust font handling."""
from OpenGL.GL import *
import OpenGL.GLUT as glut
from src.M4_rendering_gameplay.crosshair import Crosshair


def get_glut_font(font_name: str = "GLUT_BITMAP_HELVETICA_18"):
    """Safely retrieves a GLUT bitmap font pointer with fallback support."""
    # 1. Try direct attribute lookup from OpenGL.GLUT
    font_ptr = getattr(glut, font_name, None)
    if font_ptr is not None:
        return font_ptr

    # 2. Try fonts sub-module if available
    try:
        from OpenGL.GLUT import fonts
        font_ptr = getattr(fonts, font_name, None)
        if font_ptr is not None:
            return font_ptr
    except Exception:
        pass

    # 3. Fallbacks to standard universally supported GLUT bitmap fonts
    for fallback_name in ("GLUT_BITMAP_9_BY_15", "GLUT_BITMAP_8_BY_13", "GLUT_BITMAP_HELVETICA_12"):
        font_ptr = getattr(glut, fallback_name, None)
        if font_ptr is not None:
            return font_ptr

    return None


class HUD:
    def __init__(self):
        self.crosshair = Crosshair()
        self._font_normal = None
        self._font_title = None

    @property
    def font_normal(self):
        if self._font_normal is None:
            self._font_normal = get_glut_font("GLUT_BITMAP_HELVETICA_18")
        return self._font_normal

    @property
    def font_title(self):
        if self._font_title is None:
            self._font_title = get_glut_font("GLUT_BITMAP_TIMES_ROMAN_24") or self.font_normal
        return self._font_title

    def draw_text(self, x: float, y: float, text: str, font=None):
        if font is None:
            font = self.font_normal

        if font is None:
            return

        glRasterPos2f(x, y)
        for char in text:
            try:
                glut.glutBitmapCharacter(font, ord(char))
            except Exception:
                break

    def draw(
        self,
        width: int,
        height: int,
        hp: float,
        max_hp: float,
        chrono_energy: float,
        max_chrono: float,
        score: int,
        is_chrono_active: bool,
        can_teleport: bool,
        is_first_person: bool,
        game_state_str: str
    ):
        # Switch to 2D Orthographic projection
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # 1. Health Bar (Bottom Left)
        bar_w = 200.0
        bar_h = 16.0
        x0 = 30.0
        y0 = 30.0

        # HP Background
        glColor4f(0.1, 0.1, 0.15, 0.7)
        glBegin(GL_QUADS)
        glVertex2f(x0, y0)
        glVertex2f(x0 + bar_w, y0)
        glVertex2f(x0 + bar_w, y0 + bar_h)
        glVertex2f(x0, y0 + bar_h)
        glEnd()

        # HP Filled Portion
        hp_ratio = max(0.0, min(hp / max_hp, 1.0))
        glColor4f(0.1, 0.9, 0.3, 0.9)
        glBegin(GL_QUADS)
        glVertex2f(x0, y0)
        glVertex2f(x0 + bar_w * hp_ratio, y0)
        glVertex2f(x0 + bar_w * hp_ratio, y0 + bar_h)
        glVertex2f(x0, y0 + bar_h)
        glEnd()

        # HP Text
        glColor3f(1.0, 1.0, 1.0)
        self.draw_text(x0, y0 + bar_h + 6, f"SUIT INTEGRITY: {int(hp)}/{int(max_hp)}")

        # 2. Chrono Energy Bar
        y1 = y0 + 40.0
        # Chrono Background
        glColor4f(0.1, 0.1, 0.15, 0.7)
        glBegin(GL_QUADS)
        glVertex2f(x0, y1)
        glVertex2f(x0 + bar_w, y1)
        glVertex2f(x0 + bar_w, y1 + bar_h)
        glVertex2f(x0, y1 + bar_h)
        glEnd()

        # Chrono Filled Portion
        chrono_ratio = max(0.0, min(chrono_energy / max_chrono, 1.0))
        if is_chrono_active:
            glColor4f(0.0, 0.8, 1.0, 1.0)  # Bright Active Cyan
        else:
            glColor4f(0.0, 0.45, 0.75, 0.8)
        glBegin(GL_QUADS)
        glVertex2f(x0, y1)
        glVertex2f(x0 + bar_w * chrono_ratio, y1)
        glVertex2f(x0 + bar_w * chrono_ratio, y1 + bar_h)
        glVertex2f(x0, y1 + bar_h)
        glEnd()

        # Chrono Text
        status = "[ACTIVE - Q to cancel]" if is_chrono_active else "[Q to slow time]"
        glColor3f(0.4, 0.9, 1.0)
        self.draw_text(x0, y1 + bar_h + 6, f"CHRONO DILATION: {int(chrono_energy)}% {status}")

        # 3. Score & Info (Top Left)
        glColor3f(1.0, 0.85, 0.2)
        self.draw_text(30.0, height - 35.0, f"SCORE: {score}")

        view_mode_str = "1st Person [V/C to toggle]" if is_first_person else "3rd Person [V/C to toggle]"
        glColor3f(0.8, 0.8, 0.9)
        self.draw_text(30.0, height - 60.0, f"CAMERA: {view_mode_str}")

        # 4. Teleport Prompt (Center Screen)
        if can_teleport:
            glColor3f(0.0, 1.0, 0.9)
            self.draw_text(width * 0.5 - 130.0, height * 0.4, ">> PRESS 'F' TO RIFT TELEPORT <<")

        # 5. Crosshair (Center Screen)
        self.crosshair.draw(width * 0.5, height * 0.5)

        # 6. End-Game States
        if game_state_str == "GAME_OVER":
            glColor3f(1.0, 0.1, 0.2)
            self.draw_text(width * 0.5 - 75.0, height * 0.55, "GAME OVER", font=self.font_title)
            glColor3f(1.0, 1.0, 1.0)
            self.draw_text(width * 0.5 - 105.0, height * 0.48, "Press 'R' to Restart Mission")
        elif game_state_str == "VICTORY":
            glColor3f(0.2, 1.0, 0.4)
            self.draw_text(width * 0.5 - 140.0, height * 0.55, "MISSION ACCOMPLISHED!", font=self.font_title)
            glColor3f(1.0, 1.0, 1.0)
            self.draw_text(width * 0.5 - 105.0, height * 0.48, "Press 'R' to Play Again")

        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
