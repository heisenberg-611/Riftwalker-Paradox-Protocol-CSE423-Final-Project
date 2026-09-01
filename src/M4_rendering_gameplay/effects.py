"""Visual Filters and Post-process-style Effects."""
from OpenGL.GL import *


class Effects:
    @staticmethod
    def draw_screen_flash(width: int, height: int, color=(1.0, 1.0, 1.0), alpha=0.5):
        """Draws a semi-transparent full-screen flash quad."""
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

        try:
            glColor4f(color[0], color[1], color[2], alpha)
            glBegin(GL_QUADS)
            glVertex2f(0, 0)
            glVertex2f(width, 0)
            glVertex2f(width, height)
            glVertex2f(0, height)
            glEnd()
        finally:
            glDisable(GL_BLEND)
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_LIGHTING)

            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)

    @staticmethod
    def draw_chrono_slow_overlay(width: int, height: int, alpha: float = 0.15):
        """Draws cool-blue temporal distortion tint and corner vignette."""
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

        try:
            # 1. Full Screen Cyan/Blue Tint
            glColor4f(0.0, 0.4, 0.85, alpha)
            glBegin(GL_QUADS)
            glVertex2f(0, 0)
            glVertex2f(width, 0)
            glVertex2f(width, height)
            glVertex2f(0, height)
            glEnd()

            # 2. Temporal Corner Vignette Lines
            glColor4f(0.0, 0.9, 1.0, alpha * 2.0)
            glLineWidth(2.5)
            glBegin(GL_LINES)
            # Top-Left corner accent
            glVertex2f(20, height - 20)
            glVertex2f(80, height - 20)
            glVertex2f(20, height - 20)
            glVertex2f(20, height - 80)
            # Top-Right corner accent
            glVertex2f(width - 20, height - 20)
            glVertex2f(width - 80, height - 20)
            glVertex2f(width - 20, height - 20)
            glVertex2f(width - 20, height - 80)
            glEnd()
        finally:
            glDisable(GL_BLEND)
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_LIGHTING)

            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)

