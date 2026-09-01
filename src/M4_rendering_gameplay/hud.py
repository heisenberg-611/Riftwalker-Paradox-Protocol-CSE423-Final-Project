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
        chrono_charge: float,
        max_chrono: float,
        score: int,
        is_chrono_active: bool,
        chrono_time_remaining: float,
        can_teleport: bool,
        is_first_person: bool,
        game_state_str: str,
        boss_hp: float = 0.0,
        boss_max_hp: float = 0.0,
        weapon_cooldown_ratio: float = 1.0,
        objective_title: str = "",
        objective_subtitle: str = "",
        combo_multiplier: int = 1,
        combo_ratio: float = 0.0,
        is_intermission: bool = False,
        **kwargs
    ):
        # Switch to 2D Orthographic projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        try:
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

            # 2. Chrono Charge Bar
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
            if is_chrono_active:
                # Active 5.0s countdown bar
                countdown_ratio = max(0.0, min(chrono_time_remaining / 5.0, 1.0))
                glColor4f(0.0, 0.9, 1.0, 1.0)  # Bright Cyan
                glBegin(GL_QUADS)
                glVertex2f(x0, y1)
                glVertex2f(x0 + bar_w * countdown_ratio, y1)
                glVertex2f(x0 + bar_w * countdown_ratio, y1 + bar_h)
                glVertex2f(x0, y1 + bar_h)
                glEnd()
                glColor3f(0.2, 1.0, 1.0)
                self.draw_text(x0, y1 + bar_h + 6, f"CHRONO SLOW: {chrono_time_remaining:.1f}s REMAINING")
            else:
                # Charging bar (0% to 100%)
                chrono_ratio = max(0.0, min(chrono_charge / max_chrono, 1.0))
                if chrono_charge >= max_chrono:
                    glColor4f(0.0, 1.0, 0.9, 1.0)  # Full 100% Glow
                    glBegin(GL_QUADS)
                    glVertex2f(x0, y1)
                    glVertex2f(x0 + bar_w * chrono_ratio, y1)
                    glVertex2f(x0 + bar_w * chrono_ratio, y1 + bar_h)
                    glVertex2f(x0, y1 + bar_h)
                    glEnd()
                    glColor3f(0.0, 1.0, 0.9)
                    self.draw_text(x0, y1 + bar_h + 6, "CHRONO CHARGE: [100% READY - PRESS 'Q']")
                else:
                    glColor4f(0.0, 0.45, 0.75, 0.8)
                    glBegin(GL_QUADS)
                    glVertex2f(x0, y1)
                    glVertex2f(x0 + bar_w * chrono_ratio, y1)
                    glVertex2f(x0 + bar_w * chrono_ratio, y1 + bar_h)
                    glVertex2f(x0, y1 + bar_h)
                    glEnd()
                    glColor3f(0.5, 0.8, 1.0)
                    self.draw_text(x0, y1 + bar_h + 6, f"CHRONO CHARGE: {int(chrono_charge)}% [KILLS / RIFT PICKUPS]")

            # 3. Weapon Cooldown & Overcharge Status Bar
            y2 = y1 + 40.0
            glColor4f(0.1, 0.1, 0.15, 0.7)
            glBegin(GL_QUADS)
            glVertex2f(x0, y2)
            glVertex2f(x0 + bar_w, y2)
            glVertex2f(x0 + bar_w, y2 + bar_h)
            glVertex2f(x0, y2 + bar_h)
            glEnd()

            w_ratio = max(0.0, min(weapon_cooldown_ratio, 1.0))
            charge_ratio = max(0.0, min(kwargs.get('weapon_charge_ratio', 0.0), 1.0))

            if w_ratio < 1.0:
                # Cooling down / cycling
                glColor4f(1.0, 0.65, 0.1, 0.85)  # Amber
                glBegin(GL_QUADS)
                glVertex2f(x0, y2)
                glVertex2f(x0 + bar_w * w_ratio, y2)
                glVertex2f(x0 + bar_w * w_ratio, y2 + bar_h)
                glVertex2f(x0, y2 + bar_h)
                glEnd()
                glColor3f(1.0, 0.75, 0.2)
                self.draw_text(x0, y2 + bar_h + 6, f"RIFLE CYCLING: {int(w_ratio * 100)}%")
            else:
                # Weapon Ready -> Check if charging
                if charge_ratio <= 0.0:
                    glColor4f(0.0, 0.95, 1.0, 0.95)  # Bright Cyan
                    glBegin(GL_QUADS)
                    glVertex2f(x0, y2)
                    glVertex2f(x0 + bar_w, y2)
                    glVertex2f(x0 + bar_w, y2 + bar_h)
                    glVertex2f(x0, y2 + bar_h)
                    glEnd()
                    glColor3f(0.3, 1.0, 1.0)
                    self.draw_text(x0, y2 + bar_h + 6, "LASER RIFLE: [READY - TAP OR HOLD TO CHARGE]")
                elif charge_ratio < 0.85:
                    # Charging Up
                    glColor4f(1.0, 0.85, 0.2, 0.95)  # Golden Yellow
                    glBegin(GL_QUADS)
                    glVertex2f(x0, y2)
                    glVertex2f(x0 + bar_w * charge_ratio, y2)
                    glVertex2f(x0 + bar_w * charge_ratio, y2 + bar_h)
                    glVertex2f(x0, y2 + bar_h)
                    glEnd()
                    glColor3f(1.0, 0.9, 0.3)
                    self.draw_text(x0, y2 + bar_h + 6, f"⚡ CHARGING OVERCHARGE: {int(charge_ratio * 100)}% ⚡")
                else:
                    # Full Overcharge Ready!
                    glColor4f(1.0, 0.95, 0.4, 0.98)  # Blinding Gold
                    glBegin(GL_QUADS)
                    glVertex2f(x0, y2)
                    glVertex2f(x0 + bar_w, y2)
                    glVertex2f(x0 + bar_w, y2 + bar_h)
                    glVertex2f(x0, y2 + bar_h)
                    glEnd()
                    glColor3f(1.0, 1.0, 0.4)
                    self.draw_text(x0, y2 + bar_h + 6, "⚡ OVERCHARGE READY [3X DAMAGE - RELEASE] ⚡")

            # 4. Boss Health Bar (Top Center)
            has_boss = boss_hp > 0.0 and boss_max_hp > 0.0
            if has_boss:
                boss_w = 380.0
                boss_h = 16.0
                bx0 = (width - boss_w) * 0.5
                by0 = height - 52.0

                # Background
                glColor4f(0.1, 0.1, 0.15, 0.85)
                glBegin(GL_QUADS)
                glVertex2f(bx0, by0)
                glVertex2f(bx0 + boss_w, by0)
                glVertex2f(bx0 + boss_w, by0 + boss_h)
                glVertex2f(bx0, by0 + boss_h)
                glEnd()

                # Filled Health Bar
                b_ratio = max(0.0, min(boss_hp / boss_max_hp, 1.0))
                if b_ratio <= 0.5:
                    glColor4f(1.0, 0.15, 0.25, 0.98)  # Rage Red in Phase 2
                else:
                    glColor4f(0.85, 0.2, 0.95, 0.95)  # Violet in Phase 1
                glBegin(GL_QUADS)
                glVertex2f(bx0, by0)
                glVertex2f(bx0 + boss_w * b_ratio, by0)
                glVertex2f(bx0 + boss_w * b_ratio, by0 + boss_h)
                glVertex2f(bx0, by0 + boss_h)
                glEnd()

                # Boss Name & Phase Text (Centered Above Boss Bar)
                glColor3f(1.0, 0.85, 0.3)
                phase_str = "PHASE 2 — DESTABILIZED" if b_ratio <= 0.5 else "PHASE 1 — SHIELDED"
                boss_title_str = f"👑 RIFT GUARDIAN [{phase_str}]: {int(boss_hp)}/{int(boss_max_hp)}"
                boss_title_x = width * 0.5 - (len(boss_title_str) * 4.4)
                self.draw_text(boss_title_x, by0 + boss_h + 6.0, boss_title_str)

            # 5. Score & Combo Multiplier (Top Left)
            glColor3f(1.0, 0.85, 0.2)
            self.draw_text(30.0, height - 35.0, f"SCORE: {score}")

            if combo_multiplier > 1:
                glColor3f(1.0, 0.70, 0.1)
                self.draw_text(30.0, height - 58.0, f"COMBO: x{combo_multiplier}")
                # Combo decay mini bar
                glColor4f(1.0, 0.65, 0.1, 0.85)
                glBegin(GL_QUADS)
                glVertex2f(30.0, height - 68.0)
                glVertex2f(30.0 + 80.0 * combo_ratio, height - 68.0)
                glVertex2f(30.0 + 80.0 * combo_ratio, height - 64.0)
                glVertex2f(30.0, height - 64.0)
                glEnd()
                view_y = height - 90.0
            else:
                view_y = height - 60.0

            view_mode_str = "1st Person [V to toggle]" if is_first_person else "3rd Person [V to toggle]"
            glColor3f(0.8, 0.8, 0.9)
            self.draw_text(30.0, view_y, f"CAMERA: {view_mode_str}")

            # 6. Live Wave Objectives & Banners (Upper Center - dynamically placed below Boss Bar)
            if objective_title:
                # If boss is active, place objective banner lower so it NEVER collides with Boss Bar
                obj_y_title = height - 76.0 if has_boss else height - 35.0
                obj_y_sub = height - 96.0 if has_boss else height - 58.0

                if is_intermission:
                    # Prominent yellow/orange banner during wave intermission
                    glColor3f(1.0, 0.85, 0.1)
                    title_x = width * 0.5 - (len(objective_title) * 4.8)
                    self.draw_text(title_x, obj_y_title, objective_title)
                    if objective_subtitle:
                        glColor3f(0.9, 0.9, 1.0)
                        sub_x = width * 0.5 - (len(objective_subtitle) * 4.0)
                        self.draw_text(sub_x, obj_y_sub, objective_subtitle)
                else:
                    # Standard active wave objective
                    glColor3f(0.2, 0.95, 1.0)
                    title_x = width * 0.5 - (len(objective_title) * 4.4)
                    self.draw_text(title_x, obj_y_title, objective_title)
                    if objective_subtitle:
                        glColor3f(1.0, 0.8, 0.3)
                        sub_x = width * 0.5 - (len(objective_subtitle) * 4.0)
                        self.draw_text(sub_x, obj_y_sub, objective_subtitle)

            # 7. Teleport Prompt (Center Screen)
            if can_teleport:
                glColor3f(0.0, 1.0, 0.9)
                self.draw_text(width * 0.5 - 130.0, height * 0.4, ">> PRESS 'F' TO RIFT TELEPORT <<")

            # 8. Crosshair (Center Screen)
            self.crosshair.draw(width * 0.5, height * 0.5)

            # 9. End-Game States
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

        finally:
            glDisable(GL_BLEND)
            glEnable(GL_LIGHTING)
            glEnable(GL_DEPTH_TEST)
            glMatrixMode(GL_MODELVIEW)
