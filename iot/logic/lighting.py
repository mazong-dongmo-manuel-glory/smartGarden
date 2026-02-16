import datetime
from config import LIGHT_SCHEDULE_HIGH_START, LIGHT_SCHEDULE_MED_START, LIGHT_SCHEDULE_OFF_START
from utils.logger import logger

class LightingManager:
    def __init__(self, grow_light):
        self.grow_light = grow_light

    def check(self):
        """
        Implements Schedule:
        - 5h - 12h: High Intensity (100%)
        - 12h - 17h: Medium Intensity (50%)
        - 17h - 5h: OFF (0%)
        """
        now = datetime.datetime.now()
        hour = now.hour

        intensity = 0
        
        if LIGHT_SCHEDULE_HIGH_START <= hour < LIGHT_SCHEDULE_MED_START:
            intensity = 100
            mode = "Morning (High)"
        elif LIGHT_SCHEDULE_MED_START <= hour < LIGHT_SCHEDULE_OFF_START:
            intensity = 50
            mode = "Afternoon (Medium)"
        else:
            intensity = 0
            mode = "Night (OFF)"

        current_intensity = self.grow_light.intensity
        if current_intensity != intensity:
            logger.info(f"Lighting: Time is {hour}h ({mode}). Setting light to {intensity}%.")
            self.grow_light.set_intensity(intensity)
