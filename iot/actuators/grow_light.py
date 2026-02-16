from config import MOCK_MODE
from utils.logger import logger

class GrowLight:
    def __init__(self, pin):
        self.pin = pin
        self.intensity = 0

    def set_intensity(self, level):
        """Sets intensity (0-100%)."""
        self.intensity = level
        logger.info(f"Actuator [Light]: Set to {level}% (Pin {self.pin})")
        if not MOCK_MODE:
            # PWM implementation here
            pass
