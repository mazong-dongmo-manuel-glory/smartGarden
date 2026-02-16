import React from 'react';

const StatusCard = ({ title, description, type }) => {
    let borderColor = 'border-primary';
    let iconColor = 'text-primary';
    let iconBg = 'bg-primary/20';
    let iconClass = 'fa-check';

    if (type === 'warning') {
        borderColor = 'border-warning';
        iconColor = 'text-warning';
        iconBg = 'bg-warning/20';
        iconClass = 'fa-exclamation-triangle';
    } else if (type === 'danger') {
        borderColor = 'border-danger';
        iconColor = 'text-danger';
        iconBg = 'bg-danger/20';
        iconClass = 'fa-skull-crossbones';
    }

    return (
        <div className={`bg-gray-900 border-l-4 ${borderColor} rounded-lg p-6 ${type !== 'success' ? 'opacity-50' : ''}`}>
            <div className="flex items-center gap-4">
                <div className={`w-12 h-12 ${iconBg} rounded-full flex items-center justify-center`}>
                    <i className={`fa-solid ${iconClass} ${iconColor} text-xl`}></i>
                </div>
                <div>
                    <h3 className="font-semibold text-white mb-1">{title}</h3>
                    <p className="text-sm text-gray-400">{description}</p>
                </div>
            </div>
        </div>
    );
};

export default StatusCard;
