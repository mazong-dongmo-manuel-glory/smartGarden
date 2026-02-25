import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import MetricCard from '../components/MetricCard';
import StatusCard from '../components/StatusCard';
import PlantCard from '../components/PlantCard';
import useMqtt from '../hooks/useMqtt';

// Rain ADC value (0-255) → colour + label
function rainMeta(rain) {
    if (rain === null) return { color: 'bg-gray-500', label: '--' };
    if (rain < 80) return { color: 'bg-green-500', label: 'Sec' };
    if (rain < 150) return { color: 'bg-yellow-500', label: 'Légère' };
    return { color: 'bg-red-500', label: 'Forte' };
}

export default function DashboardPage() {
    const { isConnected, sensorData, alerts } = useMqtt();
    const { color: rainColor } = rainMeta(sensorData.rain);

    const fmt = (v, decimals = 0) =>
        v !== null && v !== undefined ? Number(v).toFixed(decimals) : '--';

    return (
        <div className="bg-gray-950 text-gray-100 font-sans min-h-screen">
            <Header />

            <main id="main-content" className="max-w-[1440px] mx-auto px-8 py-8">

                {/* Hero Status */}
                <section id="hero-status" className="mb-8">
                    <div className="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 rounded-2xl p-8 border border-gray-700">
                        <div className="flex items-center justify-between">
                            <div>
                                <h2 className="text-3xl font-bold mb-2">État du Système</h2>
                                <p className="text-gray-400">
                                    Surveillance en temps réel —{' '}
                                    {isConnected
                                        ? <span className="text-green-400 font-semibold">Connecté au Broker MQTT</span>
                                        : <span className="text-red-400 font-semibold">Déconnecté</span>}
                                </p>
                                {alerts.length > 0 && (
                                    <p className="mt-2 text-sm text-yellow-400">
                                        <i className="fa-solid fa-triangle-exclamation mr-2" />
                                        {alerts[0].message}
                                    </p>
                                )}
                            </div>
                            <div className="text-center">
                                <div className={`w-16 h-16 ${isConnected ? 'bg-primary/20' : 'bg-red-500/20'} rounded-full flex items-center justify-center mb-2`}>
                                    <i className={`fa-solid fa-circle ${isConnected ? 'text-primary' : 'text-red-500'} text-2xl ${isConnected ? 'animate-pulse' : ''}`} />
                                </div>
                                <span className="text-xs text-gray-400">{isConnected ? 'Système OK' : 'Erreur Connexion'}</span>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Alerts Section */}
                <section id="alerts-section" className="mb-8">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {alerts.length > 0 ? (
                            alerts.map((alert, index) => (
                                <StatusCard
                                    key={index}
                                    title={alert.level === 'error' ? 'Erreur Critique' : 'Avertissement'}
                                    description={alert.message}
                                    type={alert.level === 'error' ? 'danger' : 'warning'}
                                />
                            ))
                        ) : (
                            <StatusCard title="Système Normal" description="Aucune alerte récente" type="success" />
                        )}
                    </div>
                </section>

                {/* Sensors Grid — 6 tiles */}
                <section id="sensors-grid" className="mb-8">
                    <h2 className="text-2xl font-bold mb-6">Capteurs Environnementaux</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6">
                        <MetricCard
                            title="Température"
                            value={fmt(sensorData.temperature, 1)}
                            unit="°C"
                            icon="fa-temperature-half"
                            color="bg-red-500"
                            status="Temps Réel"
                            progress={sensorData.temperature ? (sensorData.temperature / 40) * 100 : 0}
                        />
                        <MetricCard
                            title="Humidité Air"
                            value={fmt(sensorData.humidity)}
                            unit="%"
                            icon="fa-cloud"
                            color="bg-purple-500"
                            status="Temps Réel"
                            progress={sensorData.humidity || 0}
                        />
                        <MetricCard
                            title="Humidité Sol"
                            value={fmt(sensorData.moisture)}
                            unit="%"
                            icon="fa-droplet"
                            color="bg-blue-500"
                            status="Temps Réel"
                            progress={sensorData.moisture || 0}
                        />
                        <MetricCard
                            title="Luminosité"
                            value={fmt(sensorData.light)}
                            unit="lux"
                            icon="fa-sun"
                            color="bg-yellow-500"
                            status="Temps Réel"
                            progress={sensorData.light ? (sensorData.light / 1000) * 100 : 0}
                        />
                        {/* Rain tile — dynamically coloured */}
                        <MetricCard
                            title="Pluie (ADC)"
                            value={fmt(sensorData.rain)}
                            unit="/255"
                            icon="fa-cloud-rain"
                            color={rainColor}
                            status={sensorData.rain === null ? 'En attente' : sensorData.rain < 80 ? 'Sec' : sensorData.rain < 150 ? 'Pluie légère' : 'Forte pluie'}
                            progress={sensorData.rain ? (sensorData.rain / 255) * 100 : 0}
                        />
                        {/* Water level tile */}
                        <MetricCard
                            title="Niveau d'eau"
                            value={fmt(sensorData.waterLevel)}
                            unit="%"
                            icon="fa-water"
                            color={sensorData.waterLevel !== null && sensorData.waterLevel < 20 ? 'bg-red-500' : 'bg-cyan-500'}
                            status={sensorData.waterLevel !== null && sensorData.waterLevel < 20 ? 'Niveau bas !' : 'Temps Réel'}
                            progress={sensorData.waterLevel || 0}
                        />
                    </div>
                </section>

                {/* Plants Status */}
                <section id="plants-status" className="mb-8">
                    <h2 className="text-2xl font-bold mb-6">État des Plants</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                        <PlantCard name="Haricot #1" type="Capsule K-Cup" growthDay={8} height={12} health="Excellente" />
                        <PlantCard name="Haricot #2" type="Capsule K-Cup" growthDay={8} height={10} health="Bonne" />
                        <PlantCard name="Haricot #3" type="Capsule K-Cup" growthDay={8} height={14} health="Excellente" />
                        <PlantCard name="Haricot #4" type="Capsule K-Cup" growthDay={8} height={11} health="Bonne" />
                    </div>
                </section>

            </main>
            <Footer />
        </div>
    );
}
