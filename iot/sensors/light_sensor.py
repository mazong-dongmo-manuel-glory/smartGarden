import random
import time
from config import MOCK_MODE, PIN_LDR, PIN_LDR_RC, ADC_ADDRESS
from utils.logger import logger


class LightSensor:
    """
    Capteur de luminosité combiné :
      - Primaire  : ADC PCF8591 (I2C, 0x4B, canal A2) → lux approx.
      - Secondaire: RC-timing GPIO (PIN_LDR_RC = GPIO 25) → compte de charge.

    Câblage RC-timing :
        GPIO 25 ── résistance (ex. 10 kΩ) ── LDR ── GND
                                           └─ condensateur (ex. 1 µF) ── GND
    Plus la lumière est forte → LDR moins résistant → charge plus rapide → count plus bas.
    """

    # ── Seuils RC (à ajuster selon votre LDR / condensateur) ──────────────
    _RC_TOUCH_DELTA_ON  = 0.30   # +30 % au-dessus de la baseline → lumière faible
    _RC_TOUCH_DELTA_OFF = 0.15   # +15 % au-dessus de la baseline → hystérésis
    _RC_TIMEOUT_S       = 0.5    # Timeout max par mesure RC (s)
    _RC_AVG_N           = 10     # Nombre de lectures pour la moyenne
    _RC_AVG_DELAY       = 0.02   # Délai entre chaque lecture RC (s)

    def __init__(self, channel=PIN_LDR, address=ADC_ADDRESS, rc_pin=PIN_LDR_RC):
        self.channel = channel    # A2 → luminosité (ADC PCF8591)
        self.address = address    # 0x4B
        self.rc_pin  = rc_pin     # GPIO 25 (PIN_LDR_RC)
        self._bus    = None

        # État RC (auto-calibration au premier appel)
        self._rc_baseline    = None
        self._rc_threshold_on  = None
        self._rc_threshold_off = None
        self._rc_active      = False   # True si la lumière est jugée FAIBLE via RC

        if not MOCK_MODE:
            self._init_bus()

    # ── Initialisation ─────────────────────────────────────────────────────

    def _init_bus(self):
        try:
            import smbus
            self._bus = smbus.SMBus(1)
            logger.info(
                f"Sensor [Light]: SMBus initialisé "
                f"(adresse={hex(self.address)}, canal ADC={self.channel}, GPIO RC={self.rc_pin})"
            )
        except Exception as e:
            logger.error(f"Sensor [Light]: Impossible d'initialiser SMBus: {e}")

    # ── Lecture ADC (PCF8591, canal A2) ────────────────────────────────────

    def _read_adc(self):
        """Lit la valeur brute du canal ADC (0-255)."""
        command = 0x84 | (self.channel << 4)
        self._bus.write_byte(self.address, command)
        return self._bus.read_byte(self.address)

    # ── Méthode RC-timing ──────────────────────────────────────────────────

    def _rc_time(self, timeout_s=None):
        """
        Compte le temps de charge du condensateur via GPIO (RC-timing).
        Retourne un entier (plus élevé = charge plus lente = moins de lumière).
        """
        import RPi.GPIO as GPIO
        timeout_s = timeout_s or self._RC_TIMEOUT_S

        # Vider le condensateur
        GPIO.setup(self.rc_pin, GPIO.OUT)
        GPIO.output(self.rc_pin, GPIO.LOW)
        time.sleep(0.02)

        # Mesurer le temps de charge
        GPIO.setup(self.rc_pin, GPIO.IN)
        count = 0
        start = time.time()
        while GPIO.input(self.rc_pin) == GPIO.LOW:
            count += 1
            if time.time() - start > timeout_s:
                break
        return count

    def _rc_average(self, n=None, delay=None):
        """Retourne la moyenne de n lectures RC."""
        n     = n     or self._RC_AVG_N
        delay = delay or self._RC_AVG_DELAY
        total = 0
        for _ in range(n):
            total += self._rc_time()
            time.sleep(delay)
        return total / n

    def _rc_calibrate(self):
        """Auto-calibration : établit la baseline RC en conditions actuelles."""
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        logger.info(f"Sensor [Light RC]: Calibration sur GPIO {self.rc_pin} (2 s)…")
        time.sleep(2)
        self._rc_baseline = self._rc_average(n=15)
        self._rc_threshold_on  = self._rc_baseline * (1 + self._RC_TOUCH_DELTA_ON)
        self._rc_threshold_off = self._rc_baseline * (1 + self._RC_TOUCH_DELTA_OFF)
        logger.info(
            f"Sensor [Light RC]: baseline={self._rc_baseline:.1f}, "
            f"seuil_on={self._rc_threshold_on:.1f}, "
            f"seuil_off={self._rc_threshold_off:.1f}"
        )

    def read_rc_raw(self):
        """
        Retourne le compte RC brut et l'état (True = lumière faible / obscurité).
        Lance la calibration automatiquement au premier appel.
        """
        if self._rc_baseline is None:
            self._rc_calibrate()

        avg = self._rc_average()

        # Hystérésis
        if not self._rc_active and avg >= self._rc_threshold_on:
            self._rc_active = True
        elif self._rc_active and avg < self._rc_threshold_off:
            self._rc_active = False

        logger.debug(
            f"Sensor [Light RC]: GPIO={self.rc_pin}, count={avg:.1f}, "
            f"baseline={self._rc_baseline:.1f}, faible={'OUI' if self._rc_active else 'NON'}"
        )
        return avg, self._rc_active

    # ── Interface principale ───────────────────────────────────────────────

    def read(self):
        """
        Retourne l'intensité lumineuse en lux approx. (0-1000) via ADC.
        En mode réel, effectue aussi une lecture RC en parallèle (loguée).
        """
        if MOCK_MODE:
            lux = random.randint(100, 1000)
            logger.debug(f"Sensor [Light] (mock): {lux} lux")
            return lux

        try:
            # ── Lecture primaire : ADC PCF8591 ──
            raw = self._read_adc()
            lux = round((raw / 255.0) * 1000)
            logger.debug(f"Sensor [Light] ADC: raw={raw}, lux≈{lux}")

            # ── Lecture secondaire : RC-timing ──
            try:
                rc_count, low_light = self.read_rc_raw()
                if low_light:
                    logger.info(
                        f"Sensor [Light RC]: Lumière FAIBLE détectée "
                        f"(count={rc_count:.1f} ≥ seuil {self._rc_threshold_on:.1f})"
                    )
            except Exception as e_rc:
                logger.warning(f"Sensor [Light RC]: Lecture ignorée: {e_rc}")

            return lux

        except Exception as e:
            logger.error(f"Sensor [Light]: Erreur lecture ADC: {e}")
            return 0
