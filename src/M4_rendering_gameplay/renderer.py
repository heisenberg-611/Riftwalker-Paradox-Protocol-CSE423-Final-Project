"""Master Renderer coordinating 3D Perspective Pass, Lighting, Particles, and HUD."""
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from src.shared.constants import (
    FOV_DEGREES,
    NEAR_PLANE,
    FAR_PLANE,
    STATE_TELEPORTING
)
from src.shared.math3d import Vector3
from src.M4_rendering_gameplay.lighting import LightingSystem
from src.M4_rendering_gameplay.particles import ParticleSystem
from src.M4_rendering_gameplay.effects import Effects
from src.M4_rendering_gameplay.hud import HUD


class MasterRenderer:
    def __init__(self, width: int = 1024, height: int = 768):
        self.width = width
        self.height = height
        self.hud = HUD()
        self.particles = ParticleSystem()

    def reshape(self, w: int, h: int):
        self.width = max(1, w)
        self.height = max(1, h)
        glViewport(0, 0, self.width, self.height)

    def begin_frame(self):
        glClearColor(0.04, 0.04, 0.08, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = float(self.width) / float(self.height)
        gluPerspective(FOV_DEGREES, aspect, NEAR_PLANE, FAR_PLANE)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)

    def render_scene(
        self,
        player,
        world,
        enemies,
        weapons,
        chrono_manager,
        game_state,
        score_manager,
        can_teleport: bool,
        dt: float
    ):
        self.begin_frame()

        # 1. Camera View Matrix
        player.apply_camera()

        # 2. Lighting Updates
        LightingSystem.update_point_lights(
            beacon_pos=world.current_arena.rift_beacons[0].position if world.current_arena.rift_beacons else Vector3(0, 0, 0),
            is_beacon_active=True
        )

        # 3. Render 3D World Geometry
        world.draw()

        # 4. Render Enemies
        for enemy in enemies:
            if not enemy.is_dead:
                enemy.draw()

        # 5. Render Projectiles
        weapons.draw()

        # 6. Render Player Model (Third person mode)
        player.draw(dt=dt)

        # 7. Render Particle Effects
        self.particles.draw()

        # 8. Post-process Screen Flash (during Teleport or Chrono)
        if game_state.current_state == STATE_TELEPORTING:
            Effects.draw_screen_flash(self.width, self.height, color=(0.0, 0.8, 1.0), alpha=0.35)
        elif chrono_manager.is_active:
            Effects.draw_screen_flash(self.width, self.height, color=(0.1, 0.3, 0.8), alpha=0.12)

        # 9. 2D HUD Pass
        self.hud.draw(
            width=self.width,
            height=self.height,
            hp=player.hp,
            max_hp=player.max_hp,
            chrono_energy=chrono_manager.energy,
            max_chrono=chrono_manager.max_energy,
            score=score_manager.score,
            is_chrono_active=chrono_manager.is_active,
            can_teleport=can_teleport,
            is_first_person=player.is_first_person,
            game_state_str=game_state.current_state
        )

        glutSwapBuffers()
