import React from 'react';
import { Link } from 'react-router-dom';

export default function LoginPage() {
    return (
        <div className="bg-gray-950 min-h-screen flex items-center justify-center p-4 font-sans text-gray-100">
            <div className="w-full max-w-md bg-gray-900 rounded-2xl p-8 border border-gray-800 shadow-xl">
                <div className="text-center mb-8">
                    <div className="w-16 h-16 bg-gradient-to-br from-primary to-secondary rounded-xl flex items-center justify-center mx-auto mb-4">
                        <i className="fa-solid fa-seedling text-white text-3xl"></i>
                    </div>
                    <h1 className="text-2xl font-bold text-white mb-2">Bienvenue sur AgriSmart</h1>
                    <p className="text-gray-400 text-sm">Connectez-vous pour gérer votre jardin</p>
                </div>

                <form className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-400 mb-2">Email</label>
                        <div className="relative">
                            <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500">
                                <i className="fa-solid fa-envelope"></i>
                            </span>
                            <input
                                type="email"
                                className="w-full bg-gray-800 border border-gray-700 text-white rounded-lg py-3 pl-12 pr-4 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition"
                                placeholder="exemple@email.com"
                            />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-400 mb-2">Mot de passe</label>
                        <div className="relative">
                            <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500">
                                <i className="fa-solid fa-lock"></i>
                            </span>
                            <input
                                type="password"
                                className="w-full bg-gray-800 border border-gray-700 text-white rounded-lg py-3 pl-12 pr-4 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition"
                                placeholder="••••••••"
                            />
                        </div>
                    </div>

                    <div className="flex items-center justify-between text-sm">
                        <label className="flex items-center gap-2 cursor-pointer">
                            <input type="checkbox" className="w-4 h-4 rounded bg-gray-800 border-gray-700 text-primary focus:ring-primary" />
                            <span className="text-gray-400">Se souvenir de moi</span>
                        </label>
                        <a href="#" className="text-primary hover:text-primary/80 transition">Mot de passe oublié ?</a>
                    </div>

                    <Link to="/dashboard" className="block text-center w-full bg-primary hover:bg-secondary text-white font-semibold py-3 rounded-lg transition duration-300">
                        Se Connecter
                    </Link>
                </form>

            </div>
        </div>
    );
}