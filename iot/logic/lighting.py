import datetime
from config import LIGHT_SCHEDULE_HIGH_START, LIGHT_SCHEDULE_MED_START, LIGHT_SCHEDULE_OFF_START
from utils.logger import logger

class LightingManager:
    def __init__(self, grow_light):
        self.grow_light = grow_light

    def check(self):
        """
        Planning éclairage :
        - 5h → 17h : Jour → lumière naturelle → lampe OFF
        - 17h → 5h : Nuit → lampe ON (100%)
        """
        hour = __import__('datetime').datetime.now().hour

        intensity = 100 if (hour >= 17 or hour < 5) else 0
        mode      = "Nuit (ON)" if intensity == 100 else "Jour (OFF)"

        if self.grow_light.intensity != intensity:
            logger.info(f"Lighting: {hour}h → {mode} → {intensity}%")
            self.grow_light.set_intensity(intensity)
