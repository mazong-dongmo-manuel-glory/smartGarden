import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
    return (
        <header id="header" className="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">
            <div className="max-w-[1440px] mx-auto px-8 py-4 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-primary to-secondary rounded-lg flex items-center justify-center">
                        <i className="fa-solid fa-seedling text-white text-xl"></i>
                    </div>
                    <div>
                        <h1 className="text-xl font-bold text-white">AgriSmart IoT</h1>
                        <p className="text-xs text-gray-400">Système Post-Apocalyptique</p>
                    </div>
                </div>

                <nav className="flex items-center gap-8">
                    <Link to="/dashboard" className="text-primary font-medium hover:text-primary/80 transition flex items-center gap-2">
                        <i className="fa-solid fa-gauge-high"></i>
                        <span>Tableau de bord</span>
                    </Link>
                    <Link to="/setting" className="text-gray-400 hover:text-white transition flex items-center gap-2">
                        <i className="fa-solid fa-sliders"></i>
                        <span>Contrôles</span>
                    </Link>
                    <Link to="/history" className="text-gray-400 hover:text-white transition flex items-center gap-2">
                        <i className="fa-solid fa-clock-rotate-left"></i>
                        <span>Historique</span>
                    </Link>
                </nav>

                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2 bg-gray-800 px-4 py-2 rounded-lg">
                        <div className="w-2 h-2 bg-primary rounded-full animate-pulse"></div>
                        <span className="text-sm text-gray-300">Connecté</span>
                    </div>
                    <img src="https://storage.googleapis.com/uxpilot-auth.appspot.com/avatars/avatar-2.jpg" alt="User" className="w-10 h-10 rounded-full border-2 border-primary" />
                </div>
            </div>
        </header>
    );
};

export default Header;
