import React, { useEffect, useMemo, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import AdvancedSearch from './AdvancedSearch';
import CategoryBubbles from './CategoryBubbles';
import InteractiveHeatMap from './InteractiveHeatMap';
import NCMap from './NCMap';
import { format } from 'date-fns';
import { eventService } from '../services/api';
import { Event } from '../types/Event';

const Dashboard: React.FC = () => {
  const [view, setView] = useState<'events' | 'holidays' | 'map'>('events');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedEventTypes, setSelectedEventTypes] = useState<string[]>([]);
  const [allEvents, setAllEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [mapMode, setMapMode] = useState<'live' | 'all'>('live');
  const navigate = useNavigate();

  // categories drive selectedEventTypes; no modal needed

  const handleCategorySelect = (category: any) => {
    setSelectedCategory(category.id);
    setSelectedEventTypes(category.eventTypes);
  };
  
  const handleDateSelect = (date: Date) => {
    navigate(`/day/${format(date, 'yyyy-MM-dd')}`);
  };

  const [mapOverlayDate, setMapOverlayDate] = useState<Date | null>(null);

  const handleSearch = (filters: any) => {
    setSelectedEventTypes(filters.eventTypes);
  };

  // Simple frontend validation to hide obviously bad events
  const isValidEvent = (ev: Event): boolean => {
    const start = new Date(ev.start_date).getTime();
    const end = new Date(ev.end_date).getTime();
    if (!Number.isFinite(start) || !Number.isFinite(end)) return false;
    if (end <= start) return false; // end before start
    const durationHours = (end - start) / (1000 * 60 * 60);
    if (durationHours > 14) return false; // unusually long single-day event
    // optional: filter obviously invalid geos
    if (ev.latitude == null || ev.longitude == null) return false;
    if (Math.abs(ev.latitude) > 90 || Math.abs(ev.longitude) > 180) return false;
    return true;
  };

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await eventService.getEvents();
        // Deduplicate by id and filter invalid
        const seen = new Set<number>();
        const cleaned = data.filter(ev => {
          if (seen.has(ev.id)) return false;
          seen.add(ev.id);
          return isValidEvent(ev);
        });
        setAllEvents(cleaned);
      } catch (e) {
        setError('Failed to load events');
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const filteredEvents = useMemo(() => {
    if (!selectedEventTypes || selectedEventTypes.length === 0) return allEvents;
    return allEvents.filter(ev => selectedEventTypes.includes(ev.event_type));
  }, [allEvents, selectedEventTypes]);

  return (
    <div className="p-6 max-w-6xl mx-auto font-sans">
      {/* Top Navigation */}
      <nav className="flex justify-between items-center mb-6">
        <Link to="/" className="text-2xl font-bold text-blue-500">
          EventPulse NC
        </Link>
        <div className="flex space-x-4">
          <Link to="/analytics" className="text-gray-600 hover:text-gray-800">
            Analytics
          </Link>
          <button onClick={() => setView('events')} className={
            `px-3 py-1 rounded ${view === 'events' ? 'bg-blue-500 text-white font-semibold' : 'bg-gray-200 text-gray-700'}`
          }>
            Events
          </button>
          <button onClick={() => setView('holidays')} className={
            `px-3 py-1 rounded ${view === 'holidays' ? 'bg-blue-500 text-white font-semibold' : 'bg-gray-200 text-gray-700'}`
          }>
            Holidays
          </button>
          <button onClick={() => setView('map')} className={
            `px-3 py-1 rounded ${view === 'map' ? 'bg-blue-500 text-white font-semibold' : 'bg-gray-200 text-gray-700'}`
          }>
            Map
          </button>
        </div>
      </nav>
      {/* Tagline */}
      <p className="text-center text-gray-600 mb-8">
        Never Miss What Matters in North Carolina
      </p>
      {loading && (
        <div className="text-center text-gray-500 mb-4">Loading events…</div>
      )}
      {/* Toggle Buttons */}
      {/* Main Panels */}
      {view === 'events' ? (
        <div className="space-y-6">
          {/* Advanced Search */}
          <AdvancedSearch
            onSearch={handleSearch}
            onClear={() => {
              setSelectedEventTypes([]);
              setSelectedCategory('all');
            }}
          />
          <div className="flex flex-col md:flex-row gap-6">
            <div className="md:w-1/3">
              <CategoryBubbles
                onCategorySelect={handleCategorySelect}
                selectedCategory={selectedCategory}
              />
            </div>
            <div className="md:flex-1">
              <InteractiveHeatMap
                onDateSelect={handleDateSelect}
                onOpenMapForDate={(d) => setMapOverlayDate(d)}
                selectedEventTypes={selectedEventTypes}
              />
            </div>
          </div>
        </div>
      ) : view === 'holidays' ? (
        <div className="flex flex-col md:flex-row gap-6">
          {/* Holidays Heatmap: show only holiday events */}
          <div className="md:flex-1">
            <InteractiveHeatMap
              onDateSelect={handleDateSelect}
              onOpenMapForDate={(d) => setMapOverlayDate(d)}
              selectedEventTypes={['holiday']}
            />
          </div>
        </div>
      ) : (
        <div className="space-y-6">
          <AdvancedSearch
            onSearch={handleSearch}
            onClear={() => {
              setSelectedEventTypes([]);
              setSelectedCategory('all');
            }}
          />
          {/* Map view controls */}
          <div className="flex items-center justify-center gap-3">
            <span className="text-sm text-gray-600">Map filter:</span>
            <button
              onClick={() => setMapMode('live')}
              className={`px-3 py-1 rounded text-sm ${mapMode === 'live' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'}`}
            >
              Live / Next Hour
            </button>
            <button
              onClick={() => setMapMode('all')}
              className={`px-3 py-1 rounded text-sm ${mapMode === 'all' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'}`}
            >
              All Events
            </button>
          </div>
          {error ? (
            <div className="text-center text-red-600">{error}</div>
          ) : (
            <NCMap events={filteredEvents} mode={mapMode} />
          )}
        </div>
      )}
      {/* no modal: use separate page for day events */}
      {mapOverlayDate && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50" onClick={() => setMapOverlayDate(null)}>
          <div className="bg-white rounded-lg shadow-xl p-4 w-11/12 max-w-5xl" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-3">
              <div className="text-lg font-semibold">Events on {format(mapOverlayDate, 'MMMM d, yyyy')}</div>
              <button className="text-gray-600 hover:text-gray-900" onClick={() => setMapOverlayDate(null)}>Close</button>
            </div>
            <NCMap
              events={filteredEvents.filter(ev => format(new Date(ev.start_date), 'yyyy-MM-dd') === format(mapOverlayDate, 'yyyy-MM-dd'))}
              mode={'all'}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
