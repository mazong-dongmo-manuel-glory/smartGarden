from config import MOCK_MODE, PIN_GROW_LIGHT
from utils.logger import logger


class GrowLight:
    """
    Lampe de croissance contrôlée via PWM sur GPIO 27 (PIN_GROW_LIGHT).
    Intensité : 0% = éteint, 100% = pleine puissance.
    """
    PWM_FREQ = 100  # Hz

    def __init__(self, pin=PIN_GROW_LIGHT):
        self.pin       = pin
        self.intensity = 0
        self._pwm      = None

        if not MOCK_MODE:
            self._init_gpio()

    def _init_gpio(self):
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)
            self._pwm = GPIO.PWM(self.pin, self.PWM_FREQ)
            self._pwm.start(0)  # éteint au démarrage
            logger.info(f"Actuator [GrowLight]: PWM initialisé sur GPIO {self.pin} ({self.PWM_FREQ} Hz)")
        except Exception as e:
            logger.error(f"Actuator [GrowLight]: Impossible d'initialiser PWM GPIO {self.pin}: {e}")
            self._pwm = None

    def set_intensity(self, level: int):
        """Définit l'intensité lumineuse (0-100%)."""
        level = max(0, min(100, int(level)))
        self.intensity = level
        logger.info(f"Actuator [GrowLight]: Intensité → {level}% (GPIO {self.pin})")

        if not MOCK_MODE:
            if self._pwm:
                try:
                    self._pwm.ChangeDutyCycle(level)
                except Exception as e:
                    logger.error(f"Actuator [GrowLight]: Erreur PWM ChangeDutyCycle: {e}")
            else:
                logger.warning("Actuator [GrowLight]: PWM non initialisé, commande ignorée.")

    def cleanup(self):
        """Arrête le PWM proprement."""
        self.set_intensity(0)
        if not MOCK_MODE and self._pwm:
            try:
                self._pwm.stop()
                logger.info("Actuator [GrowLight]: PWM arrêté.")
            except Exception as e:
                logger.error(f"Actuator [GrowLight]: Erreur cleanup: {e}")
