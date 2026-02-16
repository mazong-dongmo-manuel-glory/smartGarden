import React from 'react';

const MetricCard = ({ title, value, unit, icon, color, status, progress }) => {
    return (
        <div className="bg-gray-900 rounded-xl p-6 border border-gray-800 hover:border-primary transition duration-300">
            <div className="flex items-center justify-between mb-4">
                <div className={`w-12 h-12 ${color}/20 rounded-lg flex items-center justify-center`}>
                    <i className={`${icon} ${color.replace('bg-', 'text-')} text-2xl`}></i>
                </div>
                <span className="text-xs text-gray-500 bg-gray-800 px-3 py-1 rounded-full">Temps réel</span>
            </div>
            <h3 className="text-gray-400 text-sm mb-2">{title}</h3>
            <div className="flex items-end gap-2">
                <span className="text-4xl font-bold text-white">{value}</span>
                <span className="text-xl text-gray-400 mb-1">{unit}</span>
            </div>
            <div className="mt-4 flex items-center gap-2">
                <div className="flex-1 bg-gray-800 rounded-full h-2">
                    <div className={`${color.replace('/20', '')} h-2 rounded-full`} style={{ width: `${progress}%` }}></div>
                </div>
                <span className="text-xs text-gray-500">{status}</span>
            </div>
        </div>
    );
};

export default MetricCard;
