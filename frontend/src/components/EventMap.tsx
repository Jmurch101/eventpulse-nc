import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { Event } from '../types/Event';
import { eventService } from '../services/api';
import { format } from 'date-fns';
import 'leaflet/dist/leaflet.css';

// Fix for default markers in React Leaflet
import L from 'leaflet';
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

interface EventMapProps {
  events?: Event[];
  onEventClick?: (event: Event) => void;
}

const EventMap: React.FC<EventMapProps> = ({ events: propEvents, onEventClick }) => {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        if (propEvents) {
          setEvents(propEvents);
        } else {
          const data = await eventService.getEvents();
          setEvents(data);
        }
      } catch (error) {
        console.error('Error fetching events for map:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, [propEvents]);

  const getEventTypeIcon = (eventType: string) => {
    switch (eventType.toLowerCase()) {
      case 'academic': return '📚';
      case 'government': return '🏛';
      case 'holiday': return '📅';
      case 'workshop': return '⚙️';
      case 'tech': return '⚡';
      case 'community': return '👥';
      default: return '📅';
    }
  };

  const getEventTypeColor = (eventType: string) => {
    switch (eventType) {
      case 'academic': return '#3b82f6';
      case 'government': return '#059669';
      case 'holiday': return '#7c3aed';
      default: return '#6b7280';
    }
  };

  // Filter events with valid coordinates
  const eventsWithLocation = events.filter(event => 
    event.latitude && event.longitude && 
    event.latitude !== 0 && event.longitude !== 0
  );

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '400px',
        backgroundColor: '#f9fafb',
        borderRadius: '0.5rem'
      }}>
        <div style={{ 
          width: '1.5rem', 
          height: '1.5rem', 
          backgroundColor: '#f3f4f6',
          borderRadius: '50%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          margin: '0 auto 1rem auto'
        }}>
          <div style={{ 
            border: '4px solid #f3f4f6', 
            borderTop: '4px solid #2563eb', 
            borderRadius: '50%', 
            width: '3rem', 
            height: '3rem', 
            animation: 'spin 1s linear infinite' 
          }}></div>
        </div>
      </div>
    );
  }

  if (eventsWithLocation.length === 0) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '400px',
        backgroundColor: '#f9fafb',
        borderRadius: '0.5rem',
        flexDirection: 'column',
        gap: '1rem'
      }}>
        <div style={{ fontSize: '0.875rem' }}>🗺️</div>
        <h3 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#374151' }}>
          No events with locations
        </h3>
        <p style={{ color: '#6b7280', textAlign: 'center' }}>
          Events with location data will appear on the map
        </p>
      </div>
    );
  }

  // Calculate center point for the map
  const centerLat = eventsWithLocation.reduce((sum, event) => sum + event.latitude, 0) / eventsWithLocation.length;
  const centerLng = eventsWithLocation.reduce((sum, event) => sum + event.longitude, 0) / eventsWithLocation.length;

  return (
    <div style={{
      backgroundColor: 'white',
      borderRadius: '0.75rem',
      padding: '1.5rem',
      boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
      marginBottom: '2rem'
    }}>
      <div style={{ marginBottom: '1rem' }}>
        <h3 style={{ fontSize: '1.25rem', fontWeight: '600', color: '#111827', marginBottom: '0.5rem' }}>
          Event Locations
        </h3>
        <p style={{ color: '#6b7280', fontSize: '0.875rem' }}>
          {eventsWithLocation.length} event{eventsWithLocation.length !== 1 ? 's' : ''} with location data
        </p>
      </div>

      <div style={{ height: '500px', borderRadius: '0.5rem', overflow: 'hidden' }}>
        <MapContainer
          center={[centerLat, centerLng]}
          zoom={8}
          style={{ height: '100%', width: '100%' }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          
          {eventsWithLocation.map((event) => (
            <Marker
              key={event.id}
              position={[event.latitude, event.longitude]}
              eventHandlers={{
                click: () => onEventClick?.(event)
              }}
            >
              <Popup>
                <div style={{ minWidth: '200px' }}>
                  <div style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    gap: '0.5rem', 
                    marginBottom: '0.5rem' 
                  }}>
                    <span style={{ fontSize: '1rem' }}>
                      {getEventTypeIcon(event.event_type)}
                    </span>
                    <span style={{
                      padding: '0.125rem 0.5rem',
                      borderRadius: '0.25rem',
                      fontSize: '0.75rem',
                      fontWeight: '500',
                      backgroundColor: getEventTypeColor(event.event_type),
                      color: 'white'
                    }}>
                      {event.event_type}
                    </span>
                  </div>
                  
                  <h4 style={{ 
                    fontSize: '0.875rem', 
                    fontWeight: '600', 
                    color: '#111827',
                    marginBottom: '0.25rem',
                    lineHeight: '1.3'
                  }}>
                    {event.title}
                  </h4>
                  
                  <p style={{ 
                    fontSize: '0.75rem', 
                    color: '#6b7280',
                    marginBottom: '0.5rem',
                    lineHeight: '1.4'
                  }}>
                    {event.description.length > 100 
                      ? `${event.description.substring(0, 100)}...` 
                      : event.description
                    }
                  </p>
                  
                  <div style={{ fontSize: '0.75rem', color: '#6b7280' }}>
                    <div style={{ marginBottom: '0.25rem' }}>
                      📅 {format(new Date(event.start_date), 'MMM d, yyyy h:mm a')}
                    </div>
                    <div>
                      📍 {event.location_name}
                    </div>
                  </div>
                  
                  {onEventClick && (
                    <button
                      onClick={() => onEventClick(event)}
                      style={{
                        marginTop: '0.5rem',
                        padding: '0.25rem 0.5rem',
                        backgroundColor: '#2563eb',
                        color: 'white',
                        border: 'none',
                        borderRadius: '0.25rem',
                        fontSize: '0.75rem',
                        fontWeight: '500',
                        cursor: 'pointer',
                        width: '100%'
                      }}
                    >
                      View Details
                    </button>
                  )}
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>

      {/* Legend */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        gap: '1.5rem', 
        marginTop: '1rem',
        padding: '1rem',
        backgroundColor: '#f9fafb',
        borderRadius: '0.5rem'
      }}>
        <span style={{ fontSize: '0.875rem', color: '#6b7280', fontWeight: '500' }}>
          Event Types:
        </span>
        {['academic', 'government', 'holiday'].map(type => (
          <div key={type} style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
            <div style={{
              width: '0.75rem',
              height: '0.75rem',
              backgroundColor: getEventTypeColor(type),
              borderRadius: '50%'
            }} />
            <span style={{ fontSize: '0.75rem', color: '#6b7280' }}>
              {type.charAt(0).toUpperCase() + type.slice(1)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EventMap; 