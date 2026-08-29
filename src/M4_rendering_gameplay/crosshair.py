"""Dynamic Interactive Crosshair."""
from OpenGL.GL import *


class Crosshair:
    def __init__(self):
        self.hit_feedback_timer = 0.0

    def trigger_hit(self):
        self.hit_feedback_timer = 0.15

    def update(self, dt: float):
        if self.hit_feedback_timer > 0.0:
            self.hit_feedback_timer = max(0.0, self.hit_feedback_timer - dt)

    def draw(self, cx: float, cy: float):
        size = 12.0
        gap = 4.0

        if self.hit_feedback_timer > 0.0:
            glColor3f(1.0, 0.2, 0.2)  # Red hitmarker
            # Draw X hitmarker
            glBegin(GL_LINES)
            glVertex2f(cx - 8, cy - 8)
            glVertex2f(cx + 8, cy + 8)
            glVertex2f(cx - 8, cy + 8)
            glVertex2f(cx + 8, cy - 8)
            glEnd()
        else:
            glColor3f(0.0, 1.0, 0.8)  # Cyan default reticle
            glBegin(GL_LINES)
            # Top
            glVertex2f(cx, cy + gap)
            glVertex2f(cx, cy + gap + size)
            # Bottom
            glVertex2f(cx, cy - gap)
            glVertex2f(cx, cy - gap - size)
            # Left
            glVertex2f(cx - gap, cy)
            glVertex2f(cx - gap - size, cy)
            # Right
            glVertex2f(cx + gap, cy)
            glVertex2f(cx + gap + size, cy)
            glEnd()
