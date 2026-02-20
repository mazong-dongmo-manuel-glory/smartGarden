import random
from config import MOCK_MODE, PIN_LDR, ADC_ADDRESS
from utils.logger import logger

class LightSensor:
    """
    Capteur de luminosité via ADC PCF8591 (I2C, adresse 0x4B).
    Canal A2 → luminosité (LDR/photorésistance).
    """
    def __init__(self, channel=PIN_LDR, address=ADC_ADDRESS):
        self.channel = channel
        self.address = address
        self._bus = None
        if not MOCK_MODE:
            self._init_bus()

    def _init_bus(self):
        try:
            import smbus
            self._bus = smbus.SMBus(1)
            logger.info(f"Sensor [Light]: SMBus initialisé (adresse={hex(self.address)}, canal={self.channel})")
        except Exception as e:
            logger.error(f"Sensor [Light]: Impossible d'initialiser SMBus: {e}")

    def _read_adc(self):
        """Lit la valeur brute du canal ADC (0-255)."""
        command = 0x84 | (self.channel << 4)
        self._bus.write_byte(self.address, command)
        return self._bus.read_byte(self.address)

    def read(self):
        """
        Retourne l'intensité lumineuse en lux approximatif (0-1000).
        Valeur ADC élevée = plus de lumière.
        """
        if MOCK_MODE:
            lux = random.randint(100, 1000)
            logger.debug(f"Sensor [Light] (mock): {lux} lux")
            return lux
        else:
            try:
                raw = self._read_adc()
                # Conversion linéaire : 0-255 → 0-1000 lux (approximatif)
                lux = round((raw / 255.0) * 1000)
                logger.debug(f"Sensor [Light]: ADC={raw}, Luminosité≈{lux} lux")
                return lux
            except Exception as e:
                logger.error(f"Sensor [Light]: Erreur de lecture: {e}")
                return 0
