import threading
from config import SOIL_MOISTURE_LOW, SOIL_MOISTURE_HIGH
from utils.logger import logger

class IrrigationManager:
    def __init__(self, pump):
        self.pump = pump
        self.is_watering = False
        self.manual_override = False

    def check(self, moisture_level):
        """
        Implements Hysteresis:
        - ON if moisture < LOW (30%)
        - OFF if moisture > HIGH (60%)
        - No change if in between
        """
        if self.manual_override:
            return  # Skip automatic check during manual operation

        if moisture_level is None:
            return

        if moisture_level < SOIL_MOISTURE_LOW:
            if not self.is_watering:
                logger.info(f"Irrigation: Soil too dry ({moisture_level}% < {SOIL_MOISTURE_LOW}%). Pump ON.")
                self.pump.on()
                self.is_watering = True
        
        elif moisture_level > SOIL_MOISTURE_HIGH:
            if self.is_watering:
                logger.info(f"Irrigation: Soil moist enough ({moisture_level}% > {SOIL_MOISTURE_HIGH}%). Pump OFF.")
                self.pump.off()
                self.is_watering = False
        
        else:
            # In hysteresis zone (deadband), maintain current state
            logger.debug(f"Irrigation: In range ({moisture_level}%). Pump remains {'ON' if self.is_watering else 'OFF'}.")

    def start_watering_manual(self, duration):
        """Starts watering for a specific duration in a separate thread."""
        if self.is_watering:
            logger.warning("Irrigation: Pump is already running.")
            return

        logger.info(f"Irrigation: Starting manual watering for {duration} seconds.")
        self.manual_override = True
        self.pump.on()
        self.is_watering = True

        # Non-blocking timer
        timer = threading.Timer(duration, self._stop_manual_watering)
        timer.start()

    def _stop_manual_watering(self):
        logger.info("Irrigation: Manual watering finished.")
        self.pump.off()
        self.is_watering = False
        self.manual_override = False
