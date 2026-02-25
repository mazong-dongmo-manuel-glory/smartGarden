import time
import sys
import json
from config import LOOP_INTERVAL, PIN_PUMP, PIN_GROW_LIGHT, PIN_LED_GREEN, PIN_LED_ORANGE, PIN_LED_RED
from utils.logger import logger

from sensors.temperature import TemperatureSensor
from sensors.soil_moisture import SoilMoistureSensor
from sensors.light_sensor import LightSensor
from sensors.water_level import WaterLevelSensor

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

    temp_sensor        = TemperatureSensor()
    soil_sensor        = SoilMoistureSensor()
    light_sensor       = LightSensor()
    water_level_sensor = WaterLevelSensor()

    pump       = Pump(PIN_PUMP)
    grow_light = GrowLight(PIN_GROW_LIGHT)
    leds       = Leds(PIN_LED_GREEN, PIN_LED_ORANGE, PIN_LED_RED)
    lcd        = Lcd()

    irrigation = IrrigationManager(pump)
    lighting   = LightingManager(grow_light)
    alerts     = AlertManager(leds, lcd)

    db               = DatabaseManager()
    anomaly_detector = AnomalyDetector()

    # --- MQTT ---
    def command_callback(topic, payload):
        try:
            data    = json.loads(payload)
            command = data.get('command')
            logger.info(f"Command received: {command}")

            if command == 'START_WATERING':
                irrigation.start_watering_manual(data.get('duration', 10))
            elif command == 'STOP_WATERING':
                irrigation.stop_watering_manual()
            elif command == 'SET_INTENSITY':
                grow_light.set_intensity(data.get('value', 0))
            elif command == 'EXPORT_DATA':
                db.export_to_csv()
        except Exception as e:
            logger.error(f"Failed to parse command: {e}")

    mqtt_client = MqttClient(command_callback)
    mqtt_client.connect()

    # Calibration RC (bloque ~2 s une seule fois)
    logger.info("Calibration RC lumière (2 s)…")
    light_sensor.calibrate_rc()

    logger.info("System Initialized. Starting Main Loop...")

    try:
        while True:
            temp, hum   = temp_sensor.read()
            moisture    = soil_sensor.read()
            light_level = light_sensor.read()
            water_level = water_level_sensor.read()

            logger.info(f"T:{temp}°C H:{hum}% Sol:{moisture}% Lux:{light_level} Eau:{water_level}%")

            db.save_reading(temp, hum, moisture, light_level, water_level)

            if anomaly_detector.check(temp, hum, moisture, light_level, water_level):
                logger.warning("Anomaly Detected!")
                mqtt_client.publish_alert("Anomalie détectée par IA", "error")
                leds.set('red', True)

            irrigation.check(moisture)

            if light_sensor.is_dark:
                if grow_light.intensity != 100:
                    logger.info("Obscurité RC → lampe ON")
                    grow_light.set_intensity(100)
            else:
                lighting.check()

            alert_msg = None
            if water_level is not None and water_level < 20:
                logger.warning("Niveau d'eau bas !")
                leds.set('orange', True)
                alert_msg = "Niveau d'eau bas"

            alerts.update(temp, hum, moisture, light_level)

            mqtt_client.publish_sensors(
                temp, hum, moisture, light_level,
                water_level=water_level,
                rain_level=water_level
            )
            if alert_msg:
                mqtt_client.publish_alert(alert_msg, "warning")

            time.sleep(LOOP_INTERVAL)

    except KeyboardInterrupt:
        logger.info("Arrêt…")
        pump.cleanup()
        grow_light.cleanup()
        leds.set('green', False)
        if not __import__('config').MOCK_MODE:
            try:
                import RPi.GPIO as GPIO
                GPIO.cleanup()
            except Exception:
                pass

if __name__ == "__main__":
    main()
