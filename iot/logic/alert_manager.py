from config import SOIL_MOISTURE_LOW
from utils.logger import logger


class AlertManager:
    """
    Gère les LEDs et l'affichage LCD en fonction des lectures capteurs.
    Capteurs réels : DHT11 (temp/hum), pluie (ADC %), lumière (jour/nuit).
    """
    _FAIL_THRESHOLD = 5

    def __init__(self, leds, lcd):
        self.leds        = leds
        self.lcd         = lcd
        self._fail_count = 0

    def update(self, temp, hum, rain_pct, rain_digital, is_dark):
        """
        rain_digital : 0 = pluie détectée, 1 = sec
        is_dark      : True = nuit → lampe allumée
        """
        # ── Erreur capteur ────────────────────────────────────────────
        if temp is None or hum is None:
            self._fail_count += 1
            if self._fail_count >= self._FAIL_THRESHOLD:
                logger.error("Alert: DHT11 Failure!")
                self.leds.set('red', True)
                self.leds.set('green', False)
                self.leds.set('orange', False)
                self.lcd.display("ERROR", "E01: DHT11")
            return

        self._fail_count = 0

        # ── Pluie détectée ───────────────────────────────────────────
        if rain_digital == 0:                          # 0 = pluie (actif bas)
            self.leds.set('orange', True)
            self.leds.set('green', False)
            self.leds.set('red', False)
            self.lcd.display(
                f"T:{temp}C H:{int(hum)}%",
                f"Pluie {int(rain_pct)}%"
            )
            return

        # ── Humidité air élevée (risque champignons) ─────────────────
        if hum > 80:
            self.leds.set('orange', True)
            self.leds.set('green', False)
            self.leds.set('red', False)
            self.lcd.display(
                f"T:{temp}C H:{int(hum)}%",
                "Warn: Humidite"
            )
            return

        # ── Tout normal ───────────────────────────────────────────────
        self.leds.set('green', True)
        self.leds.set('orange', False)
        self.leds.set('red', False)

        night_label = "Nuit" if is_dark else "Jour"
        self.lcd.display(
            f"T:{temp}C H:{int(hum)}%",
            f"Lux:OK {night_label}"
        )
