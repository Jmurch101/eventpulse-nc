import React, { useState } from 'react';
import { MapPinIcon } from '@heroicons/react/24/outline';

interface AdvancedSearchProps {
  onSearch: (filters: SearchFilters) => void;
  onClear: () => void;
}

export interface SearchFilters {
  query: string;
  eventTypes: string[];
  dateRange: {
    start: string;
    end: string;
  };
  location: {
    city: string;
    radius: number;
  };
  price: {
    min: number;
    max: number;
  };
  tags: string[];
}

const AdvancedSearch: React.FC<AdvancedSearchProps> = ({ onSearch, onClear }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [filters, setFilters] = useState<SearchFilters>({
    query: '',
    eventTypes: [],
    dateRange: {
      start: '',
      end: ''
    },
    location: {
      city: '',
      radius: 25
    },
    price: {
      min: 0,
      max: 1000
    },
    tags: []
  });

  const eventTypeOptions = [
    { value: 'academic', label: 'Academic', color: 'bg-blue-500' },
    { value: 'government', label: 'Government', color: 'bg-green-500' },
    { value: 'community', label: 'Community', color: 'bg-purple-500' },
    { value: 'tech', label: 'Tech', color: 'bg-orange-500' },
    { value: 'holiday', label: 'Holiday', color: 'bg-red-500' }
  ];

  const cityOptions = [
    { value: 'raleigh', label: 'Raleigh' },
    { value: 'durham', label: 'Durham' },
    { value: 'chapel_hill', label: 'Chapel Hill' },
    { value: 'cary', label: 'Cary' },
    { value: 'morrisville', label: 'Morrisville' },
    { value: 'apex', label: 'Apex' },
    { value: 'holly_springs', label: 'Holly Springs' },
    { value: 'fuquay_varina', label: 'Fuquay-Varina' }
  ];

  const tagOptions = [
    'Free', 'Paid', 'Registration Required', 'Virtual', 'In-Person',
    'Workshop', 'Conference', 'Lecture', 'Meeting', 'Festival',
    'Networking', 'Educational', 'Professional', 'Family-Friendly',
    'Student', 'Senior', 'All Ages'
  ];

  const handleFilterChange = (key: keyof SearchFilters, value: any) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleEventTypeToggle = (eventType: string) => {
    setFilters(prev => ({
      ...prev,
      eventTypes: prev.eventTypes.includes(eventType)
        ? prev.eventTypes.filter(type => type !== eventType)
        : [...prev.eventTypes, eventType]
    }));
  };

  const handleTagToggle = (tag: string) => {
    setFilters(prev => ({
      ...prev,
      tags: prev.tags.includes(tag)
        ? prev.tags.filter(t => t !== tag)
        : [...prev.tags, tag]
    }));
  };

  const handleSearch = () => {
    onSearch(filters);
  };

  const handleClear = () => {
    setFilters({
      query: '',
      eventTypes: [],
      dateRange: {
        start: '',
        end: ''
      },
      location: {
        city: '',
        radius: 25
      },
      price: {
        min: 0,
        max: 1000
      },
      tags: []
    });
    onClear();
  };

  const getActiveFiltersCount = () => {
    let count = 0;
    if (filters.query) count++;
    if (filters.eventTypes.length > 0) count++;
    if (filters.dateRange.start || filters.dateRange.end) count++;
    if (filters.location.city) count++;
    if (filters.tags.length > 0) count++;
    return count;
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mb-6" role="region" aria-label="Advanced search filters">
      {/* Search Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <span className="text-xs text-gray-600">🔍</span>
          <h3 className="text-lg font-semibold text-gray-900">Advanced Search</h3>
          {getActiveFiltersCount() > 0 && (
            <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
              {getActiveFiltersCount()} active
            </span>
          )}
        </div>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center space-x-2 text-gray-600 hover:text-gray-900"
        >
          <span className="text-xs">⚙️</span>
          <span className="text-sm font-medium">
            {isExpanded ? 'Hide Filters' : 'Show Filters'}
          </span>
        </button>
      </div>

      {/* Basic Search */}
      <div className="mb-4">
        <div className="relative">
          <input
            type="text"
            placeholder="Search events, locations, or keywords..."
            value={filters.query}
            onChange={(e) => handleFilterChange('query', e.target.value)}
            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            aria-label="Search query"
          />
          <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-xs text-gray-400">🔍</span>
        </div>
      </div>

      {/* Advanced Filters */}
      {isExpanded && (
        <div className="space-y-6">
          {/* Event Types */}
          <div>
            <h4 className="text-sm font-medium text-gray-900 mb-3">Event Types</h4>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
              {eventTypeOptions.map((option) => (
                <button
                  key={option.value}
                  onClick={() => handleEventTypeToggle(option.value)}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg border text-sm font-medium transition-colors ${
                    filters.eventTypes.includes(option.value)
                      ? 'bg-blue-50 border-blue-200 text-blue-700'
                      : 'bg-gray-50 border-gray-200 text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <div className={`w-3 h-3 rounded-full ${option.color}`}></div>
                  <span>{option.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Date Range */}
          <div>
            <h4 className="text-sm font-medium text-gray-900 mb-3 flex items-center">
              <span className="text-xs mr-2">📅</span>
              Date Range
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  From
                </label>
                <input
                  type="date"
                  value={filters.dateRange.start}
                  onChange={(e) => handleFilterChange('dateRange', {
                    ...filters.dateRange,
                    start: e.target.value
                  })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  aria-label="Start date"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  To
                </label>
                <input
                  type="date"
                  value={filters.dateRange.end}
                  onChange={(e) => handleFilterChange('dateRange', {
                    ...filters.dateRange,
                    end: e.target.value
                  })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  aria-label="End date"
                />
              </div>
            </div>
          </div>

          {/* Location */}
          <div>
            <h4 className="text-sm font-medium text-gray-900 mb-3 flex items-center">
              <MapPinIcon className="h-4 w-4 mr-2" />
              Location
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  City
                </label>
                <select
                  value={filters.location.city}
                  onChange={(e) => handleFilterChange('location', {
                    ...filters.location,
                    city: e.target.value
                  })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  aria-label="City"
                >
                  <option value="">All Cities</option>
                  {cityOptions.map((city) => (
                    <option key={city.value} value={city.value}>
                      {city.label}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  Radius (miles)
                </label>
                <input
                  type="range"
                  min="5"
                  max="100"
                  step="5"
                  value={filters.location.radius}
                  onChange={(e) => handleFilterChange('location', {
                    ...filters.location,
                    radius: parseInt(e.target.value)
                  })}
                  className="w-full"
                  aria-label="Radius in miles"
                />
                <div className="text-xs text-gray-500 mt-1">
                  {filters.location.radius} miles
                </div>
              </div>
            </div>
          </div>

          {/* Tags */}
          <div>
            <h4 className="text-sm font-medium text-gray-900 mb-3">Tags</h4>
            <div className="flex flex-wrap gap-2">
              {tagOptions.map((tag) => (
                <button
                  key={tag}
                  onClick={() => handleTagToggle(tag)}
                  className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                    filters.tags.includes(tag)
                      ? 'bg-blue-100 text-blue-800 border border-blue-200'
                      : 'bg-gray-100 text-gray-700 border border-gray-200 hover:bg-gray-200'
                  }`}
                >
                  {tag}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex items-center justify-between mt-6 pt-4 border-t border-gray-200">
        <button
          onClick={handleClear}
          className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-900"
        >
          Clear All
        </button>
        <button
          onClick={handleSearch}
          className="px-6 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
        >
          Search Events
        </button>
      </div>
    </div>
  );
};

export default AdvancedSearch; 