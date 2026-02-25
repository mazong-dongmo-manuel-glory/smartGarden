import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import MetricCard from '../components/MetricCard';
import StatusCard from '../components/StatusCard';
import PlantCard from '../components/PlantCard';
import useMqtt from '../hooks/useMqtt';

// Pluie valeur brute ADC (0-255) : valeur ÉLEVÉE = SEC
function rainMeta(rawVal) {
    if (rawVal === null) return { color: 'bg-gray-500', label: 'En attente' };
    if (rawVal >= 150) return { color: 'bg-green-500', label: 'Sec' };
    if (rawVal >= 80) return { color: 'bg-blue-400', label: 'Pluie légère' };
    return { color: 'bg-blue-600', label: 'Forte pluie' };
}

export default function DashboardPage() {
    const { isConnected, sensorData, alerts } = useMqtt();
    const { color: rainColor, label: rainLabel } = rainMeta(sensorData.rainPct);

    const fmt = (v, decimals = 0) =>
        v !== null && v !== undefined ? Number(v).toFixed(decimals) : '--';

    return (
        <div className="bg-gray-950 text-gray-100 font-sans min-h-screen">
            <Header />

            <main id="main-content" className="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-8 overflow-x-hidden">

                {/* Hero Status */}
                <section id="hero-status" className="mb-8">
                    <div className="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 rounded-2xl p-4 sm:p-8 border border-gray-700">
                        <div className="flex items-center justify-between">
                            <div>
                                <h2 className="text-xl sm:text-3xl font-bold mb-1 sm:mb-2">État du Système</h2>
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
                    <div className="grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-6 gap-3 sm:gap-6">
                        {/* 1 - Température */}
                        <MetricCard
                            title="Température"
                            value={fmt(sensorData.temperature, 1)}
                            unit="°C"
                            icon="fa-temperature-half"
                            color="bg-red-500"
                            status="Temps réel"
                            progress={sensorData.temperature ? (sensorData.temperature / 50) * 100 : 0}
                        />
                        {/* 2 - Humidité Air */}
                        <MetricCard
                            title="Humidité Air"
                            value={fmt(sensorData.humidity)}
                            unit="%"
                            icon="fa-cloud"
                            color="bg-purple-500"
                            status="Temps réel"
                            progress={sensorData.humidity || 0}
                        />
                        {/* 3 - Pluie ADC */}
                        <MetricCard
                            title="Pluie"
                            value={fmt(sensorData.rainPct)}
                            unit="/255"
                            icon="fa-cloud-rain"
                            color={rainColor}
                            status={rainLabel}
                            progress={sensorData.rainPct !== null ? ((255 - sensorData.rainPct) / 255) * 100 : 0}
                        />
                        {/* 4 - Luminosité */}
                        <MetricCard
                            title="Luminosité"
                            value={fmt(sensorData.light)}
                            unit="lux"
                            icon="fa-sun"
                            color="bg-yellow-500"
                            status="Temps réel"
                            progress={sensorData.light ? (sensorData.light / 1000) * 100 : 0}
                        />
                        {/* 6 - Jour / Nuit */}
                        <MetricCard
                            title="Éclairage"
                            value={sensorData.isDark === null ? '--' : sensorData.isDark ? 'Nuit' : 'Jour'}
                            unit=""
                            icon={sensorData.isDark ? 'fa-moon' : 'fa-sun'}
                            color={sensorData.isDark ? 'bg-indigo-500' : 'bg-yellow-400'}
                            status={sensorData.isDark ? 'Lampe ON' : 'Lampe OFF'}
                            progress={sensorData.isDark ? 100 : 20}
                        />
                    </div>
                </section>

                {/* Plants Status */}
                <section id="plants-status" className="mb-8">
                    <h2 className="text-2xl font-bold mb-6">État des Plants</h2>
                    <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
                        <PlantCard name="Haricot #1" type="Capsule K-Cup" growthDay={8} height={12} health="Excellente" />

                    </div>
                </section>

            </main>
            <Footer />
        </div>
    );
}
