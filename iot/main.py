import time
import sys
import json
from config import LOOP_INTERVAL, PIN_PUMP, PIN_GROW_LIGHT, PIN_LED_GREEN, PIN_LED_ORANGE, PIN_LED_RED
from utils.logger import logger

# Import Components
from sensors.temperature import TemperatureSensor
from sensors.soil_moisture import SoilMoistureSensor
from sensors.light_sensor import LightSensor
from sensors.water_level import WaterLevelSensor # Bonus

from actuators.pump import Pump
from actuators.grow_light import GrowLight
from actuators.leds import Leds
from actuators.lcd import Lcd
from utils.database import DatabaseManager
from analysis.inference import AnomalyDetector

from logic.irrigation import IrrigationManager
from logic.lighting import LightingManager
from logic.alert_manager import AlertManager

from mqtt.client import MqttClient

def main():
    logger.info("Initializing Smart Garden IoT System...")

    # --- Hardware Initialization ---
    temp_sensor = TemperatureSensor()
    soil_sensor = SoilMoistureSensor()
    light_sensor = LightSensor()
    water_level_sensor = WaterLevelSensor() # Bonus
    
    pump = Pump(PIN_PUMP)
    grow_light = GrowLight(PIN_GROW_LIGHT)
    leds = Leds(PIN_LED_GREEN, PIN_LED_ORANGE, PIN_LED_RED)
    lcd = Lcd()

    # --- Logic Initialization ---
    irrigation = IrrigationManager(pump)
    lighting = LightingManager(grow_light)
    alerts = AlertManager(leds, lcd)
    
    # --- Database & AI Initialization ---
    db = DatabaseManager()
    anomaly_detector = AnomalyDetector()

    # --- MQTT Initialization ---
    def command_callback(topic, payload):
        """Handles incoming MQTT commands."""
        try:
            data = json.loads(payload)
            logger.info(f"Command received: {data}")
            
            command = data.get('command')
            
            if command == 'START_WATERING':
                duration = data.get('duration', 10)
                irrigation.start_watering_manual(duration)
                
            elif command == 'STOP_WATERING':
                irrigation.stop_watering_manual()

            elif command == 'SET_INTENSITY':
                value = data.get('value', 0)
                grow_light.set_intensity(value)

            elif command == 'EXPORT_DATA':
                success = db.export_to_csv()
                if success:
                    mqtt_client.publish_alert("Rapport généré avec succès!", "info")
                else:
                    mqtt_client.publish_alert("Erreur lors de la génération du rapport.", "error")
                
        except Exception as e:
            logger.error(f"Failed to parse command: {e}")

    mqtt_client = MqttClient(command_callback)
    mqtt_client.connect()

    logger.info("System Initialized. Starting Main Loop...")

    try:
        while True:
            # 1. Read Sensors
            temp, hum = temp_sensor.read()
            moisture = soil_sensor.read()
            light_level = light_sensor.read()
            water_level = water_level_sensor.read() # Bonus

            logger.info(f"--- Cycle Data ---")
            logger.info(f"Temp: {temp}°C, Hum: {hum}%, Soil: {moisture}%, Light: {light_level}lux, WaterLvl: {water_level}%")

            # 2. Save to Database
            db.save_reading(temp, hum, moisture, light_level, water_level)

            # 3. Anomaly Detection
            if anomaly_detector.check(temp, hum, moisture, light_level, water_level):
                logger.warning("Anomaly Detected by AI Model!")
                mqtt_client.publish_alert("Anomaly Detected!", "error")
                leds.set('red', True)

            # 4. Run Logic
            irrigation.check(moisture)
            lighting.check()
            
            # 5. Update Alerts (LEDs & LCD)
            # Add water level check to alerts
            if water_level < 20:
                logger.warning("Low Water Level!")
                leds.set('orange', True) # Warning
            
            alerts.update(temp, hum, moisture, light_level)

            # 6. MQTT Publish
            mqtt_client.publish_sensors(temp, hum, moisture, light_level)
            if water_level < 20:
                 mqtt_client.publish_alert("Low Water Level", "warning")

            time.sleep(LOOP_INTERVAL)

    except KeyboardInterrupt:
        logger.info("System stopping...")
        pump.cleanup()
        leds.set('green', False)
        # Nettoyage GPIO (capteur pluie numérique, etc.)
        if not __import__('config').MOCK_MODE:
            try:
                import RPi.GPIO as GPIO
                GPIO.cleanup()
                logger.info("GPIO nettoyé.")
            except Exception:
                pass

if __name__ == "__main__":
    main()
