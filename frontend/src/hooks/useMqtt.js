import { useState, useEffect, useRef } from 'react';
import mqtt from 'mqtt';

const MQTT_BROKER = 'ws://172.16.206.37:9001'; // Broker Mosquitto local sur le Pi

export default function useMqtt() {
    const clientRef = useRef(null);
    const [isConnected, setIsConnected] = useState(false);
    const [sensorData, setSensorData] = useState({
        temperature: null,
        humidity: null,
        moisture: null,
        light: null,
        rain: null,   // ADC 0-255 from rain_sensor.py (jardin/sensors/rain)
        waterLevel: null,   // % from water_level.py (jardin/sensors/soil)
    });
    const [alerts, setAlerts] = useState([]);
    const [eventLog, setEventLog] = useState([]); // live MQTT events (max 20)

    // ── accumulate live chart data (last 20 readings) ───────────────────
    const [chartTemp, setChartTemp] = useState([]);
    const [chartMoisture, setChartMoisture] = useState([]);

    const pushChartPoint = (setter, value) => {
        if (value == null) return;
        const ts = new Date().toLocaleTimeString('fr-CA', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        setter(prev => [...prev, { time: ts, value }].slice(-20));
    };

    const addEvent = (topic, summary, type = 'info') => {
        const ts = new Date().toLocaleString('fr-CA', {
            day: '2-digit', month: '2-digit', year: 'numeric',
            hour: '2-digit', minute: '2-digit',
        });
        setEventLog(prev => [{ ts, topic, summary, type }, ...prev].slice(0, 20));
    };

    useEffect(() => {
        console.log('Connecting to MQTT broker…');
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
            addEvent('system', 'Connexion au broker MQTT établie', 'success');

            // Sensors
            mqttClient.subscribe('jardin/sensors/+', err => {
                if (!err) console.log('Subscribed to jardin/sensors/+');
            });
            // Alerts
            mqttClient.subscribe('jardin/alerts', err => {
                if (!err) console.log('Subscribed to jardin/alerts');
            });
        });

        mqttClient.on('message', (topic, message) => {
            const payload = message.toString();
            console.log(`[MQTT] ${topic}: ${payload}`);

            try {
                const data = JSON.parse(payload);

                if (topic === 'jardin/sensors/temperature') {
                    setSensorData(prev => ({ ...prev, temperature: data.temperature, humidity: data.humidity }));
                    pushChartPoint(setChartTemp, data.temperature);
                    addEvent(topic, `Temp ${data.temperature}°C | Hum ${data.humidity}%`, 'info');

                } else if (topic === 'jardin/sensors/soil') {
                    setSensorData(prev => ({ ...prev, moisture: data.moisture, waterLevel: data.water_level ?? null }));
                    pushChartPoint(setChartMoisture, data.moisture);
                    addEvent(topic, `Sol ${data.moisture}%`, 'info');

                } else if (topic === 'jardin/sensors/light') {
                    setSensorData(prev => ({ ...prev, light: data.light }));
                    addEvent(topic, `Lumière ${data.light} lux`, 'info');

                } else if (topic === 'jardin/sensors/rain') {
                    // Payload from rain_sensor.py: { rain: <ADC 0-255>, soil: <ADC 0-255> }
                    setSensorData(prev => ({
                        ...prev,
                        rain: data.rain ?? prev.rain,
                        moisture: data.soil != null ? data.soil : prev.moisture,
                    }));
                    const level = data.rain < 80 ? 'Pas de pluie' : data.rain < 150 ? 'Pluie légère' : 'Forte pluie';
                    addEvent(topic, `Pluie ADC=${data.rain} → ${level}`, data.rain >= 150 ? 'warning' : 'info');

                } else if (topic === 'jardin/alerts') {
                    setAlerts(prev => [data, ...prev].slice(0, 5));
                    addEvent(topic, data.message, data.level === 'error' ? 'error' : 'warning');
                }

            } catch (e) {
                console.error('Failed to parse MQTT message', e);
            }
        });

        mqttClient.on('error', err => {
            console.error('MQTT Error:', err);
            mqttClient.end();
        });

        mqttClient.on('close', () => {
            setIsConnected(false);
        });

        clientRef.current = mqttClient;

        return () => { mqttClient.end(); };
    }, []);

    // ── publish helpers ──────────────────────────────────────────────────
    const publishCommand = (topic, message) => {
        const c = clientRef.current;
        if (c && isConnected) {
            c.publish(topic, JSON.stringify(message));
            console.log(`[MQTT publish] ${topic}:`, message);
        } else {
            console.warn('MQTT not connected — command not sent');
        }
    };

    const startWatering = (duration = 10) =>
        publishCommand('jardin/commands/water', { command: 'START_WATERING', duration });

    const stopWatering = () =>
        publishCommand('jardin/commands/water', { command: 'STOP_WATERING' });

    const setLightIntensity = (value) =>
        publishCommand('jardin/commands/light', { command: 'SET_INTENSITY', value });

    return {
        isConnected,
        sensorData,
        alerts,
        eventLog,
        chartTemp,
        chartMoisture,
        publishCommand,
        startWatering,
        stopWatering,
        setLightIntensity,
    };
}
