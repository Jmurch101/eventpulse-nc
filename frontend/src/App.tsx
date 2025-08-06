import React from 'react';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Dashboard from './components/Dashboard';
import Analytics from './pages/Analytics';
import DayEventsPage from './pages/DayEventsPage';
import InteractiveHeatMap from './components/InteractiveHeatMap';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/calendar" element={<InteractiveHeatMap onDateSelect={(date) => console.log('Selected date:', date)} />} />
          <Route path="/day/:date" element={<DayEventsPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
