import os

# --- General Settings ---
MOCK_MODE = False  # False = Raspberry Pi réel | True = simulation PC
LOOP_INTERVAL = 5  # Seconds

# --- MQTT Settings ---
MQTT_BROKER = "localhost"   # Broker Mosquitto local sur le Pi
MQTT_PORT = 1883
MQTT_USERNAME = None  # Add if needed
MQTT_PASSWORD = None
MQTT_CLIENT_ID = "smart_garden_raspberry_pi"

# --- Topics ---
TOPIC_PREFIX = "jardin"
TOPIC_SENSORS_TEMP  = f"{TOPIC_PREFIX}/sensors/temperature"
TOPIC_SENSORS_SOIL  = f"{TOPIC_PREFIX}/sensors/soil"
TOPIC_SENSORS_LIGHT = f"{TOPIC_PREFIX}/sensors/light"
TOPIC_SENSORS_WATER = f"{TOPIC_PREFIX}/sensors/water"   # niveau eau + pluie
TOPIC_ALERTS        = f"{TOPIC_PREFIX}/alerts"
TOPIC_COMMANDS_WATER = f"{TOPIC_PREFIX}/commands/water"
TOPIC_COMMANDS_LIGHT = f"{TOPIC_PREFIX}/commands/light"

# --- GPIO Pins (BCM Mode) ---
PIN_PUMP = 18       # Relais pompe → GPIO 18 (GPIO 17 réservé au capteur pluie)
PIN_GROW_LIGHT = 27
PIN_LED_GREEN = 16
PIN_LED_ORANGE = 6
PIN_LED_RED = 5
PIN_DHT = 4         # DHT11 → GPIO 4
RAIN_PIN = 17       # Capteur pluie numérique → GPIO 17
PIN_LDR_RC = 25     # LDR RC-timing → GPIO 25 (condensateur + résistance)

# --- ADC PCF8591 (I2C) ---
ADC_ADDRESS = 0x4B        # Adresse I2C du PCF8591
RAIN_ADC_CHANNEL = 0      # A0 → Pluie (analogique)
PIN_SOIL = 1              # A1 → Humidité du sol
PIN_LDR = 2               # A2 → Luminosité (si branché)

# --- Thresholds ---
SOIL_MOISTURE_LOW = 30  # %
SOIL_MOISTURE_HIGH = 60 # %

LIGHT_SCHEDULE_HIGH_START = 5   # 5h
LIGHT_SCHEDULE_MED_START = 12   # 12h
LIGHT_SCHEDULE_OFF_START = 17   # 17h
