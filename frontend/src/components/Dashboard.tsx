import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import AdvancedSearch from './AdvancedSearch';
import CategoryBubbles from './CategoryBubbles';
import InteractiveHeatMap from './InteractiveHeatMap';
import { format } from 'date-fns';

const Dashboard: React.FC = () => {
  const [view, setView] = useState<'events' | 'holidays'>('events');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedEventTypes, setSelectedEventTypes] = useState<string[]>([]);
  const navigate = useNavigate();

  // categories drive selectedEventTypes; no modal needed

  const handleCategorySelect = (category: any) => {
    setSelectedCategory(category.id);
    setSelectedEventTypes(category.eventTypes);
  };
  
  const handleDateSelect = (date: Date) => {
    navigate(`/day/${format(date, 'yyyy-MM-dd')}`);
  };

  const handleSearch = (filters: any) => {
    setSelectedEventTypes(filters.eventTypes);
  };

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
        </div>
      </nav>
      {/* Tagline */}
      <p className="text-center text-gray-600 mb-8">
        Never Miss What Matters in North Carolina
      </p>
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
                selectedEventTypes={selectedEventTypes}
              />
            </div>
          </div>
        </div>
      ) : (
        <div className="flex flex-col md:flex-row gap-6">
          {/* Holidays Heatmap: show only holiday events */}
          <div className="md:flex-1">
            <InteractiveHeatMap
              onDateSelect={handleDateSelect}
              selectedEventTypes={['holiday']}
            />
          </div>
        </div>
      )}
      {/* no modal: use separate page for day events */}
    </div>
  );
};

export default Dashboard;
