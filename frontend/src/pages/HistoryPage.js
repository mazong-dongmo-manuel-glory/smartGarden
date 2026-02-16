import React from 'react';
import Layout from '../components/Layout';
import RefactoredChart from '../components/RefactoredChart';

// Sample Data for Charts
const tempData = [
    { time: '00:00', value: 20 },
    { time: '04:00', value: 18 },
    { time: '08:00', value: 22 },
    { time: '12:00', value: 28 },
    { time: '16:00', value: 26 },
    { time: '20:00', value: 23 },
    { time: '23:59', value: 21 },
];

const humidityData = [
    { time: '00:00', value: 65 },
    { time: '04:00', value: 70 },
    { time: '08:00', value: 68 },
    { time: '12:00', value: 55 },
    { time: '16:00', value: 60 },
    { time: '20:00', value: 65 },
    { time: '23:59', value: 70 },
];

export default function HistoryPage() {
    return (
        <Layout>
            <section id="charts-section" className="mb-8">
                <h2 className="text-2xl font-bold mb-6">Historique des Données</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                    <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
                        <h3 className="text-lg font-semibold mb-4 flex items-center gap-3">
                            <i className="fa-solid fa-temperature-half text-red-500"></i>
                            Température (24h)
                        </h3>
                        <RefactoredChart data={tempData} dataKey="value" color="#ef4444" unit="°C" />
                    </div>

                    <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
                        <h3 className="text-lg font-semibold mb-4 flex items-center gap-3">
                            <i className="fa-solid fa-droplet text-blue-500"></i>
                            Humidité du Sol (24h)
                        </h3>
                        <RefactoredChart data={humidityData} dataKey="value" color="#3b82f6" unit="%" />
                    </div>

                </div>
            </section>

            <section id="lcd-display-section" className="mb-8">
                <h2 className="text-2xl font-bold mb-6">Journal des Événements</h2>
                <div className="bg-gray-900 rounded-xl border border-gray-800 overflow-hidden">
                    <table className="w-full text-left text-sm text-gray-400">
                        <thead className="bg-gray-800 text-gray-200 uppercase font-medium">
                            <tr>
                                <th className="px-6 py-4">Date & Heure</th>
                                <th className="px-6 py-4">Événement</th>
                                <th className="px-6 py-4">Type</th>
                                <th className="px-6 py-4">Statut</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-800">
                            <tr className="hover:bg-gray-800/50 transition">
                                <td className="px-6 py-4">16/02/2026 14:23</td>
                                <td className="px-6 py-4">Arrosage automatique (Zone 1)</td>
                                <td className="px-6 py-4">Action</td>
                                <td className="px-6 py-4"><span className="text-green-500">Succès</span></td>
                            </tr>
                            <tr className="hover:bg-gray-800/50 transition">
                                <td className="px-6 py-4">16/02/2026 12:00</td>
                                <td className="px-6 py-4">Alerte: Humidité basse</td>
                                <td className="px-6 py-4">Alerte</td>
                                <td className="px-6 py-4"><span className="text-yellow-500">En cours</span></td>
                            </tr>
                            <tr className="hover:bg-gray-800/50 transition">
                                <td className="px-6 py-4">16/02/2026 08:00</td>
                                <td className="px-6 py-4">Démarrage système</td>
                                <td className="px-6 py-4">Système</td>
                                <td className="px-6 py-4"><span className="text-green-500">OK</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>
        </Layout>
    );
}