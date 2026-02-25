from config import MOCK_MODE
from utils.logger import logger


class Leds:
    """
    Contrôle trois LEDs (verte, orange, rouge) via GPIO BCM.
    Pins définies dans config.py : PIN_LED_GREEN=16, PIN_LED_ORANGE=6, PIN_LED_RED=5.
    """

    def __init__(self, pin_green, pin_orange, pin_red):
        self.pins  = {'green': pin_green, 'orange': pin_orange, 'red': pin_red}
        self.state = {'green': False, 'orange': False, 'red': False}

        if not MOCK_MODE:
            self._init_gpio()

    def _init_gpio(self):
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            for color, pin in self.pins.items():
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.LOW)   # OFF au démarrage
            logger.info(f"Actuator [LEDs]: GPIO initialisés "
                        f"(G={self.pins['green']}, O={self.pins['orange']}, R={self.pins['red']})")
        except Exception as e:
            logger.error(f"Actuator [LEDs]: Impossible d'initialiser GPIO: {e}")

    def set(self, color, state: bool):
        """Allume (True) ou éteint (False) une LED."""
        if color not in self.pins:
            logger.warning(f"Actuator [LEDs]: couleur inconnue '{color}'")
            return

        self.state[color] = state
        status = "ON" if state else "OFF"
        logger.info(f"Actuator [LED]: {color.upper()} → {status} (GPIO {self.pins[color]})")

        if not MOCK_MODE:
            try:
                import RPi.GPIO as GPIO
                GPIO.output(self.pins[color], GPIO.HIGH if state else GPIO.LOW)
            except Exception as e:
                logger.error(f"Actuator [LEDs]: Erreur GPIO set({color}, {state}): {e}")
