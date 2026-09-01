"""Master Renderer coordinating 3D Perspective Pass, Lighting, Particles, and HUD."""
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from src.shared.constants import (
    FOV_DEGREES,
    NEAR_PLANE,
    FAR_PLANE,
    STATE_STORY,
    STATE_TELEPORTING,
    STATE_VICTORY,
    BOSS_RIFT_GUARDIAN
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
        dt: float,
        story_intro=None,
        story_epilogue=None,
        level_manager=None
    ):
        # 0A. Story Introduction Screen
        if game_state.current_state == STATE_STORY and story_intro is not None:
            glClearColor(0.03, 0.03, 0.06, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            story_intro.draw(self.width, self.height)
            glutSwapBuffers()
            return

        # 0B. Cinematic Victory Epilogue Screen
        if game_state.current_state == STATE_VICTORY and story_epilogue is not None:
            glClearColor(0.02, 0.02, 0.05, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            story_epilogue.draw(self.width, self.height, final_score=score_manager.score)
            glutSwapBuffers()
            return

        self.begin_frame()


        # 1. Camera View Matrix
        player.apply_camera()

        # 2. Lighting Updates
        is_beacon_active = True
        if world.current_arena.rift_beacons:
            is_beacon_active = world.current_arena.rift_beacons[0].is_active

        LightingSystem.update_point_lights(
            beacon_pos=world.current_arena.rift_beacons[0].position if world.current_arena.rift_beacons else Vector3(0, 0, 0),
            is_beacon_active=is_beacon_active
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

        # 7. Render 3D Particle Effects & Laser Tracers (In full 3D world space)
        self.particles.draw()

        # 8. Render 1st-Person Weapon Viewmodel (First person mode foreground)
        if player.is_first_person:
            player.weapon.draw_viewmodel(self.width, self.height, is_moving=player.is_moving)

        # 9. Post-process Screen Flash & Chrono Distortion
        if game_state.current_state == STATE_TELEPORTING:
            Effects.draw_screen_flash(self.width, self.height, color=(0.0, 0.85, 1.0), alpha=0.35)
        elif chrono_manager.is_active:
            Effects.draw_chrono_slow_overlay(self.width, self.height, alpha=0.18)

        # 10. 2D HUD Pass (Detect active boss HP)
        boss_hp = 0.0
        boss_max_hp = 0.0
        for e in enemies:
            if getattr(e, 'enemy_id', None) == BOSS_RIFT_GUARDIAN and not e.is_dead:
                boss_hp = e.hp
                boss_max_hp = e.max_hp
                break

        # Level objective text
        obj_title = level_manager.get_objective_title() if level_manager else ""
        obj_sub = level_manager.get_objective_subtitle() if level_manager else ""
        is_intermission = (level_manager.wave_state == level_manager.STATE_INTERMISSION) if level_manager else False

        self.hud.draw(
            width=self.width,
            height=self.height,
            hp=player.hp,
            max_hp=player.max_hp,
            chrono_charge=chrono_manager.charge,
            max_chrono=chrono_manager.max_charge,
            score=score_manager.score,
            is_chrono_active=chrono_manager.is_active,
            chrono_time_remaining=chrono_manager.active_time_remaining,
            can_teleport=can_teleport,
            is_first_person=player.is_first_person,
            game_state_str=game_state.current_state,
            boss_hp=boss_hp,
            boss_max_hp=boss_max_hp,
            weapon_cooldown_ratio=player.weapon.get_cooldown_ratio(),
            objective_title=obj_title,
            objective_subtitle=obj_sub,
            combo_multiplier=score_manager.combo,
            combo_ratio=score_manager.combo_ratio,
            is_intermission=is_intermission
        )


        glutSwapBuffers()
