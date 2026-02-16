import random
from config import MOCK_MODE
from utils.logger import logger

class WaterLevelSensor:
    def __init__(self, pin=5):
        self.pin = pin

    def read(self):
        """Returns water level percentage."""
        if MOCK_MODE:
            # Randomly fluctuate, mostly full
            level = round(random.uniform(10.0, 100.0), 1)
            logger.debug(f"Sensor [Water]: Read {level}%")
            return level
        else:
            return 0
