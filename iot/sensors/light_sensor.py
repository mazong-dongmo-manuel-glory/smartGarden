import random
from config import MOCK_MODE, PIN_LDR
from utils.logger import logger

class LightSensor:
    def __init__(self, pin=PIN_LDR):
        self.pin = pin

    def read(self):
        """Returns light intensity in Lux (approx)."""
        if MOCK_MODE:
            lux = random.randint(100, 1000)
            logger.debug(f"Sensor [Light]: Read {lux} lux")
            return lux
        else:
            return 0
