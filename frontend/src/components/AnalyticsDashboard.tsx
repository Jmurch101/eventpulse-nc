import React, { useState, useEffect } from 'react';
import { 
  UsersIcon, 
  CalendarIcon, 
  MapPinIcon,
  ArrowTrendingUpIcon,
  EyeIcon,
  ClockIcon
} from '@heroicons/react/24/outline';

interface AnalyticsData {
  totalEvents: number;
  totalUsers: number;
  activeUsers: number;
  eventsByType: { [key: string]: number };
  eventsByLocation: { [key: string]: number };
  popularEvents: Array<{
    id: number;
    title: string;
    views: number;
    event_type: string;
  }>;
  recentActivity: Array<{
    id: number;
    action: string;
    timestamp: string;
    details: string;
  }>;
  performanceMetrics: {
    avgLoadTime: number;
    apiResponseTime: number;
    cacheHitRate: number;
    errorRate: number;
  };
}

const AnalyticsDashboard: React.FC = () => {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('7d'); // 7d, 30d, 90d

  useEffect(() => {
    fetchAnalyticsData();
  }, [timeRange]);

  const fetchAnalyticsData = async () => {
    try {
      setLoading(true);
      // Simulate API call - replace with actual analytics endpoint
      const mockData: AnalyticsData = {
        totalEvents: 1091,
        totalUsers: 2456,
        activeUsers: 892,
        eventsByType: {
          academic: 458,
          government: 234,
          community: 189,
          tech: 156,
          holiday: 54
        },
        eventsByLocation: {
          'Raleigh': 345,
          'Durham': 234,
          'Chapel Hill': 189,
          'Cary': 156,
          'Other': 167
        },
        popularEvents: [
          { id: 1, title: 'NC State Engineering Career Fair', views: 1245, event_type: 'academic' },
          { id: 2, title: 'Raleigh City Council Meeting', views: 892, event_type: 'government' },
          { id: 3, title: 'Triangle Tech Meetup', views: 756, event_type: 'tech' },
          { id: 4, title: 'Durham Farmers Market', views: 634, event_type: 'community' },
          { id: 5, title: 'UNC Research Symposium', views: 523, event_type: 'academic' }
        ],
        recentActivity: [
          { id: 1, action: 'Event Created', timestamp: '2024-01-15T10:30:00Z', details: 'New academic event added' },
          { id: 2, action: 'User Registration', timestamp: '2024-01-15T09:15:00Z', details: 'New user joined platform' },
          { id: 3, action: 'Event Updated', timestamp: '2024-01-15T08:45:00Z', details: 'Government meeting details updated' },
          { id: 4, action: 'Search Query', timestamp: '2024-01-15T08:20:00Z', details: 'Popular search: "tech events"' },
          { id: 5, action: 'Map Interaction', timestamp: '2024-01-15T07:55:00Z', details: 'User explored Raleigh area' }
        ],
        performanceMetrics: {
          avgLoadTime: 1.2,
          apiResponseTime: 0.8,
          cacheHitRate: 85.5,
          errorRate: 0.3
        }
      };

      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setAnalyticsData(mockData);
    } catch (error) {
      console.error('Error fetching analytics data:', error);
    } finally {
      setLoading(false);
    }
  };

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
        {/* Status + Presented By (always visible) */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <div className="rounded-md border border-blue-200 bg-blue-50 p-4">
              <p className="text-sm text-blue-800">
                Analytics collection is currently limited on the public demo. Production metrics will populate
                after launch with privacy-friendly, aggregated tracking. In the meantime, charts will appear here.
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

      {/* Status + Presented By */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="rounded-md border border-blue-200 bg-blue-50 p-4">
            <p className="text-sm text-blue-800">
              Analytics collection is currently limited on the public demo. Production metrics will populate
              after launch with privacy-friendly, aggregated tracking. In the meantime, charts below use
              representative sample data to illustrate the experience.
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
            <UsersIcon style={{ width: 12, height: 12 }} className="text-green-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Active Users</p>
              <p className="text-2xl font-bold text-gray-900">{analyticsData.activeUsers.toLocaleString()}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <ArrowTrendingUpIcon style={{ width: 12, height: 12 }} className="text-purple-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Growth Rate</p>
              <p className="text-2xl font-bold text-gray-900">+12.5%</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <EyeIcon style={{ width: 12, height: 12 }} className="text-orange-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Page Views</p>
              <p className="text-2xl font-bold text-gray-900">45.2K</p>
            </div>
          </div>
        </div>
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

      {/* Popular Events */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Most Popular Events</h3>
        <div className="space-y-3">
          {analyticsData.popularEvents.map((event) => (
            <div key={event.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className={`w-3 h-3 rounded-full ${getEventTypeColor(event.event_type)}`}></div>
                <div>
                  <p className="text-sm font-medium text-gray-900">{event.title}</p>
                  <p className="text-xs text-gray-600 capitalize">{event.event_type}</p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <EyeIcon style={{ width: 12, height: 12 }} className="text-gray-400" />
                <span className="text-sm text-gray-600">{event.views.toLocaleString()}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Performance Metrics */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Metrics</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <p className="text-2xl font-bold text-blue-600">{analyticsData.performanceMetrics.avgLoadTime}s</p>
            <p className="text-sm text-gray-600">Avg Load Time</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-green-600">{analyticsData.performanceMetrics.apiResponseTime}ms</p>
            <p className="text-sm text-gray-600">API Response</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-purple-600">{analyticsData.performanceMetrics.cacheHitRate}%</p>
            <p className="text-sm text-gray-600">Cache Hit Rate</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-red-600">{analyticsData.performanceMetrics.errorRate}%</p>
            <p className="text-sm text-gray-600">Error Rate</p>
          </div>
        </div>
      </div>

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