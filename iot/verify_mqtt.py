import paho.mqtt.client as mqtt
import json
import time

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC_SENSORS = "jardin/sensors/#"
TOPIC_COMMANDS = "jardin/commands/water"

def on_connect(client, userdata, flags, rc):
    print(f"VERIFIER: Connected to broker with result code {rc}")
    client.subscribe(TOPIC_SENSORS)
    print(f"VERIFIER: Subscribed to {TOPIC_SENSORS}")
    
    # Send a test command to the backend
    print("VERIFIER: Sending START_WATERING command...")
    command = {"command": "START_WATERING", "duration": 5}
    client.publish(TOPIC_COMMANDS, json.dumps(command))

def on_message(client, userdata, msg):
    print(f"VERIFIER: Received message on {msg.topic}: {msg.payload.decode()}")
    # If we receive sensor data, the backend is publishing!
    if "sensors" in msg.topic:
        print("VERIFIER: SUCCESS! Backend is sending sensor data.")
        client.disconnect()

client = mqtt.Client(protocol=mqtt.MQTTv311) # Force protocol version to be safe
client.on_connect = on_connect
client.on_message = on_message

print("VERIFIER: Connecting to MQTT broker...")
client.connect(BROKER, PORT, 60)
client.loop_forever()
