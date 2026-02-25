import paho.mqtt.client as mqtt
import json
from config import (MQTT_BROKER, MQTT_PORT, MQTT_CLIENT_ID,
                    TOPIC_COMMANDS_WATER, TOPIC_COMMANDS_LIGHT,
                    TOPIC_SENSORS_TEMP, TOPIC_SENSORS_SOIL,
                    TOPIC_SENSORS_LIGHT, TOPIC_SENSORS_WATER, TOPIC_ALERTS)
from utils.logger import logger


class MqttClient:
    """
    Client MQTT pour le Raspberry Pi (paho-mqtt v1 et v2 compatibles).
    - Publie les données capteurs sur jardin/sensors/...
    - Reçoit les commandes sur jardin/commands/...
    """

    def __init__(self, command_callback):
        # Compatibilité paho-mqtt v1 (callback_api_version absent) et v2
        try:
            self.client = mqtt.Client(
                callback_api_version=mqtt.CallbackAPIVersion.VERSION1,
                client_id=MQTT_CLIENT_ID
            )
        except AttributeError:
            # paho-mqtt < 2.0
            self.client = mqtt.Client(client_id=MQTT_CLIENT_ID)

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        self.command_callback = command_callback

    def connect(self):
        try:
            logger.info(f"MQTT: Connexion à {MQTT_BROKER}:{MQTT_PORT}…")
            self.client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
            self.client.loop_start()
        except Exception as e:
            logger.error(f"MQTT: Connexion échouée — {e}")

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("MQTT: Connecté avec succès.")
            client.subscribe(TOPIC_COMMANDS_WATER)
            client.subscribe(TOPIC_COMMANDS_LIGHT)
            logger.info("MQTT: Abonné aux topics de commande.")
        else:
            logger.error(f"MQTT: Connexion refusée — code {rc}")

    def _on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logger.warning(f"MQTT: Déconnexion inattendue (code {rc}). Reconnexion auto…")

    def _on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode()
            logger.info(f"MQTT: Commande reçue [{msg.topic}]: {payload}")
            self.command_callback(msg.topic, payload)
        except Exception as e:
            logger.error(f"MQTT: Erreur traitement message — {e}")

    # ── Publication ────────────────────────────────────────────────────────

    def publish_sensors(self, temp, hum, soil, light, water_level=None, rain_level=None):
        """Publie un cycle complet de données capteurs."""
        self._publish(TOPIC_SENSORS_TEMP,  {"temperature": temp,  "humidity": hum})
        self._publish(TOPIC_SENSORS_SOIL,  {"moisture":    soil})
        self._publish(TOPIC_SENSORS_LIGHT, {"light":       light})
        self._publish(TOPIC_SENSORS_WATER, {"water_level": water_level, "rain": rain_level})

    def publish_alert(self, message, level="info"):
        self._publish(TOPIC_ALERTS, {"message": message, "level": level})

    def _publish(self, topic, data: dict):
        try:
            payload = json.dumps(data)
            result = self.client.publish(topic, payload, qos=0, retain=False)
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                logger.warning(f"MQTT: Publication échouée sur {topic} (rc={result.rc})")
            else:
                logger.debug(f"MQTT: Publié sur {topic}: {payload}")
        except Exception as e:
            logger.error(f"MQTT: Erreur publication sur {topic} — {e}")
