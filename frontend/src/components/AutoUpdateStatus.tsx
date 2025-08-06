import React, { useState, useEffect } from 'react';
import { ClockIcon, CheckCircleIcon, ExclamationTriangleIcon, ArrowPathIcon } from '@heroicons/react/24/outline';

interface AutoUpdateStatusProps {
  lastUpdateTime?: string;
  totalEvents?: number;
  dataSources?: number;
}

const AutoUpdateStatus: React.FC<AutoUpdateStatusProps> = ({ 
  lastUpdateTime, 
  totalEvents = 121, 
  dataSources = 5 
}) => {
  const [timeSinceUpdate, setTimeSinceUpdate] = useState<string>('');
  const [isUpdating, setIsUpdating] = useState(false);

  useEffect(() => {
    const updateTimeSince = () => {
      if (!lastUpdateTime) {
        setTimeSinceUpdate('Just now');
        return;
      }

      const now = new Date();
      const lastUpdate = new Date(lastUpdateTime);
      const diffInMinutes = Math.floor((now.getTime() - lastUpdate.getTime()) / (1000 * 60));

      if (diffInMinutes < 1) {
        setTimeSinceUpdate('Just now');
      } else if (diffInMinutes < 60) {
        setTimeSinceUpdate(`${diffInMinutes} minutes ago`);
      } else if (diffInMinutes < 1440) {
        const hours = Math.floor(diffInMinutes / 60);
        setTimeSinceUpdate(`${hours} hour${hours > 1 ? 's' : ''} ago`);
      } else {
        const days = Math.floor(diffInMinutes / 1440);
        setTimeSinceUpdate(`${days} day${days > 1 ? 's' : ''} ago`);
      }
    };

    updateTimeSince();
    const interval = setInterval(updateTimeSince, 60000); // Update every minute

    return () => clearInterval(interval);
  }, [lastUpdateTime]);

  const handleRefresh = () => {
    setIsUpdating(true);
    // Simulate refresh
    setTimeout(() => {
      setIsUpdating(false);
      window.location.reload();
    }, 2000);
  };

  const getStatusColor = () => {
    if (!lastUpdateTime) return 'text-green-600';
    
    const now = new Date();
    const lastUpdate = new Date(lastUpdateTime);
    const diffInHours = (now.getTime() - lastUpdate.getTime()) / (1000 * 60 * 60);
    
    if (diffInHours < 6) return 'text-green-600';
    if (diffInHours < 24) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getStatusIcon = () => {
    if (!lastUpdateTime) return CheckCircleIcon;
    
    const now = new Date();
    const lastUpdate = new Date(lastUpdateTime);
    const diffInHours = (now.getTime() - lastUpdate.getTime()) / (1000 * 60 * 60);
    
    if (diffInHours < 6) return CheckCircleIcon;
    if (diffInHours < 24) return ExclamationTriangleIcon;
    return ExclamationTriangleIcon;
  };

  const StatusIcon = getStatusIcon();

  return (
    <div className="bg-white rounded-lg shadow p-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className={`${getStatusColor()}`}>
            <StatusIcon className="h-5 w-5" />
          </div>
          <div>
            <h3 className="text-sm font-medium text-gray-900">Data Status</h3>
            <p className="text-xs text-gray-600">
              Last updated: {timeSinceUpdate}
            </p>
          </div>
        </div>
        
        <button
          onClick={handleRefresh}
          disabled={isUpdating}
          className={`inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded-md transition-colors ${
            isUpdating 
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed' 
              : 'bg-primary-100 text-primary-700 hover:bg-primary-200'
          }`}
        >
          <ArrowPathIcon className={`h-3 w-3 mr-1 ${isUpdating ? 'animate-spin' : ''}`} />
          {isUpdating ? 'Updating...' : 'Refresh'}
        </button>
      </div>

      {/* Stats */}
      <div className="mt-4 grid grid-cols-2 gap-4">
        <div className="text-center">
          <div className="text-lg font-bold text-gray-900">{totalEvents}+</div>
          <div className="text-xs text-gray-600">Total Events</div>
        </div>
        <div className="text-center">
          <div className="text-lg font-bold text-gray-900">{dataSources}</div>
          <div className="text-xs text-gray-600">Data Sources</div>
        </div>
      </div>

      {/* Update Schedule */}
      <div className="mt-4 pt-4 border-t border-gray-100">
        <div className="flex items-center justify-between text-xs text-gray-600">
          <span>Auto-updates every 6 hours</span>
          <ClockIcon className="h-3 w-3" />
        </div>
      </div>

      {/* Data Sources */}
      <div className="mt-3">
        <div className="text-xs text-gray-600 mb-2">Active Sources:</div>
        <div className="flex flex-wrap gap-1">
          {['NC State', 'UNC', 'Duke', 'Raleigh', 'Commerce'].map((source) => (
            <span
              key={source}
              className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800"
            >
              {source}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AutoUpdateStatus; 