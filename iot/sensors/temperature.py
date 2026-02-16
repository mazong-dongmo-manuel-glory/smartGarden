import random
from config import MOCK_MODE, PIN_DHT
from utils.logger import logger

class TemperatureSensor:
    def __init__(self, pin=PIN_DHT):
        self.pin = pin
        self.type = "DHT22"

    def read(self):
        """Returns (temperature, humidity) tuple."""
        if MOCK_MODE:
            # Simulate realistic fluctuations
            temp = round(random.uniform(20.0, 25.0), 1)
            hum = round(random.uniform(40.0, 60.0), 1)
            logger.debug(f"Sensor [Temp]: Read {temp}°C, {hum}%")
            return temp, hum
        else:
            # Actual implementation would use Adafruit_DHT library
            # import Adafruit_DHT
            # humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, self.pin)
            return None, None
