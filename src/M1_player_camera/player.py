"""Player Entity coordinating Rig, Movement, Weapons, Camera, and Stats."""
from OpenGL.GL import glPushMatrix, glPopMatrix, glTranslatef, glRotatef
from src.shared.math3d import Vector3, clamp
from src.shared.constants import MAX_PLAYER_HP, MAX_CHRONO_ENERGY, PLAYER_RADIUS
from src.M1_player_camera.astronaut_rig import AstronautRig
from src.M1_player_camera.player_movement import PlayerMovement
from src.M1_player_camera.player_weapon import PlayerWeapon
from src.M1_player_camera.blink_teleport import BlinkTeleport
from src.M1_player_camera.first_person_camera import FirstPersonCamera
from src.M1_player_camera.third_person_camera import ThirdPersonCamera


class Player:
    def __init__(self, start_pos: Vector3 = Vector3(0.0, 0.0, 0.0)):
        self.position = start_pos
        self.hp = MAX_PLAYER_HP
        self.max_hp = MAX_PLAYER_HP
        self.chrono_energy = MAX_CHRONO_ENERGY
        self.max_chrono_energy = MAX_CHRONO_ENERGY
        self.radius = PLAYER_RADIUS
        self.is_first_person = False

        self.rig = AstronautRig()
        self.movement = PlayerMovement()
        self.weapon = PlayerWeapon()
        self.blink = BlinkTeleport()
        self.fp_cam = FirstPersonCamera()
        self.tp_cam = ThirdPersonCamera()
        self.is_moving = False

    def update(self, dt: float):
        self.weapon.update(dt)
        self.blink.update(dt)

    def toggle_camera(self):
        self.is_first_person = not self.is_first_person
        if self.is_first_person:
            self.fp_cam.yaw = self.tp_cam.yaw
            self.fp_cam.pitch = self.tp_cam.pitch
        else:
            self.tp_cam.yaw = self.fp_cam.yaw
            self.tp_cam.pitch = self.fp_cam.pitch

    def apply_camera(self):
        if self.is_first_person:
            self.fp_cam.apply(self.position)
        else:
            self.tp_cam.apply(self.position)

    def draw(self, dt: float):
        # In first person mode, we don't render our own body (only viewmodel if desired)
        if not self.is_first_person:
            glPushMatrix()
            glTranslatef(self.position.x, self.position.y, self.position.z)
            glRotatef(self.tp_cam.yaw, 0.0, 1.0, 0.0)
            self.rig.draw(is_moving=self.is_moving, dt=dt)
            glPopMatrix()

    def take_damage(self, amount: float):
        self.hp = max(0.0, self.hp - amount)

    def is_alive(self) -> bool:
        return self.hp > 0.0
