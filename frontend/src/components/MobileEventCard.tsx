import React from 'react';
import { Link } from 'react-router-dom';
import { MapPinIcon, ClockIcon, CalendarIcon } from '@heroicons/react/24/outline';
import { Event } from '../types/Event';
import { format } from 'date-fns';

interface MobileEventCardProps {
  event: Event;
  showLocation?: boolean;
}

const MobileEventCard: React.FC<MobileEventCardProps> = ({ event, showLocation = true }) => {
  const getEventTypeColor = (eventType: string) => {
    switch (eventType) {
      case 'academic': return 'bg-blue-100 text-blue-800';
      case 'government': return 'bg-green-100 text-green-800';
      case 'city': return 'bg-purple-100 text-purple-800';
      case 'holiday': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getEventTypeName = (eventType: string) => {
    return eventType.charAt(0).toUpperCase() + eventType.slice(1);
  };

  return (
    <Link
      to={`/events/${event.id}`}
      className="block bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200"
    >
      <div className="p-4">
        {/* Event Type Badge */}
        <div className="flex items-center justify-between mb-2">
          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getEventTypeColor(event.event_type)}`}>
            {getEventTypeName(event.event_type)}
          </span>
          <span className="text-xs text-gray-500">
            {format(new Date(event.start_date), 'MMM d')}
          </span>
        </div>

        {/* Event Title */}
        <h3 className="text-sm font-semibold text-gray-900 mb-2 line-clamp-2 leading-tight">
          {event.title}
        </h3>

        {/* Event Description */}
        {event.description && (
          <p className="text-xs text-gray-600 mb-3 line-clamp-2 leading-relaxed">
            {event.description}
          </p>
        )}

        {/* Event Details */}
        <div className="space-y-1">
          {/* Time */}
          <div className="flex items-center text-xs text-gray-600">
            <ClockIcon className="h-3 w-3 mr-1 flex-shrink-0" />
            <span>
              {format(new Date(event.start_date), 'h:mm a')} - {format(new Date(event.end_date), 'h:mm a')}
            </span>
          </div>

          {/* Date */}
          <div className="flex items-center text-xs text-gray-600">
            <CalendarIcon className="h-3 w-3 mr-1 flex-shrink-0" />
            <span>{format(new Date(event.start_date), 'EEEE, MMMM d, yyyy')}</span>
          </div>

          {/* Location */}
          {showLocation && event.location_name && (
            <div className="flex items-center text-xs text-gray-600">
              <MapPinIcon className="h-3 w-3 mr-1 flex-shrink-0" />
              <span className="truncate">{event.location_name}</span>
            </div>
          )}
        </div>

        {/* Quick Actions */}
        <div className="mt-3 pt-3 border-t border-gray-100">
          <div className="flex items-center justify-between">
            <span className="text-xs text-primary-600 font-medium">
              View Details →
            </span>
            {event.latitude && event.longitude && (
              <span className="text-xs text-green-600">
                📍 Has Location
              </span>
            )}
          </div>
        </div>
      </div>
    </Link>
  );
};

export default MobileEventCard; 