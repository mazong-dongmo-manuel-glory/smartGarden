import { useState, useEffect, useRef } from 'react';
import mqtt from 'mqtt';

const MQTT_BROKER = 'ws://172.16.206.37:9090';

export default function useMqtt() {
    const clientRef = useRef(null);
    const [isConnected, setIsConnected] = useState(false);
    const [sensorData, setSensorData] = useState({
        temperature: null,
        humidity: null,
        light: null,   // lux ADC
        isDark: null,   // bool RC
        rainPct: null,   // % analogique
        rainDigital: null,   // 0=pluie, 1=sec
    });
    const [alerts, setAlerts] = useState([]);
    const [eventLog, setEventLog] = useState([]);
    const [chartTemp, setChartTemp] = useState([]);
    const [chartHum, setChartHum] = useState([]);

    const addEvent = (topic, summary, type = 'info') => {
        const ts = new Date().toLocaleString('fr-CA', {
            day: '2-digit', month: '2-digit', year: 'numeric',
            hour: '2-digit', minute: '2-digit',
        });
        setEventLog(prev => [{ ts, topic, summary, type }, ...prev].slice(0, 20));
    };

    const pushPoint = (setter, value) => {
        if (value == null) return;
        const ts = new Date().toLocaleTimeString('fr-CA', {
            hour: '2-digit', minute: '2-digit', second: '2-digit',
        });
        setter(prev => [...prev, { time: ts, value }].slice(-20));
    };

    useEffect(() => {
        const client = mqtt.connect(MQTT_BROKER, {
            clientId: `sgarden_${Math.random().toString(16).slice(2, 8)}`,
            keepalive: 60,
            protocolVersion: 4,
            clean: true,
            reconnectPeriod: 1000,
            connectTimeout: 30_000,
        });

        client.on('connect', () => {
            setIsConnected(true);
            addEvent('system', `Connecté au broker MQTT (${MQTT_BROKER})`, 'success');
            client.subscribe('jardin/sensors/+');
            client.subscribe('jardin/alerts');
        });

        client.on('message', (topic, message) => {
            try {
                const data = JSON.parse(message.toString());

                if (topic === 'jardin/sensors/temperature') {
                    setSensorData(prev => ({ ...prev, temperature: data.temperature, humidity: data.humidity }));
                    pushPoint(setChartTemp, data.temperature);
                    pushPoint(setChartHum, data.humidity);
                    addEvent(topic, `T:${data.temperature}°C | H:${data.humidity}%`);

                } else if (topic === 'jardin/sensors/light') {
                    setSensorData(prev => ({ ...prev, light: data.light, isDark: data.is_dark }));
                    addEvent(topic, `${data.light} lux | ${data.is_dark ? 'Nuit 🌙' : 'Jour ☀️'}`);

                } else if (topic === 'jardin/sensors/water') {
                    setSensorData(prev => ({
                        ...prev,
                        rainPct: data.rain_pct,
                        rainDigital: data.rain_digital,
                    }));
                    const label = data.rain_digital === 0 ? '🌧️ Pluie détectée' : '☀️ Sec';
                    addEvent(topic, `${data.rain_pct}% | ${label}`,
                        data.rain_digital === 0 ? 'warning' : 'info');

                } else if (topic === 'jardin/alerts') {
                    setAlerts(prev => [data, ...prev].slice(0, 5));
                    addEvent(topic, data.message, data.level === 'error' ? 'error' : 'warning');
                }
            } catch (e) {
                console.error('[MQTT] Parse error:', e);
            }
        });

        client.on('error', err => console.error('[MQTT]', err));
        client.on('close', () => { setIsConnected(false); addEvent('system', 'Déconnecté', 'error'); });
        client.on('reconnect', () => console.log('[MQTT] Reconnexion…'));

        clientRef.current = client;
        return () => client.end();
    }, []); // eslint-disable-line

    const publishCommand = (topic, message) => {
        if (clientRef.current && isConnected)
            clientRef.current.publish(topic, JSON.stringify(message));
    };

    const setLightIntensity = (value) =>
        publishCommand('jardin/commands/light', { command: 'SET_INTENSITY', value });

    // Pompe non disponible — stub pour compatibilité SettingPage
    const startWatering = () => console.warn('Pompe non disponible');
    const stopWatering = () => console.warn('Pompe non disponible');

    return {
        isConnected, sensorData, alerts, eventLog,
        chartTemp, chartMoisture: chartHum,
        publishCommand, startWatering, stopWatering, setLightIntensity,
    };
}
