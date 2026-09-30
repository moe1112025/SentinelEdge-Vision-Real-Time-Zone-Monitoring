from dataclasses import dataclass


@dataclass(frozen=True)
class Zone:
    left: int = 150
    top: int = 100
    right: int = 490
    bottom: int = 380

    def contains(self, x, y):
        return self.left <= x <= self.right and self.top <= y <= self.bottom


@dataclass(frozen=True)
class Settings:
    model_path: str = "yolo26n.pt"
    confidence: float = 0.45
    alarm_cooldown_seconds: float = 2.5
