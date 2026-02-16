from config import MOCK_MODE
from utils.logger import logger

class Leds:
    def __init__(self, pin_green, pin_orange, pin_red):
        self.pins = {'green': pin_green, 'orange': pin_orange, 'red': pin_red}
        self.state = {'green': False, 'orange': False, 'red': False}

    def set(self, color, state):
        if color in self.pins:
            self.state[color] = state
            status = "ON" if state else "OFF"
            logger.info(f"Actuator [LED]: {color.upper()} -> {status}")
            if not MOCK_MODE:
                # GPIO.output(self.pins[color], state)
                pass
