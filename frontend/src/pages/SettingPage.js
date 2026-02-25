import React, { useState } from 'react';
import Layout from '../components/Layout';
import useMqtt from '../hooks/useMqtt';

export default function SettingPage() {
    const [notifications, setNotifications] = useState(true);
    const [autoMode, setAutoMode] = useState(true);
    const [duration, setDuration] = useState(10);   // watering duration (s)
    const [isPumping, setIsPumping] = useState(false);

    const { isConnected, sensorData, startWatering, stopWatering, setLightIntensity } = useMqtt();

    const handleStart = () => {
        startWatering(duration);
        setIsPumping(true);
    };

    const handleStop = () => {
        stopWatering();
        setIsPumping(false);
    };

    // Light intensity fallback to 0 if not yet received
    const currentIntensity = sensorData.lightIntensity || 0;

    const lightLevels = [
        { label: 'Matin', sublabel: 'Intense', value: 100, icon: 'fa-sun', active: currentIntensity === 100 },
        { label: 'Après-midi', sublabel: 'Modéré', value: 50, icon: 'fa-cloud-sun', active: currentIntensity === 50 },
        { label: 'Nuit', sublabel: 'OFF', value: 0, icon: 'fa-moon', active: currentIntensity === 0 },
    ];

    return (
        <Layout>
            <h2 className="text-2xl font-bold mb-6">Paramètres &amp; Contrôles</h2>

            {/* MQTT connection badge */}
            <div className={`inline-flex items-center gap-2 mb-6 px-3 py-1 rounded-full text-xs font-medium ${isConnected ? 'bg-green-500/10 text-green-400' : 'bg-red-500/10 text-red-400'}`}>
                <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
                {isConnected ? 'MQTT connecté — commandes actives' : 'MQTT déconnecté — commandes désactivées'}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                {/* ── Lighting Control ── */}
                <div id="lighting-control" className="bg-gray-900 rounded-xl p-4 sm:p-8 border border-gray-800">
                    <div className="flex items-center justify-between mb-6">
                        <div>
                            <h3 className="text-xl font-semibold mb-2">Système d'Éclairage</h3>
                            <p className="text-sm text-gray-400">Mode automatique actif (5h–17h)</p>
                        </div>
                        <div className="w-12 h-12 sm:w-16 sm:h-16 bg-yellow-500/20 rounded-full flex items-center justify-center">
                            <i className="fa-solid fa-lightbulb text-yellow-500 text-2xl sm:text-3xl" />
                        </div>
                    </div>

                    <div className="grid grid-cols-3 gap-3 mb-6">
                        {lightLevels.map(({ label, sublabel, value, icon, active }) => (
                            <button
                                key={value}
                                onClick={() => setLightIntensity(value)}
                                disabled={!isConnected}
                                className={`rounded-lg p-3 text-center border-2 transition disabled:opacity-40 disabled:cursor-not-allowed
                                    ${active ? 'bg-gray-800 border-yellow-500 hover:bg-gray-700' : 'bg-gray-800 border-gray-700 hover:border-gray-500 hover:bg-gray-700'}`}
                            >
                                <i className={`fa-solid ${icon} ${active ? 'text-yellow-500' : 'text-gray-500'} text-xl mb-2 block`} />
                                <div className="text-xs text-gray-400">{label}</div>
                                <div className={`text-xs font-semibold ${active ? 'text-white' : 'text-gray-500'}`}>{sublabel}</div>
                            </button>
                        ))}
                    </div>

                    <button
                        onClick={() => setLightIntensity(0)}
                        disabled={!isConnected}
                        className="w-full bg-gray-800 hover:bg-gray-700 text-white font-semibold py-4 rounded-lg transition flex items-center justify-center gap-3 disabled:opacity-40 disabled:cursor-not-allowed"
                    >
                        <i className="fa-solid fa-power-off" />
                        Éteindre Manuellement
                    </button>
                </div>

                {/* ── Watering Control ── */}
                <div id="watering-control" className="bg-gray-900 rounded-xl p-4 sm:p-8 border border-gray-800 flex flex-col">
                    <div className="flex items-center justify-between mb-6">
                        <div>
                            <h3 className="text-xl font-semibold mb-2">Système d'Arrosage</h3>
                            <p className="text-sm text-gray-400">Contrôlez la pompe (relais GPIO 18)</p>
                        </div>
                        <div className={`w-16 h-16 rounded-full flex items-center justify-center transition ${isPumping ? 'bg-blue-500/40' : 'bg-blue-500/20'}`}>
                            <i className={`fa-solid fa-faucet-drip text-blue-500 text-3xl ${isPumping ? 'animate-bounce' : ''}`} />
                        </div>
                    </div>

                    {/* Pump state badge */}
                    <div className={`self-start mb-6 px-3 py-1 rounded-full text-xs font-semibold ${isPumping ? 'bg-blue-500/20 text-blue-300' : 'bg-gray-700 text-gray-400'}`}>
                        Pompe : {isPumping ? 'EN MARCHE' : 'ARRÊTÉE'}
                    </div>

                    {/* Duration slider */}
                    <div className="mb-6">
                        <div className="flex items-center justify-between mb-2">
                            <label className="text-sm text-gray-300">Durée d'arrosage</label>
                            <span className="text-sm font-bold text-blue-400">{duration} s</span>
                        </div>
                        <input
                            type="range"
                            min={5}
                            max={60}
                            step={5}
                            value={duration}
                            onChange={e => setDuration(Number(e.target.value))}
                            className="w-full accent-blue-500"
                        />
                        <div className="flex justify-between text-xs text-gray-600 mt-1">
                            <span>5 s</span><span>60 s</span>
                        </div>
                    </div>

                    {/* Start / Stop buttons */}
                    <div className="grid grid-cols-2 gap-3 mt-auto">
                        <button
                            onClick={handleStart}
                            disabled={!isConnected || isPumping}
                            className="bg-primary hover:bg-secondary text-white font-semibold py-4 rounded-lg transition flex items-center justify-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed"
                        >
                            <i className="fa-solid fa-play" />
                            Démarrer
                        </button>
                        <button
                            onClick={handleStop}
                            disabled={!isConnected || !isPumping}
                            className="bg-red-600 hover:bg-red-700 text-white font-semibold py-4 rounded-lg transition flex items-center justify-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed"
                        >
                            <i className="fa-solid fa-stop" />
                            Arrêter
                        </button>
                    </div>
                </div>

                {/* ── Preferences ── */}
                <div className="md:col-span-2 bg-gray-900 rounded-xl p-4 sm:p-8 border border-gray-800">
                    <h3 className="text-xl font-semibold mb-6">Préférences Générales</h3>
                    <div className="space-y-6">
                        {[
                            {
                                id: 'notifications', label: 'Notifications',
                                desc: 'Recevoir des alertes sur l\'état des plantes',
                                icon: 'fa-bell', color: 'text-purple-500', bg: 'bg-purple-500/20',
                                value: notifications, toggle: () => setNotifications(v => !v),
                            },
                            {
                                id: 'autoMode', label: 'Mode Automatique',
                                desc: 'Laisser le système gérer l\'arrosage et la lumière',
                                icon: 'fa-robot', color: 'text-blue-500', bg: 'bg-blue-500/20',
                                value: autoMode, toggle: () => setAutoMode(v => !v),
                            },
                        ].map(({ id, label, desc, icon, color, bg, value, toggle }) => (
                            <div key={id} className="flex items-center justify-between gap-3 p-3 sm:p-4 bg-gray-800 rounded-lg">
                                <div className="flex items-center gap-3 min-w-0">
                                    <div className={`w-9 h-9 sm:w-10 sm:h-10 ${bg} rounded-full flex items-center justify-center shrink-0`}>
                                        <i className={`fa-solid ${icon} ${color} text-sm sm:text-base`} />
                                    </div>
                                    <div className="min-w-0">
                                        <h4 className="font-semibold text-sm sm:text-base leading-tight">{label}</h4>
                                        <p className="text-xs sm:text-sm text-gray-400 leading-snug mt-0.5">{desc}</p>
                                    </div>
                                </div>
                                <button
                                    onClick={toggle}
                                    className={`shrink-0 w-12 h-6 sm:w-14 sm:h-7 rounded-full p-1 transition duration-300 ${value ? 'bg-primary' : 'bg-gray-600'}`}
                                >
                                    <div className={`w-4 h-4 sm:w-5 sm:h-5 bg-white rounded-full shadow-md transform transition duration-300 ${value ? 'translate-x-6 sm:translate-x-7' : 'translate-x-0'}`} />
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </Layout>
    );
}
