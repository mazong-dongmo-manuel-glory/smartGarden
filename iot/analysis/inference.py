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

    def check(self, temp, hum, soil, light, water_level):
        """
        Returns True if anomaly detected, False otherwise.
        ISOLATION FOREST: 1 for inliers (normal), -1 for outliers (anomaly).
        """
        if self.model is None:
            return False

        try:
            # Reshape for single sample prediction
            features = np.array([[temp, hum, soil, light, water_level]])
            prediction = self.model.predict(features)
            
            if prediction[0] == -1:
                return True
            return False
        except Exception as e:
            logger.error(f"Inference error: {e}")
            return False
