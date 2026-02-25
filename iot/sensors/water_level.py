import random
from config import MOCK_MODE, ADC_ADDRESS, RAIN_ADC_CHANNEL, RAIN_PIN
from utils.logger import logger

class WaterLevelSensor:
    """
    Capteur de pluie / niveau d'eau.
    - Lecture analogique via PCF8591 ADC (I2C, 0x4B), canal A0 → intensité de pluie.
    - Lecture numérique via RPi.GPIO, pin 17 → détection de pluie (0 = pluie).
    """
    def __init__(self, adc_channel=RAIN_ADC_CHANNEL, address=ADC_ADDRESS, digital_pin=RAIN_PIN):
        self.adc_channel = adc_channel
        self.address = address
        self.digital_pin = digital_pin
        self._bus = None
        if not MOCK_MODE:
            self._init_hardware()

    def _init_hardware(self):
        try:
            import smbus
            import RPi.GPIO as GPIO
            self._bus = smbus.SMBus(1)
            # GPIO.setmode déjà appelé par leds.py — pas besoin de le répéter
            GPIO.setup(self.digital_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            logger.info(f"Sensor [Rain]: SMBus + GPIO{self.digital_pin} initialisés")
        except Exception as e:
            logger.error(f"Sensor [Rain]: Impossible d'initialiser le matériel: {e}")

    def _read_adc(self):
        """Lit la valeur analogique brute du canal ADC (0-255)."""
        command = 0x84 | (self.adc_channel << 4)
        self._bus.write_byte(self.address, command)
        return self._bus.read_byte(self.address)

    def _read_digital(self):
        """Lit l'état numérique du capteur de pluie (0 = pluie détectée)."""
        import RPi.GPIO as GPIO
        return GPIO.input(self.digital_pin)

    def read(self):
        """
        Retourne un pourcentage d'eau / intensité de pluie (0-100%).
        0% = sec, 100% = saturation.
        """
        if MOCK_MODE:
            level = round(random.uniform(0.0, 100.0), 1)
            logger.debug(f"Sensor [Rain] (mock): {level}%")
            return level
        else:
            try:
                raw = self._read_adc()
                # Plus la valeur est élevée, plus il y a d'eau sur le capteur
                level = round((raw / 255.0) * 100, 1)
                digital_state = self._read_digital()
                if digital_state == 0:
                    logger.debug(f"Sensor [Rain]: 🌧️ Pluie détectée ! ADC={raw}, Niveau={level}%")
                else:
                    logger.debug(f"Sensor [Rain]: ☀️ Pas de pluie. ADC={raw}, Niveau={level}%")
                return level
            except Exception as e:
                logger.error(f"Sensor [Rain]: Erreur de lecture: {e}")
                return 0
