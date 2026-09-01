"""Centralized Input Manager for Keyboard and Mouse state tracking."""
from typing import Set, Tuple
from src.shared.constants import WINDOW_WIDTH, WINDOW_HEIGHT


class InputManager:
    def __init__(self, width: int = WINDOW_WIDTH, height: int = WINDOW_HEIGHT):
        self.keys_down: Set[str] = set()
        self.special_keys_down: Set[int] = set()
        self.window_width: int = width
        self.window_height: int = height
        self.center_x: int = width // 2
        self.center_y: int = height // 2

        self.last_x: int = self.center_x
        self.last_y: int = self.center_y
        self.mouse_pos: Tuple[int, int] = (self.center_x, self.center_y)
        self.mouse_delta: Tuple[float, float] = (0.0, 0.0)
        self.mouse_buttons: Set[int] = set()
        self.just_pressed_mouse_buttons: Set[int] = set()
        self.just_pressed_keys: Set[str] = set()
        self.just_pressed_special_keys: Set[int] = set()
        self.first_mouse: bool = True


    def set_window_size(self, width: int, height: int):
        """Update window dimensions and recalculate center point."""
        self.window_width = max(1, width)
        self.window_height = max(1, height)
        self.center_x = self.window_width // 2
        self.center_y = self.window_height // 2
        self.first_mouse = True

    def on_mouse_enter(self, state: int):
        """Handle mouse entering or leaving the window (GLUT entry func)."""
        self.first_mouse = True

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
        if key not in self.special_keys_down:
            self.just_pressed_special_keys.add(key)
        self.special_keys_down.add(key)

    def on_special_up(self, key: int, x: int, y: int):
        self.special_keys_down.discard(key)

    def is_special_key_down(self, key: int) -> bool:
        return key in self.special_keys_down

    def was_special_key_just_pressed(self, key: int) -> bool:
        return key in self.just_pressed_special_keys

    def on_mouse_motion(self, x: int, y: int):
        if self.first_mouse:
            self.last_x = x
            self.last_y = y
            self.mouse_pos = (x, y)
            self.mouse_delta = (0.0, 0.0)
            self.first_mouse = False
            return

        raw_dx = float(x - self.last_x)
        raw_dy = float(y - self.last_y)

        self.last_x = x
        self.last_y = y
        self.mouse_pos = (x, y)

        # Ignore large position discontinuities on window re-entry or focus change
        if abs(raw_dx) > 100.0 or abs(raw_dy) > 100.0:
            self.mouse_delta = (0.0, 0.0)
            return

        self.mouse_delta = (raw_dx, raw_dy)

    def on_mouse_button(self, button: int, state: int, x: int, y: int):
        # state == 0 is GLUT_DOWN, state == 1 is GLUT_UP
        if state == 0:
            if button not in self.mouse_buttons:
                self.just_pressed_mouse_buttons.add(button)
            self.mouse_buttons.add(button)
        else:
            self.mouse_buttons.discard(button)
        self.last_x = x
        self.last_y = y
        self.mouse_pos = (x, y)

    def is_key_down(self, key: str) -> bool:
        return key.lower() in self.keys_down

    def was_key_just_pressed(self, key: str) -> bool:
        return key.lower() in self.just_pressed_keys

    def is_mouse_button_down(self, button: int) -> bool:
        return button in self.mouse_buttons

    def was_mouse_button_just_pressed(self, button: int) -> bool:
        return button in self.just_pressed_mouse_buttons

    def end_frame(self):
        """Clear single-frame trigger buffers at the end of the frame."""
        self.just_pressed_keys.clear()
        self.just_pressed_special_keys.clear()
        self.just_pressed_mouse_buttons.clear()
        self.mouse_delta = (0.0, 0.0)





