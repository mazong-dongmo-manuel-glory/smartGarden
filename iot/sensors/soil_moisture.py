import random
from config import MOCK_MODE, PIN_SOIL
from utils.logger import logger

class SoilMoistureSensor:
    def __init__(self, pin=PIN_SOIL):
        self.pin = pin  # Analog pin (channel)

    def read(self):
        """Returns soil moisture percentage."""
        if MOCK_MODE:
            # Simulate drying out over time or random value
            moisture = round(random.uniform(20.0, 80.0), 1)
            logger.debug(f"Sensor [Soil]: Read {moisture}%")
            return moisture
        else:
            # Actual implementation would read from MCP3008 via SPI
            return 0
