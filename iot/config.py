import os

# --- General Settings ---
MOCK_MODE = True  # Set to False on actual Raspberry Pi
LOOP_INTERVAL = 5  # Seconds

# --- MQTT Settings ---
MQTT_BROKER = "test.mosquitto.org"  # Public test broker for now
MQTT_PORT = 1883
MQTT_USERNAME = None  # Add if needed
MQTT_PASSWORD = None
MQTT_CLIENT_ID = "smart_garden_raspberry_pi"

# --- Topics ---
TOPIC_PREFIX = "jardin"
TOPIC_SENSORS_TEMP = f"{TOPIC_PREFIX}/sensors/temperature"
TOPIC_SENSORS_SOIL = f"{TOPIC_PREFIX}/sensors/soil"
TOPIC_SENSORS_LIGHT = f"{TOPIC_PREFIX}/sensors/light"
TOPIC_ALERTS = f"{TOPIC_PREFIX}/alerts"
TOPIC_COMMANDS_WATER = f"{TOPIC_PREFIX}/commands/water"
TOPIC_COMMANDS_LIGHT = f"{TOPIC_PREFIX}/commands/light"

# --- GPIO Pins (BCM Mode) ---
PIN_PUMP = 17
PIN_GROW_LIGHT = 27
PIN_LED_GREEN = 22
PIN_LED_ORANGE = 23
PIN_LED_RED = 24
PIN_DHT = 4  # Temperature sensor
PIN_SOIL = 0  # ADC Channel 0 (requires MCP3008 usually, or digital pin)
PIN_LDR = 1   # ADC Channel 1

# --- Thresholds ---
SOIL_MOISTURE_LOW = 30  # %
SOIL_MOISTURE_HIGH = 60 # %

LIGHT_SCHEDULE_HIGH_START = 5   # 5h
LIGHT_SCHEDULE_MED_START = 12   # 12h
LIGHT_SCHEDULE_OFF_START = 17   # 17h
