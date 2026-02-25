import random
from config import MOCK_MODE, PIN_SOIL, ADC_ADDRESS
from utils.logger import logger


class SoilMoistureSensor:
    """
    Capteur d'humidité du sol via ADC PCF8591 (I2C, adresse 0x4B).
    Canal A1 → humidité du sol.
    """

    def __init__(self, channel=PIN_SOIL, address=ADC_ADDRESS):
        self.channel = channel
        self.address = address
        self._bus = None
        if not MOCK_MODE:
            self._init_bus()

    def _init_bus(self):
        try:
            import smbus
            self._bus = smbus.SMBus(1)
            logger.info(f"Sensor [Soil]: SMBus initialisé (adresse={hex(self.address)}, canal A{self.channel})")
        except Exception as e:
            logger.error(f"Sensor [Soil]: Impossible d'initialiser SMBus: {e}")
            self._bus = None

    def _read_adc_raw(self):
        """
        Double lecture PCF8591 : la première retourne la valeur du cycle précédent.
        La deuxième retourne la valeur réelle du canal courant.
        """
        command = 0x84 | (self.channel << 4)
        self._bus.write_byte(self.address, command)
        self._bus.read_byte(self.address)          # lecture fantôme (stale)
        return self._bus.read_byte(self.address)   # valeur réelle

    def read(self):
        """
        Retourne le pourcentage d'humidité du sol (0-100%).
        ADC élevé → sol SEC → faible humidité.
        ADC faible → sol HUMIDE → humidité élevée.
        """
        if MOCK_MODE:
            moisture = round(random.uniform(20.0, 80.0), 1)
            logger.debug(f"Sensor [Soil] (mock): {moisture}%")
            return moisture

        if self._bus is None:
            logger.error("Sensor [Soil]: Bus I2C non disponible.")
            return 0

        try:
            raw = self._read_adc_raw()
            moisture = round((1 - raw / 255.0) * 100, 1)
            label = "🌵 SEC" if raw > 130 else "💧 HUMIDE"
            logger.debug(f"Sensor [Soil]: {label} | ADC={raw}, Humidité={moisture}%")
            return moisture
        except Exception as e:
            logger.error(f"Sensor [Soil]: Erreur de lecture: {e}")
            try:
                self._init_bus()
            except Exception:
                pass
            return 0
