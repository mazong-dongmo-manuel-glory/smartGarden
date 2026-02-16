import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import MetricCard from '../components/MetricCard';
import StatusCard from '../components/StatusCard';
import PlantCard from '../components/PlantCard';

export default function DashboardPage() {
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
                                <p className="text-gray-400">Surveillance en temps réel - Dernière mise à jour: Il y a 2 secondes</p>
                            </div>
                            <div className="flex items-center gap-4">
                                <div className="text-center">
                                    <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mb-2">
                                        <i className="fa-solid fa-circle text-primary text-2xl animate-pulse"></i>
                                    </div>
                                    <span className="text-xs text-gray-400">Système OK</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Alerts Section */}
                <section id="alerts-section" className="mb-8">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <StatusCard title="Système Normal" description="Toutes les conditions sont optimales" type="success" />
                        <StatusCard title="Avertissement Mineur" description="Humidité légèrement basse" type="warning" />
                        <StatusCard title="Défaillance Majeure" description="Aucune défaillance détectée" type="danger" />
                    </div>
                </section>

                {/* Sensors Grid */}
                <section id="sensors-grid" className="mb-8">
                    <h2 className="text-2xl font-bold mb-6">Capteurs Environnementaux</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                        <MetricCard
                            title="Température"
                            value="23.5"
                            unit="°C"
                            icon="fa-temperature-half"
                            color="bg-red-500"
                            status="Optimal"
                            progress={65}
                        />
                        <MetricCard
                            title="Humidité du Sol"
                            value="68"
                            unit="%"
                            icon="fa-droplet"
                            color="bg-blue-500"
                            status="Bon"
                            progress={68}
                        />
                        <MetricCard
                            title="Luminosité"
                            value="850"
                            unit="lux"
                            icon="fa-sun"
                            color="bg-yellow-500"
                            status="Intense"
                            progress={85}
                        />
                        <MetricCard
                            title="Qualité de l'Air"
                            value="92"
                            unit="AQI"
                            icon="fa-wind"
                            color="bg-purple-500"
                            status="Excellent"
                            progress={92}
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
