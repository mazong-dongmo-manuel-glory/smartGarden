import React from 'react';
import Layout from '../components/Layout';
import RefactoredChart from '../components/RefactoredChart';
import useMqtt from '../hooks/useMqtt';

// Type badge colours
const typeBadge = {
    success: 'text-green-400',
    info: 'text-blue-400',
    warning: 'text-yellow-400',
    error: 'text-red-400',
};
const typeLabel = {
    success: 'Système',
    info: 'Capteur',
    warning: 'Alerte',
    error: 'Erreur',
};

export default function HistoryPage() {
    const { publishCommand, chartTemp, chartMoisture, eventLog } = useMqtt();

    const handleExport = () => {
        publishCommand('jardin/commands/water', { command: 'EXPORT_DATA' });
        setTimeout(() => {
            const link = document.createElement('a');
            link.href = '/report.csv';
            link.download = 'rapport_jardin.csv';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }, 2000);
    };

    return (
        <Layout>
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold">Historique des Données</h2>
                <button
                    onClick={handleExport}
                    className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition flex items-center gap-2"
                >
                    <i className="fa-solid fa-file-csv" />
                    Télécharger Rapport
                </button>
            </div>

            {/* Live Charts */}
            <section id="charts-section" className="mb-8">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                    <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
                        <h3 className="text-lg font-semibold mb-1 flex items-center gap-3">
                            <i className="fa-solid fa-temperature-half text-red-500" />
                            Température en direct
                        </h3>
                        <p className="text-xs text-gray-500 mb-4">Dernières 20 lectures MQTT</p>
                        {chartTemp.length > 0 ? (
                            <RefactoredChart data={chartTemp} dataKey="value" color="#ef4444" unit="°C" />
                        ) : (
                            <div className="h-40 flex items-center justify-center text-gray-600 text-sm">
                                <i className="fa-solid fa-satellite-dish mr-2" />
                                En attente des données MQTT…
                            </div>
                        )}
                    </div>

                    <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
                        <h3 className="text-lg font-semibold mb-1 flex items-center gap-3">
                            <i className="fa-solid fa-droplet text-blue-500" />
                            Humidité du sol en direct
                        </h3>
                        <p className="text-xs text-gray-500 mb-4">Dernières 20 lectures MQTT</p>
                        {chartMoisture.length > 0 ? (
                            <RefactoredChart data={chartMoisture} dataKey="value" color="#3b82f6" unit="%" />
                        ) : (
                            <div className="h-40 flex items-center justify-center text-gray-600 text-sm">
                                <i className="fa-solid fa-satellite-dish mr-2" />
                                En attente des données MQTT…
                            </div>
                        )}
                    </div>

                </div>
            </section>

            {/* Live Event Log */}
            <section id="event-log-section" className="mb-8">
                <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                    <i className="fa-solid fa-list-check" />
                    Journal des Événements
                    {eventLog.length > 0 && (
                        <span className="ml-2 text-xs bg-gray-700 text-gray-300 px-2 py-1 rounded-full">
                            {eventLog.length}
                        </span>
                    )}
                </h2>
                <div className="bg-gray-900 rounded-xl border border-gray-800 overflow-hidden">
                    <table className="w-full text-left text-sm text-gray-400">
                        <thead className="bg-gray-800 text-gray-200 uppercase font-medium">
                            <tr>
                                <th className="px-6 py-4">Date &amp; Heure</th>
                                <th className="px-6 py-4">Topic MQTT</th>
                                <th className="px-6 py-4">Événement</th>
                                <th className="px-6 py-4">Type</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-800">
                            {eventLog.length === 0 ? (
                                <tr>
                                    <td colSpan={4} className="px-6 py-8 text-center text-gray-600">
                                        <i className="fa-solid fa-satellite-dish mr-2" />
                                        Aucun événement — en attente de la connexion MQTT…
                                    </td>
                                </tr>
                            ) : (
                                eventLog.map((ev, i) => (
                                    <tr key={i} className="hover:bg-gray-800/50 transition">
                                        <td className="px-6 py-4 whitespace-nowrap">{ev.ts}</td>
                                        <td className="px-6 py-4 font-mono text-xs text-gray-500">{ev.topic}</td>
                                        <td className="px-6 py-4">{ev.summary}</td>
                                        <td className="px-6 py-4">
                                            <span className={typeBadge[ev.type] || 'text-gray-400'}>
                                                {typeLabel[ev.type] || ev.type}
                                            </span>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </section>
        </Layout>
    );
}