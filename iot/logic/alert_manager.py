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

    def update(self, temp, hum, rain_pct, rain_digital, is_dark, has_anomaly=False):
        """
        rain_digital : 0 = pluie détectée, 1 = sec
        is_dark      : True = nuit → lampe allumée
        has_anomaly  : True = Erreur critique détectée par l'IA
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

        # ── Anomalie IA ──────────────────────────────────────────────
        if has_anomaly:
            self.leds.set('red', True)
            self.leds.set('green', False)
            self.leds.set('orange', False)
            self.lcd.display("ALERTE CRITIQUE", "Anomalie IA !")
            return

        # ── Pluie détectée ───────────────────────────────────────────
        if rain_pct < 150:                           # < 150 = Pluie (actif bas)
            self.leds.set('orange', True)
            self.leds.set('green', False)
            self.leds.set('red', False)
            self.lcd.display(
                f"T:{temp}C H:{int(hum)}%",
                f"Pluie: {int(rain_pct)}/255"
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

        import datetime
        current_time = datetime.datetime.now().strftime("%H:%M")
        night_label = "Nuit" if is_dark else "Jour"
        
        self.lcd.display(
            f"{current_time} T:{temp}C",
            f"H:{int(hum)}% {night_label}"
        )
