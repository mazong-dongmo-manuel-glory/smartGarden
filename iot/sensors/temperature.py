import random
from config import MOCK_MODE, PIN_DHT
from utils.logger import logger

class TemperatureSensor:
    """
    Capteur de température et d'humidité DHT11 via adafruit_dht.
    GPIO 4 (par défaut) en mode BCM.
    """
    def __init__(self, pin=PIN_DHT):
        self.pin = pin
        self.type = "DHT11"
        self._dht        = None
        self._last_temp   = None   # dernière valeur valide
        self._last_hum    = None
        self._fail_count  = 0
        if not MOCK_MODE:
            self._init_sensor()

    def _init_sensor(self):
        try:
            import board
            import adafruit_dht
            gpio_pin = getattr(board, f"D{self.pin}")
            self._dht = adafruit_dht.DHT11(gpio_pin)
            logger.info(f"Sensor [Temp/Hum]: DHT11 initialisé sur GPIO{self.pin}")
        except Exception as e:
            logger.error(f"Sensor [Temp/Hum]: Impossible d'initialiser DHT11: {e}")

    def read(self):
        """
        Retourne un tuple (température °C, humidité %).
        Retourne (None, None) en cas d'erreur de lecture.
        """
        if MOCK_MODE:
            temp = round(random.uniform(20.0, 35.0), 1)
            hum = round(random.uniform(40.0, 90.0), 1)
            logger.debug(f"Sensor [Temp/Hum] (mock): {temp}°C, {hum}%")
            return temp, hum
        else:
            # Jusqu'à 3 tentatives — le DHT11 rate souvent la 1ère lecture
            for attempt in range(3):
                try:
                    temperature = self._dht.temperature
                    humidity    = self._dht.humidity
                    if temperature is not None and humidity is not None:
                        self._last_temp  = temperature
                        self._last_hum   = humidity
                        self._fail_count = 0
                        logger.debug(f"Sensor [Temp/Hum]: {temperature}°C | {humidity}%")
                        return temperature, humidity
                    logger.warning(f"Sensor [Temp/Hum]: None (tentative {attempt+1}/3)")
                except RuntimeError as e:
                    logger.warning(f"Sensor [Temp/Hum]: RuntimeError tentative {attempt+1}/3: {e}")
                except Exception as e:
                    logger.error(f"Sensor [Temp/Hum]: Erreur inattendue: {e}")
                    break
                import time; time.sleep(0.5)

            # Toutes les tentatives échouent → réutiliser la dernière valeur connue
            self._fail_count += 1
            if self._last_temp is not None:
                logger.warning(f"Sensor [Temp/Hum]: Échec lecture ({self._fail_count}x) — valeur cachée utilisée")
                return self._last_temp, self._last_hum
            return None, None
