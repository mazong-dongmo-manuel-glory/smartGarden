import random
from config import MOCK_MODE, ADC_ADDRESS, RAIN_ADC_CHANNEL
from utils.logger import logger


class WaterLevelSensor:
    """
    Capteur de pluie — PCF8591 canal A0.
    Formule ADC identique au code de test : 0x84 | (channel << 4)
    Retourne la valeur brute 0-255 :
      < 80  → sec (vert)
      80-149 → pluie légère (jaune)
      >= 150 → forte pluie (rouge)
    GPIO 17 est réservé à la pompe — aucun GPIO numérique ici.
    """

    def __init__(self, adc_channel=RAIN_ADC_CHANNEL, address=ADC_ADDRESS):
        self.adc_channel = adc_channel
        self.address     = address
        self._bus        = None

        if not MOCK_MODE:
            self._init_hardware()

    def _init_hardware(self):
        try:
            import smbus
            self._bus = smbus.SMBus(1)
            logger.info(f"Sensor [Rain]: SMBus initialisé (A{self.adc_channel})")
        except Exception as e:
            logger.error(f"Sensor [Rain]: Impossible d'initialiser SMBus: {e}")

    def _read_adc_raw(self):
        """
        Formule identique au code de test :
          command = 0x84 | (channel << 4)
        Double-read pour vider le byte périmé (PCF8591).
        """
        command = 0x84 | (self.adc_channel << 4)
        self._bus.write_byte(self.address, command)
        self._bus.read_byte(self.address)           # byte périmé
        return self._bus.read_byte(self.address)    # valeur réelle (0-255)

    def _read_digital(self):
        """GPIO 17 = pompe → stub retourne 1 (sec)."""
        return 1

    def read(self):
        """Retourne la valeur brute ADC 0-255."""
        if MOCK_MODE:
            raw = random.randint(0, 255)
            logger.debug(f"Sensor [Rain] (mock): {raw}/255")
            return raw

        if not self._bus:
            return 0

        try:
            raw = self._read_adc_raw()
            label = "Sec" if raw >= 150 else ("Pluie légère" if raw >= 80 else "Forte pluie")
            logger.debug(f"Sensor [Rain]: {raw}/255 → {label}")
            return raw
        except Exception as e:
            logger.error(f"Sensor [Rain]: Erreur: {e}")
            try:
                self._init_hardware()
            except Exception:
                pass
            return 0
