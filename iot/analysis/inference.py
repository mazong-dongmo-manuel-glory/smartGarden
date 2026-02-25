import joblib
import os
import numpy as np
from utils.logger import logger

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

class AnomalyDetector:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
                logger.info("AI Model loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load AI model: {e}")
        else:
            logger.warning("AI Model not found. Please run train_model.py first.")

    def check(self, temp, hum, rain, light, water_level=None):
        """
        Returns True if anomaly detected, False otherwise.
        Capteurs réels : temp, hum, rain_pct, light.
        water_level gardé pour compatibilité API (ignoré si None).
        """
        if self.model is None:
            return False

        # Ignorer si valeurs critiques manquantes
        if temp is None or hum is None:
            return False

        try:
            rain_val  = rain        if rain        is not None else 0
            light_val = light       if light       is not None else 0
            wl_val    = water_level if water_level is not None else 0
            features  = np.array([[temp, hum, rain_val, light_val, wl_val]])
            return self.model.predict(features)[0] == -1
        except Exception as e:
            logger.error(f"Inference error: {e}")
            return False
