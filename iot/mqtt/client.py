import paho.mqtt.client as mqtt
import json
from config import MQTT_BROKER, MQTT_PORT, MQTT_CLIENT_ID, TOPIC_COMMANDS_WATER, TOPIC_COMMANDS_LIGHT, TOPIC_SENSORS_TEMP, TOPIC_SENSORS_SOIL, TOPIC_SENSORS_LIGHT, TOPIC_ALERTS
from utils.logger import logger

class MqttClient:
    def __init__(self, command_callback):
        self.client = mqtt.Client(client_id=MQTT_CLIENT_ID)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.command_callback = command_callback

    def connect(self):
        try:
            logger.info(f"MQTT: Connecting to {MQTT_BROKER}...")
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.client.loop_start()
        except Exception as e:
            logger.error(f"MQTT: Connection failed - {e}")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("MQTT: Connected successfully.")
            # Subscribe to command topics
            self.client.subscribe(TOPIC_COMMANDS_WATER)
            self.client.subscribe(TOPIC_COMMANDS_LIGHT)
            logger.info(f"MQTT: Subscribed to commands.")
        else:
            logger.error(f"MQTT: Connection failed with code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode()
            logger.info(f"MQTT: Received command [{msg.topic}]: {payload}")
            self.command_callback(msg.topic, payload)
        except Exception as e:
            logger.error(f"MQTT: Error processing message - {e}")

    def publish_sensors(self, temp, hum, soil, light):
        self._publish(TOPIC_SENSORS_TEMP, json.dumps({"temperature": temp, "humidity": hum}))
        self._publish(TOPIC_SENSORS_SOIL, json.dumps({"moisture": soil}))
        self._publish(TOPIC_SENSORS_LIGHT, json.dumps({"light": light}))

    def publish_alert(self, message, level="info"):
        self._publish(TOPIC_ALERTS, json.dumps({"message": message, "level": level}))

    def _publish(self, topic, payload):
        try:
            self.client.publish(topic, payload)
            logger.debug(f"MQTT: Published to {topic}")
        except Exception as e:
            logger.error(f"MQTT: Publish failed - {e}")
