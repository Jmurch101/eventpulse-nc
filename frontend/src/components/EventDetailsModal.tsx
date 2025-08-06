import React from 'react';
import { Event } from '../types/Event';
import { format } from 'date-fns';

interface EventDetailsModalProps {
  event: Event | null;
  isOpen: boolean;
  onClose: () => void;
}

const EventDetailsModal: React.FC<EventDetailsModalProps> = ({ event, isOpen, onClose }) => {
  if (!isOpen || !event) return null;

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
      case 'academic': return { backgroundColor: '#dbeafe', color: '#1e40af' };
      case 'government': return { backgroundColor: '#dcfce7', color: '#166534' };
      case 'holiday': return { backgroundColor: '#f3e8ff', color: '#7c3aed' };
      default: return { backgroundColor: '#f3f4f6', color: '#374151' };
    }
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '1rem'
    }}>
      <div style={{
        backgroundColor: 'white',
        borderRadius: '1rem',
        maxWidth: '600px',
        width: '100%',
        maxHeight: '90vh',
        overflow: 'auto',
        position: 'relative',
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)'
      }}>
        {/* Header */}
        <div style={{
          padding: '1.5rem',
          borderBottom: '1px solid #e5e7eb',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start'
        }}>
          <div style={{ flex: 1 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
              <span style={{
                fontSize: '1.25rem',
                width: '2rem',
                height: '2rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                backgroundColor: getEventTypeColor(event.event_type).backgroundColor,
                borderRadius: '0.5rem'
              }}>
                {getEventTypeIcon(event.event_type)}
              </span>
              <span style={{
                padding: '0.25rem 0.75rem',
                borderRadius: '0.375rem',
                fontSize: '0.75rem',
                fontWeight: '600',
                ...getEventTypeColor(event.event_type)
              }}>
                {event.event_type.charAt(0).toUpperCase() + event.event_type.slice(1)}
              </span>
            </div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: '700', color: '#111827', lineHeight: '1.3' }}>
              {event.title}
            </h2>
          </div>
          
          <button
            onClick={onClose}
            style={{
              backgroundColor: 'transparent',
              border: 'none',
              cursor: 'pointer',
              padding: '0.5rem',
              borderRadius: '0.375rem',
              color: '#6b7280',
              marginLeft: '1rem'
            }}
          >
            <svg style={{ width: '1.5rem', height: '1.5rem' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div style={{ padding: '1.5rem' }}>
          {/* Description */}
          <div style={{ marginBottom: '2rem' }}>
            <h3 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#111827', marginBottom: '0.75rem' }}>
              About This Event
            </h3>
            <p style={{ color: '#4b5563', lineHeight: '1.6' }}>
              {event.description}
            </p>
          </div>

          {/* Event Details Grid */}
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
            gap: '1.5rem',
            marginBottom: '2rem'
          }}>
            {/* Date & Time */}
            <div style={{
              backgroundColor: '#f9fafb',
              padding: '1rem',
              borderRadius: '0.5rem'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                <span style={{ fontSize: '0.875rem' }}>📅</span>
                <h4 style={{ fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
                  Date & Time
                </h4>
              </div>
              <p style={{ color: '#6b7280', fontSize: '0.875rem' }}>
                {format(new Date(event.start_date), 'EEEE, MMMM d, yyyy')}
              </p>
              <p style={{ color: '#6b7280', fontSize: '0.875rem' }}>
                {format(new Date(event.start_date), 'h:mm a')} - {format(new Date(event.end_date), 'h:mm a')}
              </p>
            </div>

            {/* Location */}
            <div style={{
              backgroundColor: '#f9fafb',
              padding: '1rem',
              borderRadius: '0.5rem'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                <span style={{ fontSize: '0.875rem' }}>📍</span>
                <h4 style={{ fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
                  Location
                </h4>
              </div>
              <p style={{ color: '#6b7280', fontSize: '0.875rem' }}>
                {event.location_name || 'Location TBD'}
              </p>
              {event.latitude && event.longitude && (
                <p style={{ color: '#6b7280', fontSize: '0.75rem', marginTop: '0.25rem' }}>
                  📍 {event.latitude.toFixed(4)}, {event.longitude.toFixed(4)}
                </p>
              )}
            </div>

            {/* Organization */}
            <div style={{
              backgroundColor: '#f9fafb',
              padding: '1rem',
              borderRadius: '0.5rem'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                <span style={{ fontSize: '0.875rem' }}>🏢</span>
                <h4 style={{ fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
                  Organization
                </h4>
              </div>
              <p style={{ color: '#6b7280', fontSize: '0.875rem' }}>
                Organization ID: {event.organization_id}
              </p>
            </div>

            {/* Source */}
            <div style={{
              backgroundColor: '#f9fafb',
              padding: '1rem',
              borderRadius: '0.5rem'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                <span style={{ fontSize: '0.875rem' }}>🔗</span>
                <h4 style={{ fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
                  Source
                </h4>
              </div>
              {event.source_url ? (
                <a 
                  href={event.source_url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  style={{ 
                    color: '#2563eb', 
                    fontSize: '0.875rem',
                    textDecoration: 'underline'
                  }}
                >
                  View Original Source
                </a>
              ) : (
                <p style={{ color: '#6b7280', fontSize: '0.875rem' }}>
                  EventPulse NC
                </p>
              )}
            </div>
          </div>

          {/* Additional Info */}
          <div style={{
            backgroundColor: '#fef3c7',
            border: '1px solid #f59e0b',
            borderRadius: '0.5rem',
            padding: '1rem',
            marginBottom: '2rem'
          }}>
            <h4 style={{ fontSize: '0.875rem', fontWeight: '600', color: '#92400e', marginBottom: '0.5rem' }}>
              📊 Event Information
            </h4>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem' }}>
              <div>
                <span style={{ fontSize: '0.75rem', color: '#92400e', fontWeight: '500' }}>Event ID:</span>
                <p style={{ fontSize: '0.875rem', color: '#92400e' }}>{event.id}</p>
              </div>
              <div>
                <span style={{ fontSize: '0.75rem', color: '#92400e', fontWeight: '500' }}>Created:</span>
                <p style={{ fontSize: '0.875rem', color: '#92400e' }}>
                  {format(new Date(event.created_at), 'MMM d, yyyy')}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div style={{
          padding: '1.5rem',
          borderTop: '1px solid #e5e7eb',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <div style={{ fontSize: '0.875rem', color: '#6b7280' }}>
            EventPulse NC • Event #{event.id}
          </div>
          
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button
              onClick={onClose}
              style={{
                padding: '0.5rem 1rem',
                border: '1px solid #d1d5db',
                borderRadius: '0.375rem',
                backgroundColor: 'white',
                color: '#374151',
                fontSize: '0.875rem',
                fontWeight: '500',
                cursor: 'pointer'
              }}
            >
              Close
            </button>
            {event.source_url && (
              <a
                href={event.source_url}
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  padding: '0.5rem 1rem',
                  border: '1px solid #2563eb',
                  borderRadius: '0.375rem',
                  backgroundColor: '#2563eb',
                  color: 'white',
                  fontSize: '0.875rem',
                  fontWeight: '500',
                  textDecoration: 'none',
                  display: 'inline-block'
                }}
              >
                Visit Source
              </a>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default EventDetailsModal; 