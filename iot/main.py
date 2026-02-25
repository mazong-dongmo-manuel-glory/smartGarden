import time
import json
import threading
from config import (LOOP_INTERVAL, PIN_PUMP, PIN_GROW_LIGHT,
                    PIN_LED_GREEN, PIN_LED_ORANGE, PIN_LED_RED)
from utils.logger import logger

from sensors.temperature import TemperatureSensor
from sensors.light_sensor import LightSensor
from sensors.water_level import WaterLevelSensor   # = capteur pluie ADC A0 + GPIO 17

from actuators.pump import Pump
from actuators.grow_light import GrowLight
from actuators.leds import Leds
from actuators.lcd import Lcd
from utils.database import DatabaseManager
from analysis.inference import AnomalyDetector

from logic.lighting import LightingManager
from logic.alert_manager import AlertManager
from logic.irrigation import IrrigationManager

from mqtt.client import MqttClient


def main():
    logger.info("=== Smart Garden — Démarrage ===")

    # ── GPIO : mode global avant toute initialisation matérielle ──────
    if not __import__('config').MOCK_MODE:
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)   # éviter les warnings "already in use"
            logger.info("GPIO: mode BCM activé")
        except ImportError:
            pass   # non-Pi (dev)

    # ── Capteurs ───────────────────────────────────────────────────────
    temp_sensor  = TemperatureSensor()       # DHT11 → temp + humidité
    light_sensor = LightSensor()             # LDR ADC + RC → lux + is_dark
    rain_sensor  = WaterLevelSensor()        # Pluie ADC A0 + GPIO 17

    # ── Actionneurs ────────────────────────────────────────────────────
    pump       = Pump(PIN_PUMP)              # GPIO 18 (relais actif-LOW)
    grow_light = GrowLight(PIN_GROW_LIGHT)   # GPIO 22
    leds       = Leds(PIN_LED_GREEN, PIN_LED_ORANGE, PIN_LED_RED)
    lcd        = Lcd()

    # ── Logique ────────────────────────────────────────────────────────
    irrigation = IrrigationManager(pump)
    lighting   = LightingManager(grow_light)
    alerts     = AlertManager(leds, lcd)
    db         = DatabaseManager()
    anomaly    = AnomalyDetector()

    # ── MQTT ───────────────────────────────────────────────────────────
    def command_callback(topic, payload):
        try:
            data    = json.loads(payload)
            command = data.get('command')
            logger.info(f"[CMD] {command} {data}")

            if command == 'START_WATERING':
                duration = data.get('duration', 10)
                irrigation.start_watering_manual(duration)

            elif command == 'STOP_WATERING':
                irrigation.stop_watering_manual()

            elif command == 'SET_INTENSITY':
                # Force l'éclairage manuellement pour 1h (3600s)
                lighting.set_manual(data.get('value', 0), 3600)

        except Exception as e:
            logger.error(f"[CMD] Erreur: {e}")

    mqtt_client = MqttClient(command_callback)
    mqtt_client.connect()

    # ── Calibration RC lumière ─────────────────────────────────────────
    logger.info("Calibration RC lumière (2 s)…")
    light_sensor.calibrate_rc()

    logger.info("Boucle principale démarrée.")

    try:
        while True:
            # 1. Lire les capteurs
            temp, hum    = temp_sensor.read()
            lux          = light_sensor.read()       # met à jour is_dark
            rain_pct     = rain_sensor.read()        # 0-100 %
            rain_digital = rain_sensor._read_digital()  # 0=pluie, 1=sec

            logger.info(f"T:{temp}°C H:{hum}% Pluie:{rain_pct}% Lux:{lux} Nuit:{light_sensor.is_dark}")

            # 2. Éclairage
            if lighting.manual_override:
                pass # Mode manuel en cours, on ne touche à rien
            elif light_sensor.is_dark:
                if grow_light.intensity != 100:
                    grow_light.set_intensity(100)
            else:
                lighting.check()

            # 3. IA anomalie
            alert_msg = None
            if anomaly.check(temp, hum, rain_pct, lux):
                logger.warning("Anomalie IA détectée!")
                leds.set('red', True)
                alert_msg = {"message": "Anomalie IA détectée", "level": "error"}

            # 4. Pompe manuelle (auto-irrigation désactivée sans capteur de sol)
            #    irrigation.check() est gardé pour la commande manuelle via MQTT

            # 5. Alertes LEDs + LCD
            alerts.update(temp, hum, rain_pct, rain_digital, light_sensor.is_dark)

            # 6. Sauvegarde
            db.save_reading(temp, hum, rain_pct, lux, None)

            # 5. Publication MQTT
            mqtt_client.publish_sensors(
                temp=temp,         hum=hum,
                lux=lux,           is_dark=light_sensor.is_dark,
                light_intensity=grow_light.intensity,
                rain_pct=rain_pct, rain_digital=rain_digital,
                pump_on=pump.is_on
            )

            time.sleep(LOOP_INTERVAL)

    except KeyboardInterrupt:
        logger.info("Arrêt.")
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
