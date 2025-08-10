import React, { useEffect } from 'react';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Dashboard from './components/Dashboard';
import Analytics from './pages/Analytics';
import DayEventsPage from './pages/DayEventsPage';
import InteractiveHeatMap from './components/InteractiveHeatMap';

function App() {
  useEffect(() => {
    const domain = process.env.REACT_APP_PLAUSIBLE_DOMAIN;
    if (!domain) return;
    // Inject Plausible script once
    if (document.querySelector('script[data-plausible]')) return;
    const s = document.createElement('script');
    s.setAttribute('data-plausible', 'true');
    s.defer = true;
    s.src = 'https://plausible.io/js/script.js';
    s.setAttribute('data-domain', domain);
    document.head.appendChild(s);
  }, []);

  return (
    <Router>
      <a href="#main" className="skip-link">Skip to content</a>
      <div className="App" id="top">
        <Routes>
          <Route path="/" element={<main id="main" role="main"><Dashboard /></main>} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/calendar" element={<InteractiveHeatMap onDateSelect={(date) => console.log('Selected date:', date)} />} />
          <Route path="/day/:date" element={<DayEventsPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
