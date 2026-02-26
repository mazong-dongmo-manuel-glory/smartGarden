import datetime
import threading
from config import LIGHT_SCHEDULE_HIGH_START, LIGHT_SCHEDULE_MED_START, LIGHT_SCHEDULE_OFF_START
from utils.logger import logger

class LightingManager:
    def __init__(self, grow_light):
        self.grow_light = grow_light
        self.manual_override = False
        self._timer = None

    def set_manual(self, intensity, duration=3600):
        """Active l'éclairage manuel pour une durée (défaut: 1 heure)."""
        logger.info(f"Lighting: Commande manuelle reçue → {intensity}% pour {duration}s")
        self.manual_override = True
        self.grow_light.set_intensity(intensity)

        if self._timer:
            self._timer.cancel()
        self._timer = threading.Timer(duration, self._clear_manual)
        self._timer.start()

    def _clear_manual(self):
        logger.info("Lighting: Fin de la dérogation manuelle. Retour au mode Auto.")
        self.manual_override = False
        self.check() # forcer la mise à jour immédiate

    def check(self):
        if self.manual_override:
            return  # Ignorer le planning automatique si forcé manuellement

        """
        Planning éclairage automatique :
        - 5h → 12h : Matin (Intense) → lampe ON (100%)
        - 12h → 17h : Après-midi (Modéré) → lampe ON (50%)
        - 17h → 5h : Nuit (OFF) → lampe OFF (0%)
        """
        hour = datetime.datetime.now().hour

        if 5 <= hour < 12:
            intensity = 
            mode = "Matin (Intense)"
        elif 12 <= hour < 17:
            intensity = 75
            mode = "Après-midi (Modéré)"
        else:
            intensity = 0
            mode = "Nuit (OFF)"

        if self.grow_light.intensity != intensity:
            logger.info(f"Lighting: {hour}h → {mode} → {intensity}%")
            self.grow_light.set_intensity(intensity)

