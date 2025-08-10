import React, { useState, useEffect, useCallback } from 'react';
import {
  CalendarIcon,
  MapPinIcon,
  ArrowTrendingUpIcon,
  ClockIcon
} from '@heroicons/react/24/outline';
import { eventService } from '../services/api';
import { Event } from '../types/Event';

interface AnalyticsData {
  totalEvents: number;
  eventsInRange: number;
  growthRatePercent: number;
  citiesCovered: number;
  eventsByType: { [key: string]: number };
  eventsByLocation: { [key: string]: number };
  upcomingEvents: Array<{
    id: number;
    title: string;
    start_date: string;
    event_type: string;
  }>;
  recentActivity: Array<{
    id: number;
    action: string;
    timestamp: string;
    details: string;
  }>;
}

const AnalyticsDashboard: React.FC = () => {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('7d'); // 7d, 30d, 90d
  const [ingestStats, setIngestStats] = useState<any | null>(null);

  const fetchAnalyticsData = useCallback(async () => {
    try {
      setLoading(true);
      const events: Event[] = await eventService.getEvents();

      const now = new Date();
      const days = timeRange === '7d' ? 7 : timeRange === '30d' ? 30 : 90;
      const rangeStart = new Date(now);
      rangeStart.setDate(now.getDate() - days);
      const prevRangeStart = new Date(rangeStart);
      prevRangeStart.setDate(rangeStart.getDate() - days);

      const toDate = (s: string) => new Date(s);
      const inRange = (e: Event, start: Date, end: Date) => {
        const d = toDate(e.start_date);
        return d >= start && d <= end;
      };

      const eventsInRange = events.filter(e => inRange(e, rangeStart, now));
      const prevEventsInRange = events.filter(e => inRange(e, prevRangeStart, rangeStart));

      // By type (within selected range)
      const eventsByType = eventsInRange.reduce<Record<string, number>>((acc, e) => {
        acc[e.event_type] = (acc[e.event_type] || 0) + 1;
        return acc;
      }, {});

      // Location extraction (very simple heuristic)
      const KNOWN_CITIES = [
        'Raleigh','Durham','Chapel Hill','Cary','Charlotte','Greensboro','Winston-Salem','Asheville','Fayetteville'
      ];
      const extractCity = (location: string): string => {
        if (!location) return 'Other';
        const match = KNOWN_CITIES.find(city => location.toLowerCase().includes(city.toLowerCase()));
        return match || 'Other';
      };
      const eventsByLocation = eventsInRange.reduce<Record<string, number>>((acc, e) => {
        const city = extractCity(e.location_name || '');
        acc[city] = (acc[city] || 0) + 1;
        return acc;
      }, {});

      // Upcoming events (next events after now)
      const upcomingEvents = [...events]
        .filter(e => toDate(e.start_date) >= now)
        .sort((a, b) => toDate(a.start_date).getTime() - toDate(b.start_date).getTime())
        .slice(0, 5)
        .map(e => ({ id: e.id, title: e.title, start_date: e.start_date, event_type: e.event_type }));

      // Recent activity from ingest timestamps
      const recentActivity = [...events]
        .filter(e => !!e.created_at)
        .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
        .slice(0, 5)
        .map((e, idx) => ({
          id: idx,
          action: 'Event Ingested',
          timestamp: e.created_at,
          details: e.title
        }));

      const growthRatePercent = prevEventsInRange.length === 0
        ? 100
        : ((eventsInRange.length - prevEventsInRange.length) / prevEventsInRange.length) * 100;

      const citiesCovered = Object.keys(
        events.reduce<Record<string, true>>((acc, e) => {
          acc[extractCity(e.location_name || '')] = true;
          return acc;
        }, {})
      ).length;

      setAnalyticsData({
        totalEvents: events.length,
        eventsInRange: eventsInRange.length,
        growthRatePercent,
        citiesCovered,
        eventsByType,
        eventsByLocation,
        upcomingEvents,
        recentActivity,
      });
    } catch (error) {
      console.error('Error fetching analytics data:', error);
    } finally {
      setLoading(false);
    }
  }, [timeRange]);

  useEffect(() => {
    fetchAnalyticsData();
  }, [fetchAnalyticsData]);

  useEffect(() => {
    (async () => {
      try {
        const { eventService } = await import('../services/api');
        const data = await (eventService as any).getIngestStats?.();
        if (data) setIngestStats(data);
      } catch {}
    })();
  }, []);

  const getEventTypeColor = (eventType: string) => {
    const colors = {
      academic: 'bg-blue-500',
      government: 'bg-green-500',
      community: 'bg-purple-500',
      tech: 'bg-orange-500',
      holiday: 'bg-red-500'
    };
    return colors[eventType as keyof typeof colors] || 'bg-gray-500';
  };

  if (loading || !analyticsData) {
    return (
      <div className="space-y-6">
        {/* Presented By (always visible) */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-4 flex items-center justify-center gap-3">
              <div className="text-right" aria-label="Presented by Intelligent Systems Lab, Fayetteville State University">
              <div className="text-xs uppercase tracking-wide text-gray-500">Presented by</div>
              <div className="text-sm font-semibold text-gray-800">Intelligent Systems Lab</div>
              <div className="text-xs text-gray-600">Fayetteville State University</div>
            </div>
            <img
              src={`${process.env.PUBLIC_URL}/presented-by.png`}
              alt="Fayetteville State University Intelligent Systems Laboratory"
              className="h-12 w-auto object-contain"
              onError={(e) => { (e.currentTarget as HTMLImageElement).style.display = 'none'; }}
            />
          </div>
        </div>

        {/* Loading placeholder */}
        <div className="flex justify-center items-center h-48">
          <div className="text-gray-600">Loading analytics…</div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Analytics Dashboard</h1>
          <p className="text-gray-600">Monitor platform performance and user engagement</p>
        </div>
        <div className="flex items-center space-x-4">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="7d">Last 7 days</option>
            <option value="30d">Last 30 days</option>
            <option value="90d">Last 90 days</option>
          </select>
        </div>
      </div>

      {/* Overview + Presented By */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
          <div className="rounded-md border border-blue-200 bg-blue-50 p-4">
            <p className="text-sm text-blue-800">
              EventPulse Analytics summarizes the platform at a glance: total events, active users,
              events by type and location, most‑viewed events, recent activity, and performance metrics.
              Data is aggregated from official North Carolina sources including state agencies (DOT, DHHS,
              Commerce), county and city governments (Raleigh, Durham, Chapel Hill, Wake County), and
              universities (UNC System campuses, NC State, Duke, and others). Charts reflect the current
              dataset in the backend and update as new data is ingested.
            </p>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-4 flex items-center justify-center gap-3">
          <div className="text-right">
            <div className="text-xs uppercase tracking-wide text-gray-500">Presented by</div>
            <div className="text-sm font-semibold text-gray-800">Intelligent Systems Lab</div>
            <div className="text-xs text-gray-600">Fayetteville State University</div>
          </div>
          <img
            src="/presented-by.png"
            alt="Fayetteville State University Intelligent Systems Laboratory"
            className="h-12 w-auto object-contain"
            onError={(e) => { (e.currentTarget as HTMLImageElement).style.display = 'none'; }}
          />
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <CalendarIcon style={{ width: 12, height: 12 }} className="text-blue-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Events</p>
              <p className="text-2xl font-bold text-gray-900">{analyticsData.totalEvents.toLocaleString()}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <CalendarIcon style={{ width: 12, height: 12 }} className="text-green-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Events in Range</p>
              <p className="text-2xl font-bold text-gray-900">{analyticsData.eventsInRange.toLocaleString()}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <ArrowTrendingUpIcon style={{ width: 12, height: 12 }} className="text-purple-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Growth Rate</p>
              <p className="text-2xl font-bold text-gray-900">{`${analyticsData.growthRatePercent >= 0 ? '+' : ''}${analyticsData.growthRatePercent.toFixed(1)}%`}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <MapPinIcon style={{ width: 12, height: 12 }} className="text-orange-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Cities Covered</p>
              <p className="text-2xl font-bold text-gray-900">{analyticsData.citiesCovered.toLocaleString()}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Data Quality / Ingest Stats */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Data Quality</h3>
        {ingestStats ? (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <div className="text-gray-600">Last Batch</div>
              <div className="font-semibold">{ingestStats.lastBatch.received} received</div>
              <div className="text-gray-600">{ingestStats.lastBatch.inserted} inserted</div>
              <div className="text-gray-600">{ingestStats.lastBatch.duplicates} duplicates</div>
              <div className="text-gray-600">{ingestStats.lastBatch.failed} failed</div>
            </div>
            <div>
              <div className="text-gray-600">Totals</div>
              <div className="font-semibold">{ingestStats.totals.received} received</div>
              <div className="text-gray-600">{ingestStats.totals.inserted} inserted</div>
              <div className="text-gray-600">{ingestStats.totals.duplicates} duplicates</div>
            </div>
            <div className="col-span-2">
              <div className="text-gray-600 mb-1">Rejected reasons</div>
              <ul className="text-gray-700 grid grid-cols-2 md:grid-cols-4 gap-2">
                <li>Invalid date: {ingestStats.reasons.invalid_date}</li>
                <li>Invalid order: {ingestStats.reasons.invalid_order}</li>
                <li>Too long: {ingestStats.reasons.too_long}</li>
                <li>Invalid coords: {ingestStats.reasons.invalid_coords}</li>
                <li>Missing fields: {ingestStats.reasons.missing_fields}</li>
              </ul>
            </div>
          </div>
        ) : (
          <div className="text-gray-600 text-sm">No ingest stats yet.</div>
        )}
      </div>

      {/* Charts and Data */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Events by Type */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Events by Type</h3>
          <div className="space-y-3">
            {Object.entries(analyticsData.eventsByType).map(([type, count]) => (
              <div key={type} className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className={`w-4 h-4 rounded-full ${getEventTypeColor(type)}`}></div>
                  <span className="text-sm font-medium text-gray-700 capitalize">{type}</span>
                </div>
                <span className="text-sm text-gray-600">{count.toLocaleString()}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Events by Location */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Events by Location</h3>
          <div className="space-y-3">
            {Object.entries(analyticsData.eventsByLocation).map(([location, count]) => (
              <div key={location} className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <MapPinIcon style={{ width: 12, height: 12 }} className="text-gray-400" />
                  <span className="text-sm font-medium text-gray-700">{location}</span>
                </div>
                <span className="text-sm text-gray-600">{count.toLocaleString()}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Upcoming Events */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Upcoming Events</h3>
        <div className="space-y-3">
          {analyticsData.upcomingEvents.map((event) => (
            <div key={event.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className={`w-3 h-3 rounded-full ${getEventTypeColor(event.event_type)}`}></div>
                <div>
                  <p className="text-sm font-medium text-gray-900">{event.title}</p>
                  <p className="text-xs text-gray-600 capitalize">{event.event_type}</p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <ClockIcon style={{ width: 12, height: 12 }} className="text-gray-400" />
                <span className="text-sm text-gray-600">{new Date(event.start_date).toLocaleString()}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Performance Metrics panel removed until runtime metrics are enabled */}

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
        <div className="space-y-3">
          {analyticsData.recentActivity.map((activity) => (
            <div key={activity.id} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <div>
                  <p className="text-sm font-medium text-gray-900">{activity.action}</p>
                  <p className="text-xs text-gray-600">{activity.details}</p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <ClockIcon style={{ width: 12, height: 12 }} className="text-gray-400" />
                <span className="text-xs text-gray-600">
                  {new Date(activity.timestamp).toLocaleTimeString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard; 