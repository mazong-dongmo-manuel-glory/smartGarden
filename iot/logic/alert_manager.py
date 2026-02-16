from config import SOIL_MOISTURE_LOW
from utils.logger import logger

class AlertManager:
    def __init__(self, leds, lcd):
        self.leds = leds
        self.lcd = lcd

    def update(self, temp, humidity, moisture, light_level):
        """
        Updates LEDs based on sensor values.
        - Green: Todo OK
        - Orange: Warning (e.g. Low Water)
        - Red: Error (Sensor failure)
        """
        
        # Check for sensor errors (Red LED)
        if temp is None or humidity is None or moisture is None:
            logger.error("Alert: Sensor Failure! LED RED ON.")
            self.leds.set('red', True)
            self.leds.set('green', False)
            self.leds.set('orange', False)
            self.lcd.display("ERROR", "E01: Sensor")
            return

        # Check for warnings (Orange LED)
        if moisture < SOIL_MOISTURE_LOW:
            # Low water warning
            self.leds.set('orange', True)
            self.leds.set('green', False)
            self.leds.set('red', False)
            self.lcd.display(f"T:{temp}C H:{int(humidity)}%", "Warn: Low Water")
            return

        # All Normal (Green LED)
        self.leds.set('green', True)
        self.leds.set('orange', False)
        self.leds.set('red', False)
        self.lcd.display(f"T:{temp}C H:{int(humidity)}%", f"Soil:{int(moisture)}%")
