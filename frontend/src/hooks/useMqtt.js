import { useState, useEffect, useRef } from 'react';
import mqtt from 'mqtt';

const MQTT_BROKER = 'ws://172.16.206.37:9090'; // Mosquitto WebSocket — port 9090

export default function useMqtt() {
    const clientRef = useRef(null);
    const [isConnected, setIsConnected] = useState(false);
    const [sensorData, setSensorData] = useState({
        temperature: null,
        humidity: null,
        moisture: null,
        light: null,
        rain: null,
        waterLevel: null,
    });
    const [alerts, setAlerts] = useState([]);
    const [eventLog, setEventLog] = useState([]);
    const [chartTemp, setChartTemp] = useState([]);
    const [chartMoisture, setChartMoisture] = useState([]);

    const addEvent = (topic, summary, type = 'info') => {
        const ts = new Date().toLocaleString('fr-CA', {
            day: '2-digit', month: '2-digit', year: 'numeric',
            hour: '2-digit', minute: '2-digit',
        });
        setEventLog(prev => [{ ts, topic, summary, type }, ...prev].slice(0, 20));
    };

    const pushChartPoint = (setter, value) => {
        if (value == null) return;
        const ts = new Date().toLocaleTimeString('fr-CA', {
            hour: '2-digit', minute: '2-digit', second: '2-digit',
        });
        setter(prev => [...prev, { time: ts, value }].slice(-20));
    };

    useEffect(() => {
        console.log(`[MQTT] Connexion à ${MQTT_BROKER}…`);

        const client = mqtt.connect(MQTT_BROKER, {
            clientId: `smart_garden_web_${Math.random().toString(16).slice(2, 8)}`,
            keepalive: 60,
            protocolId: 'MQTT',
            protocolVersion: 4,
            clean: true,
            reconnectPeriod: 3000,
            connectTimeout: 30_000,
        });

        client.on('connect', () => {
            console.log('[MQTT] Connecté sur', MQTT_BROKER);
            setIsConnected(true);
            addEvent('system', `Broker MQTT connecté (${MQTT_BROKER})`, 'success');

            client.subscribe('jardin/sensors/+');
            client.subscribe('jardin/alerts');
        });

        client.on('message', (topic, message) => {
            try {
                const data = JSON.parse(message.toString());
                console.log(`[MQTT] ${topic}:`, data);

                if (topic === 'jardin/sensors/temperature') {
                    setSensorData(prev => ({ ...prev, temperature: data.temperature, humidity: data.humidity }));
                    pushChartPoint(setChartTemp, data.temperature);
                    addEvent(topic, `Temp ${data.temperature}°C | Hum ${data.humidity}%`, 'info');

                } else if (topic === 'jardin/sensors/soil') {
                    setSensorData(prev => ({ ...prev, moisture: data.moisture }));
                    pushChartPoint(setChartMoisture, data.moisture);
                    addEvent(topic, `Sol ${data.moisture}%`, 'info');

                } else if (topic === 'jardin/sensors/light') {
                    setSensorData(prev => ({ ...prev, light: data.light }));
                    addEvent(topic, `Lumière ${data.light} lux`, 'info');

                } else if (topic === 'jardin/sensors/water') {
                    setSensorData(prev => ({
                        ...prev,
                        waterLevel: data.water_level,
                        rain: data.rain,
                    }));
                    addEvent(topic, `Eau ${data.water_level}% | Pluie ${data.rain}%`,
                        data.water_level < 20 ? 'warning' : 'info');

                } else if (topic === 'jardin/alerts') {
                    setAlerts(prev => [data, ...prev].slice(0, 5));
                    addEvent(topic, data.message, data.level === 'error' ? 'error' : 'warning');
                }
            } catch (e) {
                console.error('[MQTT] Parse error:', e);
            }
        });

        client.on('error', err => console.error('[MQTT] Erreur:', err));
        client.on('close', () => { setIsConnected(false); addEvent('system', 'Déconnecté', 'error'); });
        client.on('reconnect', () => console.log('[MQTT] Reconnexion…'));

        clientRef.current = client;
        return () => client.end();
    }, []); // eslint-disable-line react-hooks/exhaustive-deps

    // ── Commandes ─────────────────────────────────────────────────────
    const publishCommand = (topic, message) => {
        if (clientRef.current && isConnected) {
            clientRef.current.publish(topic, JSON.stringify(message));
        } else {
            console.warn('[MQTT] Non connecté — commande ignorée');
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
