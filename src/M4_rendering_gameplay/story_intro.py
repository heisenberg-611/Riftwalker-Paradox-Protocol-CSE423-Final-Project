"""Cinematic Story Introduction Presentation System."""
import os
import json
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


class StoryParticle:
    __slots__ = ('x', 'y', 'vx', 'vy', 'size', 'alpha', 'color')

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.vx = random.uniform(-15.0, 15.0)
        self.vy = random.uniform(10.0, 35.0)
        self.size = random.uniform(2.0, 4.0)
        self.alpha = random.uniform(0.3, 0.8)
        self.color = random.choice([
            (0.0, 0.85, 1.0),   # Cyan
            (0.8, 0.2, 1.0),    # Magenta / Rift Violet
            (0.3, 0.7, 1.0)     # Neon Blue
        ])


class StoryIntroManager:
    """Manages the 6-panel first-time cinematic story introduction."""

    def __init__(self, config_file: str = None):
        if config_file is None:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            self.config_file = os.path.join(base_dir, '.riftwalker_config.json')
        else:
            self.config_file = config_file

        self.story_seen: bool = self._load_story_seen()
        self.current_panel_index: int = 0
        self.fade_alpha: float = 0.0
        self.fade_timer: float = 0.0
        self.pulse_timer: float = 0.0

        # Background ambient floating rift particles
        self.particles: List[StoryParticle] = [
            StoryParticle(random.uniform(0, 1280), random.uniform(0, 800))
            for _ in range(35)
        ]

        # 6 Story Panels with exact canonical narrative text
        self.panels: List[Dict[str, Any]] = [
            {
                "heading": "2089 — EARTH",
                "accent_color": (0.0, 0.9, 1.0),
                "lines": [
                    "Earth did not fall in a war.",
                    "It fell in a silence.",
                    "",
                    "The oceans boiled. The atmosphere burned.",
                    "The last cities went dark one by one.",
                    "",
                    "Humanity escaped into orbit, carrying what little remained of civilization.",
                    "For thirty years, the survivors believed Earth was dead.",
                    "",
                    "They were wrong."
                ]
            },
            {
                "heading": "THE RIFTS",
                "accent_color": (0.85, 0.3, 1.0),
                "lines": [
                    "Three weeks ago, deep-space sensors detected impossible energy signatures",
                    "appearing around the abandoned colonies.",
                    "",
                    "Then the transmissions started.",
                    "",
                    "Distorted voices. Fragments of human messages.",
                    "Coordinates to places that no longer existed.",
                    "",
                    "And finally—",
                    "something came through."
                ]
            },
            {
                "heading": "THE RIFTBORN",
                "accent_color": (1.0, 0.25, 0.35),
                "lines": [
                    "The creatures were called Riftborn.",
                    "",
                    "They did not arrive in ships.",
                    "",
                    "They appeared through fractures in space itself."
                ]
            },
            {
                "heading": "THE RIFT-CHRONO PROJECT",
                "accent_color": (0.0, 1.0, 0.85),
                "lines": [
                    "In desperation, humanity activated its final experimental technology:",
                    "",
                    "THE RIFT-CHRONO SUIT",
                    "",
                    "A prototype designed to manipulate spatial coordinates",
                    "and distort local time for a few seconds.",
                    "",
                    "Only one suit survived testing.",
                    "Only one person was compatible.",
                    "",
                    "YOU."
                ]
            },
            {
                "heading": "KEPLER RELAY",
                "accent_color": (1.0, 0.8, 0.2),
                "lines": [
                    "Now the Kepler Relay is under attack.",
                    "",
                    "Its last transmission contained three words:",
                    "",
                    "\"They found us.\"",
                    "",
                    "Your mission is simple.",
                    "Reach the source. Find out what is coming through the Rifts.",
                    "And survive long enough to discover the truth."
                ]
            },
            {
                "heading": "THE PARADOX",
                "accent_color": (0.3, 0.8, 1.0),
                "lines": [
                    "Because the greatest danger may not be that the aliens are invading Earth...",
                    "",
                    "It may be that they are coming from Earth."
                ]
            }
        ]

    def _load_story_seen(self) -> bool:
        """Loads story_seen flag from local JSON configuration."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    return bool(data.get("story_seen", False))
        except Exception:
            pass
        return False

    def _save_story_seen(self):
        """Persists story_seen flag to local JSON configuration."""
        try:
            data = {}
            if os.path.exists(self.config_file):
                try:
                    with open(self.config_file, 'r') as f:
                        data = json.load(f)
                except Exception:
                    data = {}
            data["story_seen"] = self.story_seen
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def is_story_seen(self) -> bool:
        return self.story_seen

    def mark_story_seen(self):
        self.story_seen = True
        self._save_story_seen()

    def reset_story(self):
        self.story_seen = False
        self.current_panel_index = 0
        self.fade_alpha = 0.0
        self.fade_timer = 0.0
        self._save_story_seen()

    def next_panel(self) -> bool:
        """Advance to next panel. Returns False if already at final panel."""
        if self.current_panel_index < len(self.panels) - 1:
            self.current_panel_index += 1
            self.fade_alpha = 0.0
            self.fade_timer = 0.0
            return True
        else:
            self.mark_story_seen()
            return False

    def skip_story(self):
        """Instantly skip intro and record story as seen."""
        self.mark_story_seen()

    def update(self, dt: float):
        """Update fade-in transitions and particle drift."""
        self.fade_timer += dt
        self.fade_alpha = min(1.0, self.fade_timer / 0.45)
        self.pulse_timer += dt

        # Update ambient floating particles
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

    def draw(self, width: int, height: int):
        """Renders 2D cinematic story panel overlay."""
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

        # 1. Dark Futuristic Deep Space Background
        glColor4f(0.03, 0.03, 0.06, 1.0)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(width, 0)
        glVertex2f(width, height)
        glVertex2f(0, height)
        glEnd()

        # 2. Ambient Floating Rift Particles
        glPointSize(3.0)
        glBegin(GL_POINTS)
        for p in self.particles:
            sx = (p.x / 1280.0) * width
            sy = (p.y / 800.0) * height
            glColor4f(p.color[0], p.color[1], p.color[2], p.alpha * 0.7)
            glVertex2f(sx, sy)
        glEnd()

        # 3. Futuristic HUD Frame Borders & Corner Brackets
        margin = 40.0
        frame_w = width - margin * 2
        frame_h = height - margin * 2
        glColor4f(0.1, 0.35, 0.55, 0.4)
        glLineWidth(1.5)
        glBegin(GL_LINE_LOOP)
        glVertex2f(margin, margin)
        glVertex2f(margin + frame_w, margin)
        glVertex2f(margin + frame_w, margin + frame_h)
        glVertex2f(margin, margin + frame_h)
        glEnd()

        # Corner accent brackets
        bracket_len = 25.0
        glColor4f(0.0, 0.85, 1.0, 0.85)
        glBegin(GL_LINES)
        # Bottom-left
        glVertex2f(margin, margin)
        glVertex2f(margin + bracket_len, margin)
        glVertex2f(margin, margin)
        glVertex2f(margin, margin + bracket_len)
        # Bottom-right
        glVertex2f(margin + frame_w, margin)
        glVertex2f(margin + frame_w - bracket_len, margin)
        glVertex2f(margin + frame_w, margin)
        glVertex2f(margin + frame_w, margin + bracket_len)
        # Top-right
        glVertex2f(margin + frame_w, margin + frame_h)
        glVertex2f(margin + frame_w - bracket_len, margin + frame_h)
        glVertex2f(margin + frame_w, margin + frame_h)
        glVertex2f(margin + frame_w, margin + frame_h - bracket_len)
        # Top-left
        glVertex2f(margin, margin + frame_h)
        glVertex2f(margin + bracket_len, margin + frame_h)
        glVertex2f(margin, margin + frame_h)
        glVertex2f(margin, margin + frame_h - bracket_len)
        glEnd()

        panel = self.panels[self.current_panel_index]
        accent = panel["accent_color"]
        alpha = self.fade_alpha

        # 4. Large Header Title
        title_font = get_glut_font("GLUT_BITMAP_TIMES_ROMAN_24") or get_glut_font("GLUT_BITMAP_HELVETICA_18")
        title_text = panel["heading"]
        title_x = width * 0.5 - (len(title_text) * 5.8)
        title_y = height * 0.78
        glColor4f(accent[0], accent[1], accent[2], alpha)
        self.draw_text(title_x, title_y, title_text, font=title_font)

        # Title underline bar
        bar_len = min(400.0, max(220.0, len(title_text) * 16.0))
        glColor4f(accent[0], accent[1], accent[2], alpha * 0.6)
        glBegin(GL_LINES)
        glVertex2f(width * 0.5 - bar_len * 0.5, title_y - 12.0)
        glVertex2f(width * 0.5 + bar_len * 0.5, title_y - 12.0)
        glEnd()

        # 5. Narrative Body Lines
        body_font = get_glut_font("GLUT_BITMAP_HELVETICA_18") or get_glut_font("GLUT_BITMAP_9_BY_15")
        start_y = title_y - 50.0
        line_spacing = 26.0

        for i, line in enumerate(panel["lines"]):
            cur_y = start_y - i * line_spacing
            if not line:
                continue

            # Special highlight for prominent key phrases
            is_highlight = any(phrase in line for phrase in (
                "wrong", "something came through", "fractures in space",
                "THE RIFT-CHRONO SUIT", "YOU.", "\"They found us.\"", "from Earth"
            ))

            if is_highlight:
                glColor4f(accent[0], accent[1], accent[2], alpha)
            else:
                glColor4f(0.85, 0.90, 0.96, alpha * 0.95)

            line_x = width * 0.5 - (len(line) * 4.2)
            self.draw_text(line_x, cur_y, line, font=body_font)

        # 6. Page Indicator (e.g. [ 1 / 6 ])
        page_str = f"[  {self.current_panel_index + 1}  /  {len(self.panels)}  ]"
        glColor4f(0.4, 0.7, 0.9, 0.8)
        self.draw_text(width * 0.5 - 35.0, margin + 42.0, page_str, font=body_font)

        # 7. Navigation Footer Prompt
        pulse = 0.7 + 0.3 * math.sin(self.pulse_timer * 4.0)
        glColor4f(0.0, 0.95, 1.0, pulse)
        prompt_str = ">> PRESS [ENTER] OR [SPACE] TO CONTINUE    |    [S] TO SKIP <<"
        self.draw_text(width * 0.5 - 240.0, margin + 18.0, prompt_str, font=body_font)

        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
