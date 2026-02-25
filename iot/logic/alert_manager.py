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
            #self.leds.set('red', True)
            self.leds.set('green', False)
            self.leds.set('orange', False)
            self.lcd.display("ALERTE CRITIQUE", "Anomalie IA !")
            return

        # ── Gestion de l'Humidité du Sol / Pluie ─────────────────────
        # Valeurs ADC: 255 = Sec, ~120 = Humide, < 80 = Trempé
        
        if rain_pct >= 150:
            # SEC -> ROUGE
            self.leds.set('red', True)
            self.leds.set('orange', False)
            self.leds.set('green', False)
            water_status_msg = "Alerte: Sec"
        elif rain_pct < 80:
            # TROP MOUILLÉ -> ORANGE (Avertissement)
            self.leds.set('red', False)
            self.leds.set('orange', True)
            self.leds.set('green', False)
            water_status_msg = "Alerte: Trempe"
        else:
            # MOYENNEMENT MOUILLÉ (80 à 149) -> VERT (Idéal)
            # Vérifier si l'humidité de l'air n'est pas trop critique pour gâcher le vert
            if hum > 85:
                self.leds.set('orange', True)
                self.leds.set('green', False)
                water_status_msg = "Warn: Air Humide"
            else:
                self.leds.set('red', False)
                self.leds.set('orange', False)
                self.leds.set('green', True)
                water_status_msg = "Sol: Parfait"

        import datetime
        current_time = datetime.datetime.now().strftime("%H:%M")
        
        self.lcd.display(
            f"{current_time} T:{temp}C",
            f"{water_status_msg}"
        )
