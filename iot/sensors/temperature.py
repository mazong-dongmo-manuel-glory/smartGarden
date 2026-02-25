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
        self._dht = None
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
            try:
                temperature = self._dht.temperature
                humidity = self._dht.humidity
                if temperature is not None and humidity is not None:
                    logger.debug(f"Sensor [Temp/Hum]: Température={temperature}°C | Humidité={humidity}%")
                    return temperature, humidity
                else:
                    logger.warning("Sensor [Temp/Hum]: Lecture invalide (None)")
                    return None, None
            except RuntimeError as e:
                # Les erreurs intermittentes sont normales avec les capteurs DHT
                logger.warning(f"Sensor [Temp/Hum]: Erreur de lecture (normale): {e}")
                return None, None
            except Exception as e:
                logger.error(f"Sensor [Temp/Hum]: Erreur inattendue: {e}")
                return None, None
