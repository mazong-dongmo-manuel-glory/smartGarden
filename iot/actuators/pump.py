from config import MOCK_MODE
from utils.logger import logger

class Pump:
    def __init__(self, pin):
        self.pin = pin
        self.is_on = False

    def on(self):
        self.is_on = True
        logger.info(f"Actuator [Pump]: ON (Pin {self.pin})")
        if not MOCK_MODE:
            # GPIO.output(self.pin, GPIO.HIGH)
            pass

    def off(self):
        self.is_on = False
        logger.info(f"Actuator [Pump]: OFF (Pin {self.pin})")
        if not MOCK_MODE:
            # GPIO.output(self.pin, GPIO.LOW)
            pass
