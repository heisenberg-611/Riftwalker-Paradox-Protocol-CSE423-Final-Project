"""Cinematic Epilogue and Victory Story Presentation System."""
import math
import random
from typing import List, Dict, Any, Tuple
from OpenGL.GL import *
import OpenGL.GLUT as glut


def get_glut_font(font_name: str = "GLUT_BITMAP_HELVETICA_18"):
    """Safely retrieves a GLUT bitmap font pointer with fallback support."""
    font_ptr = getattr(glut, font_name, None)
    if font_ptr is not None:
        return font_ptr
    try:
        from OpenGL.GLUT import fonts
        font_ptr = getattr(fonts, font_name, None)
        if font_ptr is not None:
            return font_ptr
    except Exception:
        pass
    for fallback in ("GLUT_BITMAP_9_BY_15", "GLUT_BITMAP_8_BY_13", "GLUT_BITMAP_HELVETICA_12"):
        font_ptr = getattr(glut, fallback, None)
        if font_ptr is not None:
            return font_ptr
    return None


def get_text_width(font, text: str) -> float:
    """Calculates pixel width of string rendered in given GLUT font."""
    if not text:
        return 0.0
    try:
        if font is not None and hasattr(glut, 'glutBitmapWidth'):
            return float(sum(glut.glutBitmapWidth(font, ord(c)) for c in text))
    except Exception:
        pass
    return float(len(text) * 9.0)


class EpilogueParticle:
    __slots__ = ('x', 'y', 'vx', 'vy', 'size', 'alpha', 'color')

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.vx = random.uniform(-15.0, 15.0)
        self.vy = random.uniform(10.0, 35.0)
        self.size = random.uniform(2.0, 4.0)
        self.alpha = random.uniform(0.3, 0.85)
        self.color = random.choice([
            (0.0, 0.95, 1.0),   # Cyan
            (0.85, 0.35, 1.0),  # Violet
            (0.2, 1.0, 0.4),    # Emerald
            (1.0, 0.85, 0.2)    # Gold
        ])


class StoryEpilogueManager:
    """Manages the cinematic post-boss epilogue story panels and final mission report."""

    def __init__(self):
        self.current_panel_index: int = 0
        self.fade_alpha: float = 0.0
        self.fade_timer: float = 0.0
        self.pulse_timer: float = 0.0

        # Ambient floating victory / stardust particles
        self.particles: List[EpilogueParticle] = [
            EpilogueParticle(random.uniform(0, 1280), random.uniform(0, 800))
            for _ in range(40)
        ]

        # 3 Canonical Epilogue Narrative Panels
        self.panels: List[Dict[str, Any]] = [
            {
                "heading": "THE BREACH COLLAPSES",
                "accent_color": (0.0, 0.95, 1.0),
                "lines": [
                    "The Rift Guardian shatters into blinding crystalline shards.",
                    "Its dimensional core destabilizes with a deafening sonic pulse.",
                    "",
                    "Across the Sundered Rift, the floating hazard spires dissolve into dust.",
                    "The spatial vortex swirls violently, then collapses in on itself.",
                    "",
                    "For the first time in thirty years...",
                    "the space between dimensions falls completely silent."
                ]
            },
            {
                "heading": "THE PARADOX UNRAVELED",
                "accent_color": (0.85, 0.35, 1.0),
                "lines": [
                    "The telemetry data recorded by your Rift-Chrono suit finishes uploading.",
                    "",
                    "The Riftborn were not an alien invasion force from a distant galaxy.",
                    "They were temporal echoes of humanity's distant future—",
                    "mutated and warped by the temporal fractures of ruined Earth.",
                    "",
                    "By sealing the Sundered Rift, you severed the closed time loop.",
                    "The future is unwritten once more."
                ]
            },
            {
                "heading": "MISSION ACCOMPLISHED",
                "accent_color": (0.2, 1.0, 0.4),
                "lines": [
                    "PROTOCOL CONCLUDED.",
                    "",
                    "Kepler Relay is secured. Humanity's orbital fleet is safe.",
                    "The Riftwalker has returned from the void.",
                    "",
                    "Thank you for playing RIFTWALKER: PARADOX PROTOCOL.",
                    "[CSE423 Computer Graphics & Multimedia Laboratory Project]"
                ]
            }
        ]

    def next_panel(self) -> bool:
        """Advance to next panel. Returns False if already at final panel."""
        if self.current_panel_index < len(self.panels) - 1:
            self.current_panel_index += 1
            self.fade_alpha = 0.0
            self.fade_timer = 0.0
            return True
        return False

    def reset(self):
        self.current_panel_index = 0
        self.fade_alpha = 0.0
        self.fade_timer = 0.0

    def update(self, dt: float):
        self.fade_timer += dt
        self.fade_alpha = min(1.0, self.fade_timer / 0.35)
        self.pulse_timer += dt

        for p in self.particles:
            p.x += p.vx * dt
            p.y += p.vy * dt
            if p.y > 850:
                p.y = -20
                p.x = random.uniform(0, 1280)
            if p.x < -20:
                p.x = 1300
            elif p.x > 1300:
                p.x = -20

    def draw_text(self, x: float, y: float, text: str, font=None):
        if font is None:
            font = get_glut_font("GLUT_BITMAP_HELVETICA_18")
        if font is None:
            return
        glRasterPos2f(x, y)
        for char in text:
            try:
                glut.glutBitmapCharacter(font, ord(char))
            except Exception:
                break

    def _get_performance_rank(self, score: int) -> Tuple[str, str, Tuple[float, float, float]]:
        """Returns (Rank Letter, Rank Title, Color RGB)."""
        if score >= 12000:
            return "RANK S", "ELITE RIFTWALKER", (1.0, 0.85, 0.1)  # Gold
        elif score >= 9000:
            return "RANK A", "SENIOR OPERATIVE", (0.2, 0.95, 1.0)  # Cyan
        elif score >= 6500:
            return "RANK B", "FIELD AGENT", (0.3, 0.8, 1.0)       # Blue
        elif score >= 4000:
            return "RANK C", "VOID SURVIVOR", (0.9, 0.9, 0.9)     # Silver
        else:
            return "RANK D", "COMPROMISED", (0.8, 0.3, 0.3)        # Red

    def draw(self, width: int, height: int, final_score: int = 0):
        """Renders 2D cinematic victory epilogue panel overlay."""
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
            # 1. Dark Futuristic Deep Space Void Background
            glColor4f(0.02, 0.02, 0.05, 1.0)
            glBegin(GL_QUADS)
            glVertex2f(0, 0)
            glVertex2f(width, 0)
            glVertex2f(width, height)
            glVertex2f(0, height)
            glEnd()

            # 2. Ambient Floating Victory Particles
            glPointSize(3.5)
            glBegin(GL_POINTS)
            for p in self.particles:
                sx = (p.x / 1280.0) * width
                sy = (p.y / 800.0) * height
                glColor4f(p.color[0], p.color[1], p.color[2], p.alpha * 0.85)
                glVertex2f(sx, sy)
            glEnd()

            panel = self.panels[self.current_panel_index]
            accent = panel["accent_color"]
            alpha = self.fade_alpha

            # 3. Centered Terminal Card Container
            card_w = min(940.0, width - 80.0)
            card_h = min(540.0, height - 130.0)
            card_x = (width - card_w) * 0.5
            card_y = (height - card_h) * 0.5 + 20.0

            # Translucent Terminal Plate
            glColor4f(0.04, 0.05, 0.09, 0.94)
            glBegin(GL_QUADS)
            glVertex2f(card_x, card_y)
            glVertex2f(card_x + card_w, card_y)
            glVertex2f(card_x + card_w, card_y + card_h)
            glVertex2f(card_x, card_y + card_h)
            glEnd()

            # Terminal Plate Outer Border
            glColor4f(accent[0] * 0.6, accent[1] * 0.6, accent[2] * 0.7, 0.6)
            glLineWidth(1.5)
            glBegin(GL_LINE_LOOP)
            glVertex2f(card_x, card_y)
            glVertex2f(card_x + card_w, card_y)
            glVertex2f(card_x + card_w, card_y + card_h)
            glVertex2f(card_x, card_y + card_h)
            glEnd()

            # Sci-Fi Corner Bracket Accents
            bracket_len = 24.0
            glColor4f(accent[0], accent[1], accent[2], 0.9)
            glLineWidth(2.0)
            glBegin(GL_LINES)
            # Bottom-left
            glVertex2f(card_x, card_y)
            glVertex2f(card_x + bracket_len, card_y)
            glVertex2f(card_x, card_y)
            glVertex2f(card_x, card_y + bracket_len)
            # Bottom-right
            glVertex2f(card_x + card_w, card_y)
            glVertex2f(card_x + card_w - bracket_len, card_y)
            glVertex2f(card_x + card_w, card_y)
            glVertex2f(card_x + card_w, card_y + bracket_len)
            # Top-right
            glVertex2f(card_x + card_w, card_y + card_h)
            glVertex2f(card_x + card_w - bracket_len, card_y + card_h)
            glVertex2f(card_x + card_w, card_y + card_h)
            glVertex2f(card_x + card_w, card_y + card_h - bracket_len)
            # Top-left
            glVertex2f(card_x, card_y + card_h)
            glVertex2f(card_x + bracket_len, card_y + card_h)
            glVertex2f(card_x, card_y + card_h)
            glVertex2f(card_x, card_y + card_h - bracket_len)
            glEnd()

            # 4. Top Header Tag
            badge_font = get_glut_font("GLUT_BITMAP_8_BY_13") or get_glut_font("GLUT_BITMAP_HELVETICA_12")
            badge_text = f"// RIFTWALKER DEBRIEF // EPILOGUE ENTRY 0{self.current_panel_index + 1} OF 0{len(self.panels)} //"
            glColor4f(accent[0] * 0.9, accent[1] * 0.9, accent[2] * 0.9, alpha * 0.8)
            self.draw_text(card_x + 35.0, card_y + card_h - 32.0, badge_text, font=badge_font)

            # 5. Section Heading (Centered)
            title_font = get_glut_font("GLUT_BITMAP_TIMES_ROMAN_24") or get_glut_font("GLUT_BITMAP_HELVETICA_18")
            title_w = get_text_width(title_font, panel["heading"])
            title_x = card_x + (card_w - title_w) * 0.5
            title_y = card_y + card_h - 76.0
            glColor4f(accent[0], accent[1], accent[2], alpha)
            self.draw_text(title_x, title_y, panel["heading"], font=title_font)

            # Heading Decorative Divider Bar
            glColor4f(accent[0], accent[1], accent[2], alpha * 0.45)
            glLineWidth(1.0)
            glBegin(GL_LINES)
            glVertex2f(card_x + 45.0, title_y - 14.0)
            glVertex2f(card_x + card_w - 45.0, title_y - 14.0)
            glEnd()

            # 6. Narrative Body Text
            body_font = get_glut_font("GLUT_BITMAP_HELVETICA_18") or get_glut_font("GLUT_BITMAP_9_BY_15")
            text_left_x = card_x + 60.0
            start_y = title_y - 48.0
            line_spacing = 26.0

            for i, line in enumerate(panel["lines"]):
                cur_y = start_y - i * line_spacing
                if not line:
                    continue

                is_highlight = any(phrase in line for phrase in (
                    "shatters", "completely silent", "severed the closed time loop",
                    "PROTOCOL CONCLUDED.", "RIFTWALKER: PARADOX PROTOCOL"
                ))

                if is_highlight:
                    glColor4f(accent[0], accent[1], accent[2], alpha)
                else:
                    glColor4f(0.86, 0.90, 0.96, alpha * 0.95)

                self.draw_text(text_left_x, cur_y, line, font=body_font)

            # 7. Final Mission Report Score & Performance Rank (On Panel 3)
            if self.current_panel_index == len(self.panels) - 1:
                rank_str, rank_title, rank_color = self._get_performance_rank(final_score)
                report_y = card_y + 80.0

                glColor3f(1.0, 0.85, 0.2)
                self.draw_text(text_left_x, report_y + 24.0, f"FINAL MISSION SCORE: {final_score}")

                glColor3f(rank_color[0], rank_color[1], rank_color[2])
                self.draw_text(text_left_x, report_y, f"OPERATIONAL EVALUATION: {rank_str} — {rank_title}")

            # 8. Page Indicator
            page_str = f"[  PAGE  {self.current_panel_index + 1}  /  {len(self.panels)}  ]"
            page_w = get_text_width(body_font, page_str)
            glColor4f(0.45, 0.75, 0.95, alpha * 0.85)
            self.draw_text(card_x + (card_w - page_w) * 0.5, card_y + 25.0, page_str, font=body_font)

            # 9. Interactive Navigation Footer Prompt (Pulsating)
            pulse = 0.7 + 0.3 * math.sin(self.pulse_timer * 4.0)
            if self.current_panel_index < len(self.panels) - 1:
                prompt_str = ">> [LEFT CLICK] / [SPACE] / [ENTER] TO ADVANCE EPILOGUE <<"
                prompt_color = (0.0, 0.95, 1.0)
            else:
                prompt_str = ">> PRESS 'R' TO RESTART MISSION    |    [ESC] TO EXIT <<"
                prompt_color = (0.2, 1.0, 0.4)

            prompt_w = get_text_width(body_font, prompt_str)
            prompt_x = (width - prompt_w) * 0.5
            prompt_y = card_y - 32.0
            glColor4f(prompt_color[0], prompt_color[1], prompt_color[2], pulse)
            self.draw_text(prompt_x, prompt_y, prompt_str, font=body_font)

        finally:
            glDisable(GL_BLEND)
            glEnable(GL_LIGHTING)
            glEnable(GL_DEPTH_TEST)
            glMatrixMode(GL_MODELVIEW)
