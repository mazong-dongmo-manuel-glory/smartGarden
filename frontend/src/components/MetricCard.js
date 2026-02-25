import React from 'react';

const MetricCard = ({ title, value, unit, icon, color, status, progress }) => {
    return (
        <div className="bg-gray-900 rounded-xl p-4 sm:p-6 border border-gray-800 hover:border-primary transition duration-300">
            <div className="flex items-center justify-between mb-3">
                <div className={`w-10 h-10 sm:w-12 sm:h-12 ${color}/20 rounded-lg flex items-center justify-center`}>
                    <i className={`fa-solid ${icon} ${color.replace('bg-', 'text-')} text-lg sm:text-2xl`} />
                </div>
                <span className="text-xs text-gray-500 bg-gray-800 px-2 py-1 rounded-full truncate ml-2">
                    {status}
                </span>
            </div>
            <h3 className="text-gray-400 text-xs sm:text-sm mb-1 truncate">{title}</h3>
            <div className="flex items-end gap-1 sm:gap-2">
                <span className="text-2xl sm:text-4xl font-bold text-white leading-none">{value}</span>
                <span className="text-sm sm:text-xl text-gray-400 mb-0.5">{unit}</span>
            </div>
            <div className="mt-3 flex items-center gap-2">
                <div className="flex-1 bg-gray-800 rounded-full h-1.5">
                    <div
                        className={`${color.replace('/20', '')} h-1.5 rounded-full transition-all duration-500`}
                        style={{ width: `${Math.min(progress, 100)}%` }}
                    />
                </div>
            </div>
        </div>
    );
};

export default MetricCard;
