import random
from config import MOCK_MODE, PIN_SOIL, ADC_ADDRESS
from utils.logger import logger

class SoilMoistureSensor:
    """
    Capteur d'humidité du sol via ADC PCF8591 (I2C, adresse 0x4B).
    Canal A1 → humidité du sol.
    """
    def __init__(self, channel=PIN_SOIL, address=ADC_ADDRESS):
        self.channel = channel   # Canal ADC (A1)
        self.address = address   # Adresse I2C du PCF8591 (0x4B)
        self._bus = None
        if not MOCK_MODE:
            self._init_bus()

    def _init_bus(self):
        try:
            import smbus
            self._bus = smbus.SMBus(1)
            logger.info(f"Sensor [Soil]: SMBus initialisé (adresse={hex(self.address)}, canal={self.channel})")
        except Exception as e:
            logger.error(f"Sensor [Soil]: Impossible d'initialiser SMBus: {e}")

    def _read_adc(self):
        """Lit la valeur brute du canal ADC (0-255)."""
        command = 0x84 | (self.channel << 4)
        self._bus.write_byte(self.address, command)
        return self._bus.read_byte(self.address)

    def read(self):
        """
        Retourne le pourcentage d'humidité du sol (0-100%).
        Valeur ADC élevée = sol SEC (>130 ≈ sec), faible = sol HUMIDE.
        """
        if MOCK_MODE:
            moisture = round(random.uniform(20.0, 80.0), 1)
            logger.debug(f"Sensor [Soil] (mock): {moisture}%")
            return moisture
        else:
            try:
                raw = self._read_adc()
                # Conversion : 0 = très humide (100%), 255 = très sec (0%)
                moisture = round((1 - raw / 255.0) * 100, 1)
                if raw > 130:
                    logger.debug(f"Sensor [Soil]: 🌵 SOL SEC | Valeur ADC={raw}, Humidité={moisture}%")
                else:
                    logger.debug(f"Sensor [Soil]: 💧 SOL HUMIDE | Valeur ADC={raw}, Humidité={moisture}%")
                return moisture
            except Exception as e:
                logger.error(f"Sensor [Soil]: Erreur de lecture: {e}")
                return 0
