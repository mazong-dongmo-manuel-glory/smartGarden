from config import MOCK_MODE, PIN_GROW_LIGHT
from utils.logger import logger


class GrowLight:
    """
    Lampe de croissance / LED sur GPIO 22 (PIN_GROW_LIGHT = LED_PIN du test).

    ON  = lampe allumée (GPIO HIGH)
    OFF = lampe éteinte (GPIO LOW)

    set_intensity() accepte 0-100 :
      - 0       → OFF
      - 1-100   → ON (seuil simple, sans PWM)
    """

    def __init__(self, pin=PIN_GROW_LIGHT):
        self.pin       = pin
        self.intensity = 0   # 0 = éteint, 100 = allumé
        self._gpio_ok  = False

        if not MOCK_MODE:
            self._init_gpio()

    def _init_gpio(self):
        try:
            import RPi.GPIO as GPIO
            # GPIO.setmode déjà appelé par leds.py
            GPIO.setup(self.pin, GPIO.OUT)
            GPIO.output(self.pin, GPIO.LOW)   # éteint au démarrage
            self._gpio_ok = True
            logger.info(f"Actuator [GrowLight]: GPIO {self.pin} initialisé (ON/OFF)")
        except Exception as e:
            logger.error(f"Actuator [GrowLight]: Impossible d'initialiser GPIO {self.pin}: {e}")

    def set_intensity(self, level: int):
        """
        Allume (level > 0) ou éteint (level == 0) la lampe.
        level = 0-100.
        """
        level = max(0, min(100, int(level)))
        self.intensity = level
        state = level > 0
        logger.info(f"Actuator [GrowLight]: {'ON' if state else 'OFF'} (level={level}%, GPIO {self.pin})")

        if not MOCK_MODE and self._gpio_ok:
            try:
                import RPi.GPIO as GPIO
                GPIO.output(self.pin, GPIO.HIGH if state else GPIO.LOW)
            except Exception as e:
                logger.error(f"Actuator [GrowLight]: Erreur GPIO: {e}")

    def cleanup(self):
        self.set_intensity(0)
        if not MOCK_MODE and self._gpio_ok:
            try:
                import RPi.GPIO as GPIO
                GPIO.cleanup(self.pin)
                logger.info(f"Actuator [GrowLight]: GPIO {self.pin} libéré.")
            except Exception as e:
                logger.error(f"Actuator [GrowLight]: Erreur cleanup: {e}")
