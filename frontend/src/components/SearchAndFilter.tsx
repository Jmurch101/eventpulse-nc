import React, { useState } from 'react';

interface SearchAndFilterProps {
  onSearch: (query: string) => void;
  onFilterChange: (filters: EventFilters) => void;
  onSortChange: (sortBy: string) => void;
}

interface EventFilters {
  eventType: string;
  dateRange: string;
  location: string;
}

const SearchAndFilter: React.FC<SearchAndFilterProps> = ({ onSearch, onFilterChange, onSortChange }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState<EventFilters>({
    eventType: 'all',
    dateRange: 'all',
    location: 'all'
  });
  const [sortBy, setSortBy] = useState('date');
  const [isExpanded, setIsExpanded] = useState(false);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value;
    setSearchQuery(query);
    onSearch(query);
  };

  const handleFilterChange = (key: keyof EventFilters, value: string) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    setSortBy(value);
    onSortChange(value);
  };

  const clearFilters = () => {
    const clearedFilters = {
      eventType: 'all',
      dateRange: 'all',
      location: 'all'
    };
    setFilters(clearedFilters);
    setSearchQuery('');
    onFilterChange(clearedFilters);
    onSearch('');
  };

  return (
    <div style={{
      backgroundColor: 'white',
      borderRadius: '0.75rem',
      padding: '1.5rem',
      boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
      marginBottom: '2rem'
    }}>
      {/* Search Bar */}
      <div style={{ marginBottom: '1.5rem' }}>
        <div style={{ position: 'relative' }}>
          <div style={{
            position: 'absolute',
            left: '1rem',
            top: '50%',
            transform: 'translateY(-50%)',
            color: '#9ca3af',
            fontSize: '0.75rem',
            fontWeight: 'bold'
          }}>
            S
          </div>
          <input
            type="text"
            placeholder="Search events by title, description, or location..."
            value={searchQuery}
            onChange={handleSearchChange}
            style={{
              width: '100%',
              padding: '0.75rem 1rem 0.75rem 2.5rem',
              border: '1px solid #d1d5db',
              borderRadius: '0.5rem',
              fontSize: '0.875rem',
              outline: 'none'
            }}
          />
        </div>
      </div>

      {/* Quick Filters */}
      <div style={{ 
        display: 'flex', 
        flexWrap: 'wrap', 
        gap: '0.75rem', 
        marginBottom: '1rem',
        alignItems: 'center'
      }}>
        <span style={{ fontSize: '0.875rem', fontWeight: '500', color: '#374151' }}>
          Quick Filters:
        </span>
        
        {['all', 'academic', 'government', 'holiday'].map(type => (
          <button
            key={type}
            onClick={() => handleFilterChange('eventType', type)}
            style={{
              padding: '0.375rem 0.75rem',
              borderRadius: '0.375rem',
              fontSize: '0.75rem',
              fontWeight: '500',
              border: '1px solid',
              cursor: 'pointer',
              backgroundColor: filters.eventType === type ? '#2563eb' : 'white',
              color: filters.eventType === type ? 'white' : '#374151',
              borderColor: filters.eventType === type ? '#2563eb' : '#d1d5db'
            }}
          >
            {type.charAt(0).toUpperCase() + type.slice(1)}
          </button>
        ))}

        <button
          onClick={() => setIsExpanded(!isExpanded)}
          style={{
            padding: '0.375rem 0.75rem',
            borderRadius: '0.375rem',
            fontSize: '0.75rem',
            fontWeight: '500',
            border: '1px solid #d1d5db',
            backgroundColor: 'white',
            color: '#374151',
            cursor: 'pointer',
            marginLeft: 'auto'
          }}
        >
          {isExpanded ? 'Hide' : 'Show'} Advanced Filters
        </button>
      </div>

      {/* Advanced Filters */}
      {isExpanded && (
        <div style={{
          borderTop: '1px solid #e5e7eb',
          paddingTop: '1.5rem',
          marginTop: '1rem'
        }}>
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
            gap: '1rem',
            marginBottom: '1rem'
          }}>
            {/* Event Type Filter */}
            <div>
              <label style={{ 
                display: 'block', 
                fontSize: '0.875rem', 
                fontWeight: '500', 
                color: '#374151',
                marginBottom: '0.5rem'
              }}>
                Event Type
              </label>
              <select
                value={filters.eventType}
                onChange={(e) => handleFilterChange('eventType', e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.5rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '0.375rem',
                  fontSize: '0.875rem',
                  backgroundColor: 'white'
                }}
              >
                <option value="all">All Types</option>
                <option value="academic">Academic</option>
                <option value="government">Government</option>
                <option value="holiday">Holiday</option>
              </select>
            </div>

            {/* Date Range Filter */}
            <div>
              <label style={{ 
                display: 'block', 
                fontSize: '0.875rem', 
                fontWeight: '500', 
                color: '#374151',
                marginBottom: '0.5rem'
              }}>
                Date Range
              </label>
              <select
                value={filters.dateRange}
                onChange={(e) => handleFilterChange('dateRange', e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.5rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '0.375rem',
                  fontSize: '0.875rem',
                  backgroundColor: 'white'
                }}
              >
                <option value="all">All Dates</option>
                <option value="today">Today</option>
                <option value="tomorrow">Tomorrow</option>
                <option value="this-week">This Week</option>
                <option value="this-month">This Month</option>
                <option value="next-month">Next Month</option>
              </select>
            </div>

            {/* Location Filter */}
            <div>
              <label style={{ 
                display: 'block', 
                fontSize: '0.875rem', 
                fontWeight: '500', 
                color: '#374151',
                marginBottom: '0.5rem'
              }}>
                Location
              </label>
              <select
                value={filters.location}
                onChange={(e) => handleFilterChange('location', e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.5rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '0.375rem',
                  fontSize: '0.875rem',
                  backgroundColor: 'white'
                }}
              >
                <option value="all">All Locations</option>
                <option value="raleigh">Raleigh</option>
                <option value="durham">Durham</option>
                <option value="chapel-hill">Chapel Hill</option>
                <option value="ncsu">NC State</option>
                <option value="unc">UNC</option>
                <option value="duke">Duke</option>
              </select>
            </div>

            {/* Sort By */}
            <div>
              <label style={{ 
                display: 'block', 
                fontSize: '0.875rem', 
                fontWeight: '500', 
                color: '#374151',
                marginBottom: '0.5rem'
              }}>
                Sort By
              </label>
              <select
                value={sortBy}
                onChange={handleSortChange}
                style={{
                  width: '100%',
                  padding: '0.5rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '0.375rem',
                  fontSize: '0.875rem',
                  backgroundColor: 'white'
                }}
              >
                <option value="date">Date (Earliest First)</option>
                <option value="date-desc">Date (Latest First)</option>
                <option value="title">Title (A-Z)</option>
                <option value="title-desc">Title (Z-A)</option>
                <option value="type">Event Type</option>
                <option value="location">Location</option>
              </select>
            </div>
          </div>

          {/* Filter Actions */}
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            paddingTop: '1rem',
            borderTop: '1px solid #e5e7eb'
          }}>
            <div style={{ fontSize: '0.875rem', color: '#6b7280' }}>
              Active filters: {Object.values(filters).filter(f => f !== 'all').length}
            </div>
            
            <div style={{ display: 'flex', gap: '0.75rem' }}>
              <button
                onClick={clearFilters}
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
                Clear All
              </button>
              
              <button
                onClick={() => setIsExpanded(false)}
                style={{
                  padding: '0.5rem 1rem',
                  border: '1px solid #2563eb',
                  borderRadius: '0.375rem',
                  backgroundColor: '#2563eb',
                  color: 'white',
                  fontSize: '0.875rem',
                  fontWeight: '500',
                  cursor: 'pointer'
                }}
              >
                Apply Filters
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Active Filters Display */}
      {(Object.values(filters).some(f => f !== 'all') || searchQuery) && (
        <div style={{
          marginTop: '1rem',
          padding: '0.75rem',
          backgroundColor: '#f3f4f6',
          borderRadius: '0.5rem',
          border: '1px solid #e5e7eb'
        }}>
          <div style={{ fontSize: '0.875rem', fontWeight: '500', color: '#374151', marginBottom: '0.5rem' }}>
            Active Filters:
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
            {searchQuery && (
              <span style={{
                padding: '0.25rem 0.5rem',
                backgroundColor: '#dbeafe',
                color: '#1e40af',
                borderRadius: '0.25rem',
                fontSize: '0.75rem',
                fontWeight: '500'
              }}>
                Search: "{searchQuery}"
              </span>
            )}
            {filters.eventType !== 'all' && (
              <span style={{
                padding: '0.25rem 0.5rem',
                backgroundColor: '#dcfce7',
                color: '#166534',
                borderRadius: '0.25rem',
                fontSize: '0.75rem',
                fontWeight: '500'
              }}>
                Type: {filters.eventType}
              </span>
            )}
            {filters.dateRange !== 'all' && (
              <span style={{
                padding: '0.25rem 0.5rem',
                backgroundColor: '#fef3c7',
                color: '#92400e',
                borderRadius: '0.25rem',
                fontSize: '0.75rem',
                fontWeight: '500'
              }}>
                Date: {filters.dateRange.replace('-', ' ')}
              </span>
            )}
            {filters.location !== 'all' && (
              <span style={{
                padding: '0.25rem 0.5rem',
                backgroundColor: '#f3e8ff',
                color: '#7c3aed',
                borderRadius: '0.25rem',
                fontSize: '0.75rem',
                fontWeight: '500'
              }}>
                Location: {filters.location}
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchAndFilter; 