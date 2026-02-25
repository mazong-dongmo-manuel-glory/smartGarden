import random
import time
from config import MOCK_MODE, PIN_LDR, PIN_LDR_RC, ADC_ADDRESS
from utils.logger import logger


class LightSensor:
    """
    Capteur de luminosité — deux méthodes complémentaires :

    1. ADC PCF8591 (I2C, 0x4B, canal A2) → lux approx. (0-1000)
       Utilisé pour publier la valeur numérique sur MQTT.

    2. RC-timing GPIO (PIN_LDR_RC = GPIO 25) → détection obscurité (bool)
       Logique identique au code de test de l'utilisateur :
         - Calibration unique au démarrage (calibrate_rc())
         - count augmente = plus sombre = is_dark = True
         - Hystérésis : +30 % baseline → ON, +15 % baseline → OFF
       Résultat utilisé par main.py pour activer la lampe de croissance.

    Câblage GPIO 25 :
        3.3V ── résistance (10 kΩ) ── nœud A ── LDR ── GND
                                       └─ condensateur (1 µF) ── GND
        GPIO 25 connecté au nœud A
    """

    # ── Seuils RC (identiques au code de test) ─────────────────────────
    _DELTA_ON  = 0.30   # +30 % baseline → obscurité → lampe ON
    _DELTA_OFF = 0.15   # +15 % baseline → retour à la lumière → lampe OFF (hystérésis)
    _RC_N      = 5      # moyennes rapides (5 lectures) dans la boucle principale
    _RC_N_CAL  = 15     # lectures pour la calibration (identique au test)
    _RC_DELAY  = 0.01   # délai entre lectures (s)
    _RC_TIMEOUT = 0.5   # timeout max par mesure (s)

    def __init__(self, channel=PIN_LDR, address=ADC_ADDRESS, rc_pin=PIN_LDR_RC):
        self.channel = channel
        self.address = address
        self.rc_pin  = rc_pin

        self._bus          = None
        self._rc_baseline  = None       # défini après calibrate_rc()
        self._threshold_on = None
        self._threshold_off= None
        self.is_dark       = False      # résultat mis à jour à chaque read()

        if not MOCK_MODE:
            self._init_bus()

    # ── I2C / ADC ──────────────────────────────────────────────────────

    def _init_bus(self):
        try:
            import smbus
            self._bus = smbus.SMBus(1)
            logger.info(f"Sensor [Light]: SMBus initialisé "
                        f"(adresse={hex(self.address)}, canal A{self.channel}, RC=GPIO{self.rc_pin})")
        except Exception as e:
            logger.error(f"Sensor [Light]: Impossible d'initialiser SMBus: {e}")
            self._bus = None

    def _read_adc_raw(self):
        """Double lecture PCF8591 pour éliminer le byte périmé."""
        command = 0x84 | (self.channel << 4)
        self._bus.write_byte(self.address, command)
        self._bus.read_byte(self.address)          # byte fantôme
        return self._bus.read_byte(self.address)   # valeur réelle

    # ── RC-timing ──────────────────────────────────────────────────────

    def _rc_measure(self):
        """Une mesure RC : retourne le nombre de cycles de charge."""
        import RPi.GPIO as GPIO

        # Vider le condensateur
        GPIO.setup(self.rc_pin, GPIO.OUT)
        GPIO.output(self.rc_pin, GPIO.LOW)
        time.sleep(0.02)

        # Compter le temps de charge
        GPIO.setup(self.rc_pin, GPIO.IN)
        count = 0
        start = time.time()
        while GPIO.input(self.rc_pin) == GPIO.LOW:
            count += 1
            if time.time() - start > self._RC_TIMEOUT:
                break
        return count

    def _rc_average(self, n, delay):
        total = sum(self._rc_measure() for _ in range(n))
        if delay > 0:
            time.sleep(delay * n)
        return total / n

    def calibrate_rc(self):
        """
        Calibration RC unique au démarrage — à appeler une fois en dehors
        de la boucle principale (bloque ~2 s).
        Identique à la séquence du code de test.
        """
        if MOCK_MODE:
            return

        import RPi.GPIO as GPIO
        logger.info(f"Sensor [Light RC]: Calibration sur GPIO {self.rc_pin} (2 s)…")
        time.sleep(2)

        self._rc_baseline   = self._rc_average(self._RC_N_CAL, delay=0.02)
        self._threshold_on  = self._rc_baseline * (1 + self._DELTA_ON)
        self._threshold_off = self._rc_baseline * (1 + self._DELTA_OFF)

        logger.info(f"Sensor [Light RC]: baseline={self._rc_baseline:.1f} | "
                    f"seuil_on={self._threshold_on:.1f} | "
                    f"seuil_off={self._threshold_off:.1f}")

    def _update_rc(self):
        """Mise à jour rapide (non-bloquante) de self.is_dark avec hystérésis."""
        if self._rc_baseline is None:
            return  # pas encore calibré

        value = self._rc_average(self._RC_N, delay=self._RC_DELAY)

        if not self.is_dark and value > self._threshold_on:
            self.is_dark = True
            logger.info(f"Sensor [Light RC]: 🌑 Obscurité détectée (count={value:.1f})")
        elif self.is_dark and value < self._threshold_off:
            self.is_dark = False
            logger.info(f"Sensor [Light RC]: ☀️  Lumière revenue (count={value:.1f})")

    # ── Interface publique ──────────────────────────────────────────────

    def read(self):
        """
        Retourne la luminosité en lux (0-1000) via ADC.
        Met aussi à jour self.is_dark via RC-timing.
        """
        if MOCK_MODE:
            lux = random.randint(100, 1000)
            self.is_dark = lux < 200   # simulation : sombre si < 200 lux
            logger.debug(f"Sensor [Light] (mock): {lux} lux, is_dark={self.is_dark}")
            return lux

        # Lecture ADC
        lux = 0
        if self._bus:
            try:
                raw = self._read_adc_raw()
                lux = round((raw / 255.0) * 1000)
                logger.debug(f"Sensor [Light] ADC: raw={raw} → {lux} lux")
            except Exception as e:
                logger.error(f"Sensor [Light]: Erreur ADC: {e}")
                try:
                    self._init_bus()
                except Exception:
                    pass

        # Lecture RC (non-bloquante si déjà calibré)
        try:
            self._update_rc()
        except Exception as e:
            logger.warning(f"Sensor [Light RC]: Erreur RC: {e}")

        return lux
