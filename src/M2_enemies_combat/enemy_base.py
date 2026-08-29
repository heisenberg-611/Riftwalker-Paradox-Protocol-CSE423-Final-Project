"""Abstract Base Class for Enemies."""
import math
from OpenGL.GL import glPushMatrix, glPopMatrix, glTranslatef, glRotatef
from src.shared.math3d import Vector3


class EnemyBase:
    def __init__(self, enemy_id: str, pos: Vector3, hp: float, speed: float, radius: float):
        self.enemy_id = enemy_id
        self.position = pos
        self.hp = hp
        self.max_hp = hp
        self.speed = speed
        self.radius = radius
        self.yaw = 0.0
        self.anim_time = 0.0
        self.is_dead = False

    def update(self, player_pos: Vector3, dt: float):
        self.anim_time += dt

        # Face towards player
        to_player = player_pos - self.position
        self.yaw = math.degrees(math.atan2(to_player.x, to_player.z))

    def take_damage(self, amount: float):
        self.hp -= amount
        if self.hp <= 0.0:
            self.hp = 0.0
            self.is_dead = True

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.yaw, 0.0, 1.0, 0.0)
        self.render_model()
        glPopMatrix()

    def render_model(self):
        raise NotImplementedError("Subclasses must implement render_model")
