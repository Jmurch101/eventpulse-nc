import React, { useState, useEffect } from 'react';
import { Event } from '../types/Event';
import { eventService } from '../services/api';
import { format, isToday, isTomorrow, isThisWeek } from 'date-fns';

interface EventListProps {
  selectedCategory?: string;
  selectedDate?: Date;
  onEventClick?: (event: Event) => void;
  searchQuery?: string;
  filters?: {
    eventType: string;
    dateRange: string;
    location: string;
  };
  sortBy?: string;
}

const EventList: React.FC<EventListProps> = ({ 
  selectedCategory, 
  selectedDate, 
  onEventClick,
  searchQuery = '',
  filters = { eventType: 'all', dateRange: 'all', location: 'all' },
  sortBy = 'date'
}) => {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);
  const [filteredEvents, setFilteredEvents] = useState<Event[]>([]);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const data = await eventService.getEvents();
        setEvents(data);
      } catch (error) {
        console.error('Error fetching events:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, []);

  useEffect(() => {
    let filtered = events;

    // Filter by category
    if (selectedCategory && selectedCategory !== 'all') {
      const categoryMap: { [key: string]: string[] } = {
        'university': ['academic'],
        'government': ['government'],
        'school-holidays': ['holiday'],
        'official-holidays': ['holiday'],
        'workshops': ['academic'],
        'tech': ['academic'],
        'community': ['government']
      };

      const eventTypes = categoryMap[selectedCategory] || [];
      filtered = filtered.filter(event => eventTypes.includes(event.event_type));
    }

    // Filter by date
    if (selectedDate) {
      const selectedDateStr = format(selectedDate, 'yyyy-MM-dd');
      filtered = filtered.filter(event => 
        format(new Date(event.start_date), 'yyyy-MM-dd') === selectedDateStr
      );
    }

    // Filter by search query
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(event =>
        event.title.toLowerCase().includes(query) ||
        event.description.toLowerCase().includes(query) ||
        event.location_name.toLowerCase().includes(query)
      );
    }

    // Filter by event type
    if (filters.eventType && filters.eventType !== 'all') {
      filtered = filtered.filter(event => event.event_type === filters.eventType);
    }

    // Filter by location
    if (filters.location && filters.location !== 'all') {
      filtered = filtered.filter(event => 
        event.location_name.toLowerCase().includes(filters.location.toLowerCase())
      );
    }

    // Sort events
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'date':
          return new Date(a.start_date).getTime() - new Date(b.start_date).getTime();
        case 'date-desc':
          return new Date(b.start_date).getTime() - new Date(a.start_date).getTime();
        case 'title':
          return a.title.localeCompare(b.title);
        case 'title-desc':
          return b.title.localeCompare(a.title);
        case 'type':
          return a.event_type.localeCompare(b.event_type);
        case 'location':
          return a.location_name.localeCompare(b.location_name);
        default:
          return 0;
      }
    });

    setFilteredEvents(filtered);
  }, [events, selectedCategory, selectedDate, searchQuery, filters, sortBy]);

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
      case 'academic': return { backgroundColor: '#dbeafe', color: '#1e40af', borderColor: '#93c5fd' };
      case 'government': return { backgroundColor: '#dcfce7', color: '#166534', borderColor: '#86efac' };
      case 'holiday': return { backgroundColor: '#f3e8ff', color: '#7c3aed', borderColor: '#c4b5fd' };
      default: return { backgroundColor: '#f3f4f6', color: '#374151', borderColor: '#d1d5db' };
    }
  };

  const getDateBadge = (date: Date) => {
    if (isToday(date)) return { backgroundColor: '#fee2e2', color: '#991b1b', borderColor: '#fca5a5' };
    if (isTomorrow(date)) return { backgroundColor: '#fed7aa', color: '#c2410c', borderColor: '#fdba74' };
    if (isThisWeek(date)) return { backgroundColor: '#fef3c7', color: '#92400e', borderColor: '#fcd34d' };
    return { backgroundColor: '#f3f4f6', color: '#374151', borderColor: '#d1d5db' };
  };

  const getDateText = (date: Date) => {
    if (isToday(date)) return 'Today';
    if (isTomorrow(date)) return 'Tomorrow';
    if (isThisWeek(date)) return format(date, 'EEEE');
    return format(date, 'MMM d, yyyy');
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '16rem' }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ 
            border: '4px solid #f3f4f6', 
            borderTop: '4px solid #2563eb', 
            borderRadius: '50%', 
            width: '1.5rem', 
            height: '1.5rem', 
            animation: 'spin 1s linear infinite',
            margin: '0 auto 1rem auto'
          }}></div>
          <p style={{ color: '#6b7280', fontSize: '0.875rem' }}>Loading events...</p>
        </div>
      </div>
    );
  }

  if (filteredEvents.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '3rem 1rem' }}>
        <h3 style={{ fontSize: '1.25rem', fontWeight: '600', color: '#374151', marginBottom: '0.5rem' }}>
          No events found
        </h3>
        <p style={{ color: '#6b7280' }}>
          {searchQuery 
            ? `No events match "${searchQuery}"`
            : selectedCategory && selectedCategory !== 'all' 
              ? `No ${selectedCategory.replace('-', ' ')} events found.`
              : 'No events match your current filters.'
          }
        </p>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      {/* Results Summary */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        padding: '1rem',
        backgroundColor: 'white',
        borderRadius: '0.5rem',
        boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)'
      }}>
        <div>
          <h3 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#111827' }}>
            {filteredEvents.length} event{filteredEvents.length !== 1 ? 's' : ''} found
          </h3>
          {searchQuery && (
            <p style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '0.25rem' }}>
              Matching "{searchQuery}"
            </p>
          )}
        </div>
        <div style={{ fontSize: '0.875rem', color: '#6b7280' }}>
          Sorted by {sortBy.replace('-', ' ')}
        </div>
      </div>

      {filteredEvents.map((event) => (
        <div 
          key={event.id} 
          onClick={() => onEventClick?.(event)}
          style={{
            backgroundColor: 'white',
            borderRadius: '0.5rem',
            boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
            padding: '1rem',
            cursor: onEventClick ? 'pointer' : 'default',
            transition: 'all 0.2s ease-in-out',
            border: '1px solid transparent'
          }}
          onMouseEnter={(e) => {
            if (onEventClick) {
              e.currentTarget.style.transform = 'translateY(-1px)';
              e.currentTarget.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)';
              e.currentTarget.style.borderColor = '#2563eb';
            }
          }}
          onMouseLeave={(e) => {
            if (onEventClick) {
              e.currentTarget.style.transform = 'none';
              e.currentTarget.style.boxShadow = '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)';
              e.currentTarget.style.borderColor = 'transparent';
            }
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
            <div style={{ flex: 1 }}>
              <h3 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#111827', marginBottom: '0.5rem' }}>
                {event.title}
              </h3>
              <p style={{ color: '#6b7280', marginBottom: '0.75rem', lineHeight: '1.5' }}>
                {event.description}
              </p>
              
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', alignItems: 'center' }}>
                <span 
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '0.25rem',
                    padding: '0.25rem 0.5rem',
                    borderRadius: '0.375rem',
                    fontSize: '0.75rem',
                    fontWeight: '500',
                    border: '1px solid',
                    ...getEventTypeColor(event.event_type)
                  }}
                >
                  {getEventTypeIcon(event.event_type)} {event.event_type}
                </span>
                
                <span 
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '0.25rem',
                    padding: '0.25rem 0.5rem',
                    borderRadius: '0.375rem',
                    fontSize: '0.75rem',
                    fontWeight: '500',
                    border: '1px solid',
                    ...getDateBadge(new Date(event.start_date))
                  }}
                >
                  📅 {getDateText(new Date(event.start_date))}
                </span>
              </div>
            </div>
            
            {onEventClick && (
              <div style={{ marginLeft: '1rem' }}>
                <svg style={{ width: '1rem', height: '1rem', color: '#9ca3af' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            )}
          </div>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', fontSize: '0.875rem', color: '#6b7280' }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
              📍 {event.location_name || 'Location TBD'}
            </span>
            <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
              🕐 {format(new Date(event.start_date), 'h:mm a')}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default EventList; 