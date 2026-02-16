import React, { useState } from 'react';
import Layout from '../components/Layout';
import useMqtt from '../hooks/useMqtt';

export default function SettingPage() {
    // State simulating toggle switches
    const [notifications, setNotifications] = useState(true);
    const [autoMode, setAutoMode] = useState(true);
    const { publishCommand } = useMqtt();

    const handleLightCommand = (intensity) => {
        publishCommand('jardin/commands/light', { command: 'SET_INTENSITY', value: intensity });
    };

    const handleWaterCommand = () => {
        publishCommand('jardin/commands/water', { command: 'START_WATERING', duration: 10 });
    };

    return (
        <Layout>
            <h2 className="text-2xl font-bold mb-6">Paramètres & Contrôles</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Lighting Control Section From Design */}
                <div id="lighting-control" className="bg-gray-900 rounded-xl p-8 border border-gray-800">
                    <div className="flex items-center justify-between mb-6">
                        <div>
                            <h3 className="text-xl font-semibold mb-2">Système d'Éclairage</h3>
                            <p className="text-sm text-gray-400">Mode automatique actif (5h-17h)</p>
                        </div>
                        <div className="w-16 h-16 bg-yellow-500/20 rounded-full flex items-center justify-center">
                            <i className="fa-solid fa-lightbulb text-yellow-500 text-3xl"></i>
                        </div>
                    </div>

                    <div className="space-y-4 mb-6">
                        <div className="flex items-center justify-between">
                            <span className="text-sm text-gray-300">Intensité Actuelle</span>
                            <span className="text-sm font-semibold text-yellow-500">Intense (Matin)</span>
                        </div>
                        <div className="flex items-center gap-4">
                            <span className="text-xs text-gray-500">0%</span>
                            <div className="flex-1 bg-gray-800 rounded-full h-3">
                                <div className="bg-gradient-to-r from-yellow-500 to-yellow-400 h-3 rounded-full" style={{ width: '85%' }}></div>
                            </div>
                            <span className="text-xs text-gray-500">100%</span>
                        </div>

                        <div className="grid grid-cols-3 gap-3 mt-6">
                            <button onClick={() => handleLightCommand(100)} className="bg-gray-800 rounded-lg p-3 text-center border-2 border-yellow-500 cursor-pointer hover:bg-gray-700 transition">
                                <i className="fa-solid fa-sun text-yellow-500 mb-2"></i>
                                <div className="text-xs text-gray-400">Matin</div>
                                <div className="text-xs font-semibold text-white">Intense</div>
                            </button>
                            <button onClick={() => handleLightCommand(50)} className="bg-gray-800 rounded-lg p-3 text-center cursor-pointer hover:bg-gray-700 transition">
                                <i className="fa-solid fa-cloud-sun text-gray-600 mb-2"></i>
                                <div className="text-xs text-gray-400">Après-midi</div>
                                <div className="text-xs font-semibold text-gray-600">Modéré</div>
                            </button>
                            <button onClick={() => handleLightCommand(0)} className="bg-gray-800 rounded-lg p-3 text-center cursor-pointer hover:bg-gray-700 transition">
                                <i className="fa-solid fa-moon text-gray-600 mb-2"></i>
                                <div className="text-xs text-gray-400">Nuit</div>
                                <div className="text-xs font-semibold text-gray-600">OFF</div>
                            </button>
                        </div>
                    </div>

                    <button onClick={() => handleLightCommand(0)} className="w-full bg-gray-800 hover:bg-gray-700 text-white font-semibold py-4 rounded-lg transition flex items-center justify-center gap-3">
                        <i className="fa-solid fa-power-off"></i>
                        Éteindre Manuellement
                    </button>
                </div>

                {/* Watering Control Section From Design */}
                <div id="watering-control" className="bg-gray-900 rounded-xl p-8 border border-gray-800">
                    <div className="flex items-center justify-between mb-6">
                        <div>
                            <h3 className="text-xl font-semibold mb-2">Système d'Arrosage</h3>
                            <p className="text-sm text-gray-400">Contrôlez l'arrosage de vos 4 capsules</p>
                        </div>
                        <div className="w-16 h-16 bg-blue-500/20 rounded-full flex items-center justify-center">
                            <i className="fa-solid fa-faucet-drip text-blue-500 text-3xl"></i>
                        </div>
                    </div>

                    <div className="grid grid-cols-4 gap-4 mb-6">
                        {[1, 2, 3, 4].map((capsule) => (
                            <div key={capsule} className="text-center cursor-pointer group">
                                <div className={`w-full h-20 bg-gray-800 rounded-lg flex items-center justify-center mb-2 border-2 ${capsule % 2 !== 0 ? 'border-primary' : 'border-gray-700 group-hover:border-gray-500'} transition`}>
                                    <i className={`fa-solid fa-mug-hot text-2xl ${capsule % 2 !== 0 ? 'text-primary' : 'text-gray-600'}`}></i>
                                </div>
                                <span className="text-xs text-gray-400">Capsule {capsule}</span>
                                <div className={`mt-1 text-xs ${capsule % 2 !== 0 ? 'text-primary' : 'text-gray-600'}`}>
                                    {capsule % 2 !== 0 ? 'Actif' : 'Inactif'}
                                </div>
                            </div>
                        ))}
                    </div>

                    <button onClick={handleWaterCommand} className="w-full bg-primary hover:bg-secondary text-white font-semibold py-4 rounded-lg transition flex items-center justify-center gap-3">
                        <i className="fa-solid fa-play"></i>
                        Démarrer l'Arrosage
                    </button>
                </div>

                {/* General Settings */}
                <div className="md:col-span-2 bg-gray-900 rounded-xl p-8 border border-gray-800">
                    <h3 className="text-xl font-semibold mb-6">Préférences Générales</h3>
                    <div className="space-y-6">
                        <div className="flex items-center justify-between p-4 bg-gray-800 rounded-lg">
                            <div className="flex items-center gap-4">
                                <div className="w-10 h-10 bg-purple-500/20 rounded-full flex items-center justify-center">
                                    <i className="fa-solid fa-bell text-purple-500"></i>
                                </div>
                                <div>
                                    <h4 className="font-semibold">Notifications</h4>
                                    <p className="text-sm text-gray-400">Recevoir des alertes sur l'état des plantes</p>
                                </div>
                            </div>
                            <button
                                onClick={() => setNotifications(!notifications)}
                                className={`w-14 h-7 rounded-full p-1 transition duration-300 ${notifications ? 'bg-primary' : 'bg-gray-600'}`}
                            >
                                <div className={`w-5 h-5 bg-white rounded-full shadow-md transform transition duration-300 ${notifications ? 'translate-x-7' : 'translate-x-0'}`}></div>
                            </button>
                        </div>

                        <div className="flex items-center justify-between p-4 bg-gray-800 rounded-lg">
                            <div className="flex items-center gap-4">
                                <div className="w-10 h-10 bg-blue-500/20 rounded-full flex items-center justify-center">
                                    <i className="fa-solid fa-robot text-blue-500"></i>
                                </div>
                                <div>
                                    <h4 className="font-semibold">Mode Automatique</h4>
                                    <p className="text-sm text-gray-400">Laisser le système gérer l'arrosage et la lumière</p>
                                </div>
                            </div>
                            <button
                                onClick={() => setAutoMode(!autoMode)}
                                className={`w-14 h-7 rounded-full p-1 transition duration-300 ${autoMode ? 'bg-primary' : 'bg-gray-600'}`}
                            >
                                <div className={`w-5 h-5 bg-white rounded-full shadow-md transform transition duration-300 ${autoMode ? 'translate-x-7' : 'translate-x-0'}`}></div>
                            </button>
                        </div>
                    </div>
                </div>

            </div>
        </Layout>
    );
}
