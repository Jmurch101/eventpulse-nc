import React, { useState } from 'react';
import { XMarkIcon, FunnelIcon } from '@heroicons/react/24/outline';

interface FilterOptions {
  eventType: string;
  dateRange: {
    start: string;
    end: string;
  };
  location: string;
  search: string;
  sortBy: string;
}

interface AdvancedFiltersProps {
  filters: FilterOptions;
  onFiltersChange: (filters: FilterOptions) => void;
  onClearFilters: () => void;
}

const AdvancedFilters: React.FC<AdvancedFiltersProps> = ({
  filters,
  onFiltersChange,
  onClearFilters
}) => {
  const [isOpen, setIsOpen] = useState(false);

  const eventTypes = [
    { value: '', label: 'All Types' },
    { value: 'academic', label: 'Academic' },
    { value: 'government', label: 'Government' },
    { value: 'city', label: 'City' },
    { value: 'holiday', label: 'Holiday' }
  ];

  const sortOptions = [
    { value: 'start_date', label: 'Date' },
    { value: 'title', label: 'Title' },
    { value: 'location_name', label: 'Location' },
    { value: 'event_type', label: 'Type' }
  ];

  const locations = [
    { value: '', label: 'All Locations' },
    { value: 'Raleigh', label: 'Raleigh' },
    { value: 'Durham', label: 'Durham' },
    { value: 'Chapel Hill', label: 'Chapel Hill' },
    { value: 'Cary', label: 'Cary' },
    { value: 'NC State', label: 'NC State University' },
    { value: 'UNC', label: 'UNC Chapel Hill' },
    { value: 'Duke', label: 'Duke University' }
  ];

  const handleFilterChange = (key: keyof FilterOptions, value: any) => {
    onFiltersChange({
      ...filters,
      [key]: value
    });
  };

  const handleDateRangeChange = (field: 'start' | 'end', value: string) => {
    onFiltersChange({
      ...filters,
      dateRange: {
        ...filters.dateRange,
        [field]: value
      }
    });
  };

  const hasActiveFilters = () => {
    return (
      filters.eventType ||
      filters.dateRange.start ||
      filters.dateRange.end ||
      filters.location ||
      filters.search ||
      filters.sortBy !== 'start_date'
    );
  };

  return (
    <div className="bg-white rounded-lg shadow border">
      {/* Filter Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <FunnelIcon className="h-5 w-5 text-gray-400 mr-2" />
            <h3 className="text-lg font-medium text-gray-900">Advanced Filters</h3>
            {hasActiveFilters() && (
              <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                Active
              </span>
            )}
          </div>
          <div className="flex items-center space-x-2">
            {hasActiveFilters() && (
              <button
                onClick={onClearFilters}
                className="text-sm text-gray-500 hover:text-gray-700"
              >
                Clear All
              </button>
            )}
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-gray-400 hover:text-gray-600"
            >
              {isOpen ? (
                <XMarkIcon className="h-5 w-5" />
              ) : (
                <FunnelIcon className="h-5 w-5" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Filter Content */}
      {isOpen && (
        <div className="px-6 py-4 space-y-4">
          {/* Search */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Search Events
            </label>
            <input
              type="text"
              placeholder="Search by title, description, or location..."
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-primary-500 focus:border-primary-500"
              value={filters.search}
              onChange={(e) => handleFilterChange('search', e.target.value)}
            />
          </div>

          {/* Event Type and Location */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Event Type
              </label>
              <select
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-primary-500 focus:border-primary-500"
                value={filters.eventType}
                onChange={(e) => handleFilterChange('eventType', e.target.value)}
              >
                {eventTypes.map(type => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Location
              </label>
              <select
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-primary-500 focus:border-primary-500"
                value={filters.location}
                onChange={(e) => handleFilterChange('location', e.target.value)}
              >
                {locations.map(location => (
                  <option key={location.value} value={location.value}>
                    {location.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Date Range */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Date Range
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs text-gray-500 mb-1">Start Date</label>
                <input
                  type="date"
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-primary-500 focus:border-primary-500"
                  value={filters.dateRange.start}
                  onChange={(e) => handleDateRangeChange('start', e.target.value)}
                />
              </div>
              <div>
                <label className="block text-xs text-gray-500 mb-1">End Date</label>
                <input
                  type="date"
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-primary-500 focus:border-primary-500"
                  value={filters.dateRange.end}
                  onChange={(e) => handleDateRangeChange('end', e.target.value)}
                />
              </div>
            </div>
          </div>

          {/* Sort Options */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Sort By
            </label>
            <select
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-primary-500 focus:border-primary-500"
              value={filters.sortBy}
              onChange={(e) => handleFilterChange('sortBy', e.target.value)}
            >
              {sortOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          {/* Quick Filter Buttons */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Quick Filters
            </label>
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => {
                  const today = new Date();
                  const nextWeek = new Date();
                  nextWeek.setDate(today.getDate() + 7);
                  
                  onFiltersChange({
                    ...filters,
                    dateRange: {
                      start: today.toISOString().split('T')[0],
                      end: nextWeek.toISOString().split('T')[0]
                    }
                  });
                }}
                className="px-3 py-1 text-xs bg-blue-100 text-blue-800 rounded-full hover:bg-blue-200"
              >
                Next 7 Days
              </button>
              <button
                onClick={() => {
                  const today = new Date();
                  const nextMonth = new Date();
                  nextMonth.setMonth(today.getMonth() + 1);
                  
                  onFiltersChange({
                    ...filters,
                    dateRange: {
                      start: today.toISOString().split('T')[0],
                      end: nextMonth.toISOString().split('T')[0]
                    }
                  });
                }}
                className="px-3 py-1 text-xs bg-green-100 text-green-800 rounded-full hover:bg-green-200"
              >
                Next 30 Days
              </button>
              <button
                onClick={() => onFiltersChange({ ...filters, eventType: 'academic' })}
                className="px-3 py-1 text-xs bg-purple-100 text-purple-800 rounded-full hover:bg-purple-200"
              >
                Academic Only
              </button>
              <button
                onClick={() => onFiltersChange({ ...filters, eventType: 'city' })}
                className="px-3 py-1 text-xs bg-orange-100 text-orange-800 rounded-full hover:bg-orange-200"
              >
                City Events
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdvancedFilters; 