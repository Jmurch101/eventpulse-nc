import React, { useMemo, useState } from 'react';
import { XMarkIcon, MapPinIcon, ClockIcon, CalendarIcon } from '@heroicons/react/24/outline';
import { MapContainer, TileLayer, Popup, CircleMarker } from 'react-leaflet';
import { Event } from '../types/Event';
import { format } from 'date-fns';

interface DayMapModalProps {
  isOpen: boolean;
  onClose: () => void;
  selectedDate: Date | null;
  events: Event[];
}

const DayMapModal: React.FC<DayMapModalProps> = ({ isOpen, onClose, selectedDate, events }) => {
  const [selectedTypes, setSelectedTypes] = useState<string[]>(['academic','government','city','holiday']);
  const [mode, setMode] = useState<'all' | 'live'>('all');

  const dayEvents = useMemo(() => {
    if (!selectedDate) return [] as Event[];
    return events.filter(event => {
      const eventDate = new Date(event.start_date);
      return format(eventDate, 'yyyy-MM-dd') === format(selectedDate, 'yyyy-MM-dd');
    });
  }, [events, selectedDate]);

  const eventsWithLocation = useMemo(() => {
    const now = Date.now();
    const ONE_HOUR = 60 * 60 * 1000;
    return dayEvents.filter(event => {
      if (!event.latitude || !event.longitude) return false;
      if (event.latitude === 0 && event.longitude === 0) return false;
      if (!selectedTypes.includes(event.event_type)) return false;
      if (mode === 'live') {
        const start = new Date(event.start_date).getTime();
        const end = new Date(event.end_date).getTime();
        const isLive = start <= now && now < end;
        const isSoon = start > now && start - now <= ONE_HOUR;
        return isLive || isSoon;
      }
      return true;
    });
  }, [dayEvents, selectedTypes, mode]);

  if (!isOpen || !selectedDate) return null;

  const getEventTypeColor = (eventType: string) => {
    switch (eventType) {
      case 'academic': return '#3B82F6';
      case 'government': return '#10B981';
      case 'city': return '#8B5CF6';
      case 'holiday': return '#F59E0B';
      default: return '#6B7280';
    }
  };

  const getEventTypeName = (eventType: string) => {
    return eventType.charAt(0).toUpperCase() + eventType.slice(1);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        {/* Background overlay */}
        <div 
          className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
          onClick={onClose}
        />

        {/* Modal content */}
        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
          {/* Header */}
          <div className="bg-white px-6 py-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <MapPinIcon style={{ width: 12, height: 12 }} className="text-primary-600 mr-2" />
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    Events on {format(selectedDate, 'EEEE, MMMM d, yyyy')}
                  </h3>
                  <p className="text-sm text-gray-600">
                    {dayEvents.length} events • {eventsWithLocation.length} with locations
                  </p>
                </div>
              </div>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <XMarkIcon className="h-6 w-6" />
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="bg-white">
            {/* Filters */}
            <div className="px-6 pt-4 pb-2 flex flex-wrap items-center gap-3 text-xs text-gray-700">
              <div className="flex items-center gap-2">
                {['academic','government','city','holiday'].map(t => (
                  <label key={t} className="inline-flex items-center gap-1">
                    <input
                      type="checkbox"
                      checked={selectedTypes.includes(t)}
                      onChange={() => setSelectedTypes(prev => prev.includes(t) ? prev.filter(x => x !== t) : [...prev, t])}
                    />
                    <span className="capitalize">{t}</span>
                  </label>
                ))}
              </div>
              <div className="ml-auto flex items-center gap-2">
                <span>Show:</span>
                <button
                  className={`px-2 py-1 rounded ${mode === 'live' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-800'}`}
                  onClick={() => setMode('live')}
                >Live / Next Hour</button>
                <button
                  className={`px-2 py-1 rounded ${mode === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-800'}`}
                  onClick={() => setMode('all')}
                >All</button>
              </div>
            </div>
            {/* Map */}
            <div className="h-80 w-full">
              <MapContainer
                center={[35.7796, -78.6382]}
                zoom={11}
                style={{ height: '100%', width: '100%' }}
              >
                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                
                {eventsWithLocation.map((event) => (
                  <CircleMarker
                    key={event.id}
                    center={[event.latitude, event.longitude]}
                    radius={6}
                    fillColor={getEventTypeColor(event.event_type)}
                    color={getEventTypeColor(event.event_type)}
                    weight={1.5}
                    opacity={0.9}
                    fillOpacity={0.7}
                  >
                    <Popup>
                      <div className="p-2">
                        <h3 className="font-semibold text-gray-900 text-sm mb-1">
                          {event.title}
                        </h3>
                        <p className="text-xs text-gray-600 mb-2">
                          {event.location_name}
                        </p>
                        <p className="text-xs text-gray-500 mb-2">
                          {format(new Date(event.start_date), 'h:mm a')} - {format(new Date(event.end_date), 'h:mm a')}
                        </p>
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                          event.event_type === 'academic' ? 'bg-blue-100 text-blue-800' :
                          event.event_type === 'government' ? 'bg-green-100 text-green-800' :
                          event.event_type === 'city' ? 'bg-purple-100 text-purple-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {getEventTypeName(event.event_type)}
                        </span>
                      </div>
                    </Popup>
                  </CircleMarker>
                ))}
              </MapContainer>
            </div>

            {/* Events List */}
            <div className="p-6">
              <h4 className="text-lg font-semibold text-gray-900 mb-4">
                All Events on {format(selectedDate, 'MMM d, yyyy')}
              </h4>
              
              {dayEvents.length > 0 ? (
                <div className="space-y-3 max-h-64 overflow-y-auto">
                  {dayEvents.map((event) => (
                    <div key={event.id} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                      <div className="flex-shrink-0">
                        <ClockIcon style={{ width: 12, height: 12 }} className="text-gray-400" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h5 className="text-sm font-medium text-gray-900 truncate">
                          {event.title}
                        </h5>
                        <p className="text-sm text-gray-600">
                          {event.location_name}
                        </p>
                        <div className="flex items-center space-x-4 mt-1">
                          <span className="text-xs text-gray-500">
                            {format(new Date(event.start_date), 'h:mm a')} - {format(new Date(event.end_date), 'h:mm a')}
                          </span>
                          <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                            event.event_type === 'academic' ? 'bg-blue-100 text-blue-800' :
                            event.event_type === 'government' ? 'bg-green-100 text-green-800' :
                            event.event_type === 'city' ? 'bg-purple-100 text-purple-800' :
                            'bg-gray-100 text-gray-800'
                          }`}>
                            {getEventTypeName(event.event_type)}
                          </span>
                        </div>
                      </div>
                      {event.latitude && event.longitude && (
                        <div className="flex-shrink-0">
                          <MapPinIcon style={{ width: 12, height: 12 }} className="text-green-500" />
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <CalendarIcon className="h-6 w-6 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">No events scheduled for this day</p>
                </div>
              )}
            </div>
          </div>

          {/* Footer */}
          <div className="bg-gray-50 px-6 py-3 border-t border-gray-200">
            <div className="flex justify-between items-center">
              <p className="text-sm text-gray-600">
                Right-click any day on the calendar to view events
              </p>
              <button
                onClick={onClose}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DayMapModal; 