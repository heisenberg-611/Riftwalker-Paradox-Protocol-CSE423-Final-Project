"""Time management and Chrono Slow time dilation calculation."""
import time
from src.shared.constants import CHRONO_SLOW_FACTOR


class GameTime:
    def __init__(self):
        self.last_time = time.time()
        self.unscaled_dt = 0.01666  # Initial 60 FPS estimate
        self.chrono_active = False
        self.chrono_factor = 1.0
        self.total_real_time = 0.0
        self.total_game_time = 0.0

    def tick(self) -> float:
        """Call once per frame in idle / mainloop callback."""
        now = time.time()
        raw_dt = now - self.last_time
        self.last_time = now

        # Clamp dt to prevent massive jumps when window is paused or moved
        self.unscaled_dt = max(0.001, min(raw_dt, 0.1))
        self.total_real_time += self.unscaled_dt

        self.chrono_factor = CHRONO_SLOW_FACTOR if self.chrono_active else 1.0
        scaled_dt = self.unscaled_dt * self.chrono_factor
        self.total_game_time += scaled_dt

        return self.unscaled_dt

    @property
    def dt(self) -> float:
        """World/enemy simulation delta time (scaled during Chrono Slow)."""
        return self.unscaled_dt * self.chrono_factor

    @property
    def real_dt(self) -> float:
        """Real-time delta time (for player movement, camera, HUD)."""
        return self.unscaled_dt

    def set_chrono_slow(self, active: bool):
        self.chrono_active = active
