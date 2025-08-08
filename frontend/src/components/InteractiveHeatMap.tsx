import React, { useState, useEffect } from 'react';
import { format, startOfMonth, endOfMonth, eachDayOfInterval, isSameMonth, isToday, isSameDay } from 'date-fns';
import { eventService } from '../services/api';
import { Event } from '../types/Event';

interface InteractiveHeatMapProps {
  selectedDate?: Date;
  onDateSelect: (date: Date) => void;
  onOpenMapForDate?: (date: Date) => void; // right-click handler
  selectedEventTypes?: string[];
}

const InteractiveHeatMap: React.FC<InteractiveHeatMapProps> = ({ selectedDate, onDateSelect, onOpenMapForDate, selectedEventTypes }) => {
  const [currentMonth, setCurrentMonth] = useState(startOfMonth(new Date())); // current month
  const [events, setEvents] = useState<Event[]>([]);
  const [eventCounts, setEventCounts] = useState<{ [key: string]: number }>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Try to get 2026 events first, then fall back to all events
        let data: Event[];
        try {
          data = await eventService.getEvents(); // Get all events since they're in 2026
          console.log(`✅ Loaded ${data.length} events for heatmap`);
        } catch (err) {
          console.log('⚠️ Could not get events, trying fallback');
          data = await eventService.getEvents();
          console.log(`✅ Loaded ${data.length} total events for heatmap`);
        }
        
        // Apply simple validation and then category filter
        const isValid = (e: Event) => {
          const s = new Date(e.start_date).getTime();
          const en = new Date(e.end_date).getTime();
          if (!Number.isFinite(s) || !Number.isFinite(en)) return false;
          if (en <= s) return false;
          const hours = (en - s) / (1000 * 60 * 60);
          if (hours > 14) return false;
          return true;
        };

        const validated = data.filter(isValid);
        const filteredData = selectedEventTypes && selectedEventTypes.length > 0
          ? validated.filter(e => selectedEventTypes!.includes(e.event_type))
          : validated;
        setEvents(filteredData);
        
        // Calculate event counts for each date
        const counts: { [key: string]: number } = {};
        filteredData.forEach(event => {
          const dateKey = format(new Date(event.start_date), 'yyyy-MM-dd');
          counts[dateKey] = (counts[dateKey] || 0) + 1;
        });
        setEventCounts(counts);
        
        // Debug: Log some event counts
        const totalDates = Object.keys(counts).length;
        const totalEvents = Object.values(counts).reduce((sum, count) => sum + count, 0);
        console.log(`📊 Heatmap stats: ${totalEvents} events across ${totalDates} dates`);
        
        // Log some sample dates with events
        const sampleDates = Object.entries(counts).slice(0, 5);
        console.log('📅 Sample dates with events:', sampleDates);
        
      } catch (error) {
        console.error('❌ Error fetching events for heat map:', error);
        setError('Failed to load events');
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, [selectedEventTypes]);

  const monthStart = startOfMonth(currentMonth);
  const monthEnd = endOfMonth(currentMonth);
  const days = eachDayOfInterval({ start: monthStart, end: monthEnd });

  const getEventCount = (date: Date) => {
    const dateKey = format(date, 'yyyy-MM-dd');
    return eventCounts[dateKey] || 0;
  };

  const getHeatColor = (count: number) => {
    if (count === 0) return '#f8fafc'; // Lighter background for no events
    if (count <= 2) return '#bfdbfe'; // Light blue - more vibrant
    if (count <= 5) return '#60a5fa'; // Medium blue - more saturated
    if (count <= 10) return '#2563eb'; // Dark blue - more intense
    if (count <= 15) return '#1d4ed8'; // Very dark blue
    if (count <= 20) return '#1e40af'; // Deep blue
    if (count <= 30) return '#1e3a8a'; // Very deep blue
    return '#0f172a'; // Darkest blue for 30+ events
  };

  const navigateMonth = (direction: 'prev' | 'next') => {
    setCurrentMonth(prev => {
      const newMonth = new Date(prev);
      if (direction === 'prev') {
        newMonth.setMonth(prev.getMonth() - 1);
      } else {
        newMonth.setMonth(prev.getMonth() + 1);
      }
      return newMonth;
    });
  };

  if (loading) {
    return (
      <div style={{ padding: '1rem 0', textAlign: 'center' }}>
        <div style={{ fontSize: '1.125rem', color: '#6b7280' }}>
          Loading events for heatmap...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '1rem 0', textAlign: 'center' }}>
        <div style={{ fontSize: '1.125rem', color: '#dc2626' }}>
          Error: {error}
        </div>
      </div>
    );
  }

  return (
    <div style={{ padding: '1rem 0' }}>
      <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#111827', marginBottom: '0.5rem' }}>
          Event Calendar
        </h2>
        <p style={{ color: '#6b7280', fontSize: '1rem' }}>
          Click any date to see events happening on that day
        </p>
        <p style={{ color: '#059669', fontSize: '0.875rem', marginTop: '0.5rem' }}>
          Loaded {events.length} events • {Object.keys(eventCounts).length} dates with events
        </p>
      </div>

      <div style={{
        backgroundColor: 'white',
        borderRadius: '1rem',
        padding: '1.5rem',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        maxWidth: '800px',
        margin: '0 auto'
      }}>
        {/* Month Navigation */}
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center', 
          marginBottom: '2rem' 
        }}>
          <button
            onClick={() => navigateMonth('prev')}
            style={{
              backgroundColor: 'transparent',
              border: 'none',
              cursor: 'pointer',
              padding: '0.5rem',
              borderRadius: '0.5rem',
              color: '#6b7280'
            }}
          >
            <svg style={{ width: '1.25rem', height: '1.25rem' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          
          <h3 style={{ fontSize: '1.25rem', fontWeight: '600', color: '#111827' }}>
            {format(currentMonth, 'MMMM yyyy')}
          </h3>
          
          <button
            onClick={() => navigateMonth('next')}
            style={{
              backgroundColor: 'transparent',
              border: 'none',
              cursor: 'pointer',
              padding: '0.5rem',
              borderRadius: '0.5rem',
              color: '#6b7280'
            }}
          >
            <svg style={{ width: '1.25rem', height: '1.25rem' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>

        {/* Day Headers */}
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(7, 1fr)', 
          gap: '0.5rem', 
          marginBottom: '0.5rem' 
        }}>
          {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
            <div key={day} style={{ 
              textAlign: 'center', 
              fontWeight: '600', 
              color: '#6b7280', 
              fontSize: '0.875rem',
              padding: '0.5rem'
            }}>
              {day}
            </div>
          ))}
        </div>

        {/* Calendar Grid */}
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(7, 1fr)', 
          gap: '0.5rem' 
        }}>
          {days.map((day, index) => {
            const eventCount = getEventCount(day);
            const isCurrentMonth = isSameMonth(day, currentMonth);
            const isCurrentDay = isToday(day);
            const isSelected = selectedDate && isSameDay(day, selectedDate);
            
            return (
              <div
                key={index}
                onClick={() => {
                  if (isCurrentMonth) {
                    onDateSelect(day);
                  }
                }}
                style={{
                  aspectRatio: '1',
                  backgroundColor: isSelected ? '#2563eb' : getHeatColor(eventCount),
                  color: isSelected ? 'white' : isCurrentDay ? '#dc2626' : '#374151',
                  border: isCurrentDay ? '2px solid #dc2626' : '1px solid #e5e7eb',
                  borderRadius: '0.5rem',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  cursor: isCurrentMonth ? 'pointer' : 'default',
                  opacity: isCurrentMonth ? 1 : 0.3,
                  position: 'relative',
                  transition: 'all 0.2s ease-in-out',
                  transform: isSelected ? 'scale(1.05)' : 'none'
                }}
                onContextMenu={(e) => {
                  if (!isCurrentMonth) return;
                  e.preventDefault();
                  if (onOpenMapForDate) onOpenMapForDate(day);
                }}
                onMouseEnter={(e) => {
                  if (isCurrentMonth && !isSelected) {
                    e.currentTarget.style.transform = 'scale(1.02)';
                    e.currentTarget.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
                  }
                }}
                onMouseLeave={(e) => {
                  if (isCurrentMonth && !isSelected) {
                    e.currentTarget.style.transform = 'none';
                    e.currentTarget.style.boxShadow = 'none';
                  }
                }}
              >
                <span style={{ 
                  fontSize: '0.875rem', 
                  fontWeight: isCurrentDay ? '700' : '500'
                }}>
                  {format(day, 'd')}
                </span>
                
                {eventCount > 0 && (
                  <div style={{
                    position: 'absolute',
                    top: '2px',
                    right: '2px',
                    backgroundColor: isSelected ? 'white' : '#ef4444',
                    color: isSelected ? '#2563eb' : 'white',
                    borderRadius: '50%',
                    width: '1.25rem',
                    height: '1.25rem',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '0.625rem',
                    fontWeight: '600'
                  }}>
                    {eventCount}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Legend */}
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          gap: '1rem', 
          marginTop: '2rem',
          padding: '1rem',
          backgroundColor: '#f9fafb',
          borderRadius: '0.5rem',
          flexWrap: 'wrap'
        }}>
          <span style={{ fontSize: '0.875rem', color: '#6b7280', fontWeight: '600' }}>Event Count:</span>
          {[0, 1, 3, 6, 11, 16, 21, 31].map((count, index) => (
            <div key={index} style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
              <div style={{
                width: '1.25rem',
                height: '1.25rem',
                backgroundColor: getHeatColor(count),
                borderRadius: '0.375rem',
                border: '1px solid #e5e7eb',
                boxShadow: '0 1px 2px rgba(0, 0, 0, 0.1)'
              }} />
              <span style={{ fontSize: '0.75rem', color: '#6b7280', fontWeight: '500' }}>
                {count === 0 ? '0' : count === 21 ? '21-30' : count === 31 ? '30+' : count}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default InteractiveHeatMap; 