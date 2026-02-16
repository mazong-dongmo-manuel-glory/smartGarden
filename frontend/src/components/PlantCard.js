import React from 'react';

const PlantCard = ({ name, type, growthDay, height, health }) => {
    return (
        <div className="bg-gray-900 rounded-xl p-6 border border-gray-800 hover:border-primary transition duration-300">
            <div className="text-center mb-4">
                <div className="w-20 h-20 mx-auto bg-primary/20 rounded-full flex items-center justify-center mb-3">
                    <i className="fa-solid fa-seedling text-primary text-3xl"></i>
                </div>
                <h3 className="font-semibold text-white mb-1">{name}</h3>
                <span className="text-xs text-gray-400">{type}</span>
            </div>
            <div className="space-y-3">
                <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-400">Croissance</span>
                    <span className="text-primary font-semibold">Jour {growthDay}</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-400">Hauteur</span>
                    <span className="text-white font-semibold">{height} cm</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-400">Santé</span>
                    <span className="text-primary font-semibold">{health}</span>
                </div>
            </div>
        </div>
    );
};

export default PlantCard;
