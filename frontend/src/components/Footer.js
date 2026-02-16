import React from 'react';

const Footer = () => {
    return (
        <footer id="footer" className="bg-gray-900 border-t border-gray-800 mt-16">
            <div className="max-w-[1440px] mx-auto px-8 py-8">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-gradient-to-br from-primary to-secondary rounded-lg flex items-center justify-center">
                            <i className="fa-solid fa-seedling text-white text-xl"></i>
                        </div>
                        <div>
                            <h3 className="font-semibold text-white">AgriSmart IoT</h3>
                            <p className="text-xs text-gray-500">Survivre à l'apocalypse avec l'agriculture intelligente</p>
                        </div>
                    </div>
                    <div className="text-sm text-gray-500">
                        © 2026 Projet Post-Apocalyptique - MQTT & IoT
                    </div>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
