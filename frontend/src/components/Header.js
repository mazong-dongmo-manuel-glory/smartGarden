import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

const navLinks = [
    { to: '/dashboard', label: 'Tableau de bord', icon: 'fa-gauge-high' },
    { to: '/setting', label: 'Contrôles', icon: 'fa-sliders' },
    { to: '/history', label: 'Historique', icon: 'fa-clock-rotate-left' },
];

const Header = () => {
    const [menuOpen, setMenuOpen] = useState(false);
    const location = useLocation();

    return (
        <header id="header" className="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">
            <div className="max-w-[1440px] mx-auto px-4 sm:px-8 py-4 flex items-center justify-between">

                {/* Logo */}
                <div className="flex items-center gap-3 shrink-0">
                    <div className="w-10 h-10 bg-gradient-to-br from-primary to-secondary rounded-lg flex items-center justify-center">
                        <i className="fa-solid fa-seedling text-white text-xl" />
                    </div>
                    <div className="hidden sm:block">
                        <h1 className="text-xl font-bold text-white">AgriSmart IoT</h1>
                        <p className="text-xs text-gray-400">Système Post-Apocalyptique</p>
                    </div>
                    <div className="sm:hidden">
                        <h1 className="text-base font-bold text-white">AgriSmart</h1>
                    </div>
                </div>

                {/* Desktop nav */}
                <nav className="hidden md:flex items-center gap-6">
                    {navLinks.map(({ to, label, icon }) => {
                        const active = location.pathname === to;
                        return (
                            <Link
                                key={to}
                                to={to}
                                className={`flex items-center gap-2 font-medium transition text-sm ${active ? 'text-primary' : 'text-gray-400 hover:text-white'}`}
                            >
                                <i className={`fa-solid ${icon}`} />
                                <span>{label}</span>
                            </Link>
                        );
                    })}
                </nav>

                {/* Right side */}
                <div className="flex items-center gap-3">
                    <div className="hidden sm:flex items-center gap-2 bg-gray-800 px-3 py-2 rounded-lg">
                        <div className="w-2 h-2 bg-primary rounded-full animate-pulse" />
                        <span className="text-sm text-gray-300">Connecté</span>
                    </div>
                    <img
                        src="https://storage.googleapis.com/uxpilot-auth.appspot.com/avatars/avatar-2.jpg"
                        alt="User"
                        className="w-9 h-9 rounded-full border-2 border-primary"
                    />
                    {/* Hamburger */}
                    <button
                        onClick={() => setMenuOpen(o => !o)}
                        className="md:hidden p-2 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 transition"
                        aria-label="Menu"
                    >
                        <i className={`fa-solid ${menuOpen ? 'fa-xmark' : 'fa-bars'} text-xl`} />
                    </button>
                </div>
            </div>

            {/* Mobile dropdown nav */}
            {menuOpen && (
                <nav className="md:hidden bg-gray-900 border-t border-gray-800 px-4 pb-4 pt-2 flex flex-col gap-1">
                    {navLinks.map(({ to, label, icon }) => {
                        const active = location.pathname === to;
                        return (
                            <Link
                                key={to}
                                to={to}
                                onClick={() => setMenuOpen(false)}
                                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition text-sm font-medium
                                    ${active ? 'bg-primary/10 text-primary' : 'text-gray-400 hover:bg-gray-800 hover:text-white'}`}
                            >
                                <i className={`fa-solid ${icon} w-4`} />
                                {label}
                            </Link>
                        );
                    })}
                </nav>
            )}
        </header>
    );
};

export default Header;
