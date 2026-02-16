from config import MOCK_MODE
from utils.logger import logger

class Lcd:
    def __init__(self):
        pass

    def display(self, line1, line2=""):
        logger.info(f"Actuator [LCD]:\n  | {line1:<16} |\n  | {line2:<16} |")
        if not MOCK_MODE:
            # I2C LCD implementation
            pass
