"""
Riftwalker: Paradox Protocol
CSE423 Final Project — Main Entry Point
"""
import sys
import os
import math
import time

# Ensure project root is in sys.path
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# Windows FreeGLUT DLL Setup
if sys.platform == 'win32':
    _dll_dir = os.path.join(_PROJECT_ROOT, 'OpenGL', 'DLLS')
    if os.path.exists(_dll_dir):
        if hasattr(os, 'add_dll_directory'):
            try:
                os.add_dll_directory(_dll_dir)
            except Exception:
                pass
        os.environ['PATH'] = _dll_dir + os.pathsep + _PROJECT_ROOT + os.pathsep + os.environ.get('PATH', '')
    if hasattr(os, 'add_dll_directory'):
        try:
            os.add_dll_directory(_PROJECT_ROOT)
        except Exception:
            pass

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.shared.constants import (
    WINDOW_TITLE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    STATE_STORY,
    STATE_PLAYING,
    STATE_TELEPORTING,
    STATE_GAME_OVER,
    STATE_VICTORY,
    ARENA_01_KEPLER_RELAY,
    ARENA_02_SUNDERED_RIFT,
    ENEMY_MELEE_RIFT_STALKER,
    ENEMY_RANGED_RIFT_SPITTER,
    BOSS_RIFT_GUARDIAN,
    CHRONO_CHARGE_KILL_STALKER,
    CHRONO_CHARGE_KILL_SPITTER,
    CHRONO_CHARGE_BOSS_HIT
)
from src.shared.math3d import Vector3
from src.shared.game_time import GameTime
from src.shared.input_manager import InputManager
from src.M1_player_camera.player import Player
from src.M2_enemies_combat.weapon_system import WeaponSystem
from src.M2_enemies_combat.raycast import RaycastSystem
from src.M2_enemies_combat.collision import CollisionSystem
from src.M2_enemies_combat.ranged_rift_spitter import RangedRiftSpitter
from src.M2_enemies_combat.rift_guardian_boss import RiftGuardianBoss
from src.M3_world_teleport.world import World
from src.M4_rendering_gameplay.renderer import MasterRenderer
from src.M4_rendering_gameplay.lighting import LightingSystem
from src.M4_rendering_gameplay.chrono_slow import ChronoSlowManager
from src.M4_rendering_gameplay.game_state import GameState
from src.M4_rendering_gameplay.scoring import ScoreManager
from src.M4_rendering_gameplay.level_manager import LevelManager
from src.M4_rendering_gameplay.story_intro import StoryIntroManager
from src.M4_rendering_gameplay.story_epilogue import StoryEpilogueManager


class GameApp:
    def __init__(self):
        self.game_time = GameTime()
        self.input_mgr = InputManager()
        self.renderer = MasterRenderer(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.world = World()
        self.player = Player(Vector3(0.0, 0.0, -35.0))
        self.weapons = WeaponSystem()
        self.chrono_mgr = ChronoSlowManager()
        self.story_intro = StoryIntroManager()
        self.story_epilogue = StoryEpilogueManager()
        self.game_state = GameState(initial_state=STATE_STORY)
        self.score_mgr = ScoreManager()

        self.level_mgr = LevelManager()
        active_beacon = self.world.current_arena.rift_beacons[0] if self.world.current_arena.rift_beacons else None
        self.enemies = self.level_mgr.start_arena(self.world.active_arena_id, beacon=active_beacon)
        self.destination_arena = None


    def reset_game(self):
        self.game_state.restart()
        self.world.active_arena_id = ARENA_01_KEPLER_RELAY
        self.player = Player(Vector3(0.0, 0.0, -35.0))
        self.weapons = WeaponSystem()
        self.chrono_mgr = ChronoSlowManager()
        self.score_mgr = ScoreManager()
        self.story_epilogue.reset()
        self.level_mgr = LevelManager()
        active_beacon = self.world.current_arena.rift_beacons[0] if self.world.current_arena.rift_beacons else None
        self.enemies = self.level_mgr.start_arena(ARENA_01_KEPLER_RELAY, beacon=active_beacon)
        self.input_mgr.first_mouse = True

    def handle_input(self, real_dt: float):
        # 0A. Story Introduction Screen Controls
        if self.game_state.current_state == STATE_STORY:
            # Advance Panel on Left Click / Enter / Space / Right Arrow
            if (self.input_mgr.was_mouse_button_just_pressed(0) or
                self.input_mgr.was_key_just_pressed('\r') or
                self.input_mgr.was_key_just_pressed('\n') or
                self.input_mgr.was_key_just_pressed(' ') or
                self.input_mgr.was_special_key_just_pressed(GLUT_KEY_RIGHT)):
                if not self.story_intro.next_panel():
                    self.game_state.current_state = STATE_PLAYING
            # Skip Story on 'S'
            elif self.input_mgr.was_key_just_pressed('s'):
                self.story_intro.skip_story()
                self.game_state.current_state = STATE_PLAYING
            # Fullscreen Toggle on F11 during Story
            if self.input_mgr.was_special_key_just_pressed(GLUT_KEY_F11):
                glutFullScreen()
            return

        # 0B. Cinematic Victory Epilogue Screen Controls
        if self.game_state.current_state == STATE_VICTORY:
            # Advance Epilogue Panel on Left Click / Enter / Space / Right Arrow
            if (self.input_mgr.was_mouse_button_just_pressed(0) or
                self.input_mgr.was_key_just_pressed('\r') or
                self.input_mgr.was_key_just_pressed('\n') or
                self.input_mgr.was_key_just_pressed(' ') or
                self.input_mgr.was_special_key_just_pressed(GLUT_KEY_RIGHT)):
                self.story_epilogue.next_panel()
            # Restart on 'R'
            if self.input_mgr.was_key_just_pressed('r'):
                self.reset_game()
            # Fullscreen Toggle on F11
            if self.input_mgr.was_special_key_just_pressed(GLUT_KEY_F11):
                glutFullScreen()
            return

        # End-Game (Game Over) Screen Controls
        if self.game_state.current_state == STATE_GAME_OVER:
            # Restart on 'R'
            if self.input_mgr.was_key_just_pressed('r'):
                self.reset_game()
            # Fullscreen Toggle on F11
            if self.input_mgr.was_special_key_just_pressed(GLUT_KEY_F11):
                glutFullScreen()
            return

        # Fullscreen Toggle (F11)
        if self.input_mgr.was_special_key_just_pressed(GLUT_KEY_F11):
            glutFullScreen()

        # 1. View Switching (V / C)
        if self.input_mgr.was_key_just_pressed('v') or self.input_mgr.was_key_just_pressed('c'):
            self.player.toggle_camera()

        # 2. Chrono Slow (Q) - requires 100% charge
        if self.input_mgr.was_key_just_pressed('q'):
            if self.chrono_mgr.activate():
                self.game_time.set_chrono_slow(True)
                self.renderer.particles.spawn_chrono_ripple(self.player.position, count=30)
                self.renderer.particles.spawn_teleport_vortex(self.player.position, count=20)

        # 3. Blink Teleport (Shift / E)
        if self.input_mgr.was_key_just_pressed('e'):
            if self.player.blink.is_ready():
                current_yaw = self.player.fp_cam.yaw if self.player.is_first_person else self.player.tp_cam.yaw
                new_pos = self.player.blink.execute_blink(self.player.position, current_yaw)
                resolved_pos = self.world.current_arena.resolve_collision(new_pos, self.player.radius)
                self.player.position = CollisionSystem.clamp_to_arena_bounds(
                    resolved_pos, self.world.current_arena.half_extent
                )
                self.renderer.particles.spawn_teleport_vortex(self.player.position, count=15)

        # 4. Arena Rift Teleportation (F)
        can_teleport = self.world.check_teleport_trigger(self.player.position) is not None
        if self.input_mgr.was_key_just_pressed('f') and can_teleport:
            dest = self.world.check_teleport_trigger(self.player.position)
            if dest and self.game_state.current_state == STATE_PLAYING:
                self.destination_arena = dest
                self.game_state.start_teleport(duration=1.8)
                self.renderer.particles.spawn_teleport_vortex(self.player.position, count=35)


        # 5. Restart (R)
        if self.input_mgr.was_key_just_pressed('r'):
            if self.game_state.current_state in (STATE_GAME_OVER, STATE_VICTORY):
                self.reset_game()

        # Fullscreen Toggle (F11)
        if self.input_mgr.was_special_key_just_pressed(GLUT_KEY_F11):
            glutFullScreen()

        # Smooth Keyboard Camera Aiming (Arrow Keys)
        rot_speed = 120.0 * real_dt
        if self.input_mgr.is_special_key_down(GLUT_KEY_LEFT):
            if self.player.is_first_person:
                self.player.fp_cam.yaw += rot_speed
            else:
                self.player.tp_cam.yaw += rot_speed
        if self.input_mgr.is_special_key_down(GLUT_KEY_RIGHT):
            if self.player.is_first_person:
                self.player.fp_cam.yaw -= rot_speed
            else:
                self.player.tp_cam.yaw -= rot_speed
        if self.input_mgr.is_special_key_down(GLUT_KEY_UP):
            cam = self.player.fp_cam if self.player.is_first_person else self.player.tp_cam
            cam.pitch = min(cam.pitch + rot_speed, 85.0 if self.player.is_first_person else 65.0)
        if self.input_mgr.is_special_key_down(GLUT_KEY_DOWN):
            cam = self.player.fp_cam if self.player.is_first_person else self.player.tp_cam
            cam.pitch = max(cam.pitch - rot_speed, -85.0 if self.player.is_first_person else -60.0)

        # 6. Player Movement (WASD)
        if self.game_state.current_state == STATE_PLAYING:

            fwd = 0.0
            strafe = 0.0
            if self.input_mgr.is_key_down('w'):
                fwd += 1.0
            if self.input_mgr.is_key_down('s'):
                fwd -= 1.0
            if self.input_mgr.is_key_down('d'):
                strafe += 1.0
            if self.input_mgr.is_key_down('a'):
                strafe -= 1.0

            current_yaw = self.player.fp_cam.yaw if self.player.is_first_person else self.player.tp_cam.yaw
            delta_pos = self.player.movement.compute_movement(fwd, strafe, current_yaw, real_dt)
            new_pos = self.player.position + delta_pos
            resolved_pos = self.world.current_arena.resolve_collision(new_pos, self.player.radius)
            self.player.position = CollisionSystem.clamp_to_arena_bounds(
                resolved_pos, self.world.current_arena.half_extent
            )
            self.player.is_moving = delta_pos.length_squared() > 1e-6

            # 7. Shooting (Hold to Charge / Tap to Fire)
            is_fire_down = self.input_mgr.is_mouse_button_down(0) or self.input_mgr.is_key_down(' ')
            was_fire_released = self.input_mgr.was_mouse_button_just_released(0) or self.input_mgr.was_key_just_released(' ')

            should_discharge = (
                was_fire_released and self.player.weapon.can_fire()
            ) or (
                is_fire_down and self.player.weapon.is_fully_charged()
            )

            if should_discharge:
                if self.player.weapon.trigger_shot():
                    is_overcharged = self.player.weapon.is_overcharged
                    shot_damage = self.player.weapon.last_shot_damage

                    active_cam = self.player.fp_cam if self.player.is_first_person else self.player.tp_cam
                    cam_eye = active_cam.get_cam_eye(self.player.position)
                    cam_forward, cam_right, cam_up = active_cam.get_basis_vectors()

                    # Calculate visual weapon muzzle in world space
                    if self.player.is_first_person:
                        muzzle_world = self.player.weapon.get_fp_muzzle_world(
                            cam_eye, cam_forward, cam_right, cam_up
                        )
                    else:
                        muzzle_world = self.player.rig.get_tp_muzzle_world(
                            self.player.position, self.player.tp_cam.yaw, self.player.tp_cam.pitch
                        )

                    # Spawn muzzle flash sparks at the visual weapon tip
                    self.renderer.particles.spawn_muzzle_flash(muzzle_world, is_overcharged=is_overcharged)

                    # Authoritative crosshair-driven gameplay raycast from camera eye
                    aim_result = RaycastSystem.fire_ray(cam_eye, cam_forward, self.enemies, self.player.weapon.range)

                    # Visual 3D laser tracer connects weapon muzzle directly to aim_point
                    self.renderer.particles.spawn_laser_tracer(muzzle_world, aim_result.hit_point, is_overcharged=is_overcharged)

                    if aim_result.hit_enemy:
                        enemy = aim_result.hit_enemy
                        enemy.take_damage(shot_damage)
                        self.renderer.hud.crosshair.trigger_hit()
                        spark_count = 28 if is_overcharged else 14
                        self.renderer.particles.spawn_hit_sparks(aim_result.hit_point, count=spark_count)
                        if enemy.is_dead:
                            self.score_mgr.add_kill(enemy.enemy_id)
                            self.renderer.particles.spawn_death_burst(enemy.position, count=24)
                            # Reward Chrono Charge on enemy kills
                            if enemy.enemy_id == ENEMY_MELEE_RIFT_STALKER:
                                self.chrono_mgr.add_charge(CHRONO_CHARGE_KILL_STALKER)
                            elif enemy.enemy_id == ENEMY_RANGED_RIFT_SPITTER:
                                self.chrono_mgr.add_charge(CHRONO_CHARGE_KILL_SPITTER)
                            elif enemy.enemy_id == BOSS_RIFT_GUARDIAN:
                                self.chrono_mgr.add_charge(50.0)
                                self.game_state.trigger_victory()
                        else:
                            if enemy.enemy_id == BOSS_RIFT_GUARDIAN:
                                self.chrono_mgr.add_charge(CHRONO_CHARGE_BOSS_HIT)




    def update(self):
        real_dt = self.game_time.tick()
        game_dt = self.game_time.dt

        # If in story introduction mode, update story and skip world physics
        if self.game_state.current_state == STATE_STORY:
            self.handle_input(real_dt)
            self.story_intro.update(real_dt)
            self.input_mgr.end_frame()
            return

        # If in Victory Epilogue, update epilogue particles and fade
        if self.game_state.current_state == STATE_VICTORY:
            self.handle_input(real_dt)
            self.story_epilogue.update(real_dt)
            self.input_mgr.end_frame()
            return

        # If in Game Over, freeze world simulation, player, and enemies
        if self.game_state.current_state == STATE_GAME_OVER:
            self.handle_input(real_dt)
            self.renderer.particles.update(real_dt)
            self.renderer.hud.crosshair.update(real_dt)
            self.input_mgr.end_frame()
            return

        # Update input
        self.handle_input(real_dt)


        # Update player & camera
        is_fire_down = (
            self.game_state.current_state == STATE_PLAYING and
            (self.input_mgr.is_mouse_button_down(0) or self.input_mgr.is_key_down(' '))
        )
        self.player.update(real_dt, is_holding_fire=is_fire_down)
        self.chrono_mgr.update(real_dt)
        self.game_time.set_chrono_slow(self.chrono_mgr.is_active)
        self.score_mgr.update(real_dt)
        self.renderer.particles.update(real_dt)
        self.renderer.hud.crosshair.update(real_dt)
        self.world.update(game_dt)

        # Check Rift Energy Pickups
        if self.game_state.current_state == STATE_PLAYING:
            for pickup in self.world.current_arena.energy_pickups:
                if pickup.is_player_in_range(self.player.position, self.player.radius):
                    gained = pickup.collect()
                    if gained > 0.0:
                        self.chrono_mgr.add_charge(gained)
                        self.score_mgr.add_score(150)
                        self.renderer.particles.spawn_pickup_burst(pickup.position, count=18)

        # Handle Teleportation Transition
        if self.game_state.current_state == STATE_TELEPORTING:
            if self.game_state.update_teleport(real_dt):
                if self.destination_arena:
                    new_pos = self.world.switch_arena(self.destination_arena)
                    self.player.position = new_pos
                    active_beacon = self.world.current_arena.rift_beacons[0] if self.world.current_arena.rift_beacons else None
                    self.enemies = self.level_mgr.start_arena(self.world.active_arena_id, beacon=active_beacon)
                    self.destination_arena = None
                    self.renderer.particles.spawn_teleport_vortex(self.player.position, count=30)

        # Update Enemies & Projectiles (Scaled by Chrono Slow dt)
        if self.game_state.current_state == STATE_PLAYING:
            # Wave Progression Update
            active_beacon = self.world.current_arena.rift_beacons[0] if self.world.current_arena.rift_beacons else None
            self.enemies = self.level_mgr.update(
                dt=game_dt,
                enemies=self.enemies,
                score_manager=self.score_mgr,
                beacon=active_beacon
            )

            for enemy in self.enemies:
                if isinstance(enemy, RangedRiftSpitter):
                    proj = enemy.update_and_shoot(self.player.position, game_dt)
                    if proj:
                        self.weapons.add_projectile(proj)
                elif isinstance(enemy, RiftGuardianBoss):
                    projs = enemy.update_and_attack(self.player.position, game_dt)
                    self.weapons.add_projectiles(projs)
                else:
                    enemy.update(self.player.position, game_dt)

                if not enemy.is_dead:
                    enemy.position = self.world.current_arena.resolve_collision(enemy.position, enemy.radius)
                    enemy.position = CollisionSystem.clamp_to_arena_bounds(
                        enemy.position, self.world.current_arena.half_extent
                    )

                # Melee contact damage
                if not enemy.is_dead and hasattr(enemy, 'attack_damage'):
                    if CollisionSystem.check_sphere_sphere(
                        self.player.position, self.player.radius,
                        enemy.position, enemy.radius
                    ):
                        if getattr(enemy, 'attack_timer', 0.0) <= 0.0:
                            self.player.take_damage(enemy.attack_damage)
                            self.score_mgr.take_damage_penalty()
                            enemy.attack_timer = enemy.attack_cooldown
                            if not self.player.is_alive():
                                self.game_state.trigger_game_over()

            self.weapons.update(game_dt)

            # Check projectile collisions against player
            for p in self.weapons.enemy_projectiles:
                if p.is_alive and CollisionSystem.check_sphere_sphere(
                    self.player.position + Vector3(0.0, 1.2, 0.0), self.player.radius,
                    p.position, p.radius
                ):
                    p.is_alive = False
                    self.player.take_damage(p.damage)
                    self.score_mgr.take_damage_penalty()
                    self.renderer.particles.spawn_hit_sparks(p.position, count=8)
                    if not self.player.is_alive():
                        self.game_state.trigger_game_over()

        # End of frame input cleanup
        self.input_mgr.end_frame()

    def render(self):
        can_teleport = self.world.check_teleport_trigger(self.player.position) is not None
        self.renderer.render_scene(
            player=self.player,
            world=self.world,
            enemies=self.enemies,
            weapons=self.weapons,
            chrono_manager=self.chrono_mgr,
            game_state=self.game_state,
            score_manager=self.score_mgr,
            can_teleport=can_teleport,
            dt=self.game_time.real_dt,
            story_intro=self.story_intro,
            story_epilogue=self.story_epilogue,
            level_manager=self.level_mgr
        )



# Global Application Instance for GLUT Callbacks
app: GameApp = None
last_frame_time: float = 0.0
TARGET_FRAME_DURATION: float = 1.0 / 60.0


def display_callback():
    if app:
        app.render()





def idle_callback():
    global last_frame_time
    if app:
        now = time.time()
        elapsed = now - last_frame_time
        if elapsed >= TARGET_FRAME_DURATION:
            last_frame_time = now
            app.update()
            glutPostRedisplay()
        else:
            # Yield CPU to prevent core starvation and frame drops
            time.sleep(0.001)



def reshape_callback(w, h):
    if app:
        app.renderer.reshape(w, h)
        app.input_mgr.set_window_size(w, h)


def entry_callback(state):
    if app:
        app.input_mgr.on_mouse_enter(state)


def keyboard_down_callback(key, x, y):
    if app:
        if key == b'\x1b':  # Escape key
            sys.exit(0)
        app.input_mgr.on_key_down(key, x, y)


def keyboard_up_callback(key, x, y):
    if app:
        app.input_mgr.on_key_up(key, x, y)


def special_down_callback(key, x, y):
    if app:
        app.input_mgr.on_special_down(key, x, y)


def special_up_callback(key, x, y):
    if app:
        app.input_mgr.on_special_up(key, x, y)


def mouse_motion_callback(x, y):
    if app:
        app.input_mgr.on_mouse_motion(x, y)
        if app.game_state.current_state in (STATE_PLAYING, STATE_TELEPORTING):
            dx, dy = app.input_mgr.mouse_delta
            if dx != 0 or dy != 0:
                if app.player.is_first_person:
                    app.player.fp_cam.update_orientation(dx, dy)
                else:
                    app.player.tp_cam.update_orientation(dx, dy)



def mouse_button_callback(button, state, x, y):
    if app:
        app.input_mgr.on_mouse_button(button, state, x, y)


def main():
    global app

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(WINDOW_TITLE)

    LightingSystem.init_lighting()
    from src.shared.texture_loader import init_textures
    init_textures()

    app = GameApp()


    glutDisplayFunc(display_callback)
    glutIdleFunc(idle_callback)
    glutReshapeFunc(reshape_callback)
    glutKeyboardFunc(keyboard_down_callback)
    glutKeyboardUpFunc(keyboard_up_callback)
    glutSpecialFunc(special_down_callback)
    glutSpecialUpFunc(special_up_callback)
    glutPassiveMotionFunc(mouse_motion_callback)
    glutMotionFunc(mouse_motion_callback)
    glutMouseFunc(mouse_button_callback)
    glutEntryFunc(entry_callback)

    print("==================================================")
    print(" Riftwalker: Paradox Protocol [CSE423 Game Lab] ")
    print(" Controls:")
    print("   WASD         - Move Player")
    print("   Mouse        - Look / Aim")
    print("   Arrow Keys   - Continuous Smooth Camera Turn")
    print("   Left Click   - Fire Hitscan Laser (or Space)")
    print("   V / C        - Toggle 1st / 3rd Person Camera")
    print("   Q            - Chrono Slow (Time Dilation)")
    print("   F            - Interact / Rift Beacon Teleport")
    print("   E            - Blink Combat Dash")
    print("   F11          - Toggle Fullscreen")
    print("   R            - Restart Game")
    print("   Esc          - Exit")
    print("==================================================")

    glutMainLoop()



if __name__ == '__main__':
    main()

