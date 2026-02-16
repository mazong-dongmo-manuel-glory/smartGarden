import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

# Define ranges for "Normal" behavior
NORMAL_RANGES = {
    'temperature': (20.0, 30.0),
    'humidity': (40.0, 60.0),
    'soil_moisture': (30.0, 70.0),
    'light_intensity': (0, 1000),
    'water_level': (20.0, 100.0)
}

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
DATA_PATH = os.path.join(os.path.dirname(__file__), 'training_data.csv')

def generate_synthetic_data(n_samples=1000, anomaly_fraction=0.05):
    """Generates a synthetic dataset with normal and anomalous data."""
    np.random.seed(42)
    
    n_anomalies = int(n_samples * anomaly_fraction)
    n_normal = n_samples - n_anomalies
    
    data = []
    
    # Generate Normal Data
    for _ in range(n_normal):
        sample = [
            np.random.uniform(*NORMAL_RANGES['temperature']),
            np.random.uniform(*NORMAL_RANGES['humidity']),
            np.random.uniform(*NORMAL_RANGES['soil_moisture']),
            np.random.uniform(*NORMAL_RANGES['light_intensity']),
            np.random.uniform(*NORMAL_RANGES['water_level'])
        ]
        data.append(sample)
        
    # Generate Anomalies (Extreme values)
    for _ in range(n_anomalies):
        # Randomly choose a feature to be anomalous
        feature_idx = np.random.randint(0, 5)
        sample = [
            np.random.uniform(*NORMAL_RANGES['temperature']),
            np.random.uniform(*NORMAL_RANGES['humidity']),
            np.random.uniform(*NORMAL_RANGES['soil_moisture']),
            np.random.uniform(*NORMAL_RANGES['light_intensity']),
            np.random.uniform(*NORMAL_RANGES['water_level'])
        ]
        
        # Make one feature extreme
        if feature_idx == 0: # Temp
            sample[0] = np.random.choice([np.random.uniform(35, 50), np.random.uniform(-5, 10)])
        elif feature_idx == 1: # Hum
            sample[1] = np.random.choice([np.random.uniform(0, 20), np.random.uniform(80, 100)])
        elif feature_idx == 2: # Soil
            sample[2] = np.random.choice([np.random.uniform(0, 10), np.random.uniform(90, 100)])
        elif feature_idx == 3: # Light
            sample[3] = np.random.uniform(2000, 5000) # Extreme light
        elif feature_idx == 4: # Water Level
            sample[4] = np.random.uniform(0, 10) # Empty tank
        
        data.append(sample)
    
    columns = ['temperature', 'humidity', 'soil_moisture', 'light_intensity', 'water_level']
    df = pd.DataFrame(data, columns=columns)
    return df

def train_model():
    print("Generating synthetic data...")
    df = generate_synthetic_data()
    
    # Save data for reference
    df.to_csv(DATA_PATH, index=False)
    print(f"Data saved to {DATA_PATH}")
    
    print("Training Isolation Forest...")
    # contamination is the expected proportion of outliers in the data set
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(df)
    
    # Save model
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_model()
