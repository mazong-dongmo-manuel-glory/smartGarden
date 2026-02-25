import random
import time
from config import MOCK_MODE, PIN_LDR, PIN_LDR_RC, ADC_ADDRESS
from utils.logger import logger


class LightSensor:
    """
    Capteur de luminosité — deux méthodes complémentaires:

    1. ADC PCF8591 (I2C, adresse 0x4B, canal A2 = PIN_LDR)
       → valeur lux approx. (0-1000) publiée sur MQTT.
       Commande correcte : 0x40 | channel

    2. RC-timing GPIO (PIN_LDR_RC = GPIO 27)
       → détection obscurité booléenne (is_dark).
       Si le circuit RC n'est pas branché (baseline ≈ 0),
       bascule automatiquement sur le seuil ADC (lux < 100 = nuit).

    Câblage GPIO 27 (RC) :
        3.3V ──▶ R 10kΩ ──┬── LDR ──▶ GND
                          ├── C 1µF ──▶ GND
                          └── GPIO 27
    """

    # ── Seuils RC ────────────────────────────────────────────────────
    _DELTA_ON    = 0.30   # +30 % baseline → obscurité
    _DELTA_OFF   = 0.15   # +15 % baseline → lumière (hystérésis)
    _RC_N        = 5      # lectures par cycle
    _RC_N_CAL    = 15     # lectures calibration
    _RC_DELAY    = 0.01
    _RC_TIMEOUT  = 0.5

    # ── Seuil ADC de secours (si RC non branché) ──────────────────
    _ADC_DARK_THRESHOLD = 100   # lux < 100 → nuit

    def __init__(self, channel=PIN_LDR, address=ADC_ADDRESS, rc_pin=PIN_LDR_RC):
        self.channel   = channel
        self.address   = address
        self.rc_pin    = rc_pin
        self.is_dark   = False

        self._bus           = None
        self._rc_calibrated = False   # True si baseline valide
        self._rc_baseline   = None
        self._threshold_on  = None
        self._threshold_off = None

        if not MOCK_MODE:
            self._init_bus()

    # ── I2C / ADC ─────────────────────────────────────────────────

    def _init_bus(self):
        try:
            import smbus
            self._bus = smbus.SMBus(1)
            logger.info(f"Sensor [Light]: SMBus OK (adresse={hex(self.address)}, canal A{self.channel})")
        except Exception as e:
            logger.error(f"Sensor [Light]: SMBus init failed: {e}")
            self._bus = None

    def _read_adc_raw(self):
        """
        Lecture correcte du PCF8591 :
        - Commande : 0x40 (activer sortie DAC) | numéro canal (0-3)
        - Double lecture : premier byte = valeur précédente (stale) → ignoré
        """
        command = 0x40 | (self.channel & 0x03)
        self._bus.write_byte(self.address, command)
        self._bus.read_byte(self.address)           # byte périmé
        return self._bus.read_byte(self.address)    # valeur réelle

    # ── RC-timing ─────────────────────────────────────────────────

    def _rc_measure(self):
        import RPi.GPIO as GPIO
        GPIO.setup(self.rc_pin, GPIO.OUT)
        GPIO.output(self.rc_pin, GPIO.LOW)
        time.sleep(0.02)
        GPIO.setup(self.rc_pin, GPIO.IN)
        count = 0
        start = time.time()
        while GPIO.input(self.rc_pin) == GPIO.LOW:
            count += 1
            if time.time() - start > self._RC_TIMEOUT:
                break
        return count

    def _rc_average(self, n):
        readings = []
        for _ in range(n):
            readings.append(self._rc_measure())
            time.sleep(self._RC_DELAY)
        return sum(readings) / len(readings)

    def calibrate_rc(self):
        """
        Calibration RC (bloque ~2 s, à appeler une fois avant la boucle).
        Si la baseline est trop faible (circuit non branché),
        désactive le RC et utilise le seuil ADC à la place.
        """
        if MOCK_MODE:
            return

        logger.info(f"Sensor [Light RC]: Calibration GPIO {self.rc_pin} (2 s)…")
        time.sleep(2)

        try:
            baseline = self._rc_average(self._RC_N_CAL)
        except Exception as e:
            logger.warning(f"Sensor [Light RC]: Calibration échouée ({e}) → mode ADC")
            return

        if baseline < 10:
            # Circuit RC absent ou court-circuit → bascule sur ADC
            logger.warning(
                f"Sensor [Light RC]: Baseline trop faible ({baseline:.1f}) "
                f"→ circuit RC probablement absent. Mode ADC activé."
            )
            self._rc_calibrated = False
            return

        self._rc_baseline   = baseline
        self._threshold_on  = baseline * (1 + self._DELTA_ON)
        self._threshold_off = baseline * (1 + self._DELTA_OFF)
        self._rc_calibrated = True

        logger.info(
            f"Sensor [Light RC]: baseline={baseline:.1f} | "
            f"ON>{self._threshold_on:.1f} | OFF<{self._threshold_off:.1f}"
        )

    def _update_is_dark_via_rc(self):
        """Met à jour is_dark via RC (avec hystérésis)."""
        value = self._rc_average(self._RC_N)
        if not self.is_dark and value > self._threshold_on:
            self.is_dark = True
            logger.info(f"Sensor [Light RC]: Nuit (count={value:.0f})")
        elif self.is_dark and value < self._threshold_off:
            self.is_dark = False
            logger.info(f"Sensor [Light RC]: Jour (count={value:.0f})")

    # ── Interface publique ─────────────────────────────────────────

    def read(self):
        """
        Retourne la luminosité en lux (ADC).
        Met à jour `is_dark` :
          - via RC-timing si calibré
          - via seuil ADC si RC non disponible
        """
        if MOCK_MODE:
            lux = random.randint(50, 1000)
            self.is_dark = lux < 200
            logger.debug(f"Sensor [Light] (mock): {lux} lux, is_dark={self.is_dark}")
            return lux

        # ── Lecture ADC ──
        lux = 0
        if self._bus:
            try:
                raw = self._read_adc_raw()
                lux = round((raw / 255.0) * 1000)
                logger.debug(f"Sensor [Light] ADC: raw={raw} → {lux} lux")
            except Exception as e:
                logger.error(f"Sensor [Light]: Erreur ADC: {e}")
                self._init_bus()

        # ── is_dark : RC ou ADC ──
        if self._rc_calibrated:
            try:
                self._update_is_dark_via_rc()
            except Exception as e:
                logger.warning(f"Sensor [Light RC]: Erreur: {e}")
                # Fallback ADC si RC crash
                self.is_dark = lux < self._ADC_DARK_THRESHOLD
        else:
            # Pas de RC → seuil ADC simple
            self.is_dark = lux < self._ADC_DARK_THRESHOLD

        return lux
