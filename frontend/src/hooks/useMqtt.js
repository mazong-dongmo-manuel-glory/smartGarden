import { useState, useEffect } from 'react';
import mqtt from 'mqtt';

const MQTT_BROKER = 'wss://test.mosquitto.org:8081'; // Secure WebSocket port
// const MQTT_BROKER = 'ws://test.mosquitto.org:8080'; // Unsecure WebSocket port (if SSL fails)

export default function useMqtt() {
    const [client, setClient] = useState(null);
    const [isConnected, setIsConnected] = useState(false);
    const [sensorData, setSensorData] = useState({
        temperature: 0,
        humidity: 0,
        moisture: 0,
        light: 0,
    });
    const [alerts, setAlerts] = useState([]);

    useEffect(() => {
        console.log('Connecting to MQTT broker...');
        const mqttClient = mqtt.connect(MQTT_BROKER, {
            clientId: `smart_garden_web_${Math.random().toString(16).substring(2, 8)}`,
            keepalive: 60,
            protocolId: 'MQTT',
            protocolVersion: 4,
            clean: true,
            reconnectPeriod: 1000,
            connectTimeout: 30 * 1000,
        });

        mqttClient.on('connect', () => {
            console.log('MQTT Connected');
            setIsConnected(true);

            // Subscribe to topics
            mqttClient.subscribe('jardin/sensors/+', (err) => {
                if (!err) console.log('Subscribed to sensors');
            });
            mqttClient.subscribe('jardin/alerts', (err) => {
                if (!err) console.log('Subscribed to alerts');
            });
        });

        mqttClient.on('message', (topic, message) => {
            const payload = message.toString();
            console.log(`Received message on ${topic}: ${payload}`);

            try {
                const data = JSON.parse(payload);

                if (topic.includes('temperature')) {
                    setSensorData(prev => ({ ...prev, temperature: data.temperature, humidity: data.humidity }));
                } else if (topic.includes('soil')) {
                    setSensorData(prev => ({ ...prev, moisture: data.moisture }));
                } else if (topic.includes('light')) {
                    setSensorData(prev => ({ ...prev, light: data.light }));
                } else if (topic.includes('alerts')) {
                    setAlerts(prev => [data, ...prev].slice(0, 5)); // Keep last 5 alerts
                }
            } catch (e) {
                console.error('Failed to parse MQTT message', e);
            }
        });

        mqttClient.on('error', (err) => {
            console.error('MQTT Connection Error: ', err);
            mqttClient.end();
        });

        setClient(mqttClient);

        return () => {
            if (mqttClient) {
                mqttClient.end();
            }
        };
    }, []);

    const publishCommand = (topic, message) => {
        if (client && isConnected) {
            client.publish(topic, JSON.stringify(message));
        }
    };

    return { isConnected, sensorData, alerts, publishCommand };
}
