import paho.mqtt.client as mqtt
import json
from config import (MQTT_BROKER, MQTT_PORT, MQTT_CLIENT_ID,
                    TOPIC_COMMANDS_WATER, TOPIC_COMMANDS_LIGHT,
                    TOPIC_SENSORS_TEMP, TOPIC_SENSORS_LIGHT, TOPIC_SENSORS_WATER,
                    TOPIC_ALERTS)
from utils.logger import logger


class MqttClient:
    def __init__(self, command_callback):
        try:
            self.client = mqtt.Client(
                callback_api_version=mqtt.CallbackAPIVersion.VERSION1,
                client_id=MQTT_CLIENT_ID
            )
        except AttributeError:
            self.client = mqtt.Client(client_id=MQTT_CLIENT_ID)

        self.client.on_connect    = self._on_connect
        self.client.on_message    = self._on_message
        self.client.on_disconnect = self._on_disconnect
        self.command_callback     = command_callback

    def connect(self):
        try:
            logger.info(f"MQTT: Connexion à {MQTT_BROKER}:{MQTT_PORT}…")
            from config import MQTT_USERNAME, MQTT_PASSWORD
            if MQTT_USERNAME and MQTT_PASSWORD:
                self.client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
            self.client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
            self.client.loop_start()
        except Exception as e:
            logger.error(f"MQTT: Connexion échouée — {e}")

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("MQTT: Connecté.")
            client.subscribe(TOPIC_COMMANDS_WATER)   # START/STOP_WATERING
            client.subscribe(TOPIC_COMMANDS_LIGHT)   # SET_INTENSITY
        else:
            logger.error(f"MQTT: code {rc}")

    def _on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logger.warning(f"MQTT: Déconnexion inattendue (rc={rc})")

    def _on_message(self, client, userdata, msg):
        try:
            self.command_callback(msg.topic, msg.payload.decode())
        except Exception as e:
            logger.error(f"MQTT: Erreur message — {e}")

    # ── Publication ────────────────────────────────────────────────────

    def publish_sensors(self, temp, hum, lux, is_dark, light_intensity, rain_pct, rain_digital, pump_on=False):
        self._publish(TOPIC_SENSORS_TEMP,  {"temperature": temp, "humidity": hum})
        self._publish(TOPIC_SENSORS_LIGHT, {"light": lux, "is_dark": is_dark, "intensity": light_intensity})
        self._publish(TOPIC_SENSORS_WATER, {
            "rain_pct":     rain_pct,
            "rain_digital": rain_digital,
            "pump_on":      pump_on,
        })

    def publish_alert(self, message, level="info"):
        self._publish(TOPIC_ALERTS, {"message": message, "level": level})

    def _publish(self, topic, data: dict):
        try:
            result = self.client.publish(topic, json.dumps(data), qos=0)
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                logger.warning(f"MQTT: Publish rc={result.rc} → {topic}")
            else:
                logger.debug(f"MQTT: → {topic}")
        except Exception as e:
            logger.error(f"MQTT: Publish error — {e}")
