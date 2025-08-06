import React from 'react';
import { CategoryBubble } from '../types/CategoryBubble';

interface CategoryBubblesProps {
  onCategorySelect: (category: CategoryBubble) => void;
  selectedCategory: string;
}

const categories: CategoryBubble[] = [
  {
    id: 'all',
    name: 'All Events',
    icon: '📅',
    color: '#374151',
    bgColor: '#e5e7eb',
    description: 'Show all events',
    eventTypes: []
  },
  {
    id: 'university',
    name: 'University Events',
    icon: '📚',
    color: '#3b82f6',
    bgColor: '#dbeafe',
    description: 'Academic lectures, research symposiums, and campus activities',
    eventTypes: ['academic']
  },
  {
    id: 'government',
    name: 'Government Meetings',
    icon: '🏛',
    color: '#059669',
    bgColor: '#d1fae5',
    description: 'City council meetings, public hearings, and government forums',
    eventTypes: ['government']
  },
  {
    id: 'school-holidays',
    name: 'School Holidays',
    icon: '📅',
    color: '#7c3aed',
    bgColor: '#f3e8ff',
    description: 'School breaks, holidays, and academic calendar events',
    eventTypes: ['holiday']
  },
  {
    id: 'official-holidays',
    name: 'Official Holidays',
    icon: '🎊',
    color: '#dc2626',
    bgColor: '#fee2e2',
    description: 'Federal and state holidays, observances',
    eventTypes: ['holiday']
  },
  {
    id: 'workshops',
    name: 'Workshops & Training',
    icon: '⚙️',
    color: '#ea580c',
    bgColor: '#fed7aa',
    description: 'Professional development and skill-building sessions',
    eventTypes: ['academic']
  },
  {
    id: 'tech',
    name: 'Tech Events',
    icon: '⚡',
    color: '#0891b2',
    bgColor: '#cffafe',
    description: 'Technology conferences, hackathons, and innovation events',
    eventTypes: ['academic']
  },
  {
    id: 'community',
    name: 'Community Events',
    icon: '👥',
    color: '#059669',
    bgColor: '#d1fae5',
    description: 'Local community gatherings and civic engagement',
    eventTypes: ['government']
  }
];

const CategoryBubbles: React.FC<CategoryBubblesProps> = ({ onCategorySelect, selectedCategory }) => {
  return (
    <div style={{ padding: '1rem 0' }}>
      <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#111827', marginBottom: '0.5rem' }}>
          Browse by Category
        </h2>
        <p style={{ color: '#6b7280', fontSize: '1rem' }}>
          Discover events that match your interests
        </p>
      </div>
      
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
        gap: '1rem',
        maxWidth: '1200px',
        margin: '0 auto'
      }}>
        {categories.map((category) => (
          <div
            key={category.id}
            onClick={() => onCategorySelect(category)}
            style={{
              backgroundColor: selectedCategory === category.id ? category.color : 'white',
              color: selectedCategory === category.id ? 'white' : '#374151',
              padding: '1rem',
              borderRadius: '1rem',
              cursor: 'pointer',
              border: `2px solid ${selectedCategory === category.id ? category.color : '#e5e7eb'}`,
              transition: 'all 0.2s ease-in-out',
              boxShadow: selectedCategory === category.id 
                ? `0 10px 25px -5px ${category.color}40` 
                : '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
              transform: selectedCategory === category.id ? 'translateY(-2px)' : 'none'
            }}
            onMouseEnter={(e) => {
              if (selectedCategory !== category.id) {
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = '0 10px 25px -5px rgba(0, 0, 0, 0.1)';
              }
            }}
            onMouseLeave={(e) => {
              if (selectedCategory !== category.id) {
                e.currentTarget.style.transform = 'none';
                e.currentTarget.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
              }
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1rem' }}>
              <div style={{
                fontSize: '1rem',
                marginRight: '1rem',
                width: '1.5rem',
                height: '1.5rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                backgroundColor: selectedCategory === category.id ? 'rgba(255,255,255,0.2)' : category.bgColor,
                borderRadius: '0.75rem'
              }}>
                {category.icon}
              </div>
              <div>
                <h3 style={{ 
                  fontSize: '1rem', 
                  fontWeight: '600', 
                  marginBottom: '0.25rem',
                  color: selectedCategory === category.id ? 'white' : '#111827'
                }}>
                  {category.name}
                </h3>
                <p style={{ 
                  fontSize: '0.875rem',
                  color: selectedCategory === category.id ? 'rgba(255,255,255,0.8)' : '#6b7280'
                }}>
                  {category.description}
                </p>
              </div>
            </div>
            
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'space-between',
              marginTop: '1rem'
            }}>
              <span style={{
                fontSize: '0.75rem',
                padding: '0.25rem 0.5rem',
                backgroundColor: selectedCategory === category.id ? 'rgba(255,255,255,0.2)' : category.bgColor,
                color: selectedCategory === category.id ? 'white' : category.color,
                borderRadius: '0.375rem',
                fontWeight: '500'
              }}>
                {category.eventTypes.length} type{category.eventTypes.length !== 1 ? 's' : ''}
              </span>
              
              <svg 
                style={{ 
                  width: '1rem', 
                  height: '1rem',
                  color: selectedCategory === category.id ? 'white' : '#9ca3af'
                }} 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CategoryBubbles; 