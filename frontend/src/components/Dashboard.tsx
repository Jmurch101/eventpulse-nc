import React, { useEffect, useMemo, useState } from 'react';
import { useNavigate, Link, useSearchParams } from 'react-router-dom';
import AdvancedSearch, { SearchFilters } from './AdvancedSearch';
import CategoryBubbles from './CategoryBubbles';
import InteractiveHeatMap from './InteractiveHeatMap';
import NCMap from './NCMap';
import SettingsPanel from './SettingsPanel';
import DayMapModal from './DayMapModal';
import HourlyHeatmap from './HourlyHeatmap';
import BubbleCluster from './BubbleCluster';
import { format } from 'date-fns';
import { eventService } from '../services/api';
import { Event } from '../types/Event';
import { downloadICS } from '../utils/exporters';
import { getFavorites } from '../utils/favorites';
import { detectRecurring } from '../utils/recurring';

const Dashboard: React.FC = () => {
  const [view, setView] = useState<'events' | 'holidays' | 'map' | 'favorites'>('events');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedEventTypes, setSelectedEventTypes] = useState<string[]>([]);
  const [allEvents, setAllEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [mapMode, setMapMode] = useState<'live' | 'all'>('live');
  const [activeFilters, setActiveFilters] = useState<SearchFilters | null>(null);
  const [searchParams, setSearchParams] = useSearchParams();
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
  const [savedViewsMenuOpen, setSavedViewsMenuOpen] = useState(false);
  const SAVED_VIEWS_KEY = 'eventpulse_saved_views_v1';
  const [onlyFavorites, setOnlyFavorites] = useState<boolean>(false);
  const [settingsOpen, setSettingsOpen] = useState<boolean>(false);
  const SETTINGS_KEY = 'eventpulse_settings_v1';
  type Settings = { defaultView: 'events' | 'holidays' | 'map' | 'favorites'; defaultCity: string; defaultRadius: number };

  type SavedView = {
    name: string;
    view: 'events' | 'holidays' | 'map' | 'favorites';
    selectedEventTypes: string[];
    activeFilters: SearchFilters | null;
    timestamp: number;
    onlyFavorites?: boolean;
  };

  const getSavedViews = (): SavedView[] => {
    try {
      return JSON.parse(localStorage.getItem(SAVED_VIEWS_KEY) || '[]');
    } catch {
      return [];
    }
  };

  const saveCurrentView = () => {
    const name = prompt('Save current filters as view name:');
    if (!name) return;
    const views = getSavedViews();
    const payload: SavedView = {
      name,
      view,
      selectedEventTypes,
      activeFilters,
      timestamp: Date.now(),
      onlyFavorites,
    };
    const updated = [payload, ...views.filter(v => v.name !== name)];
    localStorage.setItem(SAVED_VIEWS_KEY, JSON.stringify(updated.slice(0, 25)));
    setSavedViewsMenuOpen(false);
    alert('Saved view.');
  };

  const loadSavedView = (sv: SavedView) => {
    setView(sv.view);
    setSelectedEventTypes(sv.selectedEventTypes || []);
    setActiveFilters(sv.activeFilters || null);
    setOnlyFavorites(!!sv.onlyFavorites);
    setSavedViewsMenuOpen(false);
  };

  const deleteSavedView = (name: string) => {
    const views = getSavedViews().filter(v => v.name !== name);
    localStorage.setItem(SAVED_VIEWS_KEY, JSON.stringify(views));
    setSavedViewsMenuOpen(false);
  };

  // City centers for radius filtering (miles)
  const CITY_CENTERS = useMemo(() => ({
    raleigh: { lat: 35.7796, lon: -78.6382 },
    durham: { lat: 35.9940, lon: -78.8986 },
    chapel_hill: { lat: 35.9132, lon: -79.0558 },
    cary: { lat: 35.7915, lon: -78.7811 },
    morrisville: { lat: 35.8235, lon: -78.8256 },
    apex: { lat: 35.7327, lon: -78.8503 },
    holly_springs: { lat: 35.6513, lon: -78.8336 },
    fuquay_varina: { lat: 35.5843, lon: -78.8000 },
    charlotte: { lat: 35.2271, lon: -80.8431 },
    greensboro: { lat: 36.0726, lon: -79.7920 },
    asheville: { lat: 35.5951, lon: -82.5515 },
    fayetteville: { lat: 35.0527, lon: -78.8784 },
  }), []);

  const milesBetween = (lat1: number, lon1: number, lat2: number, lon2: number): number => {
    const toRad = (v: number) => (v * Math.PI) / 180;
    const R = 3958.8; // miles
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
      Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  };

  const handleSearch = (filters: SearchFilters) => {
    setActiveFilters(filters);
    setSelectedEventTypes(filters.eventTypes);
  };

  // Initialize state from URL search params
  useEffect(() => {
    // Load defaults first
    try {
      const raw = localStorage.getItem(SETTINGS_KEY);
      if (raw) {
        const s: Settings = JSON.parse(raw);
        if (s?.defaultView && !searchParams.get('view')) setView(s.defaultView);
        if (s?.defaultCity && !searchParams.get('city')) {
          setActiveFilters(prev => ({
            ...(prev || { query: '', eventTypes: [], dateRange: { start: '', end: '' }, location: { city: '', radius: 25 }, price: { min: 0, max: 1000 }, tags: [] }),
            location: { city: s.defaultCity, radius: s.defaultRadius || 25 }
          }));
        }
      }
    } catch {}

    const viewParam = searchParams.get('view') as 'events' | 'holidays' | 'map' | 'favorites' | null;
    const typesParam = searchParams.get('types');
    const cityParam = searchParams.get('city');
    const radiusParam = searchParams.get('radius');
    const startParam = searchParams.get('start');
    const endParam = searchParams.get('end');
    const qParam = searchParams.get('q');
    const favParam = searchParams.get('fav');

    if (viewParam && ['events', 'holidays', 'map', 'favorites'].includes(viewParam)) {
      setView(viewParam);
    }

    if (typesParam) {
      const t = typesParam.split(',').filter(Boolean);
      setSelectedEventTypes(t);
    }

    if (cityParam || startParam || endParam || radiusParam || qParam) {
      setActiveFilters({
        query: qParam || '',
        eventTypes: typesParam ? typesParam.split(',').filter(Boolean) : [],
        dateRange: { start: startParam || '', end: endParam || '' },
        location: { city: cityParam || '', radius: radiusParam ? Number(radiusParam) : 25 },
        price: { min: 0, max: 1000 },
        tags: []
      });
    }
    if (favParam === '1') setOnlyFavorites(true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Sync state to URL search params
  useEffect(() => {
    const params: Record<string, string> = {};
    params.view = view;
    if (selectedEventTypes.length > 0) params.types = selectedEventTypes.join(',');
    if (activeFilters) {
      if (activeFilters.query) params.q = activeFilters.query;
      if (activeFilters.location.city) params.city = activeFilters.location.city;
      if (activeFilters.location.radius) params.radius = String(activeFilters.location.radius);
      if (activeFilters.dateRange.start) params.start = activeFilters.dateRange.start;
      if (activeFilters.dateRange.end) params.end = activeFilters.dateRange.end;
    }
    if (onlyFavorites) params.fav = '1';
    setSearchParams(params);
  }, [view, selectedEventTypes, activeFilters, setSearchParams, onlyFavorites]);

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
    let list = allEvents;
    // text query
    if (activeFilters && activeFilters.query) {
      const q = activeFilters.query.toLowerCase();
      list = list.filter(ev =>
        (ev.title || '').toLowerCase().includes(q) ||
        (ev.description || '').toLowerCase().includes(q) ||
        (ev.location_name || '').toLowerCase().includes(q)
      );
    }
    // event types
    if (selectedEventTypes && selectedEventTypes.length > 0) {
      list = list.filter(ev => selectedEventTypes.includes(ev.event_type));
    }
    // date range
    if (activeFilters && (activeFilters.dateRange.start || activeFilters.dateRange.end)) {
      const start = activeFilters.dateRange.start ? new Date(activeFilters.dateRange.start) : null;
      const end = activeFilters.dateRange.end ? new Date(activeFilters.dateRange.end) : null;
      list = list.filter(ev => {
        const d = new Date(ev.start_date);
        if (start && d < start) return false;
        if (end && d > end) return false;
        return true;
      });
    }
    // city + radius filter (haversine). Fallback to substring match if missing coordinates
    if (activeFilters && activeFilters.location.city) {
      const key = activeFilters.location.city as keyof typeof CITY_CENTERS;
      const center = CITY_CENTERS[key];
      const radiusMiles = activeFilters.location.radius || 25;
      if (center) {
        list = list.filter(ev => {
          const hasCoords = Number.isFinite(ev.latitude) && Number.isFinite(ev.longitude) && Math.abs(ev.latitude) <= 90 && Math.abs(ev.longitude) <= 180;
          if (hasCoords) {
            return milesBetween(center.lat, center.lon, ev.latitude, ev.longitude) <= radiusMiles;
          }
          // fallback substring
          const cityLabel = key.replace('_', ' ').toLowerCase();
          return (ev.location_name || '').toLowerCase().includes(cityLabel);
        });
      }
    }
    // favorites-only filter
    if (onlyFavorites) {
      const favIds = new Set<number>(getFavorites());
      list = list.filter(ev => favIds.has(ev.id));
    }
    return list;
  }, [allEvents, selectedEventTypes, activeFilters, CITY_CENTERS, onlyFavorites]);

  // Export CSV for current filtered events
  const exportFilteredAsCSV = () => {
    const rows = [
      ['Title', 'Start', 'End', 'Location', 'Type', 'Source URL'],
      ...filteredEvents.map(ev => [
        ev.title,
        new Date(ev.start_date).toISOString(),
        new Date(ev.end_date).toISOString(),
        ev.location_name || '',
        ev.event_type,
        ev.source_url || ''
      ])
    ];
    const csv = rows.map(r => r.map(f => `"${String(f).replace(/"/g, '""')}"`).join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `eventpulse_export_${Date.now()}.csv`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  };

  const countsByType = useMemo(() => {
    const m: Record<string, number> = {};
    (selectedEventTypes.length > 0 ? filteredEvents : allEvents).forEach(ev => {
      m[ev.event_type] = (m[ev.event_type] || 0) + 1;
    });
    return m;
  }, [allEvents, filteredEvents, selectedEventTypes]);

  const recurringMap = useMemo(() => detectRecurring(allEvents), [allEvents]);

  return (
    <div className="p-6 max-w-6xl mx-auto font-sans">
      {/* Top Navigation */}
       <nav role="navigation" aria-label="Primary" className="flex justify-between items-center mb-6">
        <Link to="/" className="text-2xl font-bold text-blue-500">
          EventPulse NC
        </Link>
         <div className="flex space-x-2">
          <Link to="/analytics" className="text-gray-600 hover:text-gray-800">
            Analytics
          </Link>
          <button aria-pressed={view==='events'} aria-label="Show events view" onClick={() => setView('events')} className={
            `px-3 py-1 rounded ${view === 'events' ? 'bg-blue-500 text-white font-semibold' : 'bg-gray-200 text-gray-700'}`
          }>
            Events
          </button>
          <button aria-pressed={view==='holidays'} aria-label="Show holidays view" onClick={() => setView('holidays')} className={
            `px-3 py-1 rounded ${view === 'holidays' ? 'bg-blue-500 text-white font-semibold' : 'bg-gray-200 text-gray-700'}`
          }>
            Holidays
          </button>
          <button aria-pressed={view==='map'} aria-label="Show map view" onClick={() => setView('map')} className={
            `px-3 py-1 rounded ${view === 'map' ? 'bg-blue-500 text-white font-semibold' : 'bg-gray-200 text-gray-700'}`
          }>
            Map
          </button>
          <button aria-pressed={view==='favorites'} aria-label="Show favorites view" onClick={() => setView('favorites')} className={
            `px-3 py-1 rounded ${view === 'favorites' ? 'bg-blue-500 text-white font-semibold' : 'bg-gray-200 text-gray-700'}`
          }>
            Favorites
          </button>
              <button aria-label="Open settings" onClick={() => setSettingsOpen(true)} className="px-3 py-1 rounded bg-gray-200 text-gray-700 hover:bg-gray-300">Settings</button>
            <button onClick={exportFilteredAsCSV} className="px-3 py-1 rounded bg-green-500 text-white hover:bg-green-600">
             Export CSV
           </button>
            <button onClick={() => downloadICS(filteredEvents, 'eventpulse_filtered.ics', 'EventPulse NC - Filtered')}
             className="px-3 py-1 rounded bg-indigo-500 text-white hover:bg-indigo-600">
             Export ICS
           </button>
            <a
              href={(function(){
                const base = `${process.env.REACT_APP_API_URL || 'https://eventpulse-nc-backend-ea4ecf265b40.herokuapp.com'}/api/events.csv`;
                const params = new URLSearchParams();
                if (selectedEventTypes.length > 0) params.set('event_type', selectedEventTypes[0]);
                if (activeFilters?.query) params.set('search', activeFilters.query);
                if (activeFilters?.dateRange?.start) {
                  try { params.set('year', String(new Date(activeFilters.dateRange.start).getFullYear())); } catch {}
                }
                const qs = params.toString();
                return qs ? `${base}?${qs}` : base;
              })()}
              className="px-3 py-1 rounded bg-green-700 text-white hover:bg-green-800"
              target="_blank" rel="noreferrer"
            >Download CSV</a>
            <a
              href={(function(){
                const base = `${process.env.REACT_APP_API_URL || 'https://eventpulse-nc-backend-ea4ecf265b40.herokuapp.com'}/api/events.ics`;
                const params = new URLSearchParams();
                if (selectedEventTypes.length > 0) params.set('event_type', selectedEventTypes[0]);
                if (activeFilters?.query) params.set('search', activeFilters.query);
                if (activeFilters?.dateRange?.start) {
                  try { params.set('year', String(new Date(activeFilters.dateRange.start).getFullYear())); } catch {}
                }
                const qs = params.toString();
                return qs ? `${base}?${qs}` : base;
              })()}
              className="px-3 py-1 rounded bg-purple-500 text-white hover:bg-purple-600"
              target="_blank" rel="noreferrer"
            >Subscribe ICS</a>
            <div className="relative inline-block">
              <button
                onClick={() => setSavedViewsMenuOpen(v => !v)}
                className="px-3 py-1 rounded bg-teal-600 text-white hover:bg-teal-700"
              >Saved Views</button>
              {savedViewsMenuOpen && (
                <div className="absolute right-0 mt-2 w-80 bg-white border border-gray-200 rounded shadow-lg z-10 p-2">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-semibold text-gray-700">Saved Views</span>
                    <button onClick={saveCurrentView} className="text-xs px-2 py-1 rounded bg-blue-500 text-white">Save Current</button>
                  </div>
                  <div className="max-h-64 overflow-auto space-y-1">
                    {getSavedViews().length === 0 && (
                      <div className="text-xs text-gray-500">No saved views yet.</div>
                    )}
                    {getSavedViews().map((sv) => (
                      <div key={sv.name} className="flex items-center justify-between bg-gray-50 border border-gray-100 rounded p-2">
                        <div className="min-w-0">
                          <div className="text-sm font-medium text-gray-800 truncate">{sv.name}</div>
                          <div className="text-xs text-gray-500 truncate">{sv.view} • {sv.selectedEventTypes.join(', ') || 'all types'}{sv.onlyFavorites ? ' • favorites' : ''}</div>
                        </div>
                        <div className="flex items-center gap-1 shrink-0">
                          <button onClick={() => loadSavedView(sv)} className="text-xs px-2 py-1 rounded bg-green-500 text-white">Load</button>
                          <button onClick={() => deleteSavedView(sv.name)} className="text-xs px-2 py-1 rounded bg-red-500 text-white">Delete</button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
           <button
             onClick={() => { navigator.clipboard?.writeText(window.location.href); }}
             className="px-3 py-1 rounded bg-gray-800 text-white hover:bg-black"
             aria-label="Copy shareable link"
           >Share</button>
        </div>
      </nav>
      {/* Settings Modal */}
      {settingsOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div className="absolute inset-0 bg-black/40" onClick={() => setSettingsOpen(false)} />
          <div className="relative bg-white rounded-lg shadow p-4 w-full max-w-md">
            <div className="flex items-center justify-between mb-3">
              <div className="font-semibold">Settings</div>
              <button onClick={() => setSettingsOpen(false)} className="text-sm text-gray-600">Close</button>
            </div>
            <SettingsPanel onSave={(s) => {
              localStorage.setItem(SETTINGS_KEY, JSON.stringify(s));
              setSettingsOpen(false);
            }} />
          </div>
        </div>
      )}
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
          <div className="flex items-center justify-center gap-4">
            <button
              onClick={() => setOnlyFavorites(v => !v)}
              className={`px-3 py-1 rounded text-sm ${onlyFavorites ? 'bg-yellow-400 text-yellow-900' : 'bg-yellow-100 text-yellow-800'}`}
              aria-pressed={onlyFavorites}
            >{onlyFavorites ? 'Showing Favorites' : 'Only Favorites'}</button>
          </div>
          <div className="flex flex-col md:flex-row gap-4">
            <div className="md:w-1/3 space-y-3">
              <CategoryBubbles
                onCategorySelect={handleCategorySelect}
                selectedCategory={selectedCategory}
                countsByType={countsByType}
              />
              <BubbleCluster countsByType={countsByType} onSelect={(t) => setSelectedEventTypes([t])} />
            </div>
            <div className="md:flex-1">
              <InteractiveHeatMap
                onDateSelect={handleDateSelect}
                onOpenMapForDate={(d) => setMapOverlayDate(d)}
                selectedEventTypes={selectedEventTypes}
              />
              <div className="mt-3">
                <HourlyHeatmap events={filteredEvents} compact defaultCollapsed showHourLabels />
              </div>
            </div>
          </div>
        </div>
      ) : view === 'holidays' ? (
        <div className="flex flex-col lg:flex-row gap-6">
          <div className="lg:flex-1">
            <div className="mb-4 rounded-md border border-yellow-200 bg-yellow-50 p-3 text-sm text-yellow-800">
              Holidays view shows official and academic breaks across NC. Click a date to see all holiday events; right‑click to open the map.
            </div>
            <InteractiveHeatMap
              onDateSelect={handleDateSelect}
              onOpenMapForDate={(d) => setMapOverlayDate(d)}
              selectedEventTypes={['holiday']}
            />
          </div>
          <div className="lg:w-1/3 bg-white rounded-lg shadow p-4 h-fit">
            <h3 className="text-sm font-semibold text-gray-800 mb-2">Upcoming Holidays</h3>
            <ul className="space-y-2">
              {allEvents
                .filter(ev => ev.event_type === 'holiday')
                .filter(ev => new Date(ev.start_date).getTime() >= Date.now())
                .sort((a, b) => new Date(a.start_date).getTime() - new Date(b.start_date).getTime())
                .slice(0, 10)
                .map(ev => (
                  <li key={ev.id} className="flex items-start gap-2 border border-gray-100 rounded p-2">
                    <div className="text-xs text-gray-500 w-20 shrink-0">
                      {format(new Date(ev.start_date), 'MMM d')}
                    </div>
                    <div className="text-sm text-gray-800 leading-snug">
                      <div className="font-medium">{ev.title}</div>
                      {ev.location_name && (
                        <div className="text-xs text-gray-500">{ev.location_name}</div>
                      )}
                    </div>
                  </li>
                ))}
              {allEvents.filter(ev => ev.event_type === 'holiday' && new Date(ev.start_date).getTime() >= Date.now()).length === 0 && (
                <li className="text-xs text-gray-500">No upcoming holidays found.</li>
              )}
            </ul>
          </div>
        </div>
      ) : view === 'map' ? (
        <div className="space-y-6">
          <AdvancedSearch
            onSearch={handleSearch}
            onClear={() => {
              setSelectedEventTypes([]);
              setSelectedCategory('all');
            }}
          />
          {/* Map view controls */}
          <div className="flex flex-col items-center gap-3">
            <div className="flex items-center gap-3">
              <span className="text-sm text-gray-600">Event types:</span>
              {['academic','government','city','holiday'].map(t => (
                <label key={t} className="text-sm text-gray-700 inline-flex items-center gap-1">
                  <input
                    type="checkbox"
                    checked={selectedEventTypes.includes(t)}
                    onChange={() => {
                      setSelectedEventTypes(prev => prev.includes(t) ? prev.filter(x => x !== t) : [...prev, t]);
                    }}
                  />
                  <span className="capitalize">{t}</span>
                </label>
              ))}
            </div>
            <div className="flex items-center gap-3">
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
          </div>
          {error ? (
            <div className="text-center text-red-600">{error}</div>
          ) : (
            <NCMap events={filteredEvents} mode={mapMode} />
          )}
        </div>
      ) : (
        <div className="space-y-6">
          <div className="mb-2 text-sm text-gray-600">Favorited events</div>
          <div className="grid md:grid-cols-2 gap-4">
            {filteredEvents.filter(ev => getFavorites().includes(ev.id)).map(ev => (
              <Link key={ev.id} to={`#/event/${ev.id}`} className="block border border-gray-200 rounded p-3 hover:shadow">
                <div className="text-sm font-semibold text-gray-900 truncate">{ev.title}</div>
                <div className="text-xs text-gray-500 truncate">{new Date(ev.start_date).toLocaleString()} • {ev.location_name}</div>
                <div className="text-xs text-gray-600 mt-1">{ev.event_type}</div>
                {recurringMap.has(ev.id) && (
                  <div className="mt-1 inline-flex items-center px-2 py-0.5 rounded bg-yellow-100 text-yellow-800 text-[10px]">Recurring</div>
                )}
              </Link>
            ))}
            {filteredEvents.filter(ev => getFavorites().includes(ev.id)).length === 0 && (
              <div className="text-sm text-gray-500">No favorites yet. Mark events as ★ Favorite from the event page.</div>
            )}
          </div>
        </div>
      )}
      {/* no modal: use separate page for day events */}
      {mapOverlayDate && (
        <DayMapModal
          isOpen={true}
          onClose={() => setMapOverlayDate(null)}
          selectedDate={mapOverlayDate}
          events={filteredEvents}
        />
      )}
    </div>
  );
};

export default Dashboard;
