from config import MOCK_MODE, PIN_PUMP
from utils.logger import logger


class Pump:
    """
    Contrôle la pompe via un relais sur GPIO 17 (PIN_PUMP).

    ⚠️  Relais actif-LOW :
        GPIO.LOW  → relais fermé → pompe ON
        GPIO.HIGH → relais ouvert → pompe OFF

    En mock mode, seul l'état interne est modifié.
    """

    def __init__(self, pin=PIN_PUMP):
        self.pin   = pin
        self.is_on = False
        if not MOCK_MODE:
            self._init_gpio()

    def _init_gpio(self):
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)
            GPIO.output(self.pin, GPIO.HIGH)   # Assure relais ouvert au démarrage (pompe OFF)
            logger.info(f"Actuator [Pump]: GPIO {self.pin} initialisé (relais actif-LOW)")
        except Exception as e:
            logger.error(f"Actuator [Pump]: Impossible d'initialiser GPIO {self.pin}: {e}")

    def on(self):
        """Active la pompe (ferme le relais : GPIO → LOW)."""
        self.is_on = True
        logger.info(f"Actuator [Pump]: ON  (GPIO {self.pin} → LOW)")
        if not MOCK_MODE:
            try:
                import RPi.GPIO as GPIO
                GPIO.output(self.pin, GPIO.LOW)   # Actif-LOW : LOW = relais ON
            except Exception as e:
                logger.error(f"Actuator [Pump]: Erreur GPIO on(): {e}")

    def off(self):
        """Éteint la pompe (ouvre le relais : GPIO → HIGH)."""
        self.is_on = False
        logger.info(f"Actuator [Pump]: OFF (GPIO {self.pin} → HIGH)")
        if not MOCK_MODE:
            try:
                import RPi.GPIO as GPIO
                GPIO.output(self.pin, GPIO.HIGH)  # Actif-LOW : HIGH = relais OFF
            except Exception as e:
                logger.error(f"Actuator [Pump]: Erreur GPIO off(): {e}")

    def cleanup(self):
        """Libère le GPIO (à appeler à l'arrêt du système)."""
        self.off()
        if not MOCK_MODE:
            try:
                import RPi.GPIO as GPIO
                GPIO.cleanup(self.pin)
                logger.info(f"Actuator [Pump]: GPIO {self.pin} libéré.")
            except Exception as e:
                logger.error(f"Actuator [Pump]: Erreur cleanup(): {e}")
