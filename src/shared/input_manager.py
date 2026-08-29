"""Centralized Input Manager for Keyboard and Mouse state tracking."""
from typing import Set, Tuple


class InputManager:
    def __init__(self):
        self.keys_down: Set[str] = set()
        self.special_keys_down: Set[int] = set()
        self.mouse_pos: Tuple[int, int] = (0, 0)
        self.mouse_delta: Tuple[int, int] = (0, 0)
        self.mouse_buttons: Set[int] = set()
        self.just_pressed_keys: Set[str] = set()
        self.first_mouse: bool = True

    def on_key_down(self, key: bytes, x: int, y: int):
        try:
            char = key.decode('utf-8').lower()
            if char not in self.keys_down:
                self.just_pressed_keys.add(char)
            self.keys_down.add(char)
        except UnicodeDecodeError:
            pass

    def on_key_up(self, key: bytes, x: int, y: int):
        try:
            char = key.decode('utf-8').lower()
            self.keys_down.discard(char)
        except UnicodeDecodeError:
            pass

    def on_special_down(self, key: int, x: int, y: int):
        self.special_keys_down.add(key)

    def on_special_up(self, key: int, x: int, y: int):
        self.special_keys_down.discard(key)

    def on_mouse_motion(self, x: int, y: int):
        if self.first_mouse:
            self.mouse_pos = (x, y)
            self.mouse_delta = (0, 0)
            self.first_mouse = False
            return
        dx = x - self.mouse_pos[0]
        dy = y - self.mouse_pos[1]
        self.mouse_delta = (dx, dy)
        self.mouse_pos = (x, y)

    def on_mouse_button(self, button: int, state: int, x: int, y: int):
        # state == 0 is GLUT_DOWN, state == 1 is GLUT_UP
        if state == 0:
            self.mouse_buttons.add(button)
        else:
            self.mouse_buttons.discard(button)
        self.mouse_pos = (x, y)

    def is_key_down(self, key: str) -> bool:
        return key.lower() in self.keys_down

    def was_key_just_pressed(self, key: str) -> bool:
        return key.lower() in self.just_pressed_keys

    def is_mouse_button_down(self, button: int) -> bool:
        return button in self.mouse_buttons

    def end_frame(self):
        """Clear single-frame trigger buffers at the end of the frame."""
        self.just_pressed_keys.clear()
        self.mouse_delta = (0, 0)
