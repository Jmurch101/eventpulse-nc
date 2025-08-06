import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Header: React.FC = () => {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <header style={{ backgroundColor: 'white', boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)', borderBottom: '1px solid #e5e7eb' }}>
      <div className="container" style={{ padding: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', textDecoration: 'none' }}>
              <div style={{ 
                width: '2rem', 
                height: '2rem', 
                backgroundColor: '#2563eb', 
                borderRadius: '0.5rem', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <span style={{ color: 'white', fontWeight: 'bold', fontSize: '0.875rem' }}>EP</span>
              </div>
              <span style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#111827' }}>EventPulse NC</span>
            </Link>
          </div>
          
          <nav style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
            <Link 
              to="/"
              style={{ 
                color: isActive('/') ? '#2563eb' : '#4b5563', 
                backgroundColor: 'transparent', 
                border: 'none', 
                cursor: 'pointer',
                fontSize: '0.875rem',
                textDecoration: 'none',
                fontWeight: isActive('/') ? '600' : '400'
              }}
            >
              Dashboard
            </Link>
            <Link 
              to="/calendar"
              style={{ 
                color: isActive('/calendar') ? '#2563eb' : '#4b5563', 
                backgroundColor: 'transparent', 
                border: 'none', 
                cursor: 'pointer',
                fontSize: '0.875rem',
                textDecoration: 'none',
                fontWeight: isActive('/calendar') ? '600' : '400'
              }}
            >
              Calendar
            </Link>
            <Link 
              to="/analytics"
              style={{ 
                color: isActive('/analytics') ? '#2563eb' : '#4b5563', 
                backgroundColor: 'transparent', 
                border: 'none', 
                cursor: 'pointer',
                fontSize: '0.875rem',
                textDecoration: 'none',
                fontWeight: isActive('/analytics') ? '600' : '400'
              }}
            >
              Analytics
            </Link>
          </nav>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <button style={{ 
              color: '#4b5563', 
              backgroundColor: 'transparent', 
              border: 'none', 
              cursor: 'pointer' 
            }}>
              <svg style={{ width: '1rem', height: '1rem' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
            <button style={{
              backgroundColor: '#2563eb',
              color: 'white',
              padding: '0.5rem 1rem',
              borderRadius: '0.5rem',
              fontSize: '0.875rem',
              fontWeight: '500',
              border: 'none',
              cursor: 'pointer'
            }}>
              Sign In
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header; 