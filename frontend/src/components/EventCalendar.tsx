import React, { useState, useEffect } from 'react';
import { Calendar, dateFnsLocalizer } from 'react-big-calendar';
import { format, parse, startOfWeek, getDay } from 'date-fns';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import { eventService } from '../services/api';
import { Event } from '../types/Event';
import { CategoryBubble } from '../types/CategoryBubble';
import CategoryBubbles from './CategoryBubbles';
import DayMapModal from './DayMapModal';

const locales = {
  'en-US': require('date-fns/locale/en-US')
};

const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales
});

interface CalendarEvent {
  id: number;
  title: string;
  start: Date;
  end: Date;
  resource?: any;
  eventType: string;
  location: string;
}

const EventCalendar: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [calendarEvents, setCalendarEvents] = useState<CalendarEvent[]>([]);
  const [allEvents, setAllEvents] = useState<Event[]>([]);
  const [filteredEvents, setFilteredEvents] = useState<CalendarEvent[]>([]);
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [isDayMapOpen, setIsDayMapOpen] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const data = await eventService.getEvents();
        setAllEvents(data);
        
        // Convert events to calendar format
        const calEvents = data.map(event => ({
          id: event.id,
          title: event.title,
          start: new Date(event.start_date),
          end: new Date(event.end_date),
          eventType: event.event_type,
          location: event.location_name,
          resource: event
        }));
        
        setCalendarEvents(calEvents);
        setFilteredEvents(calEvents);
      } catch (error) {
        console.error('Error fetching events:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, []);

  const eventStyleGetter = (event: CalendarEvent) => {
    let backgroundColor = '#6B7280'; // default gray
    
    switch (event.eventType) {
      case 'academic':
        backgroundColor = '#3B82F6'; // blue
        break;
      case 'government':
        backgroundColor = '#10B981'; // green
        break;
      case 'city':
        backgroundColor = '#8B5CF6'; // purple
        break;
      case 'holiday':
        backgroundColor = '#F59E0B'; // amber
        break;
    }

    return {
      style: {
        backgroundColor,
        borderRadius: '4px',
        opacity: 0.8,
        color: 'white',
        border: '0px',
        display: 'block',
        fontSize: '12px'
      }
    };
  };

  const handleSelectEvent = (event: CalendarEvent) => {
    // Navigate to event detail page
    window.location.href = `/events/${event.id}`;
  };

  const handleSelectSlot = (slotInfo: { start: Date; end: Date; slots: Date[] }) => {
    // Handle day selection
    setSelectedDate(slotInfo.start);
    setIsDayMapOpen(true);
  };

  const handleCategorySelect = (category: CategoryBubble) => {
    setSelectedCategory(category.id);
    
    if (category.id === 'all') {
      setFilteredEvents(calendarEvents);
    } else {
      const filtered = calendarEvents.filter(event => 
        category.eventTypes.includes(event.eventType)
      );
      setFilteredEvents(filtered);
    }
  };

  const handleContextMenu = (event: React.MouseEvent, date: Date) => {
    event.preventDefault();
    setSelectedDate(date);
    setIsDayMapOpen(true);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Event Calendar</h1>
        <p className="text-gray-600 mt-2">
          View events in a calendar format. Right-click any day to see events on a map!
        </p>
        <div className="mt-4 text-sm text-gray-500">
          {filteredEvents.length} events scheduled
        </div>
      </div>

      {/* Category Bubbles */}
      <CategoryBubbles
        onCategorySelect={handleCategorySelect}
        selectedCategory={selectedCategory}
      />

      {/* Calendar */}
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="h-96">
          <Calendar
            localizer={localizer}
            events={filteredEvents}
            startAccessor="start"
            endAccessor="end"
            style={{ height: '100%' }}
            eventPropGetter={eventStyleGetter}
            onSelectEvent={handleSelectEvent}
            onSelectSlot={handleSelectSlot}
            selectable
            views={['month', 'week', 'day']}
            defaultView="month"
            tooltipAccessor={(event: CalendarEvent) => `${event.title} - ${event.location}`}
            popup
            step={60}
            timeslots={1}
            onNavigate={(newDate: Date) => {
              // Handle navigation if needed
            }}
            components={{
              month: {
                dateHeader: ({ date, ...props }: any) => (
                  <div
                    {...props}
                    onContextMenu={(e) => handleContextMenu(e, date)}
                    className="cursor-pointer hover:bg-gray-100 p-1 rounded"
                  >
                    {format(date, 'd')}
                  </div>
                )
              }
            }}
          />
        </div>
      </div>

      {/* Legend */}
      <div className="bg-white rounded-lg shadow p-4">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">Event Types</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[
            { type: 'academic', color: '#3B82F6', name: 'Academic' },
            { type: 'government', color: '#10B981', name: 'Government' },
            { type: 'city', color: '#8B5CF6', name: 'City' },
            { type: 'holiday', color: '#F59E0B', name: 'Holiday' }
          ].map(({ type, color, name }) => (
            <div key={type} className="flex items-center space-x-2">
              <div 
                className="w-4 h-4 rounded"
                style={{ backgroundColor: color }}
              ></div>
              <span className="text-sm text-gray-700">{name}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow p-4">
          <div className="text-2xl font-bold text-gray-900">{filteredEvents.length}</div>
          <div className="text-sm text-gray-600">Total Events</div>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <div className="text-2xl font-bold text-blue-600">
            {filteredEvents.filter(e => e.eventType === 'academic').length}
          </div>
          <div className="text-sm text-gray-600">Academic Events</div>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <div className="text-2xl font-bold text-green-600">
            {filteredEvents.filter(e => e.eventType === 'government').length}
          </div>
          <div className="text-sm text-gray-600">Government Events</div>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <div className="text-2xl font-bold text-purple-600">
            {filteredEvents.filter(e => e.eventType === 'city').length}
          </div>
          <div className="text-sm text-gray-600">City Events</div>
        </div>
      </div>

      {/* Day Map Modal */}
      <DayMapModal
        isOpen={isDayMapOpen}
        onClose={() => setIsDayMapOpen(false)}
        selectedDate={selectedDate}
        events={allEvents}
      />
    </div>
  );
};

export default EventCalendar; 