import random
import time
from config import MOCK_MODE, PIN_LDR, ADC_ADDRESS
from utils.logger import logger


class LightSensor:
    """
    Capteur de luminosité via ADC PCF8591 (I2C, 0x4B, canal A2).
    Canal A2 → photorésistance (LDR).

    Valeur ADC élevée (0→255) = plus de lumière → lux approx. 0-1000.
    """

    def __init__(self, channel=PIN_LDR, address=ADC_ADDRESS):
        self.channel = channel   # A2 (PIN_LDR = 2)
        self.address = address   # 0x4B
        self._bus    = None

        if not MOCK_MODE:
            self._init_bus()

    # ── Initialisation ─────────────────────────────────────────────────

    def _init_bus(self):
        try:
            import smbus
            self._bus = smbus.SMBus(1)
            logger.info(
                f"Sensor [Light]: SMBus initialisé "
                f"(adresse={hex(self.address)}, canal ADC A{self.channel})"
            )
        except Exception as e:
            logger.error(f"Sensor [Light]: Impossible d'initialiser SMBus: {e}")
            self._bus = None

    # ── Lecture ADC PCF8591 ─────────────────────────────────────────────

    def _read_adc_raw(self):
        """Lit la valeur brute du canal ADC (0-255)."""
        command = 0x84 | (self.channel << 4)
        self._bus.write_byte(self.address, command)
        self._bus.read_byte(self.address)          # lecture fantôme (première donnée = précédente)
        return self._bus.read_byte(self.address)   # deuxième lecture = valeur réelle

    def read(self):
        """
        Retourne l'intensité lumineuse en lux approx. (0-1000).
        ADC élevé → plus de lumière → lux élevé.
        """
        if MOCK_MODE:
            lux = random.randint(100, 1000)
            logger.debug(f"Sensor [Light] (mock): {lux} lux")
            return lux

        if self._bus is None:
            logger.error("Sensor [Light]: Bus I2C non disponible.")
            return 0

        try:
            raw = self._read_adc_raw()
            lux = round((raw / 255.0) * 1000)
            logger.debug(f"Sensor [Light]: ADC raw={raw} → {lux} lux")
            return lux
        except Exception as e:
            logger.error(f"Sensor [Light]: Erreur de lecture ADC: {e}")
            # Tentative de réinitialisation du bus
            try:
                self._init_bus()
            except Exception:
                pass
            return 0
