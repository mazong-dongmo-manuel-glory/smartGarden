from config import MOCK_MODE, PIN_GROW_LIGHT
from utils.logger import logger


class GrowLight:
    """
    Lampe de croissance / LED sur GPIO 22 (PIN_GROW_LIGHT = LED_PIN du test).

    ON  = lampe allumée (PWM)
    OFF = lampe éteinte (PWM 0%)

    set_intensity() accepte 0-100 :
      - 0       → OFF
      - 1-100   → PWM avec duty cycle correspondant
    """

    def __init__(self, pin=PIN_GROW_LIGHT):
        self.pin       = pin
        self.intensity = 0   # 0 = éteint, 100 = allumé
        self._gpio_ok  = False
        self._pwm      = None

        if not MOCK_MODE:
            self._init_gpio()

    def _init_gpio(self):
        try:
            import RPi.GPIO as GPIO
            # GPIO.setmode déjà appelé par leds.py
            GPIO.setup(self.pin, GPIO.OUT)
            self._pwm = GPIO.PWM(self.pin, 1000)  # 1kHz PWM
            self._pwm.start(0)  # 0% au démarrage
            self._gpio_ok = True
            logger.info(f"Actuator [GrowLight]: GPIO {self.pin} initialisé (PWM)")
        except Exception as e:
            logger.error(f"Actuator [GrowLight]: Impossible d'initialiser GPIO {self.pin}: {e}")

    def set_intensity(self, level: int):
        """
        Définit l'intensité de la lampe.
        level = 0-100.
        """
        level = max(0, min(100, int(level)))
        self.intensity = level
        logger.info(f"Actuator [GrowLight]: PWM (level={level}%, GPIO {self.pin})")

        if not MOCK_MODE and self._gpio_ok and self._pwm:
            try:
                self._pwm.ChangeDutyCycle(level)
            except Exception as e:
                logger.error(f"Actuator [GrowLight]: Erreur PWM: {e}")

    def cleanup(self):
        self.set_intensity(0)
        if not MOCK_MODE and self._gpio_ok:
            try:
                if self._pwm:
                    self._pwm.stop()
                import RPi.GPIO as GPIO
                GPIO.cleanup(self.pin)
                logger.info(f"Actuator [GrowLight]: GPIO {self.pin} libéré.")
            except Exception as e:
                logger.error(f"Actuator [GrowLight]: Erreur cleanup: {e}")
